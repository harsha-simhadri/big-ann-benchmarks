import os
import sys
import math
import pandas as pd
from string import Template
import t3eval

RE_EXPORT               = False
ONLY_TEMPLATE_GEN       = True

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
    print("master")
    #print(master)
    #print(master["dataset"])

    # extract each benchmark ranking
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
        ordered_ranking = sorted(pairs,reverse=rdir, key=lambda x: x[1])
        orderings[ranking] = ordered_ranking

    print("orderings")
    print(orderings)

    f = open("t3/LEADERBOARDS.md.templ")
    lines = f.read()
    f.close()
    templ = Template(lines)
    rdct = {}

    # replace rank by subm name
    for subm in subms: # ranking info
        for mapping in [ ["recall","RR"], [ "qps", "QR" ], [ "power", "PR" ], [ "cost", "CR" ] ]:
            kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_"+ mapping[1]
            subm_order = [ el[0] for el in orderings[mapping[0]] ]
            rdct[kee] = str(subm_order.index(subm)+1) if subm in subm_order else "NQ"

    # replace benchmark rank by rank ordering
    mapping = { "recall": "RR", "qps": "QR", "power":"PR", "cost":"CR" }
    for benchmark in rankings:
        print("OB", orderings[benchmark])
        for idx, rk in enumerate(orderings[benchmark]):
            # subm name
            subm = rk[0]
            kee = "$%s%d_TM" % ( mapping[benchmark], idx+1)
            rdct[kee] = subm
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
            rdct[kee] = "baseline" if SUBM_MAPPING["baseline"]==subm else str(sc) if benchmark!="cost" else "&#36;" + str(sc)
            # readme
            rd = SUBM_MAPPING[subm]["readme"]
            kee = "$%s%d_RD" % ( mapping[benchmark], idx+1)
            rdct[kee] = rd

    # replace subm status by subm name
    for subm in subms: # status info
        kee = "$" + SUBM_MAPPING[subm]['md_prefix']+"_S"
        rdct[kee] = SUBM_MAPPING[subm]['status']

    print("Substitution dct=", rdct)
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

    # TODO: check its run from the repo top-level

    subms = [ "faiss_t3", "optanne_graphann", "gemini" ]
        
    if not ONLY_TEMPLATE_GEN:
        
        for subm in subms:
            process_subm(subm)
         
    produce_rankings(subms)
 
