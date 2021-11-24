import os
import sys
import math
import json
import pandas as pd
from string import Template
import t3eval

RE_EXPORT               = False
ONLY_TEMPLATE_GEN       = False

OFFICIAL                = False

TOTAL_SUBM              = 10
COMP_RESULTS_TOPLEVEL   = "/Users/gwilliams/Projects/BigANN/competition_results"
T3_EVAL_TOPLEVEL        = "t3/eval_2021"
SUBM_MAPPING            = \
{
    "faiss_t3": {
        "team":         "Facebook Research",
        "results_dir":  "%s/faiss_t3/results.baseline_focused" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_focused.csv",
        "system_cost":  22021.90,
        "md_prefix":    "BS",
        "status":       "final",
        "display_hw":   "NVidia GPU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md",
        "org":          True,
        "evaluator":    "George Williams",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/faiss_t3.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/EvalPublic.ipynb)"
    },
    "optanne_graphann": {
        "team":         "Intel",
        "results_dir":  "%s/optanne_graphann/results.with_power_capture" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_with_power_capture.csv",
        "system_cost":  14664.20,
        "md_prefix":    "OPT1",
        "status":       "inprog",
        "display_hw":   "Intel Optane",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md",
        "org":          False,
        "evaluator":    "George Williams",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/graphann.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/EvalPublic.ipynb)"
    },
    "gemini": {
        "team":         "GSI Technology",
        "results_dir":  "%s/gemini/results.using_gsl_release" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_gsl_release.csv",
        "system_cost":  55726.66,
        "md_prefix":    "GEM",
        "status":       "inprog",
        "display_hw":   "LedaE APU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md",
        "org":          True,
        "evaluator":    "George Williams",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/gemini.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/EvalPublic.ipynb)"
    },
    "diskann": {
        "team":         "Microsoft Research",
        "use_subm_dir": "diskann-bare-metal",
        "results_dir":  "%s/diskann/results.ms_bare_metal" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "diskann-bare-metal-res-pruned.csv", #"res.csv"
        "system_cost":  0,
        "md_prefix":    "MSD",
        "status":       "inprog",
        "display_hw":   "Dell PowerEdge",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md",
        "org":          True,
        "evaluator":    "Harsha Simhadri",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/diskann-t2.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/EvalPublic.ipynb)"
    },
    "cuanns_multigpu": {
        "team":         "NVidia",
        "results_dir":  "%s/nvidia/cuanns_multigpu/results2.power_mon" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "res2.power_mon.csv", #"res.no_power_mon.csv",
        "system_cost":  0,
        "md_prefix":    "NV",
        "status":       "inprog",
        "display_hw":   "NVidia GPU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md",
        "org":          False,
        "evaluator":    "George Williams",
        "algo":         "[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_multigpu.py)",
        "analysis":     "[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/EvalPublic.ipynb)"
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
    results_dir = SUBM_MAPPING[subm]["results_dir"]
    if not os.path.exists( eval_subm_dir ):
        print("path does not exist: ", eval_subm_dir )
        sys.exit(1)
  
    # check there is a data export file 
    do_export = False
    export_file = os.path.join( eval_subm_dir, SUBM_MAPPING[subm]["export_fname"] )
    print("EXP FILE", export_file)
    if not os.path.exists( export_file ):
        print("path does not exist: ", export_file )
        do_export = True
        #sys.exit(1)

    # create export.csv from results directory as needed
    exported = False
    if do_export or RE_EXPORT:
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
        export_cmd = "python data_export.py --recompute --sensors --output='%s'" % export_file
        print("running export command->", export_cmd )
        stream = os.popen(export_cmd)
        print("result of export=", stream.read())

        # check export file
        if not os.path.exists( export_file ):
            print("could not find export_file" % export_file)
            sys.exit(1)
        exported = True    
    else:
        print("not running data export, export file located at %s" % export_file)

    # check there is a summary file
    do_summarize = False

    # do eval
    if SUBM_MAPPING["baseline"] == subm: # it's the baseline 
        evaluator = t3eval.Evaluator(   subm, 
                                        export_file,
                                        "t3/competition2021.json",
                                        system_cost= SUBM_MAPPING[subm]["system_cost"],
                                        verbose=False,
                                        is_baseline=True,
                                        pending = [],
                                        print_best=False )
        evaluator.eval_all(             save_summary=os.path.join(eval_subm_dir, "summary.json"),
                                        save_evals=os.path.join(eval_subm_dir, "evals.json" ) )
        evaluator.commit_baseline(      "t3/baseline2021.json")
        evaluator.show_summary(         savepath=os.path.join( eval_subm_dir, "summary.png" ))
    else:
        print("EVALUATOR", SUBM_MAPPING[subm])
        evaluator = t3eval.Evaluator(   subm, 
                                        export_file,
                                        "t3/competition2021.json",
                                        baseline_path="t3/baseline2021.json",
                                        system_cost= SUBM_MAPPING[subm]["system_cost"],
                                        verbose=False,
                                        is_baseline=False,
                                        pending = [],
                                        print_best=False )
        evaluator.eval_all(             save_summary=os.path.join(eval_subm_dir, "summary.json"),
                                        save_evals=os.path.join(eval_subm_dir, "evals.json" ) )
        evaluator.show_summary(         savepath=os.path.join( eval_subm_dir, "summary.png" ))

def mklnka( val, fmt, subm, db, benchmark ):
    if benchmark=="qps": benchmark="throughput"
    use_subm = SUBM_MAPPING[subm]["use_subm_dir"] \
        if "use_subm_dir" in SUBM_MAPPING[subm].keys() else subm
    eval_img = os.path.join( "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021", use_subm, "%s_%s.png" % (db, benchmark) )
    print("eval img", val, fmt, subm, db, benchmark, "-->", eval_img)
    lnk = "[%s](%s)" % ( fmt.format(val), eval_img )
    return lnk 

def mklnkr( idx, benchmark ):
    links = {   "recall":"#recall-or-ap-rankings", 
                "qps":"#throughput-rankings",
                "power":"#power-rankings",
                "cost":"#cost-rankings" }
    lnk = "[%d](%s)" % ( idx, links[benchmark] )
    return lnk 


def produce_rankings(subms):

    print("Producing rankings...")

    def get_master_df():
        '''retrieve all submission data into one master dataframe'''
        dfs = []

        # get the data from summary csv
        for subm in subms:
      
                subm_dir = SUBM_MAPPING[subm]["use_subm_dir"] \
                    if "use_subm_dir" in SUBM_MAPPING[subm].keys() else subm
                eval_subm_dir = os.path.join( T3_EVAL_TOPLEVEL, subm_dir )
                #eval_subm_dir = os.path.join( T3_EVAL_TOPLEVEL, subm )
                print("checking %s exists..." % eval_subm_dir)
                if not os.path.exists( eval_subm_dir ):
                    print("path does not exist: ", eval_subm_dir )
                    sys.exit(1)
                
                summary_json = os.path.join(eval_subm_dir, "summary.json")
                if not os.path.exists( summary_json ):
                    print("path does not exist: ", summary_json )
                    sys.exit(1)
                use_subm = SUBM_MAPPING[subm]["use_subm_dir"]  if "use_subm_dir" in SUBM_MAPPING[subm].keys() else subm
                jpath = "t3/eval_2021/%s/summary.json" % use_subm
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
        print("MASTER DATAFRAME")
        print(master)
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
            rdct[kee] = SUBM_MAPPING[subm]['algo']
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_AN"
            rdct[kee] = SUBM_MAPPING[subm]['analysis']

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
                rdct[kee] = "baseline" if SUBM_MAPPING["baseline"]==subm else "%.3f" % sc if benchmark!="cost" else "${:,.2f}".format(sc)
                # readme
                rd = SUBM_MAPPING[subm]["readme"]
                kee = "$%s%d_RD" % ( mapping[benchmark], idx+1)
                rdct[kee] = rd

                # iterate datasets for this benchmark
                dbmapping = { "recall":"R", "qps":"Q", "cost":"C", "power":"P" }
                bestmapping = { "recall":"best_recall", "qps":"best_qps", "power":"best_wspq", "cost":"cost" }
                bestidxmapping = { "recall":1, "qps":1, "power":2, "cost":0 }
                bestformatmapping = { "recall": "{:,.5f}", "qps": "{:,.3f}", "power":"{:,.4f}", "cost":"${:,.2f}" }
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
                bestformatmapping = { "recall": "{:,.5f}", "qps": "{:,.3f}", "power":"{:,.4f}", "cost":"${:,.2f}" }
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
                    bestformatmapping = { "recall": "{:,.5f}", "qps": "{:,.3f}", "power":"{:,.4f}", "cost":"${:,.2f}" }
                    supported_dbs = SUBM_MAPPING[subm]["evals"].keys()
                    if db in supported_dbs:
                        best_val = SUBM_MAPPING[subm]["evals"][db][ bestmapping[benchmark] ]
                        val = best_val[ bestidxmapping[benchmark] ] 
                        vals = best_val
                        if val!=0: best_vals.append( (subm, val, vals) )
                best_vals = sorted( best_vals, key=lambda x: x[1], reverse=True if benchmark in [ "recall", "qps" ] else False )
                for idx, item in enumerate(best_vals):
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
                     
                for i in range(idx+1, TOTAL_SUBM):
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

    # replace offlabel status
    rdct["$OFFLABEL"] = "Official" if OFFICIAL else "Unofficial"

    # load the leaderboard template
    f = open("t3/LEADERBOARDS.md.templ")
    lines = f.read()
    f.close()
    templ = Template(lines)

    # do the substitution and create new leaderboard
    outp = lines
    for kee in rdct.keys():
        outp = outp.replace( kee, rdct[kee] )
    f = open("t3/LEADERBOARDS.md","w")
    f.write(outp)
    f.flush()
    f.close()
    print("Wrote new leaderboard README")
 
if __name__ == "__main__":

    subms = [  "faiss_t3", "optanne_graphann", "gemini", "diskann", "cuanns_multigpu" ]
    #subms = [ "diskann" ]
    #subms = [  "cuanns_multigpu" ]
       
    if not ONLY_TEMPLATE_GEN:
        for subm in subms:
            process_subm(subm)
    
    # load the evals
    for subm in subms:
        use_subm = SUBM_MAPPING[subm]["use_subm_dir"]  if "use_subm_dir" in SUBM_MAPPING[subm].keys() else subm
        jpath = "t3/eval_2021/%s/evals.json" % use_subm          
        with open(jpath) as json_file:
            SUBM_MAPPING[subm]["evals"] = json.load(json_file)

    produce_rankings(subms)
 
