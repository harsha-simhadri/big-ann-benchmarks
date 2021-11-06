import os
import pandas as pd
import sys
import json
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import math
import traceback

DATASETS        = [ "deep-1B", "bigann-1B", "text2image-1B", "msturing-1B", "msspacev-1B", "ssnpp-1B" ]
MIN_NUM_DATASETS= 3 # Set to 0 for no minimum
MAX_RUN_PARMS   = 10 # Competition rule
 
class Evaluator():
    '''Useful evaluation functionality for the T3 track.'''

    def __init__(self, csv, baseline_path, comp_path, system_cost=None, verbose=False ):
        '''Constructor performs sanity and some competition rule checks.'''

        if sys.version_info[0] < 3:
            raise Exception("Must be using Python 3")

        if not os.path.exists(csv):
            raise Exception("CSV file does not exist.")
        
        if not os.path.exists(baseline_path):
            raise Exception("baseline file does not exist.")
        
        if not os.path.exists(comp_path):
            raise Exception("competition file does not exist.")

        # read the baseline json
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
        if len(datasets)< MIN_NUM_DATASETS:
            raise Exception("Minimum number of datasets not met.")
    
        self.system_cost = system_cost
        self.verbose = verbose
        self.evals = {} 

    def eval_all(self):
        '''Evaluate all the competition datasets.'''
        
        self.evals = {}
        for dataset in DATASETS:
            self.eval_dataset(dataset)

        num_qual_datasets = len( list(self.evals.keys() ) )
        if num_qual_datasets< MIN_NUM_DATASETS:
            raise Exception("Submission does support enough datasets (%d/%d) to qualify." % (num_qual_datasets, len(DATASETS)))
       
        if self.verbose: print("This submission has qualified for the competition.")
        return True

    def show_summary(self):
        '''Show the final benchmarks.'''

        if not self.evals:
            raise Exception("No evaluation was performed yet.")

        #pd.set_option('display.float_format', lambda x: '%.3f' % x)

        # prepare a dictionary for dataframe
        summary = {}
        for dataset in DATASETS:
            if not dataset in list(self.evals.keys()):
                cols = [ None, None, None, None ]
            else:
                cols = [ self.evals[dataset]["best_recall"][1], 
                    self.evals[dataset]["best_qps"][1], 
                    self.evals[dataset]["best_wspq"][2], 
                    self.evals[dataset]["cost"] ]
            summary[dataset] = cols
      
        # 
        # compute scores (for final row)
        #
        if False: # Not ready yet...
            if self.verbose: print("computing scores")
            scores = [0,0,0,0]
            for dataset in DATASETS:
                if summary[dataset][0]:
                    diff = summary[dataset][0] - self.baseline[dataset]["recall"][0]
                    if self.verbose: print("diff recall",dataset,diff)
                    scores[0] += diff

                if summary[dataset][1]:
                    diff = summary[dataset][1] - self.baseline[dataset]["qps"][0]
                    if self.verbose: print("diff qps",dataset,diff)
                    scores[1] += diff 

                if summary[dataset][2]:
                    diff = 0
                    if self.verbose: print("diff power",dataset,diff)
                    scores[2] += diff

                if summary[dataset][3]:
                    diff = 0
                    if self.verbose: print("diff cost",dataset,diff)
                    scores[3] += diff
            
            idx = list(summary.keys()) + ["final-score"]
            summary["final-score"] = scores
            if self.verbose: 
                print("summary", summary)
        else:
            idx = list(summary.keys()) + ["final-score"]
            summary["final-score"] = [ np.nan, np.nan, np.nan, np.nan ]
       
        df = pd.DataFrame(summary.values(),columns=['recall','qps','power','cost'],index=idx)
        if self.verbose: print(df)

        # try to display a table when run in jupyter
        try:
            from IPython.display import display
            df['cost'] = df['cost'].map('${:,.2f}'.format)
            df = df.replace(np.nan,'')
            df = df.replace('$nan','')
            display(df)
        except:
            traceback.print_exc()

    def eval_dataset(self, dataset):
        '''Eval benchmarks for a dataset.'''
       
        if not dataset in DATASETS:
            raise Exception("Not a valid dataset (%s)" % dataset)

        if self.verbose: print("evaluating %s" % dataset)

        rows = self.df.loc[ self.df['dataset'] == dataset ] 
        if rows.shape[0]>MAX_RUN_PARMS:
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

        # get qualifying run parameters
        baseline_recall = self.baseline[dataset]["recall"][0]
        min_qps = self.baseline[dataset]["min-qps"]
        qualifiers = [ pair for pair in list(zip(qps,recall)) if pair[0]>=min_qps and pair[1]>=baseline_recall ]
        if self.verbose: print("qualifiers at min_qps=%f and baseline_recall=%f" % (min_qps, baseline_recall), qualifiers)
        if len(qualifiers)==0:
            print("No qualifying recall runs.")
            return False
        best_recall = sorted(qualifiers,key=lambda x: x[1])[-1]
        if self.verbose: print("Best recall at", best_recall)

        #
        # eval throughput benchmark
        #
        baseline_qps = self.baseline[dataset]["qps"][0]
        min_recall = self.baseline[dataset]["min-recall"]
        qualifiers = [ pair for pair in list(zip(recall,qps)) if pair[0]>=min_recall and pair[1]>=baseline_qps ]
        if self.verbose: print("qualifiers at min_qps=%f and baseline_recall=%f" % (min_qps, baseline_recall), qualifiers)
        if len(qualifiers)==0:
            print("No qualifying throughput runs.")
            return False
        best_qps = sorted(qualifiers,key=lambda x: x[1])[-1]
        if self.verbose: print("Best qps at ", best_qps)

        #
        # eval power benchmark
        #
        wspq = rows["wspq"].tolist()
        qualifiers = [ triple for triple in list(zip(recall,qps,wspq)) if triple[0]>=min_recall and triple[1]>=min_qps ]
        if self.verbose: print("qualifiers at min_qps=%f and min_recall=%f" % (min_qps, min_recall), qualifiers)
        if len(qualifiers)==0:
            print("No qualifying power runs.")
            return False
        best_wspq = sorted(qualifiers,key=lambda x: x[2])[0]
        if self.verbose: print("Best power at", best_wspq)

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

    def plot_recall(self, dataset, zoom=None, tweak=None):
        '''Plot all recall data for jupyterlab'''

        if not self.evals:
            raise Exception("No evaluation is available for plotting.")

        if not dataset in self.evals.keys():
            print("Submission did not qualify for %s on the recall benchmark." % dataset)
            return False

        recall = self.evals[dataset]["recall"]
        qps = self.evals[dataset]["qps"]
        best = self.evals[dataset]["best_recall"]
 
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

    def plot_throughput(self, dataset, zoom=None, tweak=None):
        '''Plot all qps data for jupyterlab'''

        if not self.evals:
            raise Exception("No evaluation is available for plotting.")

        if not dataset in self.evals.keys():
            print("Submission did not qualify for %s on the throughput benchmark." % dataset)
            return False

        recall = self.evals[dataset]["recall"]
        qps = self.evals[dataset]["qps"]
        best = self.evals[dataset]["best_qps"]

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
                    xy=best,
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
                    xy=best,
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

    def plot_power(self, dataset, zoom=None, tweak=None):
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


if __name__ == "__main__": # Unit test

    evaluator = Evaluator("gemini/evaluation/2021/public.csv","baseline2021.json", "competition2021.json", 55726.66, True)
    evaluator.eval_all()
    evaluator.show_summary()

    for dataset in DATASETS:
        print("Trying ", dataset)
        evaluator.plot_recall(dataset)
        evaluator.plot_throughput(dataset)
        evaluator.plot_power(dataset)
 
