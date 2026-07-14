#
# This is a script which creates scripts for individual track algorithms
#

import glob
import os

# Relative location of all competition track directories
TRACK_DIRS = { \
    "sparse": "../sparse", \
    "filter": "../filter", \
    "ood": "../ood", \
    "streaming": "../streaming" \
}

# Track dataset mapping
TRACK_DATASETS = { \
    "sparse": "sparse-full", \
    "filter": "yfcc-10M", \
    "ood": "text2image-10M", \
    "streaming": "msturing-30M-clustered" \
}

# Extra run flags
EXTRA = { \
    "sparse": "", \
    "filter": "", \
    "ood": "", \
    "streaming": "--runbook_file neurips23/streaming/final_runbook.yaml" \
}

# Commands dir
CDIR = "commands"

# Build command template
BUILD_CMD = "python install.py --neurips23track %s --algorithm %s"

# Run command template
RUN_CMD = "python3 run.py --dataset %s --algorithm %s --neurips23track %s %s"

if __name__ == "__main__":

    # iterate competition tracks
    for track in TRACK_DIRS.keys():

        track_dir = TRACK_DIRS[track]

        # retrieve all track participants
        match = os.path.join( track_dir, "*/Dockerfile" )
        algos_participating = [os.path.basename(os.path.dirname(p)) for p in glob.glob( match ) ]
        print("%s participants:" % track, algos_participating)

        # emit the track+algo bash script
        for algo in algos_participating:
            fname = os.path.join(CDIR, "%s__%s.sh" % (track, algo) )
            with open(fname, "w") as fd:
                fd.write("#!/bin/bash\n")
                fd.write("set -x # echo the command\n")
                fd.write("set -e # stop script on error\n")
                fd.write("\n")
                fd.write( BUILD_CMD % ( track, algo ) + "\n" )
                fd.write( RUN_CMD % ( TRACK_DATASETS[track], algo, track, EXTRA[track] ) + "\n" )

            print("Wrote %s" % fname)

print("Done.")

                
                
 


