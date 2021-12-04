import os
import sys
import math
import json
import pandas as pd
from string import Template
import t3eval

#
# variables that affect LB generation
#
RE_EXPORT               = False
PROCESS_CSV             = False
LEADERBOARD_GEN         = True

PUBLIC                  = False # Set to False for private leaderboard gen
REJECT_ANOMALIES        = False

SKIP_DB                 = [ ] if PUBLIC else [ "msspacev-1B" ] # private GT for msspacev has error
SENSORS                 = False

#
# constants
#
TOTAL_SUBM              = 6
COMP_RESULTS_TOPLEVEL   = "/Users/gwilliams/Projects/BigANN/competition_results"
CACHE_RESULTS_TOPLEVEL  = "/Users/gwilliams/Projects/BigANN/cache_detect_results"
T3_EVAL_TOPLEVEL        = "t3/eval_2021"

SUBM_MAPPING            = \
{
    "faiss_t3": {
        "team":         "Facebook Research",
        # last - "results_dir":  "%s/faiss_t3/results.baseline_focused" % COMP_RESULTS_TOPLEVEL,
        # last - "export_fname": "public_focused.csv",
        "results_dir":  ( "%s/faiss/public/results_faiss_stimes_all_dsets" % CACHE_RESULTS_TOPLEVEL ) if PUBLIC else \
            "%s/faiss/private/results_merge__faiss_priv_2_dsets__private_4_dsets" % CACHE_RESULTS_TOPLEVEL,
        "export_fname": "public_w_cache_detect.csv" if PUBLIC else \
            "private_w_cache_detect.csv",
        "cache_detect": True,
        "anomaly_explain": "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/ANOMALIES.md",
        "not_part":     [ ],
        "system_cost":  22021.90,
        "cost_approved":True,
        "md_prefix":    "BS",
        "status":       "final" if PUBLIC else "eval", 
        "display_hw":   "NVidia GPU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md",
        "org":          True,
        "evaluator":    "George Williams",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/faiss_t3.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/EvalPublic.ipynb)" if PUBLIC else \
                            "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/EvalPrivate.ipynb)" 
    },
    "optanne_graphann": {
        "team":         "Intel",
        # last - "results_dir":  "%s/optanne_graphann/results.with_power_capture" % COMP_RESULTS_TOPLEVEL,
        # last - "export_fname": "public_with_power_capture.csv",
        # last-last "results_dir":  "%s/intel/results_intel_multigpu_all_stimes" % CACHE_RESULTS_TOPLEVEL,
        # last-last-last  "results_dir":  "%s/intel/results_updated_config_with_anomaly_mitigation" % CACHE_RESULTS_TOPLEVEL,
        "results_dir":  ( "%s/intel/public/results_final_changes_to_3_dsets" %  CACHE_RESULTS_TOPLEVEL ) if PUBLIC else \
            "%s/intel/private/results_intel_priv_all" % CACHE_RESULTS_TOPLEVEL, 
        "export_fname": "public_w_cache_detect.csv" if PUBLIC else \
            "private_w_cache_detect.csv",
        "cache_detect": True,
        "anomaly_explain": "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/ANOMALIES.md",
        "not_part":     [ ],
        "system_cost":  14664.20,
        "cost_approved":True,
        "md_prefix":    "OPT1",
        "status":       "final" if PUBLIC else "eval", 
        "display_hw":   "Intel Optane",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md",
        "org":          False,
        "evaluator":    "George Williams",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/graphann.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/EvalPublic.ipynb)" if PUBLIC else \
                            "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/EvalPrivate.ipynb)"
    },
    "gemini": {
        "team":         "GSI Technology",
        # last "results_dir":  "%s/gemini/results_merge_new_ssnpp_text1image_to_use_gsl_release/merged" % COMP_RESULTS_TOPLEVEL,
        # last "export_fname": "public_gsl_release_merged_latest_ssnpp_text2image.csv",
        "results_dir":  ( "%s/gsi/results_final_run" % CACHE_RESULTS_TOPLEVEL ) if PUBLIC else \
            ( "%s/gsi/results_gsi_priv_4_dsets" % CACHE_RESULTS_TOPLEVEL ),
        "export_fname": "public_w_cache_detect.csv" if PUBLIC else "private_w_cache_detect.csv",
        "cache_detect": True,
        "anomaly_explain": False,
        "not_part":     ["power","cost" ],
        "system_cost":  55726.66,
        "cost_approved":True,
        "md_prefix":    "GEM",
        "status":       "final" if PUBLIC else "eval", 
        "display_hw":   "LedaE APU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md",
        "org":          True,
        "evaluator":    "George Williams",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/gemini.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/EvalPublic.ipynb)" if PUBLIC else \
                            "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/EvalPrivate.ipynb)"
    },
    "diskann": {
        "team":         "Microsoft Research India",
        "use_subm_dir": "diskann-bare-metal",
        "results_dir":  None,
        "export_fname": "diskann-bare-metal-res-pruned.csv" if PUBLIC else False,
        "cache_detect": False,
        "not_part":     [ "power", "cost" ],
        "system_cost":  0,
        "cost_approved":True,
        "md_prefix":    "MSD",
        "status":       "final" if PUBLIC else "eval", 
        "display_hw":   "Dell PowerEdge",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md",
        "org":          True,
        "evaluator":    "Harsha Simhadri",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/diskann-t2.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/EvalPublic.ipynb)" if PUBLIC else "NA"
    },
    "cuanns_multigpu": {
        "team":         "NVidia",
        # last - "results_dir":  "%s/nvidia/cuanns_multigpu/results3.power_mon" % COMP_RESULTS_TOPLEVEL,
        # last = "export_fname": "results3.power_mon.csv", 
        "results_dir":  ( "%s/nvidia/multigpu/public/results_nv_multi_stimes_all" % CACHE_RESULTS_TOPLEVEL ) if PUBLIC else False,
        "export_fname": "public_w_cache_detect.csv" if PUBLIC else False,
        "cache_detect": True,
        "not_part":     [ ],
        "anomaly_explain": "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/ANOMALIES.md",
        "system_cost":  150000,
        "cost_approved":False,
        "md_prefix":    "NV",
        "status":       "final" if PUBLIC else "eval", 
        "display_hw":   "NVidia GPU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md",
        "org":          False,
        "evaluator":    "George Williams",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_multigpu.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/EvalPublic.ipynb)" if PUBLIC else "NA"
    },
    "cuanns_ivfpq": {
        "team":         "NVidia",
        # lastlast - "results_dir":  "%s/nvidia/cuanns_ivfpq/results.updated_algos_ivfpq" % COMP_RESULTS_TOPLEVEL,
        # lastlast = "export_fname": "res.updated_algos_ivfpq.csv",
        # last "results_dir":  "%s/nvidia/ivfpq/results_nv_ivfpq_merge_all_and_1" % CACHE_RESULTS_TOPLEVEL,
        # last "results_dir":  "%s/nvidia/ivfpq/results_nv_ivfpq_reduce_anomalies_config_stimes_all" % CACHE_RESULTS_TOPLEVEL,
        "results_dir" : ( "%s/nvidia/ivfpq/public/results_nv_ivfpq_merge__reduce_anomalies_config_stimes_all__last_text2image_config" %  CACHE_RESULTS_TOPLEVEL ) \
            if PUBLIC else  "%s/nvidia/ivfpq/private/results_nv_ivfpq_priv_all" % CACHE_RESULTS_TOPLEVEL,
        "export_fname": "public_w_cache_detect.csv" if PUBLIC else \
            "private_w_cache_detect.csv",
        "cache_detect": True,
        "not_part":     [ ],
        "anomaly_explain": "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/ANOMALIES.md",
        "system_cost":  150000,
        "cost_approved":False,
        "md_prefix":    "NV2",
        "status":       "final" if PUBLIC else "eval", 
        "display_hw":   "NVidia GPU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md",
        "org":          False,
        "evaluator":    "George Williams",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_ivfpq.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/EvalPublic.ipynb)" if PUBLIC else \
                            "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/EvalPrivate.ipynb)"
    },
    "baseline": "faiss_t3"
}

def process_subm( subm ):

    print()
    print("processing subm=%s" % subm)

    # check submexists under eval dir
    subm_dir = SUBM_MAPPING[subm]["use_subm_dir"] \
        if "use_subm_dir" in SUBM_MAPPING[subm].keys() else subm
    eval_subm_dir = os.path.join( T3_EVAL_TOPLEVEL, subm_dir )
    print("checking %s exists..." % eval_subm_dir)
    if not os.path.exists( eval_subm_dir ):
        print("path does not exist: ", eval_subm_dir )
        sys.exit(1)

    # check results dir is valid
    override_export = False
    results_dir = SUBM_MAPPING[subm]["results_dir"]
    if results_dir == None or results_dir==False:
        override_export = True
        if RE_EXPORT:
            print("WARNING: For %s, results dir missing so overriding export..." % subm)
    elif not os.path.exists( eval_subm_dir ):
        print("results_dir path does not exist: ", results_dir )
        sys.exit(1)
  
    # check there exists an data export file
    override_eval = False
    if SUBM_MAPPING[subm]["export_fname"]==False:
        print("No export_fname for", subm, "skipping any export")
        override_export=True
        override_eval = True
    else:
        export_file = os.path.join( eval_subm_dir, SUBM_MAPPING[subm]["export_fname"] )
        if not os.path.exists( export_file ):
            print("export file path does not exist: ", export_file )
            if not RE_EXPORT: sys.exit(1)
        else:
            print("export file exists: ", export_file )

    # create export.csv from results directory as needed
    exported = False
    if RE_EXPORT and not override_export:
        print("Starting export of ",subm, "via", results_dir )

        # unlink top-level "results" dir
        print("unlinking ./results")
        stream = os.popen("unlink ./results")
        print("result of unlink=", stream.read())

        # link to relevant "results" dir
        cwd = os.getcwd()
        link_cmd = "ln -s %s  %s" % ( results_dir, os.path.join(cwd, "results") )
        print("running link command=", link_cmd)
        stream = os.popen(link_cmd)
        print("result of link=", stream.read())

        # run the export command
        if SUBM_MAPPING[subm]["cache_detect"]:
            export_cmd = "python data_export.py %s --recompute %s --search_times --detect_caching 0.3 --output \"%s\"" \
                % ( " " if "power" in SUBM_MAPPING[subm]["not_part"] else "--sensors", " " if PUBLIC else "--private-query", export_file )
        else:
            export_cmd = "python data_export.py --recompute --sensors --output='%s'" \
                % ( " " if PUBLIC else "--private-query", export_file )
        print("running export command->", export_cmd )
        stream = os.popen(export_cmd)
        print("result of export=", stream.read())

        # check export file
        if not os.path.exists( export_file ):
            print("could not find export_file" % export_file)
            sys.exit(1)
        exported = True    
    else:
        print("not running data export for", subm)

    # do eval
    if override_eval:
        print("Skipping eval for", subm)
        return False
    elif SUBM_MAPPING["baseline"] == subm: # it's the baseline 
        evaluator = t3eval.Evaluator(   subm, 
                                        export_file,
                                        "t3/competition2021.json",
                                        system_cost= SUBM_MAPPING[subm]["system_cost"],
                                        verbose=False,
                                        is_baseline=True,
                                        pending = [],
                                        print_best=False )
        evaluator.eval_all(             save_summary=os.path.join(eval_subm_dir, "%s_summary.json" % ( "public" if PUBLIC else "private") ),
                                        save_evals=os.path.join(eval_subm_dir, "%s_evals.json" % ( "public" if PUBLIC else "private" ) ),
                                        reject_anomalies=REJECT_ANOMALIES,
                                        skipdb=SKIP_DB)
        evaluator.commit_baseline(      "t3/%s_baseline2021.json" % ( "public" if PUBLIC else "private" ),
                                        skipdb=SKIP_DB)
        evaluator.show_summary(         savepath=os.path.join( eval_subm_dir, "%s_summary.png" % ( "public" if PUBLIC else "private" )),
                                        public= True if PUBLIC else False )
        return True
    else:
        # print("EVALUATOR", SUBM_MAPPING[subm])
        evaluator = t3eval.Evaluator(   subm, 
                                        export_file,
                                        "t3/competition2021.json",
                                        baseline_path="t3/%s_baseline2021.json" % ( "public" if PUBLIC else "private" ),
                                        system_cost= SUBM_MAPPING[subm]["system_cost"],
                                        verbose=False,
                                        is_baseline=False,
                                        pending = [],
                                        print_best=False )
        evaluator.eval_all(             save_summary=os.path.join(eval_subm_dir, "%s_summary.json" % ( "public" if PUBLIC else "private" )),
                                        save_evals=os.path.join(eval_subm_dir, "%s_evals.json" % ( "public" if PUBLIC else "private" )),
                                        reject_anomalies=REJECT_ANOMALIES,
                                        skipdb=SKIP_DB)
        evaluator.show_summary(         savepath=os.path.join( eval_subm_dir, "%s_summary.png" % ( "public" if PUBLIC else "private" )),
                                        public= True if PUBLIC else False )
        return True

def mklnka( val, fmt, subm, db, benchmark ):
    if benchmark=="qps": benchmark="throughput"
    use_subm = SUBM_MAPPING[subm]["use_subm_dir"] \
        if "use_subm_dir" in SUBM_MAPPING[subm].keys() else subm
    eval_img = os.path.join( "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021", \
        use_subm, ( "%s_%s.png" % ( db, benchmark) ) if PUBLIC else ( "private_%s_%s.png" % ( db, benchmark) ) )
    #print("eval img", val, fmt, subm, db, benchmark, "-->", eval_img)
    if REJECT_ANOMALIES: 
        lnk = fmt.format(val)
    else:
        lnk = "[%s](%s)" % ( fmt.format(val), eval_img )
    return lnk 

def mklnkr( idx, benchmark, approved=True ):
    links = {   "recall":"#recall-or-ap-rankings", 
                "qps":"#throughput-rankings",
                "power":"#power-rankings",
                "cost":"#cost-rankings" }
    lnk = "[%d](%s)" % ( idx, links[benchmark] )
    if not approved:
        lnk = lnk + "\*\*"
    return lnk 


def produce_rankings(subms):

    print("Producing rankings...")

    def get_master_df():
        '''retrieve all submission data into one master dataframe'''
        dfs = []

        # get the data from summary csv
        for subm in subms:
    
                if not SUBM_MAPPING[subm]["evals"]:
                    print("WARNING: no evals found for", subm)
                    continue                   
  
                subm_dir = SUBM_MAPPING[subm]["use_subm_dir"] \
                    if "use_subm_dir" in SUBM_MAPPING[subm].keys() else subm
                eval_subm_dir = os.path.join( T3_EVAL_TOPLEVEL, subm_dir )
                #eval_subm_dir = os.path.join( T3_EVAL_TOPLEVEL, subm )
                print("checking %s exists..." % eval_subm_dir)
                if not os.path.exists( eval_subm_dir ):
                    print("path does not exist: ", eval_subm_dir )
                    sys.exit(1)
                
                summary_json = os.path.join(eval_subm_dir, "%s_summary.json" % ( "public" if PUBLIC else "private" ))
                if not os.path.exists( summary_json ):
                    print("path does not exist: ", summary_json )
                    sys.exit(1)
                use_subm = SUBM_MAPPING[subm]["use_subm_dir"]  if "use_subm_dir" in SUBM_MAPPING[subm].keys() else subm
                jpath = "t3/eval_2021/%s/%s_summary.json" % ( use_subm, "public" if PUBLIC else "private" )
                with open(jpath) as json_file:
                    summary = json.load(json_file)
     
                # reconstitute the summary df
                sdf = {}
                for db in summary.keys():
                    sdf[db] = summary[db]
                df = pd.DataFrame.from_dict(sdf, orient='index', columns=['recall','qps','power','cost'] )
                df.reset_index(level=0, inplace=True)
                df.rename(columns={'index':'dataset'}, inplace=True)

                # insert new column with subm
                df.insert( 0, "subm", [ subm ] * df.shape[0])
        
                dfs.append(df)

        master = pd.concat( dfs, ignore_index=True)
        #print("MASTER DATAFRAME")
        #print(master)
        return master

    def retrieve_rankings(master):
        '''extract each benchmark ranking order'''
        orderings = {}
        rankings = [ "recall", "qps", "power", "cost" ]
        rankings_dir = [ True, True, False, False ]
        rdf = master.loc[ master['dataset'] == "ranking-score" ]
        rankings = [ "recall", "qps", "power", "cost" ]
        for ranking, rdir in zip(rankings,rankings_dir):
            rankdf = rdf[["subm",ranking]]
            data = rankdf.to_dict(orient='list')
            subm = data['subm']
            score = data[ranking]
            pairs = [ el for el in list(zip(subm,score)) if not el[1]==None and not math.isnan(el[1]) ]
            ordered_ranking = sorted(pairs,reverse=rdir, key=lambda x: x[1]) #, reverse=False if benchmark in [ "recall", "qps" ] else True )
            orderings[ranking] = ordered_ranking
        return orderings

    def ranking_by_submission(orderings, rdct):
        '''replace rank by subm name'''
        for subm in subms: # ranking info
            for mapping in [ ["recall","RR"], [ "qps", "QR" ], [ "power", "PR" ], [ "cost", "CR" ] ]:
                kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_"+ mapping[1]
                subm_order = [ el[0] for el in orderings[mapping[0]] ]
                rdct[kee] = mklnkr( subm_order.index(subm)+1, mapping[0] ) if subm in subm_order else "*NQ*"
                if mapping[0]=="cost" and not SUBM_MAPPING[subm]["cost_approved"]: # deal with unnapproved cost
                    rdct[kee] = mklnkr( subm_order.index(subm)+1, mapping[0], False ) if subm in subm_order else "*NQ*"
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_HW"
            rdct[kee] = SUBM_MAPPING[subm]["display_hw"]
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_TM"
            rdct[kee] = SUBM_MAPPING[subm]['team'] if not SUBM_MAPPING[subm]['org'] else SUBM_MAPPING[subm]['team']+"(*org*)"
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_SB"
            rdct[kee] = subm
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_RD"
            rdct[kee] = SUBM_MAPPING[subm]['readme']
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_EV"
            rdct[kee] = SUBM_MAPPING[subm]['evaluator']
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_AL"
            if REJECT_ANOMALIES:
                rdct[kee] = "-"
            else:
                rdct[kee] = SUBM_MAPPING[subm]['algo']
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_AN"
            if REJECT_ANOMALIES:
                rdct[kee] = "-"
            else:
                rdct[kee] = SUBM_MAPPING[subm]['analysis']
   
            # anomaly 
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_AC"
            if SUBM_MAPPING[subm]['cache_detect'] and SUBM_MAPPING[subm]['evals']:
                ac = sum( [ el[1]['cache'][0] for el in SUBM_MAPPING[subm]['evals'].items() if el[0]!="summary" ] )
                tc = sum( [ el[1]['cache'][1] for el in SUBM_MAPPING[subm]['evals'].items() if el[0]!="summary" ] )
                if ac>0:
                    if SUBM_MAPPING[subm]['anomaly_explain']:
                        rdct[kee] = "[%d/%d](%s)" % (ac, tc, SUBM_MAPPING[subm]['anomaly_explain'])
                    else:
                        rdct[kee] = "%d/%d" % (ac,tc)
                else:
                    rdct[kee] = "%d/%d" % (ac, tc )
            else:
                rdct[kee] = "*NA*"

    def ranking_by_benchmark(orderings, rdct):
        '''replace benchmark rank by rank ordering'''
        mapping = { "recall": "RR", "qps": "QR", "power":"PR", "cost":"CR" }
        rankings = [ "recall", "qps", "power", "cost" ]
        for benchmark in rankings:
            for idx, rk in enumerate(orderings[benchmark]):
                # subm name
                subm = rk[0]
                kee = "$%s%d_SB" % ( mapping[benchmark], idx+1)
                rdct[kee] = subm
                # team
                kee = "$%s%d_TM" % ( mapping[benchmark], idx+1)
                rdct[kee] = SUBM_MAPPING[subm]['team'] if not SUBM_MAPPING[subm]['org'] else SUBM_MAPPING[subm]['team']+"(*org*)"
                # display hardware
                hw = SUBM_MAPPING[subm]["display_hw"]
                kee = "$%s%d_HW" % ( mapping[benchmark], idx+1)
                rdct[kee] = hw
                # display status
                st = SUBM_MAPPING[subm]["status"]
                kee = "$%s%d_ST" % ( mapping[benchmark], idx+1)
                rdct[kee] = st
                # score
                sc = rk[1]
                kee = "$%s%d_SC" % ( mapping[benchmark], idx+1)
                rdct[kee] = "baseline" if SUBM_MAPPING["baseline"]==subm \
                    else "%.0f" % sc if benchmark=="qps" \
                    else "%.3f" % sc if benchmark!="cost" \
                    else "${:,.2f}".format(sc)
                if benchmark=="cost" and not SUBM_MAPPING[subm]["cost_approved"]: # deal with unapproved cost
                    rdct[kee] = "baseline" if SUBM_MAPPING["baseline"]==subm else "${:,.2f}\*\*".format(sc)
                # readme
                rd = SUBM_MAPPING[subm]["readme"]
                kee = "$%s%d_RD" % ( mapping[benchmark], idx+1)
                rdct[kee] = rd

                # iterate datasets for this benchmark
                dbmapping = { "recall":"R", "qps":"Q", "cost":"C", "power":"P" }
                bestmapping = { "recall":"best_recall", "qps":"best_qps", "power":"best_wspq", "cost":"cost" }
                bestidxmapping = { "recall":1, "qps":1, "power":2, "cost":0 }
                bestformatmapping = { "recall": "{:,.5f}", "qps": "{:,.0f}", "power":"{:,.4f}", "cost":"${:,.2f}" }
                DBS = { "deep-1B":"DP", "bigann-1B":"BA", "msturing-1B":"MT", "msspacev-1B":"MS", "text2image-1B":"TI", "ssnpp-1B":"FB" }
                for db in DBS.keys():
                    kee = "$%s%s%d" % (DBS[db], dbmapping[benchmark], idx+1 )
                    best_benchmark = bestmapping[benchmark]
                    supported_dbs = SUBM_MAPPING[subm]["evals"].keys()
                    if db in supported_dbs:
                        best_val = SUBM_MAPPING[subm]["evals"][db][best_benchmark]
                        supported_benchmarks = SUBM_MAPPING[subm]["evals"][db].keys()
                        if best_benchmark in supported_benchmarks:
                            val = best_val[ bestidxmapping[benchmark] ] #if not benchmark=="cost" else best_val
                            fmt = bestformatmapping[benchmark]
                            rdct[kee] = fmt.format(val) if benchmark=="cost" else mklnka( val, fmt, subm, db, benchmark )
                        else:
                            rdct[kee]="-"
                    else:
                        rdct[kee]="-"

            # replace the rest with "-"
            for i in range(idx+1, TOTAL_SUBM ):
                # subm name
                kee = "$%s%d_SB" % ( mapping[benchmark], i+1)
                rdct[kee] = "-"
                # team
                kee = "$%s%d_TM" % ( mapping[benchmark], i+1)
                rdct[kee] = "-"
                # display hardware
                kee = "$%s%d_HW" % ( mapping[benchmark], i+1)
                rdct[kee] = "-"
                # display status
                st = SUBM_MAPPING[subm]["status"]
                kee = "$%s%d_ST" % ( mapping[benchmark], i+1)
                rdct[kee] = "-"
                # score
                kee = "$%s%d_SC" % ( mapping[benchmark], i+1)
                rdct[kee] = "-"
                # readme
                kee = "$%s%d_RD" % ( mapping[benchmark], i+1)
                rdct[kee] = "-"

                # iterate datasets for this benchmark
                dbmapping = { "recall":"R", "qps":"Q", "cost":"C", "power":"P" }
                bestmapping = { "recall":"best_recall", "qps":"best_qps", "power":"best_wspq", "cost":"cost" }
                bestidxmapping = { "recall":1, "qps":1, "power":2, "cost":0 }
                bestformatmapping = { "recall": "{:,.5f}", "qps": "{:,.0f}", "power":"{:,.4f}", "cost":"${:,.2f}" }
                DBS = { "deep-1B":"DP", "bigann-1B":"BA", "msturing-1B":"MT", "msspacev-1B":"MS", "text2image-1B":"TI", "ssnpp-1B":"FB" }
                for db in DBS.keys():
                    kee = "$%s%s%d" % (DBS[db], dbmapping[benchmark], i+1 )
                    best_benchmark = bestmapping[benchmark]
                    rdct[kee]="-"
    
    def ranking_by_dataset(orderings, rdct):
        '''do per database replacement'''
        rankings = [ "recall", "qps", "power", "cost" ]
        DBS = { "deep-1B":"DP", "bigann-1B":"BA", "msturing-1B":"MT", "msspacev-1B":"MS", "text2image-1B":"TI", "ssnpp-1B":"FB" }
        for db in DBS.keys():
            # iterate over benchmark
            for benchmark in rankings:
                # get best values for this benchmark for the database for all subm
                best_vals = []
                for subm in subms:
                    bestidxmapping = { "recall":1, "qps":1, "power":2, "cost":0 }
                    dbmapping = { "recall":"R", "qps":"Q", "cost":"C", "power":"P" }
                    bestmapping = { "recall":"best_recall", "qps":"best_qps", "power":"best_wspq", "cost":"cost" }
                    bestformatmapping = { "recall": "{:,.5f}", "qps": "{:,.0f}", "power":"{:,.4f}", "cost":"${:,.2f}" }
                    supported_dbs = SUBM_MAPPING[subm]["evals"].keys() if SUBM_MAPPING[subm]['evals'] else []
                    if db in supported_dbs:
                        best_val = SUBM_MAPPING[subm]["evals"][db][ bestmapping[benchmark] ]
                        val = best_val[ bestidxmapping[benchmark] ] 
                        vals = best_val
                        if val!=0: best_vals.append( (subm, val, vals) )
                best_vals = sorted( best_vals, key=lambda x: x[1], reverse=True if benchmark in [ "recall", "qps" ] else False )
                lastidx = -1
                for idx, item in enumerate(best_vals):
                    print("best idx", idx)
                    kee = "$%s%d%s_SB" % ( DBS[db], idx+1, dbmapping[benchmark] )
                    kv = item[0]
                    #print("KV", kee, kv )
                    rdct[kee]=kv
                    kee = "$%s%d%s_TM" % ( DBS[db], idx+1, dbmapping[benchmark] )
                    kv = SUBM_MAPPING[item[0]]['team'] if not SUBM_MAPPING[item[0]]['org'] else SUBM_MAPPING[item[0]]['team']+"(*org*)"
                    rdct[kee]=kv
                    kee = "$%s%d%s_ST" % ( DBS[db], idx+1, dbmapping[benchmark] )
                    kv = SUBM_MAPPING[item[0]]["status"]
                    rdct[kee]=kv
                    kee = "$%s%d%s_RD" % ( DBS[db], idx+1, dbmapping[benchmark] )
                    kv = SUBM_MAPPING[item[0]]["readme"]
                    rdct[kee]=kv
                    kee = "$%s%d%s_HW" % ( DBS[db], idx+1, dbmapping[benchmark])
                    kv = SUBM_MAPPING[item[0]]["display_hw"]
                    rdct[kee]=kv
                    kee = "$%s%d%s_V" % ( DBS[db], idx+1, dbmapping[benchmark])
                    fmt = bestformatmapping[benchmark]
                    kv = fmt.format(item[1]) if benchmark=="cost" else mklnka( item[1], fmt, item[0], db, benchmark )
                    if benchmark=="cost" and not SUBM_MAPPING[item[0]]["cost_approved"]:
                        kv = fmt.format(item[1]) + "\*\*"
                    #print("TOT COST item", db, idx, item[0], benchmark, item[1])
                    rdct[kee]=kv
                    #$DP1C_CX|$DP1C_OX|$DP1C_UC |$DP1C_UN      |$DP1C_KWT|
                    if benchmark=="cost":
                        #print("COST item", db, idx, item[0], item[1], benchmark, item[2])
                        kee = "$%s%d%s_CX" % ( DBS[db], idx+1, dbmapping[benchmark])
                        kv = fmt.format(item[2][1]) #capex
                        rdct[kee]=kv
                        kee = "$%s%d%s_OX" % ( DBS[db], idx+1, dbmapping[benchmark])
                        kv = fmt.format(item[2][2]) #opex
                        rdct[kee]=kv
                        kee = "$%s%d%s_UC" % ( DBS[db], idx+1, dbmapping[benchmark])
                        kv = fmt.format(item[2][3]) #unit cost
                        rdct[kee]=kv
                        kee = "$%s%d%s_UN" % ( DBS[db], idx+1, dbmapping[benchmark])
                        kv = str(item[2][4]) #units
                        rdct[kee]=kv
                        kee = "$%s%d%s_KWT" % ( DBS[db], idx+1, dbmapping[benchmark])
                        kv = "{:,.3f}".format(item[2][5]) #kwt
                        rdct[kee]=kv
                    lastidx = idx

                idx = lastidx
                #print("idx", idx)   
                for i in range(idx+1, TOTAL_SUBM):
                    print("clearing", db, i, benchmark )
                    kee = "$%s%d%s_SB" % ( DBS[db], i+1, dbmapping[benchmark] ) 
                    rdct[kee]="-"
                    kee = "$%s%d%s_TM" % ( DBS[db], i+1, dbmapping[benchmark] )
                    rdct[kee]="-"
                    kee = "$%s%d%s_ST" % ( DBS[db], i+1, dbmapping[benchmark] )
                    rdct[kee]="-"
                    kee = "$%s%d%s_RD" % ( DBS[db], i+1, dbmapping[benchmark] )
                    rdct[kee]="-"
                    kee = "$%s%d%s_HW" % ( DBS[db], i+1, dbmapping[benchmark])
                    rdct[kee]="-"
                    kee = "$%s%d%s_V" % ( DBS[db], i+1, dbmapping[benchmark])
                    rdct[kee]="-"
                    kee = "$%s%d%s_CX" % ( DBS[db], i+1, dbmapping[benchmark])
                    rdct[kee]='-'
                    kee = "$%s%d%s_OX" % ( DBS[db], i+1, dbmapping[benchmark])
                    rdct[kee]='-'
                    kee = "$%s%d%s_UC" % ( DBS[db], i+1, dbmapping[benchmark])
                    rdct[kee]='-'
                    kee = "$%s%d%s_UN" % ( DBS[db], i+1, dbmapping[benchmark])
                    rdct[kee]='-'
                    kee = "$%s%d%s_KWT" % ( DBS[db], i+1, dbmapping[benchmark])
                    rdct[kee]='-'
    
    # retrieve data and compute rankings             
    master = get_master_df()
    orderings = retrieve_rankings(master)

    # create substitution dict
    rdct = {}
    ranking_by_submission( orderings, rdct )
    ranking_by_benchmark( orderings, rdct )
    ranking_by_dataset( orderings, rdct )

    # replace subm status by subm name
    for subm in subms: # status info
        kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_S"
        rdct[kee] = SUBM_MAPPING[subm]['status']

    # replace LB type
    rdct["$LBTYPE"] = "Public" if PUBLIC else "Private"

    # replace offlabel status
    # rdct["$OFFLABEL"] = "Official" if OFFICIAL else "Unofficial"

    # replace 'reject anomaly' status
    if REJECT_ANOMALIES:
        rdct["$REJECT_ANOM"] = "After Rejecting Anomalies"
        rdct["$ADJUSTED"] = "adjusted leaderboard rankings (above)"
    else:
        rdct["$REJECT_ANOM"] = ""
        rdct["$ADJUSTED"] = "[adjusted leaderboard rankings](LEADERBOARDS_%s_REJECT_ANOMALIES.md)" \
            % ("PUBLIC" if PUBLIC else "PRIVATE")

    # load the leaderboard template
    f = open("t3/LEADERBOARDS.md.templ")
    lines = f.read()
    f.close()
    templ = Template(lines)

    # do the substitution and create new leaderboard
    outp = lines
    for kee in rdct.keys():
        outp = outp.replace( kee, rdct[kee] )
    if REJECT_ANOMALIES: 
        out_file = "t3/LEADERBOARDS_%s_REJECT_ANOMALIES.md" % ( "PUBLIC" if PUBLIC else "PRIVATE" )
    else:
        out_file = "t3/LEADERBOARDS_%s.md" % ("PUBLIC" if PUBLIC else "PRIVATE")
    print("out_file", out_file)
    f = open(out_file,"w")
    f.write(outp)
    f.flush()
    f.close()
    print("Wrote new leaderboard file->", out_file)
 
if __name__ == "__main__":

    if PUBLIC:
        subms = [  "faiss_t3", "optanne_graphann", "gemini", "diskann", "cuanns_multigpu", "cuanns_ivfpq" ]
        #subms = [  "faiss_t3", "optanne_graphann", "gemini", "cuanns_multigpu", "cuanns_ivfpq" ]
        #subms = [ "cuanns_ivfpq" ]
        #subms = [ "optanne_graphann" ]
        #subms = [ "gemini" ]
    else: #PRIVATE
        subms = [  "faiss_t3", "optanne_graphann", "gemini", "diskann", "cuanns_multigpu", "cuanns_ivfpq" ]
        #subms = [ "gemini", "faiss_t3", "cuanns_ivfpq", "optanne_graphann" ]
        # subms = [ "gemini" ]

    # export and/or produce summary and evals json  
    if RE_EXPORT or PROCESS_CSV: 
        for subm in subms:
            #GW if SUBM_MAPPING["baseline"] != subm: # baseline is set
            ret = process_subm(subm)
            if not ret:
                print("WARNING: This submission is not participating in all benchmarks", subm)
                SUBM_MAPPING[subm]["not_part"] = ["recall","qps","power","cost"]
    
    # load the evals json
    for subm in subms:
        use_subm = SUBM_MAPPING[subm]["use_subm_dir"]  if "use_subm_dir" in SUBM_MAPPING[subm].keys() else subm
        jpath = "t3/eval_2021/%s/%s_evals.json" % (use_subm, "public" if PUBLIC else "private" )
        if os.path.exists(jpath):
            with open(jpath) as json_file:
                SUBM_MAPPING[subm]["evals"] = json.load(json_file)
        else:
            print("WARNING: No evals json for", subm)
            SUBM_MAPPING[subm]["evals"] = False

    if LEADERBOARD_GEN:
        produce_rankings(subms)

 
