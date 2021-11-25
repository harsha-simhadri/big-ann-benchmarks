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
|[$MSD_SB]($MSD_RD)  |$MSD_TM    |$MSD_HW   |inprog |$MSD_EV  |$MSD_AL  |$MSD_AN |$MSD_RR  |$MSD_QR       |$MSD_PR                      |$MSD_CR                    |
|[$BS_SB]($BS_RD)    |$BS_TM     |$BS_HW    |$BS_S  |$BS_EV   |$BS_AL   |$BS_AN  |$BS_RR   |$BS_QR        |$BS_PR                       |$BS_CR                     |
|[$GEM_SB]($GEM_RD)  |$GEM_TM    |$GEM_HW   |$GEM_S |$GEM_EV  |$GEM_AL  |$GEM_AN |$GEM_RR  |$GEM_QR       |$GEM_PR                      |$GEM_CR                    |
|kanndi              |Silo.ai    |$GEM_HW   |inprog |        -|        -|       -|        -|             -|                            -|                          -|
|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)  |NVidia    |NVidia GPU   |inprog |George Williams  |[src](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/benchmark/algorithms/cuanns_ivfpq.py)  |[nb](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/EvalPublic.ipynb) |[1](#recall-or-ap-rankings)  |[1](#throughput-rankings)       |[1](#power-rankings)                      |*NQ*                    |
|[$NV_SB]($NV_RD)    |$NV_TM     |$NV_HW    |$NV_S  |$NV_EV   |$NV_AL   |$NV_AN  |$NV_RR   |$NV_QR        |$NV_PR                       |$NV_CR                     |
|[$OPT1_SB]($OPT1_RD)|$OPT1_TM   |$OPT1_HW  |$OPT1_S|$OPT1_EV |$OPT1_AL |$OPT1_AN|$OPT1_RR |$OPT1_QR      |$OPT1_PR                     |$OPT1_CR                   |
|optanne_graphann_2  |$OPT1_TM   |$OPT1_HW  |inprog |        -|        -|       -|        -|             -|                            -|                          -|
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**0.373**|[0.99542](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_recall.png) |[0.99882](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_recall.png) |[0.98993](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_recall.png)   |[0.99428](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_recall.png)  |[0.94136](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_recall.png)     |-  |
|   2|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-  |
|   3|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-  |
|   4|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-  |
|   5|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-  |
|   6|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-  |
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**397623.802**|[97,268.471](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_throughput.png) |[84,367.141](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_throughput.png) |[111,580.136](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_throughput.png)   |[109,555.059](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_throughput.png)  |[9,249.383](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_throughput.png)     |-         |
|   2|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         | 
|   3|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         | 
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

#### Power Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-power-rankings)|[BigANN](#bigann-power-rankings)|[MSTuring](#msturing-power-rankings)|[MSSpace](#msspace-power-rankings)|[Text2Image](#text2image-power-rankings)|[FBSSNet](#fbsimsearchnet-power-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|-----|-----|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)|NVidia|NVidia GPU |inprog|**-0.744**|[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_power.png) |[0.0024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_power.png) |[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_power.png)   |[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_power.png)  |[0.0222](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_power.png)|-|
|   2|[-](-)|-|- |-|**-**|- |- |-   |-  |-|-| 
|   3|[-](-)|-|- |-|**-**|- |- |-   |-  |-|-| 
|   4|[-](-)|-|- |-|**-**|- |- |-   |-  |-|-| 
|   5|[-](-)|-|- |-|**-**|- |- |-   |-  |-|-| 
|   6|[-](-)|-|- |-|**-**|- |- |-   |-  |-|-| 
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
|   1|[$CR1_SB]($CR1_RD)|$CR1_TM|$CR1_HW |$CR1_ST|**$CR1_SC**|$DPC1 |$BAC1 |$MTC1   |$MSC1  |$TIC1     |$FBC1         |
|   2|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |
|   3|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99542](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_recall.png)**|       
|   2|[-](-)                                   |-                      |-               |-|**-**|       
|   3|[-](-)                                   |-                      |-               |-|**-**|       
|   4|[-](-)                                   |-                      |-               |-|**-**|       
|   5|[-](-)                                   |-                      |-               |-|**-**|       
|   6|[-](-)                                   |-                      |-               |-|**-**|       
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[97,268.471](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_throughput.png)**|
|   2|[-](-)                                   |-                      |-               |-|**-**|
|   3|[-](-)                                   |-                      |-               |-|**-**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
|   6|[-](-)                                   |-                      |-               |-|**-**|
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0023](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/deep-1B_power.png)**|
|   2|[-](-)                                   |-                      |-               |-|**-**|
|   3|[-](-)                                   |-                      |-               |-|**-**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|[-](-)                                   |-                      |-               |-|**-**|
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
|   1|[$DP1C_SB]($DP1C_RD)|$DP1C_TM |$DP1C_HW               |$DP1C_ST|**$DP1C_V**  |$DP1C_CX|$DP1C_OX|$DP1C_UC |$DP1C_UN      |$DP1C_KWT|
|   2|[-](-)|- |-               |-|**-**  |-|-|- |-      |-|
|   3|[-](-)|- |-               |-|**-**  |-|-|- |-      |-|
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.99882](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_recall.png)**  |
|   2|[-](-)                                   |-                      |-               |-|**-**  |
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

##### BigANN Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[84,367.141](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_throughput.png)**  |
|   2|[-](-)                                   |-                      |-               |-|**-**  |
|   3|[-](-)                                   |-                      |-               |-|**-**  |
|   4|[-](-)                                   |-                      |-               |-|**-**  |
|   5|[-](-)                                   |-                      |-               |-|**-**  |
|   6|[-](-)                                   |-                      |-               |-|**-**  |
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0024](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/bigann-1B_power.png)**|       
|   2|[-](-)                                   |-                      |-               |-|**-**|       
|   3|[-](-)                                   |-                      |-               |-|**-**|      
|   4|[-](-)                                   |-                      |-               |-|**-**|      
|   5|[-](-)                                   |-                      |-               |-|**-**|      
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
|   1|[$BA1C_SB]($BA1C_RD)|$BA1C_TM                      |$BA1C_HW            |$BA1C_ST|**$BA1C_V**   |$BA1C_CX|$BA1C_OX|$BA1C_UC |$BA1C_UN      |$BA1C_KWT|
|   2|[-](-)|-                      |-            |-|**-**   |-|-|- |-      |-|      
|   3|[-](-)|-                      |-            |-|**-**   |-|-|- |-      |-|  
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.98993](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_recall.png)**    |
|   2|[-](-)                                   |-                      |-               |-|**-**    |
|   3|[-](-)                                   |-                      |-               |-|**-**    |
|   4|[-](-)                                   |-                      |-               |-|**-**    |
|   5|[-](-)                                   |-                      |-               |-|**-**    |
|   6|[-](-)                                   |-                      |-               |-|**-**    |
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[111,580.136](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_throughput.png)** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msturing-1B_power.png)** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
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
|   1|[$MT1C_SB]($MT1C_RD)                |$MT1C_TM                      |$MT1C_HW               |$MT1C_ST|**$MT1C_V**   |$MT1C_CX|$MT1C_OX|$MT1C_UC |$MT1C_UN      |$MT1C_KWT |
|   2|[-](-)                |-                      |-               |-|**-**   |-|-|- |-      |- |         
|   3|[-](-)                |-                      |-               |-|**-**   |-|-|- |-      |- |       
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_power.png)** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[109,555.059](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_throughput.png)** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
|   6|[-](-)                                   |-                      |-               |-|**-** |
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.0017](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/msspacev-1B_power.png)** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
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
|   1|[$MS1C_SB]($MS1C_RD)|$MS1C_TM                      |$MS1C_HW               |$MS1C_ST|**$MS1C_V**   |$MS1C_CX|$MS1C_OX|$MS1C_UC |$MS1C_UN      |$MS1C_KWT |
|   2|[-](-)|-                      |-               |-|**-**   |-|-|- |-      |- |
|   3|[-](-)|-                      |-               |-|**-**   |-|-|- |-      |- |
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
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[0.94136](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_recall.png)**  |
|   2|[-](-)                                   |-                      |-               |-|**-**  |
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

##### Text2Image Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[cuanns_ivfpq](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/cuanns_ivfpq/README.md)                                   |NVidia                      |NVidia GPU               |inprog|**[9,249.383](https://github.com/harsha-simhadri/big-ann-benchmarks/blob/gw/T3/t3/eval_2021/cuanns_ivfpq/text2image-1B_throughput.png)** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|[-](-)                                   |-                      |-               |-|**-** |
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
|   2|[-](-)                                   |-                      |-               |-|**-**|
|   3|[-](-)                                   |-                      |-               |-|**-**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
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
|   1|[$TI1C_SB]($TI1C_RD) |$TI1C_TM                      |$TI1C_HW             |$TI1C_ST|**$TI1C_V**   |$TI1C_CX|$TI1C_OX|$TI1C_UC |$TI1C_UN      |$TI1C_KWT|
|   2|[-](-) |-                      |-             |-|**-**   |-|-|- |-      |-| 
|   3|[-](-) |-                      |-             |-|**-**   |-|-|- |-      |-| 
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
|   1|[$FB1R_SB]($FB1R_RD)                                   |$FB1R_TM                      |$FB1R_HW               |$FB1R_ST|**$FB1R_V**  |
|   2|[-](-)                                   |-                      |-               |-|**-**  |
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
|   1|[$FB1Q_SB]($FB1Q_RD)                                   |$FB1Q_TM                      |$FB1Q_HW               |$FB1Q_ST|**$FB1Q_V** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
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
|   1|[$FB1P_SB]($FB1P_RD)                                   |$FB1P_TM                      |$FB1P_HW               |$FB1P_ST|**$FB1P_V**|
|   2|[-](-)                                   |-                      |-               |-|**-**|
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
|   1|[$FB1C_SB]($FB1C_RD)|$FB1C_TM                      |$FB1C_HW             |$FB1C_ST|**$FB1C_V**   |$FB1C_CX|$FB1C_OX|$FB1C_UC |$FB1C_UN      |$FB1C_KWT|
|   2|[-](-)|-                      |-             |-|**-**   |       -|       -|        -|             -|        -|       
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

