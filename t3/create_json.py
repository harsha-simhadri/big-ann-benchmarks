#!/bin/bash

import json

baseline_outpath = "baseline2021.json"

baseline = { 
    "deep-1B": {
        "recall":   [0.942, 2002.490], 
        "qps":      [3422.473, 0.916],
        "min-recall":   0.9,
        "min-qps":      2000 
    },
    "bigann-1B": {
        "recall":   [0.927, 2058.950], 
        "qps":      [2186.755, 0.905],
        "min-recall":   0.9,
        "min-qps":      2000 
    },
    "msturing-1B": {
        "recall":   [0.910, 2011.542], 
        "qps":      [2421.856, 0.902],
        "min-recall":   0.9,
        "min-qps":      2000 
    },
    "msspacev-1B": {
        "recall":   [0.850, 2190.829], 
        "qps":      [1484.217, 0.869],
        "min-recall":   0.850,  # not 0.9 because baseline could not reach 0.9
        "min-qps":      1484.217 # not 2K because baseline could not reach 2K
    },
    "text2image-1B": {
        "recall":   [0.860, 2120.635],
        "qps":      [1510.624, 0.882],
        "min-recall":   0.860, # not 0.9 because baseline could not reach 0.9
        "min-qps":      1510.624 # not 2K because baseline could not reach 2K
    }
}

with open(baseline_outpath, 'w') as outfile:
    json.dump(baseline, outfile)

print("Wrote baseline json at %s" % baseline_outpath )

competition_outpath = "competition2021.json"

competition = {
    "kwh_cost": 0.10, # 10 cents
    "cost_qps": 100000, # 100,000 queries per second
    "opex_time": 4 # number of years to evaluate opex
}

with open(competition_outpath, 'w') as outfile:
    json.dump(competition, outfile)

print("Wrote competition json at %s" % competition_outpath )

