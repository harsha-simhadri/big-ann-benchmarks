#!/bin/bash

import json


baseline_outpath = "baseline2021.json"

baseline = { 
    "version":          "2021",
    "datasets": {
        "deep-1B": {
            "recall":       [0.943060, 2175.697], 
            "qps":          [4417.036, 0.90088],
            "wspq":         [0.113, 0.901, 4417.036],      
            "cost":         545952.10,
            "min-recall":   0.9,
            "min-qps":      2000,
            "min-wspq":     0.0         # No min wspq in 2021
        },
        "bigann-1B": {
            "recall":       [0.927, 2188.858], 
            "qps":          [3086.656, 0.901],
            "wspq":         [0.167, 0.90117, 3086.656],     
            "cost":         785282.45,
            "min-recall":   0.9,
            "min-qps":      2000,
            "min-wspq":     0.0,        # No min wspq in 2021
        },
        "msturing-1B": {
            "recall":       [0.909, 2007.497], 
            "qps":          [2359.4485, 0.902],
            "wspq":         [0.204, 0.903, 2359.485],    
            "cost":         1018332.30,
            "min-recall":   0.9,
            "min-qps":      2000,
            "min-wspq":     0.0         # No min wspq in 2021
        },
        "msspacev-1B": {
            "recall":       [0.927, 2770.848], 
            "qps":          [2770.848, 0.927],
            "wspq":         [0.167, 0.927, 2770.848],      
            "cost":         873460.84,
            "min-recall":   0.9,        
            "min-qps":      2000,       
            "min-wspq":     0.0         # No min wspq in 2021
        },
        "text2image-1B": {
            "recall":       [0.860, 2139.045],
            "qps":          [2403.008, 0.852],
            "wspq":         [0.214, 0.852, 2403.008],      
            "cost":         999879.39,
            "min-recall":   0.860,      # not 0.9 because baseline could not reach 0.9
            "min-qps":      2000,       
            "min-wspq":     0.0         # No min wspq in 2021
        },
        "ssnpp-1B": {
            "recall":       [0.979, 2907.414], 
            "qps":          [5572.272, 0.910], 
            "wspq":         [0.095, 0.910, 5575.272],      
            "cost":         429634.84,
            "min-recall":   0.9,       
            "min-qps":      2000,       
            "min-wspq":     0.0         # No min wspq in 2021
        }
    }
}

with open(baseline_outpath, 'w') as outfile:
    json.dump(baseline, outfile)

print("Wrote baseline json at %s" % baseline_outpath )

competition_outpath = "competition2021.json"

competition = {
    "version":          "2021", 
    "kwh_cost":         0.10,   # 10 cents
    "cost_qps":         100000, # 100,000 queries per second
    "opex_time":        4,      # number of years to evaluate opex
    "min_qual_dsets":   3,
    "max_run_params":   10
    
}

with open(competition_outpath, 'w') as outfile:
    json.dump(competition, outfile)

print("Wrote competition json at %s" % competition_outpath )

