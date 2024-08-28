#
# This python script computes the rankings suitable for summarization in the markdown.
#
import pandas as pd
import os
import glob

#
# Config: Please changes values depending on your setup.
#

# Relative path to competition data export file
CSV = "data_export_m2-medium.csv"

# Relative path to competition directory
COMPETITION_DIR = ".." 

# Competition dataset names
DATASETS = []

# Competition recall/ap threshold
RECALL_AP_THRESHOLD = 0.9

if __name__ == "__main__":

    # read CSV
    df = pd.read_csv( CSV )

    # get track/dataset groups
    # TODO: filter on track eval datasets
    grps = df.groupby(["track","dataset"])

    # iterate groups
    for name, group in grps:

        # extract groupby track and dataset
        track = name[0]
        dataset = name[1]
       
        # produce track ranking
        ranking_df = group[ group["recall/ap"]>=RECALL_AP_THRESHOLD ]\
            .groupby(["algorithm"]) \
            .max("qps") \
            .sort_values("qps", ascending=False) \
            [["qps","recall/ap"]] 
        
        # set 'status' column as 'qualified' for all surviving rows
        ranking_df['status'] = 'ok'

        #
        # Remainder of code is preparing dataframe for html export for markdown
        #

        # return the algorithm index as a column
        #ranking_df = ranking_df.reset_index() # return algorithm index as a column
        ranking_df.reset_index(inplace=True)
        print(ranking_df)
        print(list(ranking_df.index))

        # create a rank numeric column
        ranking_df['rank'] = ranking_df.apply( lambda row: int(row.name)+1, axis=1)
        ranking_df['rank'] = ranking_df['rank'].astype('Int64')

        # retrieve all participating track algorithm names via track algo subdirectory 
        track_dir = os.path.join( COMPETITION_DIR, "%s/*/Dockerfile" % track )
        algos_participating = [os.path.basename(os.path.dirname(p)) for p in glob.glob( track_dir ) ]
      
        # compute difference of algo lists of track subdirs and algos in results - these did not qualify
        algos_did_not_qualify = list( set(algos_participating) - set(list(ranking_df["algorithm"])) )

        # append not-qualified algos to dataframe
        for algo in algos_did_not_qualify:
            ranking_df = pd.concat([ranking_df, pd.DataFrame([{'algorithm':algo,'status':'error'}])], ignore_index = True)

        # return track and dataset as column
        ranking_df['track'] = track
        ranking_df['dataset'] = dataset
        print(ranking_df)
        print()
