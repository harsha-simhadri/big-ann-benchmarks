import os
import sys
import math
import pandas as pd
from string import Template
import t3eval

COMP_RESULTS_TOPLEVEL   = "/Users/gwilliams/Projects/BigANN/competition_results"
T3_EVAL_TOPLEVEL        = "t3/eval_2021"
TEAM_MAPPING            = \
{
    "faiss_t3": {
        "results_dir":  "%s/faiss_t3/results.baseline_focused" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_focused.csv",
        "system_cost":  22021.90,
        "md_prefix":    "BS",
        "status":       "final"
    },
    "optanne_graphann": {
        "results_dir":  "%s/optanne_graphann/results.with_power_capture" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_with_power_capture.csv",
        "system_cost":  0,
        "md_prefix":    "OPT1",
        "status":       "inprog"
    },
    "gemini": {
        "results_dir":  "%s/gemini/results.using_gsl_release" % COMP_RESULTS_TOPLEVEL,
        "export_fname": "public_gsl_release.csv",
        "system_cost":  55726.26,
        "md_prefix":    "GEM",
        "status":       "inprog"
    },
    "baseline": "faiss_t3"
}
RE_EXPORT               = False

def process_team( team ):

    print()
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
        evaluator.eval_all(save_path=os.path.join(eval_team_dir, "summary.csv"))
        evaluator.commit_baseline("t3/baseline2021.json")
        evaluator.show_summary(savepath=os.path.join( eval_team_dir, "summary" ))
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
        evaluator.eval_all(save_path=os.path.join(eval_team_dir, "summary.csv"))
        evaluator.show_summary(savepath=os.path.join( eval_team_dir, "summary" ))

def produce_rankings(teams):

    dfs = []

    # get the data from summary csv
    for team in teams:
   
            eval_team_dir = os.path.join( T3_EVAL_TOPLEVEL, team )
            print("checking %s exists..." % eval_team_dir)
            if not os.path.exists( eval_team_dir ):
                print("path does not exist: ", eval_team_dir )
                sys.exit(1)

            summary_csv = os.path.join(eval_team_dir, "summary.csv")
            if not os.path.exists( summary_csv ):
                print("path does not exist: ", summary_csv )
                sys.exit(1)

            df = pd.read_csv(summary_csv)

            # insert new column with team 
            df.insert( 0, "team", [ team ] * df.shape[0])
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
        rankdf = rdf[["team",ranking]]
        #print("ranking for ", ranking)
        data = rankdf.to_dict(orient='list')
        #print(data)
        team = data['team']
        score = data[ranking]
        pairs = [ el for el in list(zip(team,score)) if not math.isnan(el[1]) ]
        #print("pairs=",pairs)
        ordered_ranking = sorted(pairs,reverse=rdir, key=lambda x: x[1])
        #print("ordering", ordered_ranking)
        orderings[ranking] = ordered_ranking

    print("orderings")
    print(orderings)

    f = open("t3/LEADERBOARDS.md.templ")
    lines = f.read()
    f.close()
    templ = Template(lines)
    rdct = {}
    for team in teams: # ranking info
        for mapping in [ ["recall","RR"], [ "qps", "QR" ], [ "power", "PR" ], [ "cost", "CR" ] ]:
            kee = "$" + TEAM_MAPPING[team]['md_prefix']+"_"+ mapping[1]
            team_order = [ el[0] for el in orderings[mapping[0]] ]
            rdct[kee] = str(team_order.index(team)+1) if team in team_order else "NQ"
    for team in teams: # status info
        kee = "$" + TEAM_MAPPING[team]['md_prefix']+"_S"
        rdct[kee] = TEAM_MAPPING[team]['status']

    print("substitution")
    print(rdct) 
    #outp = templ.substitute( GEM_RR="stuff" ) #**rdct )
    outp = lines
    for kee in rdct.keys():
        outp = outp.replace( kee, rdct[kee] )

    #print("outp=",outp)

    f = open("t3/NL.md","w")
    f.write(outp)
    f.flush()
    f.close()

    print("Wrote new leaderboard") 
 
if __name__ == "__main__":

    # TODO: check its run from the repo top-level

    teams = [ "faiss_t3", "optanne_graphann", "gemini" ]
    for team in teams:
        process_team(team)

    produce_rankings(teams)
 
