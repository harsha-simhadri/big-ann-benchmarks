# T3 Track Leaderboards After Rejecting Anomalies (Unofficial)

Please note that all rankings are currently unofficial due to the following reasons:
* All [open tasks and issues](TASKS_ISSUES_RESOLUTIONS.md) must be resolved.

## Final Rankings On Private Query Set

*Not yet available*
 
## Rankings On Public Query Set

### Rankings By Submission Name (alphabetical)

|Submission          |Team       |Hardware  |[Recall Rank](#recall-or-ap-rankings)|[Thru-put Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)|Status |Anomalies|Evaluator|Algo     |Runs   |  
|--------------------|-----------|----------|---------|---------|---------|--------|---------|---------|---------|---------|--------|
|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)  |Microsoft Research India(*org*)    |Dell PowerEdge   |[1](#recall-or-ap-rankings)  |[5](#throughput-rankings)  |*NQ*  |*NQ* |final   |*NA*  |Harsha Simhadri  |-  |- |
|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)    |Facebook Research(*org*)     |NVidia GPU    |[6](#recall-or-ap-rankings)   |[6](#throughput-rankings)   |[5](#power-rankings)   |[5](#cost-rankings)  |final    |0/58   |George Williams   |-   |-  |
|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)  |GSI Technology(*org*)    |LedaE APU   |[4](#recall-or-ap-rankings)  |[4](#throughput-rankings)  |[4](#power-rankings)  |[4](#cost-rankings) |final   |0/60  |George Williams  |-  |- |
|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)  |NVidia    |NVidia GPU   |[3](#recall-or-ap-rankings)  |[3](#throughput-rankings)  |[1](#power-rankings)  |[2](#cost-rankings)\*\* |final   |[5/50](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/ANOMALIES.md)  |George Williams  |-  |- |
|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)    |NVidia     |NVidia GPU    |[5](#recall-or-ap-rankings)   |[1](#throughput-rankings)   |[3](#power-rankings)   |[3](#cost-rankings)\*\*  |final    |[4/40](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/ANOMALIES.md)   |George Williams   |-   |-  |
|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel   |Intel Optane  |[2](#recall-or-ap-rankings) |[2](#throughput-rankings) |[2](#power-rankings) |[1](#cost-rankings)|final  |[5/50](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/ANOMALIES.md) |George Williams |- |-|

* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified
  * *NA* = data is not yet available, or has not yet been processed

* *Anomalies* are defined as queries that could potentially be the result of query response caching, a violation of the competition.  Our detection method looks for a 30% or more improvement in the batch query latency between the first and last query of a query group (5).  Participants have been given a chance to explain why detected anomalies (if any) are not a result of query response caching.  In general, our analysis did not uncover this symptom of systematic query response caching from any submission.  Also, if we throw out the anomalous data points, the adjusted leaderboard rankings (above) do not change even though some scores change slightly.

* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

### Rankings Per Metric

#### Recall Or AP Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-recall-rankings)|[BigANN](#bigann-recall-rankings)|[MSTuring](#msturing-recall-rankings)|[MSSpace](#msspace-recall-rankings)|[Text2Image](#text2image-recall-rankings)|[FBSSNet](#fbsimsearchnet-ap-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|-------|
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Microsoft Research India(*org*)|Dell PowerEdge |final|**0.410**|0.99821 |0.99976 |0.99444   |0.99342  |0.98130     |-  |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |final|**0.409**|0.99882 |0.99978 |0.99568   |0.99835  |0.97340     |-  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |final|**0.368**|0.99541 |0.99882 |0.98993   |0.99428  |0.94691     |-  |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |final|**0.339**|0.99208 |0.99328 |0.97841   |0.98622  |0.92855     |0.99684  |
|   5|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |final|**0.166**|0.95736 |0.96750 |0.96286   |0.97541  |-     |-  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|0.94275 |0.93260 |0.91322   |0.90853  |0.86028     |0.97863  |

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Throughput Rankings

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-throughput-rankings)|[BigANN](#bigann-throughput-rankings)|[MSTuring](#msturing-throughput-rankings)|[MSSpace](#msspace-throughput-rankings)|[Text2Image](#text2image-throughput-rankings)|[FBSSNet](#fbsimsearchnet-throughput-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |final|**3001624**|816,807 |767,653 |586,722   |844,287  |-     |-         |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |final|**851327**|196,546 |335,991 |161,463   |155,899  |17,063     |-         | 
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |final|**401541**|91,938 |85,446 |110,830   |109,621  |19,340     |-         | 
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |final|**52429**|10,704 |10,672 |21,780   |16,422  |4,838     |9,345         | 
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Microsoft Research India(*org*)|Dell PowerEdge |final|**49398**|12,927 |19,094 |17,201   |6,503  |9,307     |-         | 
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|4,464 |3,271 |2,845   |3,265  |1,789     |5,699         | 

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Power Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-power-rankings)|[BigANN](#bigann-power-rankings)|[MSTuring](#msturing-power-rankings)|[MSSpace](#msspace-power-rankings)|[Text2Image](#text2image-power-rankings)|[FBSSNet](#fbsimsearchnet-power-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|-----|-----|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |final|**-0.691**|0.0024 |0.0023 |0.0016   |0.0017  |0.0094|-|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |final|**-0.648**|0.0041 |0.0022 |0.0048   |0.0050  |0.0446|-| 
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |final|**-0.594**|0.0002 |0.0003 |0.0004   |0.0002  |-|-| 
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |final|**-0.513**|0.0337 |0.0341 |0.0236   |0.0230  |0.1242|0.0469| 
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|0.1117 |0.1576 |0.1743   |0.1520  |0.1128|0.0904| 
|   6|[-](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|-|- |-|**-**|- |- |-   |-  |-|-| 

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Cost Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-cost-rankings)|[BigANN](#bigann-cost-rankings)|[MSTuring](#msturing-cost-rankings)|[MSSpace](#msspace-cost-rankings)|[Text2Image](#text2image-cost-rankings)|[FBSSNet](#fbsimsearchnet-cost-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel|Intel Optane |final|**$-3,978,172.56**|$16,086.82 |$15,439.92 |$16,347.45   |$16,409.08  |$103,599.49     |-         |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |final|**$-2,339,919.09\*\***|$300,843.83 |$300,815.92 |$150,563.49   |$150,605.68  |$903,307.30     |-         |
|   3|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia|NVidia GPU |final|**$-2,272,942.67\*\***|$150,082.04 |$150,088.58 |$150,127.39   |$150,078.78  |-     |-         |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |final|**$-907,570.13**|$569,058.09 |$569,210.35 |$286,911.87   |$398,163.18  |$1,213,773.56     |$629,442.91         |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|$545,633.16 |$737,886.17 |$853,857.46   |$735,942.66  |$1,272,735.86     |$428,074.79         |
|   6|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

### Rankings Per Database

#### Deep1B

##### Deep1B Recall Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.99882**|       
|   2|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**0.99821**|       
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.99541**|       
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.99208**|       
|   5|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.95736**|       
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.94275**|       

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Throughput Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S        |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**816,807**|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**196,546**|
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**91,938**|
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**12,927**|
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**10,704**|
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**4,464**|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Power Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.0002**|
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.0024**|
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.0041**|
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.0337**|
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.1117**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Cost Rankings 

|Rank|Submission          |Team     |Hardware               |Status  |Cost         |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|---------|-----------------------|--------|-------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel |Intel Optane               |final|**$16,086.82**  |$14,664.20|$1,422.62|$14,664.20 |1      |14,226.208|
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia |NVidia GPU               |final|**$150,082.04\*\***  |$150,000.00|$82.04|$150,000.00 |1      |820.405|
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia |NVidia GPU               |final|**$300,843.83\*\***  |$300,000.00|$843.83|$150,000.00 |2      |8,438.315|
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
  * *final* = final submission
  * *inprog* = algorithm development still in progress
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### BigANN

##### BigANN Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.99978**  |
|   2|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**0.99976**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.99882**  |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.99328**  |
|   5|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.96750**  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.93260**  |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**767,653**  |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**335,991**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**85,446**  |
|   4|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**19,094**  |
|   5|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**10,672**  |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**3,271**  |

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.0003**|       
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.0022**|       
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.0023**|      
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.0341**|      
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.1576**|      
|   6|[-](-)                                   |-                      |-               |-|**-**|      

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Cost Rankings

|Rank|Submission          |Team                          |Hardware            |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|------------------------------|--------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel                      |Intel Optane            |final|**$15,439.92**   |$14,664.20|$775.72|$14,664.20 |1      |7,757.221|
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia                      |NVidia GPU            |final|**$150,088.58\*\***   |$150,000.00|$88.58|$150,000.00 |1      |885.770|      
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia                      |NVidia GPU            |final|**$300,815.92\*\***   |$300,000.00|$815.92|$150,000.00 |2      |8,159.226|  
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
  * *final* = final submission
  * *inprog* = algorithm development still in progress
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### MSTuring

##### MSTuring Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10           |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.99568**    |
|   2|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**0.99444**    |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.98993**    |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.97841**    |
|   5|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.96286**    |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.91322**    |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**586,722** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**161,463** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**110,830** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**21,780** |
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**17,201** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**2,845** |

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q         |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.0004** |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.0016** |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.0048** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.0236** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.1743** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Cost Rankings

|Rank|Submission                          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|------------------------------------|------------------------------|-----------------------|--------|--------------|--------|--------|---------|--------------|----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                |Intel                      |Intel Optane               |final|**$16,347.45**   |$14,664.20|$1,683.25|$14,664.20 |1      |16,832.451 |
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                |NVidia                      |NVidia GPU               |final|**$150,127.39\*\***   |$150,000.00|$127.39|$150,000.00 |1      |1,273.870 |         
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                |NVidia                      |NVidia GPU               |final|**$150,563.49\*\***   |$150,000.00|$563.49|$150,000.00 |1      |5,634.885 |       
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
  * *final* = final submission
  * *inprog* = algorithm development still in progress
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### MSSpace

##### MSSpace Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10     |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.99835** |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.99428** |
|   3|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**0.99342** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.98622** |
|   5|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.97541** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.90853** |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**844,287** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**155,899** |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**109,621** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**16,422** |
|   5|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**6,503** |
|   6|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**3,265** |

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.0002** |
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.0017** |
|   3|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.0050** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.0230** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.1520** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Cost Rankings

|Rank|Submission          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|--------------------|------------------------------|-----------------------|------- |--------------|--------|--------|---------|--------------|----------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)|Intel                      |Intel Optane               |final|**$16,409.08**   |$14,664.20|$1,744.88|$14,664.20 |1      |17,448.764 |
|   2|[cuanns_multigpu](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_multigpu/README.md)|NVidia                      |NVidia GPU               |final|**$150,078.78\*\***   |$150,000.00|$78.78|$150,000.00 |1      |787.774 |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia                      |NVidia GPU               |final|**$150,605.68\*\***   |$150,000.00|$605.68|$150,000.00 |1      |6,056.841 |
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
  * *final* = final submission
  * *inprog* = algorithm development still in progress
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### Text2Image

##### Text2Image Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**0.98130**  |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.97340**  |
|   3|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.94691**  |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.92855**  |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.86028**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**19,340** |
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**17,063** |
|   3|[diskann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/diskann-bare-metal/README.md)                                   |Microsoft Research India(*org*)                      |Dell PowerEdge               |final|**9,307** |
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**4,838** |
|   5|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**1,789** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.860 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.860 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |final|**0.0094**|
|   2|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md)                                   |Intel                      |Intel Optane               |final|**0.0446**|
|   3|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.1128**|
|   4|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.1242**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.86 recall@10.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Cost Rankings

|Rank|Submission           |Team                          |Hardware             |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|---------------------|------------------------------|---------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/optanne_graphann/README.md) |Intel                      |Intel Optane             |final|**$103,599.49**   |$87,985.20|$15,614.29|$14,664.20 |6      |156,142.873|
|   2|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md) |NVidia                      |NVidia GPU             |final|**$903,307.30\*\***   |$900,000.00|$3,307.30|$150,000.00 |6      |33,072.963| 
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
  * *final* = final submission
  * *inprog* = algorithm development still in progress
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.

#### FBSimSearchNet

##### FBSimSearchNet AP Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |AP          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.99684**  |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.97863**  |
|   3|[-](-)                                   |-                      |-               |-|**-**  |
|   4|[-](-)                                   |-                      |-               |-|**-**  |
|   5|[-](-)                                   |-                      |-               |-|**-**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### FBSimSearchNet Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**9,345** |
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**5,699** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 average precision.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress


##### FBSimSearchNet Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[gemini](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/gemini/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |final|**0.0469**|
|   2|[faiss_t3](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/faiss_t3/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |final|**0.0904**|
|   3|[-](-)                                   |-                      |-               |-|**-**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 average precision.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

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
  * *final* = final submission
  * *inprog* = algorithm development still in progress
* \*\*Nvidia has not yet approved the MSRP cost used for ranking, so participation in this benchmark is still pending.
