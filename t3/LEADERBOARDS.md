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
|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)    |Facebook Research(*org*)     |NVidia GPU    |final  |George Williams   |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/faiss_t3.py)   |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/EvalPublic.ipynb)  |[6](#recall-or-ap-rankings)   |[6](#throughput-rankings)        |[5](#power-rankings)                       |[4](#cost-rankings)                     |
|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)  |GSI Technology(*org*)    |LedaE APU   |inprog |George Williams  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/gemini.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/EvalPublic.ipynb) |[3](#recall-or-ap-rankings)  |[5](#throughput-rankings)       |[4](#power-rankings)                      |[5](#cost-rankings)                    |
|kanndi              |Silo.ai    |LedaE APU   |inprog |        -|        -|       -|        -|             -|                            -|                          -|
|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)  |NVidia    |NVidia GPU   |inprog |George Williams  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_ivfpq.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/EvalPublic.ipynb) |[2](#recall-or-ap-rankings)  |[3](#throughput-rankings)       |[1](#power-rankings)                      |[3](#cost-rankings)                    |
|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)    |NVidia     |NVidia GPU    |inprog  |George Williams   |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_multigpu.py)   |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/EvalPublic.ipynb)  |[4](#recall-or-ap-rankings)   |[1](#throughput-rankings)        |[3](#power-rankings)                       |[2](#cost-rankings)                     |
|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel   |Intel Optane  |inprog|George Williams |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/graphann.py) |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/EvalPublic.ipynb)|[5](#recall-or-ap-rankings) |[2](#throughput-rankings)      |[2](#power-rankings)                     |[1](#cost-rankings)                   |
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
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Microsoft Research(*org*)|Dell PowerEdge |inprog|**0.410**|[0.99821](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_recall.png) |[0.99976](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_recall.png) |[0.99444](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_recall.png)   |[0.99342](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_recall.png)  |[0.98130](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_recall.png)     |-  |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**0.367**|[0.99544](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_recall.png) |[0.99881](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_recall.png) |[0.98993](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_recall.png)   |[0.99428](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_recall.png)  |[0.94566](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_recall.png)     |-  |
|   3|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**0.286**|[0.98871](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_recall.png) |[0.99253](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_recall.png) |[0.97841](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_recall.png)   |[0.98622](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_recall.png)  |[0.88585](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_recall.png)     |[0.99053](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_recall.png)  |
|   4|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |inprog|**0.268**|[0.99504](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_recall.png) |[0.99815](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_recall.png) |[0.98399](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_recall.png)   |[0.98785](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_recall.png)  |-     |-  |
|   5|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**0.226**|[0.90830](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_recall.png) |[0.99978](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_recall.png) |[0.90521](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_recall.png)   |[0.99835](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_recall.png)  |[0.97154](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_recall.png)     |-  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[0.94275](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_recall.png) |[0.93260](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_recall.png) |[0.91322](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_recall.png)   |[0.90853](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_recall.png)  |[0.86028](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_recall.png)     |[0.97863](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_recall.png)  |
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
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |inprog|**3001623.821**|[816,807.011](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_throughput.png) |[767,653.282](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_throughput.png) |[586,721.800](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_throughput.png)   |[844,286.629](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_throughput.png)  |-     |-         |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**825055.094**|[191,149.778](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_throughput.png) |[325,457.734](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_throughput.png) |[153,252.413](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_throughput.png)   |[159,581.445](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_throughput.png)  |[11,247.281](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_throughput.png)     |-         | 
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**394699.659**|[93,125.840](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_throughput.png) |[85,256.146](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_throughput.png) |[111,894.894](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_throughput.png)   |[109,378.570](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_throughput.png)  |[10,677.767](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_throughput.png)     |-         | 
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Microsoft Research(*org*)|Dell PowerEdge |inprog|**49398.127**|[12,926.890](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_throughput.png) |[19,094.371](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_throughput.png) |[17,200.601](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_throughput.png)   |[6,503.212](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_throughput.png)  |[9,306.610](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_throughput.png)     |-         | 
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**36064.137**|[9,150.271](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_throughput.png) |[9,504.865](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_throughput.png) |[20,166.678](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_throughput.png)   |[8,587.024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_throughput.png)  |[1,864.634](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_throughput.png)     |[8,123.552](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_throughput.png)         | 
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[4,464.182](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_throughput.png) |[3,270.535](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_throughput.png) |[2,844.816](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_throughput.png)   |[3,265.367](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_throughput.png)  |[1,788.657](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_throughput.png)     |[5,699.329](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_throughput.png)         | 
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |inprog|**-0.683**|[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_power.png) |[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_power.png) |[0.0016](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_power.png)   |[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_power.png)  |[0.0171](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_power.png)|-|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**-0.624**|[0.0041](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_power.png) |[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_power.png) |[0.0052](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_power.png)   |[0.0047](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_power.png)  |[0.0681](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_power.png)|-| 
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**-0.594**|[0.0002](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_power.png) |[0.0003](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_power.png) |[0.0004](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_power.png)   |[0.0002](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_power.png)  |-|-| 
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**-0.418**|[0.0398](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_power.png) |[0.0394](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_power.png) |[0.0227](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_power.png)   |[0.0485](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_power.png)  |[0.1759](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_power.png)|[0.0540](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_power.png)| 
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[0.1117](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_power.png) |[0.1576](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_power.png) |[0.1743](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_power.png)   |[0.1520](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_power.png)  |[0.1128](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_power.png)|[0.0904](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_power.png)| 
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
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**$-3,925,826.98**|$16,115.79 |$15,459.22 |$16,484.93   |$16,324.02  |$155,844.36     |-         |
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |inprog|**$-2,272,942.67**|$150,082.04 |$150,088.58 |$150,127.39   |$150,078.78  |-     |-         |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**$-1,737,278.92**|$300,820.98 |$300,805.92 |$150,561.50   |$150,588.67  |$1,505,999.32     |-         |
|   4|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|$545,633.16 |$737,886.17 |$853,857.46   |$735,942.66  |$1,272,735.86     |$428,074.79         |
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**$1,466,140.17**|$626,932.94 |$626,785.91 |$286,578.81   |$685,704.76  |$3,070,882.16     |$743,385.69         |
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
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99544](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_recall.png)**|       
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99504](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_recall.png)**|       
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.98871](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_recall.png)**|       
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.94275](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_recall.png)**|       
|   6|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.90830](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_recall.png)**|       
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
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[816,807.011](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_throughput.png)**|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[191,149.778](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_throughput.png)**|
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[93,125.840](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_throughput.png)**|
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[12,926.890](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_throughput.png)**|
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[9,150.271](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_throughput.png)**|
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[4,464.182](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_throughput.png)**|
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
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0041](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_power.png)**|
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0398](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_power.png)**|
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1117](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_power.png)**|
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
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel |Intel Optane               |inprog|**$16,115.79**  |$14,664.20|$1,451.59|$14,664.20 |1      |14,515.931|
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia |NVidia GPU               |inprog|**$150,082.04**  |$150,000.00|$82.04|$150,000.00 |1      |820.405|
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia |NVidia GPU               |inprog|**$300,820.98**  |$300,000.00|$820.98|$150,000.00 |2      |8,209.847|
|   4|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*) |NVidia GPU               |final|**$545,633.16**  |$506,503.70|$39,129.46|$22,021.90 |23      |391,294.584|
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*) |LedaE APU               |inprog|**$626,932.94**  |$612,993.26|$13,939.68|$55,726.66 |11      |139,396.812|
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
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.99978](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_recall.png)**  |
|   2|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[0.99976](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_recall.png)**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99881](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_recall.png)**  |
|   4|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99815](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_recall.png)**  |
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.99253](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_recall.png)**  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.93260](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_recall.png)**  |
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
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[767,653.282](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_throughput.png)**  |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[325,457.734](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_throughput.png)**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[85,256.146](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_throughput.png)**  |
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[19,094.371](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_throughput.png)**  |
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[9,504.865](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_throughput.png)**  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[3,270.535](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_throughput.png)**  |
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
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0003](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_power.png)**|       
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_power.png)**|       
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_power.png)**|      
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0394](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_power.png)**|      
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1576](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_power.png)**|      
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
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel                      |Intel Optane            |inprog|**$15,459.22**   |$14,664.20|$795.02|$14,664.20 |1      |7,950.241|
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia                      |NVidia GPU            |inprog|**$150,088.58**   |$150,000.00|$88.58|$150,000.00 |1      |885.770|      
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia                      |NVidia GPU            |inprog|**$300,805.92**   |$300,000.00|$805.92|$150,000.00 |2      |8,059.191|  
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)                      |LedaE APU            |inprog|**$626,785.91**   |$612,993.26|$13,792.65|$55,726.66 |11      |137,926.464|  
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU            |final|**$737,886.17**   |$682,678.90|$55,207.27|$22,021.90 |31      |552,072.703|  
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
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.91322](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_recall.png)**    |
|   6|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.90521](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_recall.png)**    |
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
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[586,721.800](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_throughput.png)** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[153,252.413](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_throughput.png)** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[111,894.894](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_throughput.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[20,166.678](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_throughput.png)** |
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[17,200.601](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_throughput.png)** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[2,844.816](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_throughput.png)** |
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
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0016](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_power.png)** |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0052](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_power.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0227](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_power.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1743](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_power.png)** |
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
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                |Intel                      |Intel Optane               |inprog|**$16,484.93**   |$14,664.20|$1,820.73|$14,664.20 |1      |18,207.329 |
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                |NVidia                      |NVidia GPU               |inprog|**$150,127.39**   |$150,000.00|$127.39|$150,000.00 |1      |1,273.870 |         
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                |NVidia                      |NVidia GPU               |inprog|**$150,561.50**   |$150,000.00|$561.50|$150,000.00 |1      |5,615.008 |       
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                |GSI Technology(*org*)                      |LedaE APU               |inprog|**$286,578.81**   |$278,633.30|$7,945.51|$55,726.66 |5      |79,455.069 |       
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                |Facebook Research(*org*)                      |NVidia GPU               |final|**$853,857.46**   |$792,788.40|$61,069.06|$22,021.90 |36      |610,690.611 |       
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
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0047](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_power.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0485](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_power.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1520](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_power.png)** |
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
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[844,286.629](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_throughput.png)** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[159,581.445](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_throughput.png)** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[109,378.570](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_throughput.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[8,587.024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_throughput.png)** |
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[6,503.212](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_throughput.png)** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[3,265.367](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_throughput.png)** |
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
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0047](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_power.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.0485](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_power.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1520](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_power.png)** |
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
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel                      |Intel Optane               |inprog|**$16,324.02**   |$14,664.20|$1,659.82|$14,664.20 |1      |16,598.186 |
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia                      |NVidia GPU               |inprog|**$150,078.78**   |$150,000.00|$78.78|$150,000.00 |1      |787.774 |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia                      |NVidia GPU               |inprog|**$150,588.67**   |$150,000.00|$588.67|$150,000.00 |1      |5,886.680 |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)                      |LedaE APU               |inprog|**$685,704.76**   |$668,719.92|$16,984.84|$55,726.66 |12      |169,848.419 |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU               |final|**$735,942.66**   |$682,678.90|$53,263.76|$22,021.90 |31      |532,637.584 |
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
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.97154](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_recall.png)**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.94566](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_recall.png)**  |
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
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[11,247.281](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_throughput.png)** |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[10,677.767](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_throughput.png)** |
|   3|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[9,306.610](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_throughput.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[1,864.634](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_throughput.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[1,788.657](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_throughput.png)** |
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0171](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_power.png)**|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.0681](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_power.png)**|
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1128](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_power.png)**|
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
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md) |Intel                      |Intel Optane             |inprog|**$155,844.36**   |$131,977.80|$23,866.56|$14,664.20 |9      |238,665.619|
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md) |Facebook Research(*org*)                      |NVidia GPU             |final|**$1,272,735.86**   |$1,233,226.40|$39,509.46|$22,021.90 |56      |395,094.625| 
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md) |NVidia                      |NVidia GPU             |inprog|**$1,505,999.32**   |$1,500,000.00|$5,999.32|$150,000.00 |10      |59,993.177| 
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md) |GSI Technology(*org*)                      |LedaE APU             |inprog|**$3,070,882.16**   |$3,009,239.64|$61,642.52|$55,726.66 |54      |616,425.231| 
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
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[5,699.329](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_throughput.png)** |
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
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.0904](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_power.png)**|
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
|   1|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU             |final|**$428,074.79**   |$396,394.20|$31,680.59|$22,021.90 |18      |316,805.859|
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

