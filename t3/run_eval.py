import os
import sys

import t3eval

COMP_RESULTS_TOPLEVEL   = "/Users/gwilliams/Projects/BigANN/competition_results"
T3_EVAL_TOPLEVEL        = "t3/eval_2021"
TEAM_MAPPING            = \
{
    "faiss_t3": {
        "results_dir":  "%s/faiss_t3/results.baseline_focused" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_focused.csv",
        "system_cost":  22021.90
    },
    "optanne_graphann": {
        "results_dir":  "%s/optanne_graphann/results.with_power_capture" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_with_power_capture.csv",
        "system_cost":  0
    },
    "baseline": "faiss_t3"
}
RE_EXPORT               = False

if __name__ == "__main__":
   
    # TODO: check its run from the repo top-level

    #team = "faiss_t3"
    team = "optanne_graphann"

    print("processing team=%s" % team)

    # check team exists under eval dir
    eval_team_dir = os.path.join( T3_EVAL_TOPLEVEL, team )
    print("checking %s exists..." % eval_team_dir)
    if not os.path.exists( eval_team_dir ):
        print("path does not exist: ", eval_team_dir )
        sys.exit(1)

    # check results dir is valid
    results_dir = TEAM_MAPPING[team]["results_dir"]
    if not os.path.exists( eval_team_dir ):
        print("path does not exist: ", eval_team_dir )
        sys.exit(1)
  
    # check there is a data export file 
    do_export = False
    export_file = os.path.join( eval_team_dir, TEAM_MAPPING[team]["export_fname"])
    if not os.path.exists( export_file ):
        print("path does not exist: ", export_file )
        do_export = True

    # create export.csv from results directory as needed
    exported = False
    if do_export or RE_EXPORT:
        export_cmd = "python data_export.py --recompute --sensors --output='%s'" % export_file
        print("running export command->", export_cmd )

        if not os.path.exists( export_file ):
            print("could not find export_file" % export_file)
            sys.exit(1)
        exported = True    
    else:
        print("not running data export, export file located at %s" % export_file)

    # check there is a summary file
    do_summarize = False

    # do eval
    if TEAM_MAPPING["baseline"] == team: # it's the baseline 
        evaluator = t3eval.Evaluator(   team, 
                                        export_file,
                                        "t3/competition2021.json",
                                        system_cost= TEAM_MAPPING[team]["system_cost"],
                                        verbose=False,
                                        is_baseline=True,
                                        pending = [],
                                        print_best=False )
        evaluator.eval_all()
        evaluator.commit_baseline("t3/baseline2021.json")
        evaluator.show_summary(savepath=os.path.join( eval_team_dir, "summary.png" ))
    else:
        evaluator = t3eval.Evaluator(   team, 
                                        export_file,
                                        "t3/competition2021.json",
                                        baseline_path="t3/baseline2021.json",
                                        system_cost= TEAM_MAPPING[team]["system_cost"],
                                        verbose=False,
                                        is_baseline=False,
                                        pending = [],
                                        print_best=False )
        evaluator.eval_all()
        evaluator.show_summary(savepath=os.path.join( eval_team_dir, "summary.png" ))

    sys.exit(0)
     
