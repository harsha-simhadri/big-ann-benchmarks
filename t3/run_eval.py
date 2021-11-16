import os
import sys
import math
import json
import pandas as pd
from string import Template
import t3eval

RE_EXPORT               = False
ONLY_TEMPLATE_GEN       = True

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
        "readme":       "../t3/faiss_t3/README.md"
    },
    "optanne_graphann": {
        "team":         "Intel",
        "results_dir":  "%s/optanne_graphann/results.with_power_capture" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_with_power_capture.csv",
        "system_cost":  0,
        "md_prefix":    "OPT1",
        "status":       "inprog",
        "display_hw":   "Intel Optane",
        "readme":       "../t3/optanne_graphann/README.md"
    },
    "gemini": {
        "team":         "GSI Technology",
        "results_dir":  "%s/gemini/results.using_gsl_release" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_gsl_release.csv",
        "system_cost":  55726.66,
        "md_prefix":    "GEM",
        "status":       "inprog",
        "display_hw":   "LedaE APU",
        "readme":       "../t3/gemini/README.md"
    },
    "baseline": "faiss_t3"
}

notyet = {
    "deepgram": {
        "team":         "DeepGram",
        "results_dir":  "",
        "export_fname": "",
        "system_cost":  0.00,
        "md_prefix":    "DG",
        "status":       "inprog",
        "display_hw":   "NVidia GPU",
        "readme":       ""
    },


}

def process_subm( subm ):

    print()
    print("processing subm=%s" % subm)

    # check submexists under eval dir
    eval_subm_dir = os.path.join( T3_EVAL_TOPLEVEL, subm )
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
    export_file = os.path.join( eval_subm_dir, SUBM_MAPPING[subm]["export_fname"])
    if not os.path.exists( export_file ):
        print("path does not exist: ", export_file )
        do_export = True

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

def mklnk( val, fmt, subm, db, benchmark ):
    if benchmark=="qps": benchmark="throughput"
    eval_img = os.path.join( "eval_2021", subm, "%s_%s.png" % (db, benchmark) )
    print("eval img", eval_img)
    lnk = "[%s](%s)" % ( fmt.format(val), eval_img )
    return lnk 

def produce_rankings(subms):

    print("Producing rankings...")

    dfs = []

    # get the data from summary csv
    for subm in subms:
   
            eval_subm_dir = os.path.join( T3_EVAL_TOPLEVEL, subm )
            print("checking %s exists..." % eval_subm_dir)
            if not os.path.exists( eval_subm_dir ):
                print("path does not exist: ", eval_subm_dir )
                sys.exit(1)

            summary_csv = os.path.join(eval_subm_dir, "summary.csv")
            if not os.path.exists( summary_csv ):
                print("path does not exist: ", summary_csv )
                sys.exit(1)

            df = pd.read_csv(summary_csv)

            # insert new column with subm
            df.insert( 0, "subm", [ subm ] * df.shape[0])
            df = df.rename(columns={"Unnamed: 0":"dataset"})
            #print(df)
    
            dfs.append(df)

    master = pd.concat( dfs, ignore_index=True)

    #
    # extract each benchmark ranking order
    #
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
        pairs = [ el for el in list(zip(subm,score)) if not math.isnan(el[1]) ]
        ordered_ranking = sorted(pairs,reverse=rdir, key=lambda x: x[1]) #, reverse=False if benchmark in [ "recall", "qps" ] else True )
        orderings[ranking] = ordered_ranking


    f = open("t3/LEADERBOARDS.md.templ")
    lines = f.read()
    f.close()
    templ = Template(lines)
    rdct = {}

    #
    # replace rank by subm name
    #
    for subm in subms: # ranking info
        for mapping in [ ["recall","RR"], [ "qps", "QR" ], [ "power", "PR" ], [ "cost", "CR" ] ]:
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_"+ mapping[1]
            subm_order = [ el[0] for el in orderings[mapping[0]] ]
            rdct[kee] = str(subm_order.index(subm)+1) if subm in subm_order else "NQ"
        kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_HW"
        rdct[kee] = SUBM_MAPPING[subm]["display_hw"]
        kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_TM"
        rdct[kee] = SUBM_MAPPING[subm]['team']
        kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_SB"
        rdct[kee] = subm
        kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_RD"
        rdct[kee] = SUBM_MAPPING[subm]['readme']

    #
    # replace benchmark rank by rank ordering
    #
    mapping = { "recall": "RR", "qps": "QR", "power":"PR", "cost":"CR" }
    for benchmark in rankings:
        for idx, rk in enumerate(orderings[benchmark]):
            # subm name
            subm = rk[0]
            kee = "$%s%d_SB" % ( mapping[benchmark], idx+1)
            rdct[kee] = subm
            # team
            kee = "$%s%d_TM" % ( mapping[benchmark], idx+1)
            rdct[kee] = SUBM_MAPPING[subm]["team"]
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
            bestidxmapping = { "recall":1, "qps":1, "power":2, "cost":-1 }
            bestformatmapping = { "recall": "{:,.3f}", "qps": "{:,.3f}", "power":"{:,.3f}", "cost":"${:,.2f}" }
            DBS = { "deep-1B":"DP", "bigann-1B":"BA", "msturing-1B":"MT", "msspacev-1B":"MS", "text2image-1B":"TI", "ssnpp-1B":"FB" }
            for db in DBS.keys():
                kee = "$%s%s%d" % (DBS[db], dbmapping[benchmark], idx+1 )
                best_benchmark = bestmapping[benchmark]
                supported_dbs = SUBM_MAPPING[subm]["evals"].keys()
                if db in supported_dbs:
                    best_val = SUBM_MAPPING[subm]["evals"][db][best_benchmark]
                    supported_benchmarks = SUBM_MAPPING[subm]["evals"][db].keys()
                    if best_benchmark in supported_benchmarks:
                        val = best_val[ bestidxmapping[benchmark] ] if not benchmark=="cost" else best_val
                        fmt = bestformatmapping[benchmark]
                        rdct[kee] = fmt.format(val)
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
            bestidxmapping = { "recall":1, "qps":1, "power":2, "cost":-1 }
            bestformatmapping = { "recall": "{:,.3f}", "qps": "{:,.3f}", "power":"{:,.3f}", "cost":"${:,.2f}" }
            DBS = { "deep-1B":"DP", "bigann-1B":"BA", "msturing-1B":"MT", "msspacev-1B":"MS", "text2image-1B":"TI", "ssnpp-1B":"FB" }
            for db in DBS.keys():
                kee = "$%s%s%d" % (DBS[db], dbmapping[benchmark], i+1 )
                best_benchmark = bestmapping[benchmark]
                rdct[kee]="-"

    #
    # do per database replacement
    #
    DBS = { "deep-1B":"DP", "bigann-1B":"BA", "msturing-1B":"MT", "msspacev-1B":"MS", "text2image-1B":"TI", "ssnpp-1B":"FB" }
    for db in DBS.keys():
        # iterate over benchmark
        for benchmark in rankings:
            # get best values for this benchmark for the database for all subm
            best_vals = []
            for subm in subms:
                bestidxmapping = { "recall":1, "qps":1, "power":2, "cost":-1 }
                dbmapping = { "recall":"R", "qps":"Q", "cost":"C", "power":"P" }
                bestmapping = { "recall":"best_recall", "qps":"best_qps", "power":"best_wspq", "cost":"cost" }
                bestformatmapping = { "recall": "{:,.3f}", "qps": "{:,.3f}", "power":"{:,.3f}", "cost":"${:,.2f}" }
                supported_dbs = SUBM_MAPPING[subm]["evals"].keys()
                if db in supported_dbs:
                    best_val = SUBM_MAPPING[subm]["evals"][db][ bestmapping[benchmark] ]
                    val = best_val if benchmark=="cost" else best_val[ bestidxmapping[benchmark] ]
                    if val!=0: best_vals.append( (subm, val) )
            best_vals = sorted( best_vals, key=lambda x: x[1], reverse=True if benchmark in [ "recall", "qps" ] else False )
            for idx, item in enumerate(best_vals):
                kee = "$%s%d%s_SB" % ( DBS[db], idx+1, dbmapping[benchmark] )
                kv = item[0]
                rdct[kee]=kv
                kee = "$%s%d%s_TM" % ( DBS[db], idx+1, dbmapping[benchmark] )
                kv = SUBM_MAPPING[item[0]]["team"]
                rdct[kee]=kv
                kee = "$%s%d%s_ST" % ( DBS[db], idx+1, dbmapping[benchmark] )
                kv = SUBM_MAPPING[subm]["status"]
                rdct[kee]=kv
                kee = "$%s%d%s_RD" % ( DBS[db], idx+1, dbmapping[benchmark] )
                kv = SUBM_MAPPING[subm]["readme"]
                rdct[kee]=kv
                kee = "$%s%d%s_HW" % ( DBS[db], idx+1, dbmapping[benchmark])
                kv = SUBM_MAPPING[subm]["display_hw"]
                rdct[kee]=kv
                kee = "$%s%d%s_V" % ( DBS[db], idx+1, dbmapping[benchmark])
                fmt = bestformatmapping[benchmark]
                kv = fmt.format(item[1]) if benchmark=="cost" else mklnk( item[1], fmt, subm, db, benchmark )
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
                 

    #
    # replace subm status by subm name
    #
    for subm in subms: # status info
        kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_S"
        rdct[kee] = SUBM_MAPPING[subm]['status']

    #
    # do the substitution 
    #
    #print("Substitution dct=", rdct)
    #outp = templ.substitute( GEM_RR="stuff" ) #**rdct )
    outp = lines
    for kee in rdct.keys():
        outp = outp.replace( kee, rdct[kee] )
    f = open("t3/NL.md","w")
    f.write(outp)
    f.flush()
    f.close()

    print("Wrote new leaderboard README")
 
if __name__ == "__main__":

    subms = [  "faiss_t3", "optanne_graphann", "gemini" ]
       
    # load the evals
    for subm in subms:
        jpath = "t3/eval_2021/%s/evals.json" % subm          
        with open(jpath) as json_file:
            SUBM_MAPPING[subm]["evals"] = json.load(json_file)
 
    if not ONLY_TEMPLATE_GEN:
        
        for subm in subms:
            process_subm(subm)
         
    produce_rankings(subms)
 
