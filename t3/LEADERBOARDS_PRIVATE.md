# T3 Track Private Dataset Leaderboards  (Unofficial)

Please note that all rankings and winners are currently unofficial due to the following reasons:
* All [open tasks and issues](TASKS_ISSUES_RESOLUTIONS.md) must be resolved.

## Rankings By Category

### Rankings By Submission Name (alphabetical)

|Submission          |Team       |Hardware  |[Recall Rank](#recall-or-ap-rankings)|[Thru-put Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)|Status |Anomalies|Evaluator|Algo     |Runs   |  
|--------------------|-----------|----------|---------|---------|---------|--------|---------|---------|---------|---------|--------|
|[$MSD_SB]($MSD_RD)  |$MSD_TM    |$MSD_HW   |$MSD_RR  |$MSD_QR  |$MSD_PR  |$MSD_CR |$MSD_S   |$MSD_AC  |$MSD_EV  |$MSD_AL  |$MSD_AN |
|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)    |Facebook Research(*org*)     |NVidia GPU    |[3](#recall-or-ap-rankings)   |[3](#throughput-rankings)   |[3](#power-rankings)   |[3](#cost-rankings)  |eval    |0/49   |George Williams   |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/faiss_t3.py)   |NA  |
|[$GEM_SB]($GEM_RD)  |$GEM_TM    |$GEM_HW   |$GEM_RR  |$GEM_QR  |$GEM_PR  |$GEM_CR |$GEM_S   |$GEM_AC  |$GEM_EV  |$GEM_AL  |$GEM_AN |
|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)  |NVidia    |NVidia GPU   |[1](#recall-or-ap-rankings)  |[2](#throughput-rankings)  |[1](#power-rankings)  |[2](#cost-rankings)\*\* |eval   |[5/40](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/ANOMALIES.md)  |George Williams  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_ivfpq.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/EvalPublic.ipynb) |
|[$NV_SB]($NV_RD)    |$NV_TM     |$NV_HW    |$NV_RR   |$NV_QR   |$NV_PR   |$NV_CR  |$NV_S    |$NV_AC   |$NV_EV   |$NV_AL   |$NV_AN  |
|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel   |Intel Optane  |[2](#recall-or-ap-rankings) |[1](#throughput-rankings) |[2](#power-rankings) |[1](#cost-rankings)|eval  |[4/40](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/ANOMALIES.md) |George Williams |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/graphann.py) |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/EvalPublic.ipynb)|

* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *NQ* = not qualified
  * *NA* = data is not yet available, or has not yet been processed

* *Anomalies* are defined as queries that could potentially be the result of query response caching, a violation of the competition.  Our detection method looks for a 30% or more improvement in the batch query latency between the first and last query of a query group (5).  Participants have been given a chance to explain why detected anomalies (if any) are not a result of query response caching.  In general, our analysis did not uncover this symptom of systematic query response caching from any submission.  Also, if we throw out the anomalous data points, the [adjusted leaderboard rankings](LEADERBOARDS_PRIVATE_REJECT_ANOMALIES.md) do not change even though some scores change slightly.

* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

### Rankings Per Benchmark

#### Recall Or AP Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-recall-rankings)|[BigANN](#bigann-recall-rankings)|[MSTuring](#msturing-recall-rankings)|[MSSpace](#msspace-recall-rankings)|[Text2Image](#text2image-recall-rankings)|[FBSSNet](#fbsimsearchnet-ap-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|-------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |eval|**0.226**|[0.99544](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_deep-1B_recall.png) |[0.99882](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_bigann-1B_recall.png) |[0.99054](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_msturing-1B_recall.png)   |-  |[0.63732](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_text2image-1B_recall.png)     |-  |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |eval|**0.089**|[0.99872](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_deep-1B_recall.png) |[0.99977](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_bigann-1B_recall.png) |[0.90255](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_msturing-1B_recall.png)   |-  |[0.58449](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_text2image-1B_recall.png)     |-  |
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |eval|**baseline**|[0.94437](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_deep-1B_recall.png) |[0.93604](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_bigann-1B_recall.png) |[0.91513](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_msturing-1B_recall.png)   |-  |[0.60105](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_text2image-1B_recall.png)     |[0.98567](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_ssnpp-1B_recall.png)  |
|   4|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-  |
|   5|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-  |
|   6|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-  |

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

#### Throughput Rankings

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-throughput-rankings)|[BigANN](#bigann-throughput-rankings)|[MSTuring](#msturing-throughput-rankings)|[MSSpace](#msspace-throughput-rankings)|[Text2Image](#text2image-throughput-rankings)|[FBSSNet](#fbsimsearchnet-throughput-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |eval|**669936**|[210,326](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_deep-1B_throughput.png) |[346,886](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_bigann-1B_throughput.png) |[123,695](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_msturing-1B_throughput.png)   |-  |[1,921](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_text2image-1B_throughput.png)     |-         |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |eval|**292753**|[95,386](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_deep-1B_throughput.png) |[86,004](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_bigann-1B_throughput.png) |[103,361](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_msturing-1B_throughput.png)   |-  |[20,894](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_text2image-1B_throughput.png)     |-         | 
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |eval|**baseline**|[5,035](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_deep-1B_throughput.png) |[3,279](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_bigann-1B_throughput.png) |[2,630](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_msturing-1B_throughput.png)   |-  |[1,948](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_text2image-1B_throughput.png)     |[6,256](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_ssnpp-1B_throughput.png)         | 
|   4|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         | 
|   5|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         | 
|   6|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         | 

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

#### Power Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-power-rankings)|[BigANN](#bigann-power-rankings)|[MSTuring](#msturing-power-rankings)|[MSSpace](#msspace-power-rankings)|[Text2Image](#text2image-power-rankings)|[FBSSNet](#fbsimsearchnet-power-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|-----|-----|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|NVidia|NVidia GPU |eval|**-0.536**|[0.0021](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_deep-1B_power.png) |[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_bigann-1B_power.png) |[0.0020](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_msturing-1B_power.png)   |-  |[0.0083](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_text2image-1B_power.png)|-|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|Intel|Intel Optane |eval|**-0.148**|[0.0036](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_deep-1B_power.png) |[0.0021](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_bigann-1B_power.png) |[0.0060](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_msturing-1B_power.png)   |-  |[0.3910](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_text2image-1B_power.png)|-| 
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |eval|**baseline**|[0.0923](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_deep-1B_power.png) |[0.1623](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_bigann-1B_power.png) |[0.1874](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_msturing-1B_power.png)   |-  |[0.1091](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_text2image-1B_power.png)|[0.0847](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_ssnpp-1B_power.png)| 
|   4|[-](-)|-|- |-|**-**|- |- |-   |-  |-|-| 
|   5|[-](-)|-|- |-|**-**|- |- |-   |-  |-|-| 
|   6|[-](-)|-|- |-|**-**|- |- |-   |-  |-|-| 

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

#### Cost Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-cost-rankings)|[BigANN](#bigann-cost-rankings)|[MSTuring](#msturing-cost-rankings)|[MSSpace](#msspace-cost-rankings)|[Text2Image](#text2image-cost-rankings)|[FBSSNet](#fbsimsearchnet-cost-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |eval|**$-2,357,906.86**|$15,939.55 |$15,388.38 |$16,776.08   |-  |$914,205.48     |-         |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |eval|**$-1,815,084.29\*\***|$300,721.93 |$300,793.63 |$150,691.36   |-  |$752,925.15     |-         |
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |eval|**baseline**|$472,764.09 |$739,552.84 |$924,531.60   |-  |$1,183,367.83     |$382,013.99         |
|   4|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |
|   5|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |
|   6|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

### Rankings Per Database

#### Deep1B

##### Deep1B Recall Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[0.99872](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_deep-1B_recall.png)**|       
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[0.99544](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_deep-1B_recall.png)**|       
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.94437](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_deep-1B_recall.png)**|       
|   4|[-](-)                                   |-                      |-               |-|**-**|       
|   5|[-](-)                                   |-                      |-               |-|**-**|       
|   6|[-](-)                                   |-                      |-               |-|**-**|       

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### Deep1B Throughput Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S        |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[210,326](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_deep-1B_throughput.png)**|
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[95,386](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_deep-1B_throughput.png)**|
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[5,035](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_deep-1B_throughput.png)**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### Deep1B Power Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[0.0021](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_deep-1B_power.png)**|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[0.0036](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_deep-1B_power.png)**|
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.0923](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_deep-1B_power.png)**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### Deep1B Cost Rankings 

|Rank|Submission          |Team     |Hardware               |Status  |Cost         |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|---------|-----------------------|--------|-------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel |Intel Optane               |eval|**$15,939.55**  |$14,664.20|$1,275.35|$14,664.20 |1      |12,753.499|
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia |NVidia GPU               |eval|**$300,721.93\*\***  |$300,000.00|$721.93|$150,000.00 |2      |7,219.311|
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*) |NVidia GPU               |eval|**$472,764.09**  |$440,438.00|$32,326.09|$22,021.90 |20      |323,260.873|
|   4|[-](-)|- |-               |-|**-**  |-|-|- |-      |-|
|   5|[-](-)|- |-               |-|**-**  |-|-|- |-      |-|
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
  * *final* = final submission
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### BigANN

##### BigANN Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[0.99977](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_bigann-1B_recall.png)**  |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[0.99882](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_bigann-1B_recall.png)**  |
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.93604](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_bigann-1B_recall.png)**  |
|   4|[-](-)                                   |-                      |-               |-|**-**  |
|   5|[-](-)                                   |-                      |-               |-|**-**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### BigANN Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[346,886](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_bigann-1B_throughput.png)**  |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[86,004](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_bigann-1B_throughput.png)**  |
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[3,279](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_bigann-1B_throughput.png)**  |
|   4|[-](-)                                   |-                      |-               |-|**-**  |
|   5|[-](-)                                   |-                      |-               |-|**-**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### BigANN Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[0.0021](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_bigann-1B_power.png)**|       
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_bigann-1B_power.png)**|       
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.1623](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_bigann-1B_power.png)**|      
|   4|[-](-)                                   |-                      |-               |-|**-**|      
|   5|[-](-)                                   |-                      |-               |-|**-**|      
|   6|[-](-)                                   |-                      |-               |-|**-**|      

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### BigANN Cost Rankings

|Rank|Submission          |Team                          |Hardware            |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|------------------------------|--------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel                      |Intel Optane            |eval|**$15,388.38**   |$14,664.20|$724.18|$14,664.20 |1      |7,241.818|
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia                      |NVidia GPU            |eval|**$300,793.63\*\***   |$300,000.00|$793.63|$150,000.00 |2      |7,936.286|      
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU            |eval|**$739,552.84**   |$682,678.90|$56,873.94|$22,021.90 |31      |568,739.415|  
|   4|[-](-)|-                      |-            |-|**-**   |-|-|- |-      |-|  
|   5|[-](-)|-                      |-            |-|**-**   |-|-|- |-      |-|  
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
  * *final* = final submission
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### MSTuring

##### MSTuring Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10           |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[0.99054](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_msturing-1B_recall.png)**    |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.91513](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_msturing-1B_recall.png)**    |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[0.90255](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_msturing-1B_recall.png)**    |
|   4|[-](-)                                   |-                      |-               |-|**-**    |
|   5|[-](-)                                   |-                      |-               |-|**-**    |
|   6|[-](-)                                   |-                      |-               |-|**-**    |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### MSTuring Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[123,695](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_msturing-1B_throughput.png)** |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[103,361](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_msturing-1B_throughput.png)** |
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[2,630](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_msturing-1B_throughput.png)** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### MSTuring Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q         |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[0.0020](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_msturing-1B_power.png)** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[0.0060](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_msturing-1B_power.png)** |
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.1874](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_msturing-1B_power.png)** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### MSTuring Cost Rankings

|Rank|Submission                          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|------------------------------------|------------------------------|-----------------------|--------|--------------|--------|--------|---------|--------------|----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                |Intel                      |Intel Optane               |eval|**$16,776.08**   |$14,664.20|$2,111.88|$14,664.20 |1      |21,118.824 |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                |NVidia                      |NVidia GPU               |eval|**$150,691.36\*\***   |$150,000.00|$691.36|$150,000.00 |1      |6,913.596 |         
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                |Facebook Research(*org*)                      |NVidia GPU               |eval|**$924,531.60**   |$858,854.10|$65,677.50|$22,021.90 |39      |656,775.000 |       
|   4|[-](-)                |-                      |-               |-|**-**   |-|-|- |-      |- |       
|   5|[-](-)                |-                      |-               |-|**-**   |-|-|- |-      |- |       
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
  * *final* = final submission
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### MSSpace

##### MSSpace Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10     |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------|
|   1|[$MS1R_SB]($MS1R_RD)                                   |$MS1R_TM                      |$MS1R_HW               |$MS1R_ST|**$MS1R_V** |
|   2|[$MS2R_SB]($MS2R_RD)                                   |$MS2R_TM                      |$MS2R_HW               |$MS2R_ST|**$MS2R_V** |
|   3|[$MS3R_SB]($MS3R_RD)                                   |$MS3R_TM                      |$MS3R_HW               |$MS3R_ST|**$MS3R_V** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### MSSpace Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[$MS1Q_SB]($MS1Q_RD)                                   |$MS1Q_TM                      |$MS1Q_HW               |$MS1Q_ST|**$MS1Q_V** |
|   2|[$MS2Q_SB]($MS2Q_RD)                                   |$MS2Q_TM                      |$MS2Q_HW               |$MS2Q_ST|**$MS2Q_V** |
|   3|[$MS3Q_SB]($MS3Q_RD)                                   |$MS3Q_TM                      |$MS3Q_HW               |$MS3Q_ST|**$MS3Q_V** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### MSSpace Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[$MS1P_SB]($MS1P_RD)                                   |$MS1P_TM                      |$MS1P_HW               |$MS1P_ST|**$MS1P_V** |
|   2|[$MS2P_SB]($MS2P_RD)                                   |$MS2P_TM                      |$MS2P_HW               |$MS2P_ST|**$MS2P_V** |
|   3|[$MS3P_SB]($MS3P_RD)                                   |$MS3P_TM                      |$MS3P_HW               |$MS3P_ST|**$MS3P_V** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### MSSpace Cost Rankings

|Rank|Submission          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|--------------------|------------------------------|-----------------------|------- |--------------|--------|--------|---------|--------------|----------|
|   1|[$MS1C_SB]($MS1C_RD)|$MS1C_TM                      |$MS1C_HW               |$MS1C_ST|**$MS1C_V**   |$MS1C_CX|$MS1C_OX|$MS1C_UC |$MS1C_UN      |$MS1C_KWT |
|   2|[$MS2C_SB]($MS2C_RD)|$MS2C_TM                      |$MS2C_HW               |$MS2C_ST|**$MS2C_V**   |$MS2C_CX|$MS2C_OX|$MS2C_UC |$MS2C_UN      |$MS2C_KWT |
|   3|[$MS3C_SB]($MS3C_RD)|$MS3C_TM                      |$MS3C_HW               |$MS3C_ST|**$MS3C_V**   |$MS3C_CX|$MS3C_OX|$MS3C_UC |$MS3C_UN      |$MS3C_KWT |
|   4|[-](-)|-                      |-               |-|**-**   |-|-|- |-      |- |
|   5|[-](-)|-                      |-               |-|**-**   |-|-|- |-      |- |
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
  * *final* = final submission
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### Text2Image

##### Text2Image Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[0.63732](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_text2image-1B_recall.png)**  |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.60105](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_text2image-1B_recall.png)**  |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[0.58449](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_text2image-1B_recall.png)**  |
|   4|[-](-)                                   |-                      |-               |-|**-**  |
|   5|[-](-)                                   |-                      |-               |-|**-**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### Text2Image Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[20,894](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_text2image-1B_throughput.png)** |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[1,948](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_text2image-1B_throughput.png)** |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[1,921](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_text2image-1B_throughput.png)** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.860 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.860 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### Text2Image Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |eval|**[0.0083](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/private_text2image-1B_power.png)**|
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.1091](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_text2image-1B_power.png)**|
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |eval|**[0.3910](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/optanne_graphann/private_text2image-1B_power.png)**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.86 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### Text2Image Cost Rankings

|Rank|Submission           |Team                          |Hardware             |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|---------------------|------------------------------|---------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md) |NVidia                      |NVidia GPU             |eval|**$752,925.15\*\***   |$750,000.00|$2,925.15|$150,000.00 |5      |29,251.505|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md) |Intel                      |Intel Optane             |eval|**$914,205.48**   |$777,202.60|$137,002.88|$14,664.20 |53      |1,370,028.787| 
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md) |Facebook Research(*org*)                      |NVidia GPU             |eval|**$1,183,367.83**   |$1,145,138.80|$38,229.03|$22,021.90 |52      |382,290.263| 
|   4|[-](-) |-                      |-             |-|**-**   |-|-|- |-      |-| 
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
  * *final* = final submission
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### FBSimSearchNet

##### FBSimSearchNet AP Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |AP          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.98567](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_ssnpp-1B_recall.png)**  |
|   2|[-](-)                                   |-                      |-               |-|**-**  |
|   3|[-](-)                                   |-                      |-               |-|**-**  |
|   4|[-](-)                                   |-                      |-               |-|**-**  |
|   5|[-](-)                                   |-                      |-               |-|**-**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### FBSimSearchNet Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[6,256](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_ssnpp-1B_throughput.png)** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 average precision.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission


##### FBSimSearchNet Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |eval|**[0.0847](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/faiss_t3/private_ssnpp-1B_power.png)**|
|   2|[-](-)                                   |-                      |-               |-|**-**|
|   3|[-](-)                                   |-                      |-               |-|**-**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 average precision.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission

##### FBSimSearchNet Cost Rankings

|Rank|Submission          |Team                          |Hardware             |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|------------------------------|---------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)                      |NVidia GPU             |eval|**$382,013.99**   |$352,350.40|$29,663.59|$22,021.90 |16      |296,635.913|
|   2|[-](-)|-                      |-             |-|**-**   |-|-|- |-      |-|
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
  * *final* = final submission
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.
