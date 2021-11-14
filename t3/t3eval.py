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

    def __init__(self,  algoname, csv, comp_path, baseline_path=None, system_cost=None, 
                        verbose=False, is_baseline=False, pending=[], print_best=False, 
                        show_baseline_table=False ):
        '''Constructor performs sanity and some competition rule checks.'''

        if sys.version_info[0] < 3:
            raise Exception("Must be using Python 3")

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
        with open(comp_path) as j_file:
            self.competition = json.load(j_file)
        if verbose: print("competition constants", self.competition)

        # read the csv
        self.df = pd.read_csv( csv )
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

    def eval_all(self, compute_score=True, save_path=None ):
        '''Evaluate all the competition datasets.'''
        
        self.evals = {}
        for dataset in self.competition["datasets"]:
            self.eval_dataset(dataset)

        num_qual_datasets = len( list(self.evals.keys() ) )
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
                            self.evals[dataset]["cost"] ]
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
                    
                idx = list(summary.keys()) + ["ranking-score"]
                summary["ranking-score"] = scores
                if self.verbose: print("summary", summary)
            else: # is_baseline=True
                # by definition, the baseline score is zero
                idx = list(summary.keys()) 
                if self.verbose: print("summary", summary)

            self.summary = summary

            df = pd.DataFrame(self.summary.values(),columns=['recall','qps','power','cost'],index=idx)
            if self.verbose: print(df)
            if save_path:
                df.to_csv(save_path)
                if self.verbose: print("Saved CSV to", save_path)

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

    def show_summary(self, savepath=None):
        '''Show the final benchmarks.'''

        if not self.evals:
            raise Exception("No evaluation was performed yet.")

        if not self.summary:
            raise Exception("No summary to show.")
            
        idx = list(self.summary.keys()) 
        df = pd.DataFrame(self.summary.values(),columns=['recall','qps','power','cost'],index=idx)
        if self.verbose: print(df)
        
        title = "BigANN Benchmarks Competition Summary For '%s'" % self.algoname

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

        if savepath: # Try to save the table to an image file
            try:
                import dataframe_image as dfi
                dfs = df.style.set_caption(title)
                dfi.export(dfs, savepath)
                if self.verbose: print("saved summary image at %s" % savepath)
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

    def eval_dataset(self, dataset):
        '''Eval benchmarks for a dataset.'''
      
        if not dataset in self.competition["datasets"]:
            raise Exception("Not a valid dataset (%s)" % dataset)

        if self.verbose: print()
        print("evaluating %s" % dataset)

        rows = self.df.loc[ self.df['dataset'] == dataset ] 
        if rows.shape[0]> self.competition["max_run_params"]:
            print("Invalid number of run parameters at %d" % rows.shape[0])
            return False

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

        # get qualifying run parameters
        if True: #self.is_baseline:
            min_qps = self.competition["min_qps"]
            if self.verbose: print("for recall, min_qps=", min_qps)
            qualifiers = [ el for el in list(zip(qps, recall, parameters)) if el[0]>=min_qps ]
            if len(qualifiers)>0:
                if self.verbose: print("qualifiers at min_qps=%f" % min_qps, qualifiers)
                best_recall = sorted(qualifiers,key=lambda x: x[1])[-1] # sort by highest recall and take it
            else:
                if self.verbose: print("WARNING: NO qualifiers meeting min_qps %f, trying without..." % min_qps)
                qualifiers = [ el for el in list(zip(qps, recall, parameters)) ]
                if self.verbose: print("WARNING: NEW qualifiers no min_qps", qualifiers)
                best_recall = sorted(qualifiers, key=lambda x: x[1][-1]) # sort by highest recall and take it
        if False: #else
            min_qps = self.baseline["datasets"][dataset]["min-qps"]
            if self.verbose: print("for recall, min_qps=", min_qps)
            qualifiers = [ el for el in list(zip(qps,recall, parameters)) if el[0]>=min_qps ]
            if self.verbose: print("qualifiers at min_qps=%f" % min_qps, qualifiers)
            if len(qualifiers)==0:
                print("NO qualifying recall runs.")
                return False
            best_recall = sorted(qualifiers,key=lambda x: x[1])[-1] # sort by highest recall and take the highest
        if self.verbose or self.print_best: print("Best recall at", best_recall, "via", qualifiers[-1])

        #
        # eval throughput benchmark
        #
        if True: #self.is_baseline:
            min_recall = self.competition["min_recall"]
            if self.verbose: print("for throughput, min_recall=", min_recall)
            qualifiers = [ el for el in list(zip(recall, qps, parameters)) if el[0]>=min_recall ]
            if len(qualifiers)==0: 
                if self.verbose: print("WARNING: NO qualifiers meeting min_recall %f, trying without..." % min_recall)
                qualifiers = [ el for el in list(zip(recall, qps, parameters)) ]
                if self.verbose: print("WARNING: NEW qualifiers no min_recall", qualifiers)
                best_qps = sorted(qualifiers,key=lambda x: x[0])[-1] # sort by highest recall and take that qps
            else:
                if self.verbose: print("qualifiers at min_recall=%f" % min_recall, qualifiers)
                best_qps = sorted(qualifiers,key=lambda x: x[1])[-1] # sort by highest qps and take that qps
        if False: #else:
            min_recall = self.baseline["datasets"][dataset]["min-recall"]
            if self.verbose: print("for throughput, min_recall=", min_recall)
            qualifiers = [ el for el in list(zip(recall,qps, parameters)) if el[0]>=min_recall ]
            if self.verbose: print("qualifiers at min_recall=%f" % min_recall, qualifiers)
            if len(qualifiers)==0:
                print("NO qualifying throughput runs.")
                return False
            best_qps = sorted(qualifiers,key=lambda x: x[0])[-1] # sort by highest recall and take that qps

        if self.verbose or self.print_best: print("Best qps at ", best_qps, "via", qualifiers[-1])

        #
        # eval power benchmark
        #
        wspq = rows["wspq"].tolist()
        if self.verbose: print("for power, min_qps=%f min_recall=%f " % (min_qps,min_recall))
        qualifiers = [ el for el in list(zip(recall, qps, wspq, parameters )) if el[0]>=min_recall and el[1]>min_qps ]
        if self.verbose: print("qualifiers at min_qps=%f and min_recall=%f" % (min_qps, min_recall), qualifiers)
        if len(qualifiers)==0:
            if self.verbose: print("WARNING: NO qualifying power runs meeting both min_qps and min_recall...")
            # fall back to min_recall threshold
            qualifiers = [ el for el in list(zip(recall, qps, wspq, parameters)) if el[0]>=min_recall ]
            if len(qualifiers)==0:
                qualifiers = [ el for el in list(zip(recall, qps, wspq, parameters)) ]
                if self.verbose: print("WARNING: NEW qualifiers at min_recall=%f" % min_recall, qualifiers)
                if len(qualifiers)==0:
                    print("No qualifying power runs meeting min_recall...")
                    return False
        best_wspq = sorted(qualifiers,key=lambda x: x[2])[0]
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
 
        this_eval = { 
            "qps": qps,
            "recall": recall,
            "wspq": wspq,
            "best_recall": best_recall,
            "best_qps": best_qps,
            "best_wspq": best_wspq,
            "cost": total_cost
        }
        
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
            if self.verbose: print("saving image to %s" % savepath )
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
 
