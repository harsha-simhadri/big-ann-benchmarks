# T3 Track Public Dataset Leaderboards  

Please note that all rankings and winners are unofficial until all [open tasks and issues](TASKS_ISSUES_RESOLUTIONS.md) are resolved.

## Rankings By Category

### Rankings By Submission Name (alphabetical)

|Submission          |Team       |Hardware  |[Recall Rank](#recall-or-ap-rankings)|[Thru-put Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)|Status |Anomalies|Evaluator|Algo     |Runs   |  
|--------------------|-----------|----------|---------|---------|---------|--------|---------|---------|---------|---------|--------|
|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)  |Microsoft Research India(*org*)    |Dell PowerEdge   |[1](#recall-or-ap-rankings)  |[5](#throughput-rankings)  |*NQ*  |*NQ* |final   |*NA*  |[Harsha Simhadri](https://github.com/harsha-simhadri)  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/diskann-t2.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/EvalPublic.ipynb) |
|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)    |Facebook Research(*org*)     |NVidia GPU    |[6](#recall-or-ap-rankings)   |[6](#throughput-rankings)   |[5](#power-rankings)   |[5](#cost-rankings)  |final    |0/58   |[George Williams](https://github.com/sourcesync)   |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/faiss_t3.py)   |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/EvalPublic.ipynb)  |
|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)  |GSI Technology(*org*)    |LedaE APU   |[4](#recall-or-ap-rankings)  |[4](#throughput-rankings)  |[4](#power-rankings)  |[4](#cost-rankings) |final   |0/60  |[George Williams](https://github.com/sourcesync)  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/gemini.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/EvalPublic.ipynb) |
|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)  |NVidia    |NVidia GPU   |[3](#recall-or-ap-rankings)  |[3](#throughput-rankings)  |[2](#power-rankings)  |[2](#cost-rankings)\*\* |final   |[6/50](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/ANOMALIES.md)  |[George Williams](https://github.com/sourcesync)  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_ivfpq.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/EvalPublic.ipynb) |
|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)    |NVidia     |NVidia GPU    |[5](#recall-or-ap-rankings)   |[1](#throughput-rankings)   |[3](#power-rankings)   |[3](#cost-rankings)\*\*  |final    |[4/40](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/ANOMALIES.md)   |[George Williams](https://github.com/sourcesync)   |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_multigpu.py)   |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/EvalPublic.ipynb)  |
|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel   |Intel Optane  |[2](#recall-or-ap-rankings) |[2](#throughput-rankings) |[1](#power-rankings) |[1](#cost-rankings)|final  |[5/50](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/ANOMALIES.md) |[George Williams](https://github.com/sourcesync) |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/graphann.py) |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/EvalPublic.ipynb)|

* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.
  * *NQ* = not qualified
  * *NA* = data is not yet available, or has not yet been processed

* *Anomalies* are defined as queries that could potentially be the result of query response caching, a violation of the competition.  Our detection method looks for a 30% or more improvement in the batch query latency between the first and last query of a query group (5).  Participants have been given a chance to explain why detected anomalies (if any) are not a result of query response caching.  In general, our analysis did not uncover this symptom of systematic query response caching from any submission.  Also, if we throw out the anomalous data points, the [adjusted leaderboard rankings](LEADERBOARDS_PUBLIC_REJECT_ANOMALIES.md) do not change even though some scores change slightly.

* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

### Rankings Per Benchmark

#### Recall Or AP Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-recall-rankings)|[BigANN](#bigann-recall-rankings)|[MSTuring](#msturing-recall-rankings)|[MSSpace](#msspace-recall-rankings)|[Text2Image](#text2image-recall-rankings)|[FBSSNet](#fbsimsearchnet-ap-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|-------|
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Microsoft Research India(*org*)|Dell PowerEdge |final|**0.410**|[0.99821](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_recall.png) |[0.99976](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_recall.png) |[0.99444](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_recall.png)   |[0.99342](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_recall.png)  |[0.98130](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_recall.png)     |-  |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |final|**0.409**|[0.99882](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_recall.png) |[0.99978](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_recall.png) |[0.99568](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_recall.png)   |[0.99835](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_recall.png)  |[0.97340](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_recall.png)     |-  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |final|**0.368**|[0.99543](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_recall.png) |[0.99881](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_recall.png) |[0.98993](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_recall.png)   |[0.99429](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_recall.png)  |[0.94692](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_recall.png)     |-  |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |final|**0.339**|[0.99208](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_recall.png) |[0.99328](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_recall.png) |[0.97841](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_recall.png)   |[0.98622](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_recall.png)  |[0.92855](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_recall.png)     |[0.99684](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_recall.png)  |
|   5|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |final|**0.268**|[0.99504](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_recall.png) |[0.99815](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_recall.png) |[0.98399](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_recall.png)   |[0.98785](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_recall.png)  |-     |-  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[0.94275](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_recall.png) |[0.93260](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_recall.png) |[0.91322](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_recall.png)   |[0.90853](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_recall.png)  |[0.86028](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_recall.png)     |[0.97863](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_recall.png)  |

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

#### Throughput Rankings

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-throughput-rankings)|[BigANN](#bigann-throughput-rankings)|[MSTuring](#msturing-throughput-rankings)|[MSSpace](#msspace-throughput-rankings)|[Text2Image](#text2image-throughput-rankings)|[FBSSNet](#fbsimsearchnet-throughput-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |final|**2959313**|[801,694](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_throughput.png) |[747,421](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_throughput.png) |[584,293](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_throughput.png)   |[839,749](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_throughput.png)  |-     |-         |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |final|**853257**|[196,546](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_throughput.png) |[335,991](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_throughput.png) |[161,463](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_throughput.png)   |[157,828](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_throughput.png)  |[17,063](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_throughput.png)     |-         | 
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |final|**393318**|[91,701](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_throughput.png) |[80,109](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_throughput.png) |[109,745](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_throughput.png)   |[108,302](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_throughput.png)  |[19,094](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_throughput.png)     |-         | 
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |final|**52429**|[10,704](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_throughput.png) |[10,672](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_throughput.png) |[21,780](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_throughput.png)   |[16,422](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_throughput.png)  |[4,838](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_throughput.png)     |[9,345](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_throughput.png)         | 
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Microsoft Research India(*org*)|Dell PowerEdge |final|**49398**|[12,927](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_throughput.png) |[19,094](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_throughput.png) |[17,201](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_throughput.png)   |[6,503](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_throughput.png)  |[9,307](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_throughput.png)     |-         | 
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[4,464](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_throughput.png) |[3,271](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_throughput.png) |[2,845](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_throughput.png)   |[3,265](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_throughput.png)  |[1,789](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_throughput.png)     |[5,699](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_throughput.png)         | 

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

#### Power Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-power-rankings)|[BigANN](#bigann-power-rankings)|[MSTuring](#msturing-power-rankings)|[MSSpace](#msspace-power-rankings)|[Text2Image](#text2image-power-rankings)|[FBSSNet](#fbsimsearchnet-power-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|-----|-----|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|Intel|Intel Optane |final|**-0.648**|[0.0041](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_power.png) |[0.0022](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_power.png) |[0.0048](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_power.png)   |[0.0049](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_power.png)  |[0.0446](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_power.png)|-|
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|NVidia|NVidia GPU |final|**-0.619**|[0.0112](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_power.png) |[0.0119](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_power.png) |[0.0090](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_power.png)   |[0.0090](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_power.png)  |[0.0480](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_power.png)|-| 
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |final|**-0.583**|[0.0029](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_power.png) |[0.0024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_power.png) |[0.0049](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_power.png)   |[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_power.png)  |-|-| 
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |final|**-0.513**|[0.0337](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_power.png) |[0.0341](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_power.png) |[0.0236](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_power.png)   |[0.0230](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_power.png)  |[0.1242](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_power.png)|[0.0469](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_power.png)| 
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[0.1117](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_power.png) |[0.1576](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_power.png) |[0.1743](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_power.png)   |[0.1520](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_power.png)  |[0.1128](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_power.png)|[0.0904](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_power.png)| 
|   6|[-](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|-|- |-|**-**|- |- |-   |-  |-|-| 

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

#### Cost Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-cost-rankings)|[BigANN](#bigann-cost-rankings)|[MSTuring](#msturing-cost-rankings)|[MSSpace](#msspace-cost-rankings)|[Text2Image](#text2image-cost-rankings)|[FBSSNet](#fbsimsearchnet-cost-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |final|**$-3,978,198.83**|$16,086.82 |$15,439.92 |$16,347.45   |$16,382.81  |$103,599.49     |-         |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |final|**$-2,314,829.98\*\***|$303,929.39 |$304,166.48 |$153,151.00   |$153,155.12  |$916,823.34     |-         |
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |final|**$-2,268,943.17\*\***|$151,009.85 |$150,824.13 |$151,726.30   |$150,816.00  |-     |-         |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |final|**$-907,570.13**|$569,058.09 |$569,210.35 |$286,911.87   |$398,163.18  |$1,213,773.56     |$629,442.91         |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|$545,633.16 |$737,886.17 |$853,857.46   |$735,942.66  |$1,272,735.86     |$428,074.79         |
|   6|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

### Rankings Per Database

#### Deep1B

##### Deep1B Recall Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.99882](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_recall.png)**|       
|   2|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[0.99821](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_recall.png)**|       
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.99543](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_recall.png)**|       
|   4|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.99504](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_recall.png)**|       
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.99208](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_recall.png)**|       
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.94275](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_recall.png)**|       

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### Deep1B Throughput Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S        |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[801,694](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_throughput.png)**|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[196,546](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_throughput.png)**|
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[91,701](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_throughput.png)**|
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[12,927](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/deep-1B_throughput.png)**|
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[10,704](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_throughput.png)**|
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[4,464](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_throughput.png)**|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### Deep1B Power Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.0029](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/deep-1B_power.png)**|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.0041](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/deep-1B_power.png)**|
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.0112](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_power.png)**|
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.0337](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/deep-1B_power.png)**|
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1117](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/deep-1B_power.png)**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### Deep1B Cost Rankings 

|Rank|Submission          |Team     |Hardware               |Status  |Cost         |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|---------|-----------------------|--------|-------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel |Intel Optane               |final|**$16,086.82**  |$14,664.20|$1,422.62|$14,664.20 |1      |14,226.208|
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia |NVidia GPU               |final|**$151,009.85\*\***  |$150,000.00|$1,009.85|$150,000.00 |1      |10,098.482|
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia |NVidia GPU               |final|**$303,929.39\*\***  |$300,000.00|$3,929.39|$150,000.00 |2      |39,293.902|
|   4|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*) |NVidia GPU               |final|**$545,633.16**  |$506,503.70|$39,129.46|$22,021.90 |23      |391,294.584|
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*) |LedaE APU               |final|**$569,058.09**  |$557,266.60|$11,791.49|$55,726.66 |10      |117,914.908|
|   6|[-](-)|- |-               |-|**-**  |-|-|- |-      |-|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.90 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH 
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### BigANN

##### BigANN Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.99978](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_recall.png)**  |
|   2|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[0.99976](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_recall.png)**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.99881](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_recall.png)**  |
|   4|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.99815](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_recall.png)**  |
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.99328](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_recall.png)**  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.93260](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_recall.png)**  |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### BigANN Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[747,421](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_throughput.png)**  |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[335,991](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_throughput.png)**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[80,109](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_throughput.png)**  |
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[19,094](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/bigann-1B_throughput.png)**  |
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[10,672](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_throughput.png)**  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[3,271](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_throughput.png)**  |

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### BigANN Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.0022](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/bigann-1B_power.png)**|       
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.0024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/bigann-1B_power.png)**|       
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.0119](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_power.png)**|      
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.0341](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/bigann-1B_power.png)**|      
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1576](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/bigann-1B_power.png)**|      
|   6|[-](-)                                   |-                      |-               |-|**-**|      

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### BigANN Cost Rankings

|Rank|Submission          |Team                          |Hardware            |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|------------------------------|--------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel                      |Intel Optane            |final|**$15,439.92**   |$14,664.20|$775.72|$14,664.20 |1      |7,757.221|
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia                      |NVidia GPU            |final|**$150,824.13\*\***   |$150,000.00|$824.13|$150,000.00 |1      |8,241.343|      
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia                      |NVidia GPU            |final|**$304,166.48\*\***   |$300,000.00|$4,166.48|$150,000.00 |2      |41,664.844|  
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)                      |LedaE APU            |final|**$569,210.35**   |$557,266.60|$11,943.75|$55,726.66 |10      |119,437.537|  
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU            |final|**$737,886.17**   |$682,678.90|$55,207.27|$22,021.90 |31      |552,072.703|  
|   6|[-](-)|-                      |-            |-|**-**   |-|-|- |-      |-|  

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.90 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### MSTuring

##### MSTuring Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10           |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.99568](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_recall.png)**    |
|   2|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[0.99444](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_recall.png)**    |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.98993](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_recall.png)**    |
|   4|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.98399](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_recall.png)**    |
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.97841](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_recall.png)**    |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.91322](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_recall.png)**    |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### MSTuring Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[584,293](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_throughput.png)** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[161,463](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_throughput.png)** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[109,745](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_throughput.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[21,780](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_throughput.png)** |
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[17,201](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msturing-1B_throughput.png)** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[2,845](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_throughput.png)** |

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### MSTuring Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q         |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.0048](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msturing-1B_power.png)** |
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.0049](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msturing-1B_power.png)** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.0090](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_power.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.0236](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msturing-1B_power.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1743](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msturing-1B_power.png)** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### MSTuring Cost Rankings

|Rank|Submission                          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|------------------------------------|------------------------------|-----------------------|--------|--------------|--------|--------|---------|--------------|----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                |Intel                      |Intel Optane               |final|**$16,347.45**   |$14,664.20|$1,683.25|$14,664.20 |1      |16,832.451 |
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                |NVidia                      |NVidia GPU               |final|**$151,726.30\*\***   |$150,000.00|$1,726.30|$150,000.00 |1      |17,262.993 |         
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                |NVidia                      |NVidia GPU               |final|**$153,151.00\*\***   |$150,000.00|$3,151.00|$150,000.00 |1      |31,509.973 |       
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                |GSI Technology(*org*)                      |LedaE APU               |final|**$286,911.87**   |$278,633.30|$8,278.57|$55,726.66 |5      |82,785.683 |       
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                |Facebook Research(*org*)                      |NVidia GPU               |final|**$853,857.46**   |$792,788.40|$61,069.06|$22,021.90 |36      |610,690.611 |       
|   6|[-](-)                |-                      |-               |-|**-**   |-|-|- |-      |- |       

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.90 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### MSSpace

##### MSSpace Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10     |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.99835](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_recall.png)** |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.99429](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_recall.png)** |
|   3|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[0.99342](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_recall.png)** |
|   4|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.98785](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_recall.png)** |
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.98622](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_recall.png)** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.90853](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_recall.png)** |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### MSSpace Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[839,749](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_throughput.png)** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[157,828](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_throughput.png)** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[108,302](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_throughput.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[16,422](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_throughput.png)** |
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[6,503](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/msspacev-1B_throughput.png)** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[3,265](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_throughput.png)** |

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### MSSpace Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_multigpu/msspacev-1B_power.png)** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.0049](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/msspacev-1B_power.png)** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.0090](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_power.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.0230](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/msspacev-1B_power.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1520](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/msspacev-1B_power.png)** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### MSSpace Cost Rankings

|Rank|Submission          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|--------------------|------------------------------|-----------------------|------- |--------------|--------|--------|---------|--------------|----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel                      |Intel Optane               |final|**$16,382.81**   |$14,664.20|$1,718.61|$14,664.20 |1      |17,186.056 |
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia                      |NVidia GPU               |final|**$150,816.00\*\***   |$150,000.00|$816.00|$150,000.00 |1      |8,160.006 |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia                      |NVidia GPU               |final|**$153,155.12\*\***   |$150,000.00|$3,155.12|$150,000.00 |1      |31,551.163 |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)                      |LedaE APU               |final|**$398,163.18**   |$390,086.62|$8,076.56|$55,726.66 |7      |80,765.638 |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU               |final|**$735,942.66**   |$682,678.90|$53,263.76|$22,021.90 |31      |532,637.584 |
|   6|[-](-)|-                      |-               |-|**-**   |-|-|- |-      |- |

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.90 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### Text2Image

##### Text2Image Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[0.98130](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_recall.png)**  |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.97340](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_recall.png)**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.94692](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_recall.png)**  |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.92855](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_recall.png)**  |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.86028](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_recall.png)**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### Text2Image Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[19,094](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_throughput.png)** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[17,063](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_throughput.png)** |
|   3|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**[9,307](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/diskann-bare-metal/text2image-1B_throughput.png)** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[4,838](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_throughput.png)** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[1,789](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_throughput.png)** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.860 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.860 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### Text2Image Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**[0.0446](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/text2image-1B_power.png)**|
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**[0.0480](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_power.png)**|
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.1128](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/text2image-1B_power.png)**|
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.1242](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/text2image-1B_power.png)**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.86 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### Text2Image Cost Rankings

|Rank|Submission           |Team                          |Hardware             |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|---------------------|------------------------------|---------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md) |Intel                      |Intel Optane             |final|**$103,599.49**   |$87,985.20|$15,614.29|$14,664.20 |6      |156,142.873|
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md) |NVidia                      |NVidia GPU             |final|**$916,823.34\*\***   |$900,000.00|$16,823.34|$150,000.00 |6      |168,233.421| 
|   3|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md) |GSI Technology(*org*)                      |LedaE APU             |final|**$1,213,773.56**   |$1,170,259.86|$43,513.70|$55,726.66 |21      |435,137.010| 
|   4|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md) |Facebook Research(*org*)                      |NVidia GPU             |final|**$1,272,735.86**   |$1,233,226.40|$39,509.46|$22,021.90 |56      |395,094.625| 
|   5|[-](-) |-                      |-             |-|**-**   |-|-|- |-      |-| 
|   6|[-](-) |-                      |-             |-|**-**   |-|-|- |-      |-| 

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.86 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### FBSimSearchNet

##### FBSimSearchNet AP Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |AP          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.99684](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_recall.png)**  |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.97863](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_recall.png)**  |
|   3|[-](-)                                   |-                      |-               |-|**-**  |
|   4|[-](-)                                   |-                      |-               |-|**-**  |
|   5|[-](-)                                   |-                      |-               |-|**-**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### FBSimSearchNet Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[9,345](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_throughput.png)** |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[5,699](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_throughput.png)** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 average precision.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.


##### FBSimSearchNet Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**[0.0469](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/gemini/ssnpp-1B_power.png)**|
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**[0.0904](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/ssnpp-1B_power.png)**|
|   3|[-](-)                                   |-                      |-               |-|**-**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 average precision.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.

##### FBSimSearchNet Cost Rankings

|Rank|Submission          |Team                          |Hardware             |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|------------------------------|---------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU             |final|**$428,074.79**   |$396,394.20|$31,680.59|$22,021.90 |18      |316,805.859|
|   2|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)                      |LedaE APU             |final|**$629,442.91**   |$612,993.26|$16,449.65|$55,726.66 |11      |164,496.451|
|   3|[-](-)|-                      |-             |-|**-**   |       -|       -|        -|             -|        -|       
|   4|[-](-)|-                      |-             |-|**-**   |       -|       -|        -|             -|        -|       

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.9 recall@10.
* The formula is based on:
  * Take the algorithm's throughput submitted to leaderboard, use it to scale no. of systems needed to scale to 100K qps (using ceiling to round up any decimal.)
  * Capex = cost per system * scale no.
  * Take w*s/q from algorithm's power metric submitted to leaderboard and convert to KwH/q.
  * Multiply by total queries at 100K qps for 4 years = 4x365x24x60x60x100000 total queries over 4 years.
  * Opex = (total queries over 4 years) * KwH/query * $0.10/KwH
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *eval* = final submissions are being evaluated.
  * *final* = final submission and ranking.
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.
