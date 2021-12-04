import os
import pandas as pd
import sys
import json
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import math
import traceback

class Evaluator():
    '''Useful evaluation functionality for the T3 track.'''

    def __init__(self,  algoname, csv=None, comp_path=None, baseline_path=None, system_cost=None, 
                        verbose=False, is_baseline=False, pending=[], print_best=False, 
                        show_baseline_table=False ):
        '''Constructor performs sanity and some competition rule checks.'''

        if sys.version_info[0] < 3:
            raise Exception("Must be using Python 3")

        if csv:
            if not os.path.exists(csv):
                raise Exception("CSV file does not exist.")
        
        if not os.path.exists(comp_path):
            raise Exception("competition file does not exist.")

        if is_baseline and baseline_path:
            raise Exception("cannot init with baseline_path while is_baseline=True")

        # read the baseline json
        if baseline_path:
            if not os.path.exists(baseline_path):
                raise Exception("baseline file does not exist.")

            with open(baseline_path) as json_file:
                self.baseline = json.load(json_file)
            if verbose: print("baseline metrics", self.baseline)
        
        # read the competition json
        if comp_path:
            with open(comp_path) as j_file:
                self.competition = json.load(j_file)
            if verbose: print("competition constants", self.competition)

        # read the csv
        if csv:
            self.df = pd.read_csv( csv, delimiter=',')
            datasets = self.df.dataset.unique()
            if verbose: print("Found unique datasets:", datasets)
            if len(datasets)< self.competition["min_qual_dsets"]:
                raise Exception("Minimum number of datasets not met.")
   
        self.algoname = algoname 
        self.system_cost = system_cost
        self.is_baseline = is_baseline
        self.pending = pending
        self.print_best = print_best
        self.show_baseline_table = show_baseline_table
        self.verbose = verbose
        self.evals = {} 
        self.summary = None

    def load_state_from_files( self, summary_json, evals_json ):
        '''Load state from previously stored json files.'''

        if not self.summary:
            print("Warning: summary was not empty/none")
        with open(summary_json) as json_file:
            self.summary = json.load(json_file) 

        if not self.evals:
            print("Warning: evals was not empty/none")
        with open(evals_json) as json_file:
            self.evals = json.load(json_file) 

        print("Loaded state from", summary_json, "and", evals_json)

    def eval_all(self, compute_score=True, save_summary=None, save_evals=None, reject_anomalies=False ):
        '''Evaluate all the competition datasets.'''
        
        self.evals = {}
        for dataset in self.competition["datasets"]:
            ret = self.eval_dataset(dataset, reject_anomalies)
            if self.is_baseline and not ret:
                raise Exception("Baseline needs to support all the datasets.")
            

        num_qual_datasets = len( list(self.evals.keys() ) )
        if self.is_baseline:
            if num_qual_datasets != len(self.competition["datasets"]):
                raise Exception("Baseline needs to support all the datasets.")
        else: # is_baseline = False
            if num_qual_datasets< self.competition["min_qual_dsets"] and not self.is_baseline:
                raise Exception("Submission does support enough datasets (%d/%d) to qualify." % 
                    (num_qual_datasets, len(self.competition["datasets"])))
       
        if self.verbose: print("This submission has qualified for the competition.")

        if compute_score:

            # prepare a dictionary for dataframe
            summary = {}
            for dataset in self.competition["datasets"]:
                if not dataset in list(self.evals.keys()):
                    cols = [ None, None, None, None ]
                else:
                    if dataset in self.pending:
                        cols = [ None, None, None, None ]
                    else:
                        cols = [ self.evals[dataset]["best_recall"][1],
                            self.evals[dataset]["best_qps"][1],
                            self.evals[dataset]["best_wspq"][2],
                            self.evals[dataset]["cost"][0] ]
                        # good change best_wspq and cost were not collected
                        if cols[2]==0.0: cols[2] = None
                        if cols[3]==0.0: cols[3] = None
                        
                summary[dataset] = cols
          
            if not self.is_baseline:
                # 
                # compute ranking scores (for final row)
                #
                if self.verbose: print("computing scores")
                scores = [0, 0, 0, 0] 
                for dataset in self.competition["datasets"]:
                    if summary[dataset][0]: # recall
                        diff = summary[dataset][0] - self.baseline["datasets"][dataset]["recall"][0]
                        if self.verbose: print("diff recall",dataset,diff)
                        scores[0] += diff

                    if summary[dataset][1]: # throughput
                        diff = summary[dataset][1] - self.baseline["datasets"][dataset]["qps"][0]
                        if self.verbose: print("diff qps",dataset,diff)
                        scores[1] += diff 

                    if summary[dataset][2]: # power
                        diff = summary[dataset][2] - self.baseline["datasets"][dataset]["wspq"][0]
                        if self.verbose: print("diff power",dataset,diff)
                        scores[2] += diff

                    if summary[dataset][3]: # cost
                        diff = summary[dataset][3] - self.baseline["datasets"][dataset]["cost"][0]
                        if self.verbose: print("diff cost",dataset,diff)
                        scores[3] += diff
                
                if scores[2]==0.0: scores[2] = None
                if scores[3]==0.0: scores[3] = None
         
                idx = list(summary.keys()) + ["ranking-score"]
                summary["ranking-score"] = scores
                if self.verbose: print("summary", summary)
            else: # is_baseline=True
                # by definition, the baseline score is zero
                summary["ranking-score"] = [ 0.0, 0.0, 0.0, 0.0 ]
                idx = list(summary.keys()) 
                if self.verbose: print("summary", summary)

            self.summary = summary
            self.evals["summary"] = summary

            df = pd.DataFrame(self.summary.values(),columns=['recall','qps','power','cost'],index=idx)
            if self.verbose: print(df)
            if save_summary:
                #df.to_csv(save_summary)
                with open(save_summary, 'w') as outfile:
                    json.dump(self.summary, outfile)  
                print("Saved CSV to", save_summary)
            if save_evals:
                with open(save_evals, 'w') as outfile:
                    json.dump(self.evals, outfile)  
                print("Saved evals JSON to", save_evals)

        return True

    def commit_baseline(self, save_path):
        '''Commit this benchmark to a baseline config.'''

        if not self.is_baseline:
            raise Exception("This is not a baseline evaluation.")
        
        if not self.summary:
            raise Exception("No summary available.")

        baseline = {
            "version":  "2021",
            "datasets": {}
        }

        # summary 0=recall, 1=qps, 2=power, 3=cost
        for dataset in self.competition["datasets"]:

            s = self.summary[dataset]
            print("S",dataset, s)
            baseline["datasets"][dataset] = {
                "recall":       [ s[0] ],
                "qps":          [ s[1] ],
                "wspq":         [ s[2] ],
                "cost":         [ s[3] ],
                "min-recall":   self.competition["min_recall"] if s[0]>= self.competition["min_recall"] else s[0],
                "min-qps":      self.competition["min_qps"] if s[1]>= self.competition["min_qps"] else s[1],
                "min-wspq":     [ 0.0 ],
                "system_cost":  self.system_cost
            }

        if self.verbose: print(baseline)

        with open(save_path, 'w') as outfile:
            json.dump(baseline, outfile)

        print("Wrote new baseline json at %s" % save_path )

    def show_summary(self, savepath=None, public=True):
        '''Show the final benchmarks.'''

        if not self.evals:
            raise Exception("No evaluation was performed yet.")

        if not self.summary:
            raise Exception("No summary to show.")
            
        idx = list(self.summary.keys()) 
        df = pd.DataFrame(self.summary.values(),columns=['recall','qps','power','cost'],index=idx)

        df['cost'] = df['cost'].map( lambda x: '{:,.2f}'.format(x) if x!=None and not np.isnan(x) else np.nan )
        df = df.replace(np.nan,'')
        if self.verbose: print(df)
        
        title = "BigANN Benchmarks Competition Summary For '%s' (%s)" % (self.algoname, "public" if public else "private" )

        # try to display a summary table when run in jupyter
        try:
            from IPython.display import display, HTML
            df['cost'] = df['cost'].map( lambda x: '{:,.2f}'.format(x) if not np.isnan(x) else np.nan )
            df = df.replace(np.nan,'')
            
            html = df.to_html()
            html = "<b>%s</b><br>" % title + html
            #print(html)
            display(HTML(html))
        except:
            print("Hiding exception: This is likely not a jupyter environment.")
            # traceback.print_exc()

        if savepath: # Try to save the table to an image file and dataframe as csv
            try:
                import dataframe_image as dfi
                dfs = df.style.set_caption(title)
                dfi.export(dfs, savepath)
                print("saved summary image at %s" % savepath)
            
            except:
                traceback.print_exc()

        # possibly show the baseline table as well in jupyter 
        if not self.is_baseline and self.show_baseline_table: 
            summary = {}
            for dataset in self.competition["datasets"]:
                cols = [ self.baseline["datasets"][dataset]["recall"][0],
                    self.baseline["datasets"][dataset]["qps"][0],
                    self.baseline["datasets"][dataset]["wspq"][0],
                    self.baseline["datasets"][dataset]["cost"][0] ]
                summary[dataset] = cols
            
            idx = list(summary.keys())
            df = pd.DataFrame(summary.values(),columns=['recall','qps','power','cost'],index=idx)
            if self.verbose: print(df)

            title = "BigANN Benchmarks Baseline"

            # try to display table when run in jupyter
            try:
                from IPython.display import display, HTML
                df['cost'] = df['cost'].map( lambda x: '{:,.2f}'.format(x) if not np.isnan(x) else np.nan )
                df = df.replace(np.nan,'')

                html = df.to_html()
                html = "<b>%s</b><br>" % title + html
                #print(html)
                display(HTML(html))
            except:
                traceback.print_exc()

    def argsort(l):
        return sorted(range(len(l)), key=l.__getitem__)

    def eval_dataset(self, dataset, reject_anomalies=False):
        '''Eval benchmarks for a dataset.'''
      
        if not dataset in self.competition["datasets"]:
            raise Exception("Not a valid dataset (%s)" % dataset)

        if self.verbose: print()
        print("evaluating %s" % dataset)

        rows = self.df.loc[ self.df['dataset'] == dataset ] 
        if rows.shape[0]> self.competition["max_run_params"]:
            print("Invalid number of run parameters at %d" % rows.shape[0])
            #return False

        if len(rows)==0:
            if self.verbose: print("Warning: No data for %s present" % dataset)
            return False 

        #
        # eval recall benchmark 
        #
        qps = rows["qps"].tolist()
        if self.verbose: print("qps:", qps)
        recall = rows["recall/ap"].tolist()
        if self.verbose: print("recall:", recall)
        parameters = rows["parameters"].tolist()
        if self.verbose: print("parameters", parameters)
        search_times = [None]*len(parameters)
        caching = [None]*len(parameters)
        anomaly = [None]*len(parameters)
        if "caching" in rows:
            search_times = rows["search_times"].tolist()
            caching = rows["caching"].tolist()
            anomaly = [ True if el.strip()[0]=="1" else False for el in rows["caching"].tolist() ]

        # get qualifying run parameters
        if self.is_baseline:
            min_qps = self.competition["min_qps"]
        else:
            min_qps = self.baseline["datasets"][dataset]["min-qps"] # The baseline informed min lives in baseline now
        if self.verbose: print("for recall, min_qps=", min_qps)
        if reject_anomalies:
            print("WARNING: REJECT ANOMALIES for best_recall...")
            qualifiers = [ el for el in list(zip(qps, recall, parameters, anomaly)) if el[0]>=min_qps and not el[3] ]
        else:
            qualifiers = [ el for el in list(zip(qps, recall, parameters, anomaly)) if el[0]>=min_qps ]
        if len(qualifiers)>0:
            if self.verbose: print("qualifiers at min_qps=%f" % min_qps, qualifiers)
            best_recall = sorted(qualifiers,key=lambda x: x[1])[-1] # sort by highest recall and take it
        else:
            if self.verbose: print("WARNING: NO qualifiers meeting min_qps %f, trying without..." % min_qps)
            if reject_anomalies:
                print("WARNING: REJECT ANOMALIES for best_recall...")
                qualifiers = [ el for el in list(zip(qps, recall, parameters, anomaly)) if not el[3] ]
            else:
                qualifiers = [ el for el in list(zip(qps, recall, parameters, anomaly)) ]
            if self.verbose: print("WARNING: NEW qualifiers no min_qps", qualifiers)
            best_recall = sorted(qualifiers, key=lambda x: x[1][-1]) # sort by highest recall and take it
        if self.verbose or self.print_best: print("Best recall at", best_recall, "via", qualifiers[-1])

        #
        # eval throughput benchmark
        #
        if self.is_baseline:
            min_recall = self.competition["min_recall"]
        else:
            min_recall = self.baseline["datasets"][dataset]["min-recall"] # The baseline informed min lives in baseline now
        if self.verbose: print("for throughput, min_recall=", min_recall)
        if reject_anomalies:
            print("WARNING: REJECT ANOMALIES for best_qps...")
            qualifiers = [ el for el in list(zip(recall, qps, parameters, anomaly)) if el[0]>=min_recall and not el[3] ]
        else:
            qualifiers = [ el for el in list(zip(recall, qps, parameters, anomaly)) if el[0]>=min_recall ]
        if len(qualifiers)==0: 
            if self.verbose: print("WARNING: NO qualifiers meeting min_recall %f, trying without..." % min_recall)
            if reject_anomalies:
                print("WARNING: REJECT ANOMALIES for best_qps...")
                qualifiers = [ el for el in list(zip(recall, qps, parameters, anomaly)) if not el[3] ]
            else:
                qualifiers = [ el for el in list(zip(recall, qps, parameters, anomaly)) ]
            if self.verbose: print("WARNING: NEW qualifiers no min_recall", qualifiers)
            best_qps = sorted(qualifiers,key=lambda x: x[0])[-1] # sort by highest recall and take that qps
        else:
            if self.verbose: print("qualifiers at min_recall=%f" % min_recall, qualifiers)
            best_qps = sorted(qualifiers,key=lambda x: x[1])[-1] # sort by highest qps and take that qps
        if self.verbose or self.print_best: print("Best qps at ", best_qps, "via", qualifiers[-1])

        #
        # eval power benchmark
        #
        if "wspq" in rows.keys():
            wspq = rows["wspq"].tolist()
            if self.verbose: print("for power, min_qps=%f min_recall=%f " % (min_qps,min_recall))
            if reject_anomalies:
                print("WARNING: REJECT ANOMALIES for best_wspq...")
                qualifiers = [ el for el in list(zip(recall, qps, wspq, parameters, anomaly )) if el[0]>=min_recall and el[1]>min_qps and not el[4] ]
            else:
                qualifiers = [ el for el in list(zip(recall, qps, wspq, parameters, anomaly )) if el[0]>=min_recall and el[1]>min_qps ]
            if self.verbose: print("qualifiers at min_qps=%f and min_recall=%f" % (min_qps, min_recall), qualifiers)
            if len(qualifiers)==0:
                if self.verbose: print("WARNING: NO qualifying power runs meeting both min_qps and min_recall...")
                # fall back to min_recall threshold
                if reject_anomalies:
                    print("WARNING: REJECT ANOMALIES for best_wspq...")
                    qualifiers = [ el for el in list(zip(recall, qps, wspq, parameters, anomaly)) if el[0]>=min_recall and not el[4]]
                else:
                    qualifiers = [ el for el in list(zip(recall, qps, wspq, parameters, anomaly)) if el[0]>=min_recall ]
                if len(qualifiers)==0:
                    qualifiers = [ el for el in list(zip(recall, qps, wspq, parameters,anomaly)) ]
                    if self.verbose: print("WARNING: NEW qualifiers at min_recall=%f" % min_recall, qualifiers)
                    if len(qualifiers)==0:
                        print("No qualifying power runs meeting min_recall...")
                        return False
            best_wspq = sorted(qualifiers,key=lambda x: x[2])[0]
        else:
            wspq = []
            best_wspq = [0,0,0]
        if self.verbose or self.print_best: print("Best power at", best_wspq, qualifiers[-1])

        #
        # eval cost benchmark
        #
        if self.system_cost!=None and self.system_cost<=0:
            print("WARNING: System cost not provided for %s, so not computing cost benchmark." % dataset)
            total_cost = 0
        else:      
            # determine (ceiling) number of units needed to scale to competition's cost qps 
            no_units = math.ceil( self.competition["cost_qps"] / best_qps[1] )
            if self.verbose: print("Cost benchmark: %d systems required at best_qps=%f" % (no_units, best_qps[1]))

            # determine capex 
            capex = no_units * self.system_cost
            if self.verbose: print("Cost benchmark: capex=%f at unit_cost=%f" % ( capex, self.system_cost ) )

            # determine opex = (w*s/q) * ( 1kw/1000w) * ( 1h/3600s) * ( $ / kwh ) * ( opex_time_yr * 365 days/yr * 24h/day * 3600s/h * cost_qps )
            opex_kwh_per_query = (best_wspq[2]) * (1.0/1000) * (1.0/3600 ) 
            if self.verbose: print("Cost benchmark: opex_kwh_per_query=%f at best_wspq=%f" % (opex_kwh_per_query, best_wspq[2]) )

            opex_tot_queries = self.competition["cost_qps"] * self.competition["opex_time"] * 365.0 * 24.0 * 3600.0
            if self.verbose: print("Cost benchmark: opex_tot_queries=%f at opex_time=%f" % (opex_tot_queries, self.competition["opex_time"] ) )

            opex = opex_kwh_per_query * opex_tot_queries * self.competition["kwh_cost"]
            if self.verbose: print("Cost benchmark: opex=%f" % opex )

            total_cost = capex + opex

            #print("TOTAL", dataset, total_cost, capex, opex )

        #
        # process anomalies
        #
        if "caching" in rows:
            search_times = rows["search_times"].tolist()
            caching = rows["caching"].tolist()
            #print("SEARCH TIMES", search_times)
            #print("CACHING", caching)
            # get anomaly counts
            ac = 0
            tc = 0
            for idx, cachinfo in enumerate(caching):
                tf = True if int(cachinfo.split()[0])==1 else False
                th = float(cachinfo.split()[1])
                perc =  float(cachinfo.split()[2])
                if tf: ac = ac+1
                query_run_count = len( search_times[idx].split() )
                tc = tc + 1 #query_run_count
            # print("CACHING STATS", ac, tc )

            # compute the number of "best" parameters that were "anomalous"
            critical_ac = 0
            if best_recall[3]: critical_ac += 1
            if best_qps[3]: critical_ac += 1
            if best_wspq[4]: critical_ac += 1

            cacheinfo = [ ac, tc, critical_ac ]

        else:
            cacheinfo = [ 0, 0, 0 ]
            
 
        this_eval = { 
            "qps": qps,
            "recall": recall,
            "wspq": wspq,
            "best_recall": best_recall,
            "best_qps": best_qps,
            "best_wspq": best_wspq,
            "cost": [total_cost, capex, opex, self.system_cost, no_units, opex_kwh_per_query*opex_tot_queries] if len(wspq)>0 and total_cost!=0 else [0,0,0,0,0,0],
            "cache": cacheinfo
        }

        #print("EVAL", dataset, this_eval)
        #print()
        
        self.evals[dataset] = this_eval

        return True

    def plot_recall(self, dataset, zoom=None, tweak=None, savepath=None):
        '''Plot all recall data for jupyterlab'''

        if not self.evals:
            raise Exception("No evaluation is available for plotting.")

        if not dataset in self.evals.keys():
            print("Submission did not qualify for %s on the recall benchmark." % dataset)
            return False

        recall = self.evals[dataset]["recall"]
        qps = self.evals[dataset]["qps"]
        best = self.evals[dataset]["best_recall"]
        if self.verbose: print("BEST RECALL", best)

        # plot all run parameters
        plt.rcParams['font.size'] = '16'
        fig = plt.figure(figsize=(16,8))
        ax = fig.add_subplot(121)
        col = ax.scatter( qps, recall, color='red' )
        ax.set_title("all run parameters")
        ax.set_ylabel("recall")
        ax.set_xlabel("qps")
        ax.annotate("%f (qps=%f)" % (best[1],best[0]),
                    xy=(best[0],best[1]),
                     xycoords='data',
                     xytext=(best[0],best[1]) if not tweak else [sum(x) for x in zip(best,tweak[0])],
                     textcoords='data',
                     arrowprops=dict(arrowstyle= '->',
                                     color='black',
                                     lw=1.0,
                                     ls='--')
                   )

        # zoom in on the parameters worth considering for this benchmark
        ax = fig.add_subplot(122)
        col = ax.scatter( qps, recall, color='red' )
        if zoom:
            ax.set_xlim(zoom[0]) #[1900,2600])
            ax.set_ylim(zoom[1]) #[0.97, 0.99])
        ax.set_xlabel("qps")
        ax.set_title("focused at min qps")
        ax.annotate("%f (qps=%f)" % (best[1],best[0]),
                    xy=(best[0],best[1]),
                     xycoords='data',
                     xytext=(best[0],best[1]) if not tweak else [sum(x) for x in zip(best,tweak[1])],
                     textcoords='data',
                     arrowprops=dict(arrowstyle= '->',
                                     color='black',
                                     lw=1.0,
                                     ls='--')
                   )

        # label the plots
        t = plt.suptitle("%s recall benchmark (recall=recall@10)" % dataset )

        if savepath: # save plot to file
            print("saving image to %s" % savepath )
            fig.savefig( savepath )

    def plot_throughput(self, dataset, zoom=None, tweak=None, savepath=None):
        '''Plot all qps data for jupyterlab'''

        if not self.evals:
            raise Exception("No evaluation is available for plotting.")

        if not dataset in self.evals.keys():
            print("Submission did not qualify for %s on the throughput benchmark." % dataset)
            return False

        recall = self.evals[dataset]["recall"]
        qps = self.evals[dataset]["qps"]
        best = self.evals[dataset]["best_qps"]
        if self.verbose: print("BEST QPS", best)

        # plot all run parameters
        plt.rcParams['font.size'] = '16'
        fig = plt.figure(figsize=(16,8))
        fig.clf()
        ax = fig.add_subplot(121)
        col = ax.scatter( recall, qps, color='red' )
        ax.set_title("all run parameters")
        ax.set_xlabel("recall")
        ax.set_ylabel("qps")
        ax.annotate("%f (recall=%f)" % (best[1], best[0]),
                    xy=(best[0],best[1]),
                     xycoords='data',
                     xytext=(best[0],best[1]) if not tweak else [sum(x) for x in zip(best,tweak[0])],
                     textcoords='data',
                     arrowprops=dict(arrowstyle= '->',
                                     color='black',
                                     lw=1.0,
                                     ls='--')
                   )

        # plot just the parameters worth considering for this benchmark
        ax = fig.add_subplot(122)
        col = ax.scatter( recall, qps, color='red' )
        if zoom:
            ax.set_xlim(zoom[0])
            ax.set_ylim(zoom[1])
        ax.set_xlabel("recall")
        ax.set_title("focused" )
        ax.annotate("%f (recall=%f)" % (best[1], best[0]),
                    xy=(best[0],best[1]),
                     xycoords='data',
                     xytext=(best[0],best[1]) if not tweak else [sum(x) for x in zip(best,tweak[1])],
                     textcoords='data',
                     arrowprops=dict(arrowstyle= '->',
                                     color='black',
                                     lw=1.0,
                                     ls='--')
                   )

        # label the plot
        t = plt.suptitle("%s throughput benchmark (qps=queries per second)" % dataset)

        if savepath: # save plot to file
            if self.verbose: print("saving image to %s" % savepath )
            fig.savefig( savepath )

    def plot_power(self, dataset, zoom=None, tweak=None, savepath=None):
        '''Plot all power data for jupyterlab'''

        if not self.evals:
            raise Exception("No evaluation is available for plotting.")

        if not dataset in self.evals.keys():
            print("Submission did not qualify for %s on the power and cost benchmark." % dataset)
            return False

        recall = self.evals[dataset]["recall"]
        qps = self.evals[dataset]["qps"]
        wspq = self.evals[dataset]["wspq"]
        best = self.evals[dataset]["best_wspq"]
        if self.verbose: print("BEST POWER", best)
    
        if len(wspq)==0:
            print("No power metrics were provided.  This submission probably did not qualify for this benchmark.")
            return False

        # plot all run parameters (recall vs wspq)
        plt.rcParams['font.size'] = '16'
        fig = plt.figure(figsize=(16,8))
        fig.clf()
        ax = fig.add_subplot(121)
        col = ax.scatter( recall, wspq, color='red' )
        ax.set_xlabel("recall")
        ax.set_ylabel("wspq")
        ax.set_title("all runs (recall vs wspq)")
        #print("tweak", (best[0],best[2]) if not tweak else [sum(x) for x in zip(best,tweak[0])])
        ax.annotate("%f (recall=%f)" % (best[2], best[0]),
                    xy=(best[0],best[2]),
                     xycoords='data',
                     xytext=(best[0],best[2]) if not tweak else [sum(x) for x in zip((best[0],best[2]),tweak[0])],
                     textcoords='data',
                     arrowprops=dict(arrowstyle= '->',
                                     color='black',
                                     lw=1.0,
                                     ls='--')
                   )

        # plot all run parameters ( qps vs wspq )
        ax = fig.add_subplot(122)
        col = ax.scatter( qps, wspq, color='red' )
        ax.set_xlabel("qps")
        ax.set_title("all runs (qps vs wspq)")
        #print("tweak", (best[1],best[2]) if not tweak else [sum(x) for x in zip(best,tweak[1])])
        ax.annotate("%f (qps=%f)" % (best[2], best[1]),
                    xy=(best[1],best[2]),
                     xycoords='data',
                     xytext=(best[1],best[2]) if not tweak else [sum(x) for x in zip((best[1],best[2]),tweak[1])],
                     textcoords='data',
                     arrowprops=dict(arrowstyle= '->',
                                     color='black',
                                     lw=1.0,
                                     ls='--')
                   )

        # label the plot
        t = plt.suptitle("%s power benchmark (wspq=watt seconds per query)" % dataset)

        if savepath: # save plot to file
            if self.verbose: print("saving image to %s" % savepath )
            fig.savefig( savepath )

def initialize_competition_json(save_path):
    '''Create the competition config.'''

    competition = {
        "version":          "2021",
        "kwh_cost":         0.10,   # 10 cents
        "cost_qps":         100000, # 100,000 queries per second
        "opex_time":        4,      # number of years to evaluate opex
        "min_qual_dsets":   3,
        "max_run_params":   10,
        "min_recall":       0.9,
        "min_qps":          2000,
        "datasets":         [ "deep-1B", "bigann-1B", "text2image-1B", "msturing-1B", "msspacev-1B", "ssnpp-1B" ]
    }

    with open(save_path, 'w') as outfile:
        json.dump(competition, outfile)

    print("Wrote new competition json at %s" % save_path )

if __name__ == "__main__": # Unit test

    # simulate committing a baseline 
    print("Simulating baseline evaluation...")
    evaluator = Evaluator(  "Test_Baseline",
                            "test.csv",
                            "competition2021.json", 
                            system_cost=22021.90, 
                            is_baseline=True,
                            verbose=False)
    evaluator.eval_all(save_path="/tmp/test_baseline_competition_benchmarks.csv")
    evaluator.commit_baseline("/tmp/baseline2021.json")
    evaluator.show_summary(savepath="/tmp/test_baseline_summary.png")
    for dataset in evaluator.competition["datasets"]:
        evaluator.plot_recall(dataset, savepath="/tmp/test_baseline_%s_recall.png" % dataset)
        evaluator.plot_throughput(dataset, savepath="/tmp/test_baseline_%s_throughput.png" % dataset)
        evaluator.plot_power(dataset, savepath="/tmp/test_baseline_%s_power.png" % dataset)
 
    # simulate evaluating a submission
    print("Simulating submission evaluation...")
    evaluator = Evaluator(  "Test_Submission",
                            "test.csv",
                            "competition2021.json", 
                            baseline_path="/tmp/baseline2021.json",
                            system_cost=22021.90, 
                            is_baseline=False )
    evaluator.eval_all(save_path="/tmp/test_submission_competition_benchmarks.csv")
    evaluator.show_summary(savepath="/tmp/test_submission_summary.png")
    for dataset in evaluator.competition["datasets"]:
        evaluator.plot_recall(dataset, savepath="/tmp/test_submission_%s_recall.png" % dataset)
        evaluator.plot_throughput(dataset, savepath="/tmp/test_submission_%s_throughput.png" % dataset)
        evaluator.plot_power(dataset, savepath="/tmp/test_submission_%s_power.png" % dataset)
 
