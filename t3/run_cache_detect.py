import os
import sys
import math
import json
import pandas as pd
from string import Template
import t3eval

RE_EXPORT               = False
ONLY_TEMPLATE_GEN       = False
TOTAL_SUBM              = 10
RESULTS_TOPLEVEL        = "/Users/gwilliams/Projects/BigANN/cache_detect_results"
T3_EVAL_TOPLEVEL        = "t3/eval_2021"

SUBM_MAPPING            = \
{
    "faiss_t3": {
        "team":         "Facebook Research",
        "results_dir":  "%s/faiss/results_faiss_stimes_4_dsets" % RESULTS_TOPLEVEL,
        "export_fname": "cache_detect.csv",
        "md_prefix":    "BS",
        "display_hw":   "NVidia GPU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md",
        "org":          True,
        "evaluator":    "George Williams",
    },
    "optanne_graphann": {
        "team":         "Intel",
        "results_dir":  "%s/intel/results_intel_multigpu_all_stimes" % RESULTS_TOPLEVEL,
        "export_fname": "cache_detect.csv",
        "md_prefix":    "OPT1",
        "display_hw":   "Intel Optane",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md",
        "org":          False,
        "evaluator":    "George Williams",
    },
    "gemini": {
        "team":         "GSI Technology",
        "results_dir":  "%s/gsi/results_gem_stimes_text2image" % RESULTS_TOPLEVEL,
        "export_fname": "cache_detect.csv",
        "md_prefix":    "GEM",
        "display_hw":   "LedaE APU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md",
        "org":          True,
        "evaluator":    "George Williams",
    },
    "diskann": {
        "team":         "Microsoft Research",
        "use_subm_dir": "diskann-bare-metal",
        "results_dir":  "%s/diskann/results.ms_bare_metal" % RESULTS_TOPLEVEL,
        "export_fname": "cache_detect.csv", 
        "md_prefix":    "MSD",
        "status":       "inprog",
        "display_hw":   "Dell PowerEdge",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md",
        "org":          True,
        "evaluator":    "Harsha Simhadri",
    },
    "cuanns_multigpu": {
        "team":         "NVidia",
        "results_dir":  "%s/nvidia/multigpu/results_nv_multi_stimes_all" % RESULTS_TOPLEVEL,
        "export_fname": "cache_detect.csv", 
        "md_prefix":    "NV",
        "status":       "inprog",
        "display_hw":   "NVidia GPU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md",
        "org":          False,
        "evaluator":    "George Williams",
    },
    "cuanns_ivfpq": {
        "team":         "NVidia",
        "results_dir":  "%s/nvidia/ivfpq/results_nv_ivfpq_stimes_all" % RESULTS_TOPLEVEL,
        "export_fname": "cache_detect.csv",
        "md_prefix":    "NV2",
        "status":       "inprog",
        "display_hw":   "NVidia GPU",
        "readme":       "https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md",
        "org":          False,
        "evaluator":    "George Williams",
    },
    "baseline": "faiss_t3"
}

def process_subm( subm ):

    print()
    print("processing subm=%s" % subm)

    # check subm exists under eval dir
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
        export_cmd = "python data_export.py --recompute --sensors --search_times --detect_caching 0.3 --output='%s'" % export_file
        print("running export command->", export_cmd )
        stream = os.popen(export_cmd)
        print("result of export=", stream.read())

        # check export file
        if not os.path.exists( export_file ):
            print("could not find export_file" % export_file)
            return False, None

        exported = True    
    else:
        print("not running data export, export file located at %s" % export_file)

    df = pd.read_csv( export_file )
    return True, df        

if __name__ == "__main__":

    #subms = [  "faiss_t3", "optanne_graphann", "gemini", "diskann", "cuanns_multigpu", "cuanns_ivfpq" ]
    subms = [  "faiss_t3", "optanne_graphann", "gemini", "cuanns_multigpu", "cuanns_ivfpq" ]
    #subms = [ "faiss_t3" ]
    #subms = [ "cuanns_multigpu" ]

    # produce a master dataframe of all results 
    dfs = [] 
    for subm in subms:
        ok, df = process_subm(subm)
        if ok: dfs.append( df )
    master = pd.concat( dfs, ignore_index=True)
    algos = list(master['algorithm'])
    #print(algos)
    #print(master.columns)
    
    datasets = [ "deep-1B", "bigann-1B", "text2image-1B", "msturing-1B", "msspacev-1B", "ssnpp-1B" ]
    submap = {  "faiss_t3": "faiss-t3", 
                "optanne_graphann": "graphann", 
                "gemini": "gsi-t3", 
                "cuanns_ivfpq": "cuanns_ivfpq",
                "cuanns_multigpu": "cuanns_multigpu"}

    print("Analyze...")
    for subm in subms:
        for dataset in datasets:
            #sdf = master.loc[ master['algorithm'] == submap[subm] & master['dataset'] == dataset ]
            sdf = master[ (master['algorithm'] == submap[subm]) & (master['dataset'] == dataset) ]
            if sdf.shape[0] == 0:
                #print(subm, dataset, "no data")
                pass
            else:
                #print(sdf.columns)
                caching = list(sdf.caching )
                recall = list(sdf['recall/ap'])
                qps = list(sdf.qps) 
                search_times = sdf.search_times
                rows = list( zip(caching, recall, qps, search_times ) )
                anomalies = [ el for el in rows if el[0].split()[0]=='1' ]
                s = "{0:15} {1:15} {2:10}".format(subm, dataset, "%d/%d anomalies" % (len(anomalies), len(rows)))
                print(s)
                for idx, an in enumerate(anomalies):
                    s = "    {0:10} search_times = {1:30} recall = {2} ".format( "anamoly %d:" % (idx+1), ",".join([ "{:.2f}".format(float(el)) for el in an[3].split() ]), an[1]) 
                    print(s)
            print()
