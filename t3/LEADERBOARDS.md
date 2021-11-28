# T3 Track Leaderboards (Unofficial)

Please note that all rankings are currently unofficial due to the following reasons:
* We continue to take changes to algorithms and indexes until Dec 1, so scores and rankings are still subject to change.
* All [open tasks and issues](TASKS_ISSUES_RESOLUTIONS.md) must be resolved.

## Final Rankings On Private Query Set

*Not yet available*
 
## Rankings On Public Query Set

### Rankings By Submission Name (alphabetical)

|Submission          |Team       |Hardware  |Status |Evaluator|Algo     |Runs    |[Recall Rank](#recall-or-ap-rankings)|[Thru-put Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)| 
|--------------------|-----------|----------|-------|---------|---------|--------|---------|--------------|-----------------------------|---------------------------|
|deepgram            |DeepGram   |NVidia GPU|final  |        -|        -|       -|     *NQ*|          *NQ*|                         *NQ*|                       *NQ*|
|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)  |Microsoft Research(*org*)    |Dell PowerEdge   |inprog |Harsha Simhadri  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/diskann-t2.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/EvalPublic.ipynb) |[1](#recall-or-ap-rankings)  |[4](#throughput-rankings)       |*NQ*                      |*NQ*                    |
|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)    |Facebook Research(*org*)     |NVidia GPU    |final  |George Williams   |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/faiss_t3.py)   |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/EvalPublic.ipynb)  |[6](#recall-or-ap-rankings)   |[6](#throughput-rankings)        |[5](#power-rankings)                       |[2](#cost-rankings)                     |
|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)  |GSI Technology(*org*)    |LedaE APU   |inprog |George Williams  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/gemini.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/EvalPublic.ipynb) |[3](#recall-or-ap-rankings)  |[5](#throughput-rankings)       |[4](#power-rankings)                      |[3](#cost-rankings)                    |
|kanndi              |Silo.ai    |LedaE APU   |inprog |        -|        -|       -|        -|             -|                            -|                          -|
|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)  |NVidia    |NVidia GPU   |inprog |George Williams  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_ivfpq.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/EvalPublic.ipynb) |[2](#recall-or-ap-rankings)  |[3](#throughput-rankings)       |[1](#power-rankings)                      |*NQ*                    |
|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)    |NVidia     |NVidia GPU    |inprog  |George Williams   |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_multigpu.py)   |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/EvalPublic.ipynb)  |[5](#recall-or-ap-rankings)   |[1](#throughput-rankings)        |[3](#power-rankings)                       |*NQ*                     |
|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel   |Intel Optane  |inprog|George Williams |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/graphann.py) |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/EvalPublic.ipynb)|[4](#recall-or-ap-rankings) |[2](#throughput-rankings)      |[2](#power-rankings)                     |[1](#cost-rankings)                   |
|optanne_graphann_2  |Intel   |Intel Optane  |inprog |        -|        -|       -|        -|             -|                            -|                          -|
|vector_t3           |Vector Inst|NVidia GPU|final  |        -|        -|       -|     *NQ*|          *NQ*|                         *NQ*|                       *NQ*|

* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

### Rankings Per Metric

#### Recall Or AP Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-recall-rankings)|[BigANN](#bigann-recall-rankings)|[MSTuring](#msturing-recall-rankings)|[MSSpace](#msspace-recall-rankings)|[Text2Image](#text2image-recall-rankings)|[FBSSNet](#fbsimsearchnet-ap-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|-------|
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Microsoft Research(*org*)|Dell PowerEdge |inprog|**0.420**|[0.99821](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_recall.png) |[0.99976](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_recall.png) |[0.99444](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_recall.png)   |[0.99342](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_recall.png)  |[0.98130](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_recall.png)     |-  |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**0.373**|[0.99542](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_recall.png) |[0.99882](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_recall.png) |[0.98993](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_recall.png)   |[0.99428](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_recall.png)  |[0.94136](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_recall.png)     |-  |
|   3|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**0.296**|[0.98871](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_recall.png) |[0.99253](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_recall.png) |[0.97841](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_recall.png)   |[0.98622](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_recall.png)  |[0.88585](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_recall.png)     |[0.99053](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_recall.png)  |
|   4|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**0.279**|[0.98264](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_recall.png) |[0.99084](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_recall.png) |[0.96218](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_recall.png)   |[0.98791](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_recall.png)  |[0.90277](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_recall.png)     |-  |
|   5|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |inprog|**0.278**|[0.99504](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_recall.png) |[0.99815](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_recall.png) |[0.98399](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_recall.png)   |[0.98785](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_recall.png)  |-     |-  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[0.94275](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_recall.png) |[0.92671](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_recall.png) |[0.90900](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_recall.png)   |[0.90853](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_recall.png)  |[0.86028](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_recall.png)     |[0.97863](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_recall.png)  |
|   7|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|
|   8|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|
|   9|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|
|  10|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Throughput Rankings

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-throughput-rankings)|[BigANN](#bigann-throughput-rankings)|[MSTuring](#msturing-throughput-rankings)|[MSSpace](#msspace-throughput-rankings)|[Text2Image](#text2image-throughput-rankings)|[FBSSNet](#fbsimsearchnet-throughput-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |inprog|**2983752.533**|[805,064.205](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_throughput.png) |[771,493.948](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_throughput.png) |[578,677.940](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_throughput.png)   |[841,150.465](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_throughput.png)  |-     |-         |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**821550.201**|[184,490.708](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_throughput.png) |[343,727.791](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_throughput.png) |[157,277.710](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_throughput.png)   |[139,612.021](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_throughput.png)  |[10,838.358](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_throughput.png)     |-         | 
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**397623.802**|[97,268.471](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_throughput.png) |[84,367.141](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_throughput.png) |[111,580.136](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_throughput.png)   |[109,555.059](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_throughput.png)  |[9,249.383](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_throughput.png)     |-         | 
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Microsoft Research(*org*)|Dell PowerEdge |inprog|**50635.296**|[12,926.890](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_throughput.png) |[19,094.371](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_throughput.png) |[17,200.601](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_throughput.png)   |[6,503.212](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_throughput.png)  |[9,306.610](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_throughput.png)     |-         | 
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**37428.363**|[9,150.271](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_throughput.png) |[9,504.865](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_throughput.png) |[20,166.678](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_throughput.png)   |[8,587.024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_throughput.png)  |[1,864.634](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_throughput.png)     |[8,123.552](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_throughput.png)         | 
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[4,417.036](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_throughput.png) |[3,086.656](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_throughput.png) |[2,359.485](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_throughput.png)   |[2,770.848](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_throughput.png)  |[1,762.363](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_throughput.png)     |[5,572.272](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_throughput.png)         | 
|   7|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   8|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   9|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|  10|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Power Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-power-rankings)|[BigANN](#bigann-power-rankings)|[MSTuring](#msturing-power-rankings)|[MSSpace](#msspace-power-rankings)|[Text2Image](#text2image-power-rankings)|[FBSSNet](#fbsimsearchnet-power-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|-----|-----|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |inprog|**-0.744**|[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_power.png) |[0.0024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_power.png) |[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_power.png)   |[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_power.png)  |[0.0222](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_power.png)|-|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**-0.687**|[0.0040](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_power.png) |[0.0021](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_power.png) |[0.0049](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_power.png)   |[0.0054](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_power.png)  |[0.0702](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_power.png)|-| 
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**-0.650**|[0.0002](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_power.png) |[0.0002](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_power.png) |[0.0004](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_power.png)   |[0.0002](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_power.png)  |-|-| 
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**-0.489**|[0.0398](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_power.png) |[0.0394](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_power.png) |[0.0227](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_power.png)   |[0.0485](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_power.png)  |[0.1759](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_power.png)|[0.0540](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_power.png)| 
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[0.1126](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_power.png) |[0.1671](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_power.png) |[0.2037](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_power.png)   |[0.1674](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_power.png)  |[0.1233](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_power.png)|[0.0949](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_power.png)| 
|   6|[-](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|-|- |-|**-**|- |- |-   |-  |-|-| 
|   7|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|
|   8|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|
|   9|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|
|  10|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Cost Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-cost-rankings)|[BigANN](#bigann-cost-rankings)|[MSTuring](#msturing-cost-rankings)|[MSSpace](#msspace-cost-rankings)|[Text2Image](#text2image-cost-rankings)|[FBSSNet](#fbsimsearchnet-cost-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**$-4,285,768.44**|$16,082.49 |$15,407.15 |$16,397.80   |$16,563.61  |$171,244.96     |-         |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|$545,952.10 |$785,282.45 |$1,018,332.30   |$873,460.84  |$1,298,436.77     |$429,634.84         |
|   3|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**$1,089,170.96**|$626,932.94 |$626,785.91 |$286,578.81   |$685,704.76  |$3,070,882.16     |$743,385.69         |
|   4|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |
|   5|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |
|   6|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |
|   7|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   8|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   9|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|  10|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

### Rankings Per Database

#### Deep1B

##### Deep1B Recall Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[0.99821](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_recall.png)**|       
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99542](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_recall.png)**|       
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99504](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_recall.png)**|       
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.98871](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_recall.png)**|       
|   5|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.98264](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_recall.png)**|       
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.94275](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_recall.png)**|       
|   7|                                                      -|                             -|                      -|       -|          -|       
|   8|                                                      -|                             -|                      -|       -|          -|       
|   9|                                                      -|                             -|                      -|       -|          -|       
|  10|                                                      -|                             -|                      -|       -|          -|       

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Throughput Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S        |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[805,064.205](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_throughput.png)**|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[184,490.708](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_throughput.png)**|
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[97,268.471](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_throughput.png)**|
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[12,926.890](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_throughput.png)**|
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[9,150.271](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_throughput.png)**|
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[4,417.036](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_throughput.png)**|
|   7|                                                      -|                             -|                      -|       -|          -|    
|   8|                                                      -|                             -|                      -|       -|          -|    
|   9|                                                      -|                             -|                      -|       -|          -|    
|  10|                                                      -|                             -|                      -|       -|          -|    

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Power Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0002](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_power.png)**|
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_power.png)**|
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0040](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_power.png)**|
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0398](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_power.png)**|
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1126](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_power.png)**|
|   6|[-](-)                                   |-                      |-               |-|**-**|
|   7|                                                      -|                             -|                      -|       -|          -|
|   8|                                                      -|                             -|                      -|       -|          -|
|   9|                                                      -|                             -|                      -|       -|          -|
|  10|                                                      -|                             -|                      -|       -|          -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Cost Rankings 

|Rank|Submission          |Team     |Hardware               |Status  |Cost         |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|---------|-----------------------|--------|-------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel |Intel Optane               |inprog|**$16,082.49**  |$14,664.20|$1,418.29|$14,664.20 |1      |14,182.933|
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*) |NVidia GPU               |final|**$545,952.10**  |$506,503.70|$39,448.40|$22,021.90 |23      |394,484.028|
|   3|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*) |LedaE APU               |inprog|**$626,932.94**  |$612,993.26|$13,939.68|$55,726.66 |11      |139,396.812|
|   4|[-](-)|- |-               |-|**-**  |-|-|- |-      |-|
|   5|[-](-)|- |-               |-|**-**  |-|-|- |-      |-|
|   6|[-](-)|- |-               |-|**-**  |-|-|- |-      |-|
|   6|                   -|        -|                      -|       -|            -|        -|      -|        -|             -|        -|
|   7|                   -|        -|                      -|       -|            -|        -|      -|        -|             -|        -|
|   8|                   -|        -|                      -|       -|            -|        -|      -|        -|             -|        -|
|   9|                   -|        -|                      -|       -|            -|        -|      -|        -|             -|        -|
|  10|                   -|        -|                      -|       -|            -|        -|      -|        -|             -|        -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.90 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH 
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### BigANN

##### BigANN Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[0.99976](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_recall.png)**  |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99882](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_recall.png)**  |
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99815](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_recall.png)**  |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.99253](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_recall.png)**  |
|   5|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.99084](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_recall.png)**  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.92671](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_recall.png)**  |
|   7|                                                      -|                             -|                      -|       -|            -|
|   8|                                                      -|                             -|                      -|       -|            -|
|   9|                                                      -|                             -|                      -|       -|            -|
|  10|                                                      -|                             -|                      -|       -|            -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[771,493.948](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_throughput.png)**  |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[343,727.791](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_throughput.png)**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[84,367.141](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_throughput.png)**  |
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[19,094.371](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_throughput.png)**  |
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[9,504.865](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_throughput.png)**  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[3,086.656](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_throughput.png)**  |
|   7|                                                      -|                             -|                      -|       -|            -|
|   8|                                                      -|                             -|                      -|       -|            -|
|   9|                                                      -|                             -|                      -|       -|            -|
|  10|                                                      -|                             -|                      -|       -|            -|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0002](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_power.png)**|       
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0021](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_power.png)**|       
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_power.png)**|      
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0394](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_power.png)**|      
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1671](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_power.png)**|      
|   6|[-](-)                                   |-                      |-               |-|**-**|      
|   7|                                                      -|                             -|                      -|       -|          -|
|   8|                                                      -|                             -|                      -|       -|          -|
|   9|                                                      -|                             -|                      -|       -|          -|
|  10|                                                      -|                             -|                      -|       -|          -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Cost Rankings

|Rank|Submission          |Team                          |Hardware            |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|------------------------------|--------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel                      |Intel Optane            |inprog|**$15,407.15**   |$14,664.20|$742.95|$14,664.20 |1      |7,429.540|
|   2|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)                      |LedaE APU            |inprog|**$626,785.91**   |$612,993.26|$13,792.65|$55,726.66 |11      |137,926.464|      
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU            |final|**$785,282.45**   |$726,722.70|$58,559.75|$22,021.90 |33      |585,597.505|  
|   4|[-](-)|-                      |-            |-|**-**   |-|-|- |-      |-|  
|   5|[-](-)|-                      |-            |-|**-**   |-|-|- |-      |-|  
|   6|[-](-)|-                      |-            |-|**-**   |-|-|- |-      |-|  
|   7|                   -|                             -|                   -|       -|             -|       -|       -|        -|             -|        -|
|   8|                   -|                             -|                   -|       -|             -|       -|       -|        -|             -|        -|
|   9|                   -|                             -|                   -|       -|             -|       -|       -|        -|             -|        -|
|  10|                   -|                             -|                   -|       -|             -|       -|       -|        -|             -|        -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.90 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### MSTuring

##### MSTuring Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10           |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------------|
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[0.99444](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_recall.png)**    |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.98993](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_recall.png)**    |
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.98399](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_recall.png)**    |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.97841](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_recall.png)**    |
|   5|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.96218](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_recall.png)**    |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.90900](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_recall.png)**    |
|   7|                                                      -|                             -|                      -|       -|              -|       
|   8|                                                      -|                             -|                      -|       -|              -|       
|   9|                                                      -|                             -|                      -|       -|              -|       
|  10|                                                      -|                             -|                      -|       -|              -|       

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[578,677.940](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_throughput.png)** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[157,277.710](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_throughput.png)** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[111,580.136](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_throughput.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[20,166.678](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_throughput.png)** |
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[17,200.601](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_throughput.png)** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[2,359.485](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_throughput.png)** |
|   7|                                                      -|                             -|                      -|       -|           -|
|   8|                                                      -|                             -|                      -|       -|           -|
|   9|                                                      -|                             -|                      -|       -|           -|
|  10|                                                      -|                             -|                      -|       -|           -|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q         |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0004](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_power.png)** |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_power.png)** |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0049](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_power.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0227](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_power.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.2037](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_power.png)** |
|   6|[-](-)                                   |-                      |-               |-|**-** |
|   7|                                                      -|                             -|                      -|       -|           -|
|   8|                                                      -|                             -|                      -|       -|           -|
|   9|                                                      -|                             -|                      -|       -|           -|
|  10|                                                      -|                             -|                      -|       -|           -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Cost Rankings

|Rank|Submission                          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|------------------------------------|------------------------------|-----------------------|--------|--------------|--------|--------|---------|--------------|----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                |Intel                      |Intel Optane               |inprog|**$16,397.80**   |$14,664.20|$1,733.60|$14,664.20 |1      |17,335.975 |
|   2|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                |GSI Technology(*org*)                      |LedaE APU               |inprog|**$286,578.81**   |$278,633.30|$7,945.51|$55,726.66 |5      |79,455.069 |         
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                |Facebook Research(*org*)                      |NVidia GPU               |final|**$1,018,332.30**   |$946,941.70|$71,390.60|$22,021.90 |43      |713,905.964 |       
|   4|[-](-)                |-                      |-               |-|**-**   |-|-|- |-      |- |       
|   5|[-](-)                |-                      |-               |-|**-**   |-|-|- |-      |- |       
|   6|[-](-)                |-                      |-               |-|**-**   |-|-|- |-      |- |       
|   7|                                   -|                             -|                      -|       -|             -|       -|        -|       -|             -|         -|
|   8|                                   -|                             -|                      -|       -|             -|       -|        -|       -|             -|         -|
|   9|                                   -|                             -|                      -|       -|             -|       -|        -|       -|             -|         -|
|  10|                                   -|                             -|                      -|       -|             -|       -|        -|       -|             -|         -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.90 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### MSSpace

##### MSSpace Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10     |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0002](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_power.png)** |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_power.png)** |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0054](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_power.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0485](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_power.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1674](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_power.png)** |
|   6|[-](-)                                   |-                      |-               |-|**-** |
|   7|                                                      -|                             -|                      -|       -|        -|
|   8|                                                      -|                             -|                      -|       -|        -|
|   9|                                                      -|                             -|                      -|       -|        -|
|  10|                                                      -|                             -|                      -|       -|        -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[841,150.465](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_throughput.png)** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[139,612.021](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_throughput.png)** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[109,555.059](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_throughput.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[8,587.024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_throughput.png)** |
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[6,503.212](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_throughput.png)** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[2,770.848](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_throughput.png)** |
|   7|                                                      -|                             -|                      -|       -|           -|    
|   8|                                                      -|                             -|                      -|       -|           -|    
|   9|                                                      -|                             -|                      -|       -|           -|   
|  10|                                                      -|                             -|                      -|       -|           -|    

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0002](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_power.png)** |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_power.png)** |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0054](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_power.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0485](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_power.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1674](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_power.png)** |
|   6|[-](-)                                   |-                      |-               |-|**-** |
|   7|                                                      -|                             -|                      -|       -|           -|
|   8|                                                      -|                             -|                      -|       -|           -|
|   9|                                                      -|                             -|                      -|       -|           -|
|  10|                                                      -|                             -|                      -|       -|           -|

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Cost Rankings

|Rank|Submission          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|--------------------|------------------------------|-----------------------|------- |--------------|--------|--------|---------|--------------|----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel                      |Intel Optane               |inprog|**$16,563.61**   |$14,664.20|$1,899.41|$14,664.20 |1      |18,994.109 |
|   2|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)                      |LedaE APU               |inprog|**$685,704.76**   |$668,719.92|$16,984.84|$55,726.66 |12      |169,848.419 |
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU               |final|**$873,460.84**   |$814,810.30|$58,650.54|$22,021.90 |37      |586,505.424 |
|   4|[-](-)|-                      |-               |-|**-**   |-|-|- |-      |- |
|   5|[-](-)|-                      |-               |-|**-**   |-|-|- |-      |- |
|   6|[-](-)|-                      |-               |-|**-**   |-|-|- |-      |- |
|   7|                   -|                             -|                      -|       -|             -|       -|       -|        -|             -|         -|        
|   8|                   -|                             -|                      -|       -|             -|       -|       -|        -|             -|         -|        
|   9|                   -|                             -|                      -|       -|             -|       -|       -|        -|             -|         -|        
|  10|                   -|                             -|                      -|       -|             -|       -|       -|        -|             -|         -|        

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.90 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Text2Image

##### Text2Image Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[0.98130](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_recall.png)**  |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.94136](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_recall.png)**  |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.90277](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_recall.png)**  |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.88585](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_recall.png)**  |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.86028](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_recall.png)**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |
|   7|                                                      -|                             -|                      -|       -|            -|
|   8|                                                      -|                             -|                      -|       -|            -|
|   9|                                                      -|                             -|                      -|       -|            -|
|  10|                                                      -|                             -|                      -|       -|            -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[10,838.358](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_throughput.png)** |
|   2|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[9,306.610](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_throughput.png)** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[9,249.383](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_throughput.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[1,864.634](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_throughput.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[1,762.363](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_throughput.png)** |
|   6|[-](-)                                   |-                      |-               |-|**-** |
|   7|                                                      -|                             -|                      -|       -|           -|    
|   8|                                                      -|                             -|                      -|       -|           -|    
|   9|                                                      -|                             -|                      -|       -|           -|    
|  10|                                                      -|                             -|                      -|       -|           -|    

* The operational point for ranking is 0.860 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.860 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0222](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_power.png)**|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0702](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_power.png)**|
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1233](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_power.png)**|
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.1759](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_power.png)**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|
|   6|                                                      -|                             -|                      -|       -|        -|
|   7|                                                      -|                             -|                      -|       -|        -|
|   8|                                                      -|                             -|                      -|       -|        -|
|   9|                                                      -|                             -|                      -|       -|        -|
|  10|                                                      -|                             -|                      -|       -|        -|

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.86 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Cost Rankings

|Rank|Submission           |Team                          |Hardware             |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|---------------------|------------------------------|---------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md) |Intel                      |Intel Optane             |inprog|**$171,244.96**   |$146,642.00|$24,602.96|$14,664.20 |10      |246,029.624|
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md) |Facebook Research(*org*)                      |NVidia GPU             |final|**$1,298,436.77**   |$1,255,248.30|$43,188.47|$22,021.90 |57      |431,884.673| 
|   3|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md) |GSI Technology(*org*)                      |LedaE APU             |inprog|**$3,070,882.16**   |$3,009,239.64|$61,642.52|$55,726.66 |54      |616,425.231| 
|   4|[-](-) |-                      |-             |-|**-**   |-|-|- |-      |-| 
|   5|[-](-) |-                      |-             |-|**-**   |-|-|- |-      |-| 
|   6|[-](-) |-                      |-             |-|**-**   |-|-|- |-      |-| 
|   7|                    -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
|   8|                    -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
|   9|                    -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
|  10|                    -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.86 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### FBSimSearchNet

##### FBSimSearchNet AP Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |AP          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.99053](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_recall.png)**  |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.97863](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_recall.png)**  |
|   3|[-](-)                                   |-                      |-               |-|**-**  |
|   4|[-](-)                                   |-                      |-               |-|**-**  |
|   5|[-](-)                                   |-                      |-               |-|**-**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |
|   7|                                                      -|                             -|                      -|       -|            -|
|   8|                                                      -|                             -|                      -|       -|            -|
|   9|                                                      -|                             -|                      -|       -|            -|
|  10|                                                      -|                             -|                      -|       -|            -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### FBSimSearchNet Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[8,123.552](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_throughput.png)** |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[5,572.272](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_throughput.png)** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |
|   7|                                                      -|                             -|                      -|       -|           -|
|   8|                                                      -|                             -|                      -|       -|           -|
|   9|                                                      -|                             -|                      -|       -|           -|
|  10|                                                      -|                             -|                      -|       -|           -|

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 average precision.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress


##### FBSimSearchNet Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0540](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_power.png)**|
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.0949](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_power.png)**|
|   3|[-](-)                                   |-                      |-               |-|**-**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|
|   7|                                                      -|                             -|                      -|       -|          -|
|   8|                                                      -|                             -|                      -|       -|          -|
|   9|                                                      -|                             -|                      -|       -|          -|
|  10|                                                      -|                             -|                      -|       -|          -|

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 average precision.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### FBSimSearchNet Cost Rankings

|Rank|Submission          |Team                          |Hardware             |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|------------------------------|---------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU             |final|**$429,634.84**   |$396,394.20|$33,240.64|$22,021.90 |18      |332,406.441|
|   2|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)                      |LedaE APU             |inprog|**$743,385.69**   |       -|       -|        -|             -|        -|       
|   3|[-](-)|-                      |-             |-|**-**   |       -|       -|        -|             -|        -|       
|   4|[-](-)|-                      |-             |-|**-**   |       -|       -|        -|             -|        -|       
|   5|                   -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
|   6|                   -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
|   7|                   -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
|   8|                   -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
|   9|                   -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
|  10|                   -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.9 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

