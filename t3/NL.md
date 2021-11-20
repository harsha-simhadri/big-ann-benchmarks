# T3 Track Leaderboards 

## Final Rankings On Private Query Set

*Available December 2021*
 
## Rankings On Public Query Set

### Rankings By Submission Name (alphabetical)

|Submission          |Team       |Hardware  |Status |[Recall Rank](#recall-rankings)|[Throughput Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)| 
|--------------------|-----------|----------|-------|-------------------------------|---------------------------------------|-----------------------------|---------------------------|
|deepgram            |DeepGram   |NVidia GPU|final  |                           *NQ*|                                   *NQ*|                         *NQ*|                       *NQ*|
|[diskann](../t3/diskann-bare-metal/README.md)  |Microsoft Research(*org*)    |Dell PowerEdge   |inprog |[1](#recall-rankings)                        |[2](#throughput-rankings)                                |*NQ*                      |*NQ*                    |
|[faiss_t3](../t3/faiss_t3/README.md)    |Facebook Research(*org*)     |NVidia GPU    |final  |[4](#recall-rankings)                         |[4](#throughput-rankings)                                 |[3](#power-rankings)                       |[2](#cost-rankings)                     |
|[gemini](../t3/gemini/README.md)  |GSI Technology(*org*)    |LedaE APU   |inprog |[2](#recall-rankings)                        |[3](#throughput-rankings)                                |[2](#power-rankings)                      |[3](#cost-rankings)                    |
|kanndi              |Silo.ai    |LedaE APU   |inprog |                              -|                                      -|                            -|                          -|
|nvidia_single_gpu   |NVidia     |NVidia GPU|inprog |                              -|                                      -|                            -|                          -|
|nvidia_multi_gpu    |NVidia     |NVidia GPU|inprog |                              -|                                      -|                            -|                          -|
|[optanne_graphann](../t3/optanne_graphann/README.md)|Intel   |Intel Optane  |inprog|[3](#recall-rankings)                       |[1](#throughput-rankings)                               |[1](#power-rankings)                     |[1](#cost-rankings)                   |
|optanne_graphann_2  |Intel   |Intel Optane  |inprog |                              -|                                      -|                            -|                          -|
|vector_t3           |Vector Inst|NVidia GPU|final  |                           *NQ*|                                   *NQ*|                         *NQ*|                       *NQ*|



* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

### Rankings Per Metric

#### Recall Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-recall-rankings)|[BigANN](#bigann-recall-rankings)|[MSTuring](#msturing-recall-rankings)|[MSSpace](#msspace-recall-rankings)|[Text2Image](#text2image-recall-rankings)|[FBSSNet](#fbsimsearchnet-recall-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|-------|
|   1|[diskann](../t3/diskann-bare-metal/README.md)|Microsoft Research(*org*)|Dell PowerEdge |inprog|**0.420**|[0.99821](eval_2021/diskann-bare-metal/deep-1B_recall.png) |[0.99976](eval_2021/diskann-bare-metal/bigann-1B_recall.png) |[0.99444](eval_2021/diskann-bare-metal/msturing-1B_recall.png)   |[0.99342](eval_2021/diskann-bare-metal/msspacev-1B_recall.png)  |[0.98130](eval_2021/diskann-bare-metal/text2image-1B_recall.png)     |-  |
|   2|[gemini](../t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**0.280**|[0.98871](eval_2021/gemini/deep-1B_recall.png) |[0.99253](eval_2021/gemini/bigann-1B_recall.png) |[0.97841](eval_2021/gemini/msturing-1B_recall.png)   |[0.98622](eval_2021/gemini/msspacev-1B_recall.png)  |[0.88163](eval_2021/gemini/text2image-1B_recall.png)     |-  |
|   3|[optanne_graphann](../t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**0.279**|[0.98264](eval_2021/optanne_graphann/deep-1B_recall.png) |[0.99084](eval_2021/optanne_graphann/bigann-1B_recall.png) |[0.96218](eval_2021/optanne_graphann/msturing-1B_recall.png)   |[0.98791](eval_2021/optanne_graphann/msspacev-1B_recall.png)  |[0.90277](eval_2021/optanne_graphann/text2image-1B_recall.png)     |-  |
|   4|[faiss_t3](../t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[0.94275](eval_2021/faiss_t3/deep-1B_recall.png) |[0.92671](eval_2021/faiss_t3/bigann-1B_recall.png) |[0.90900](eval_2021/faiss_t3/msturing-1B_recall.png)   |[0.90853](eval_2021/faiss_t3/msspacev-1B_recall.png)  |[0.86028](eval_2021/faiss_t3/text2image-1B_recall.png)     |[0.97863](eval_2021/faiss_t3/ssnpp-1B_recall.png)  |
|   5|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|   
|   6|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|
|   7|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|
|   8|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|
|   9|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|
|  10|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|      -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Throughput Rankings

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-throughput-rankings)|[BigANN](#bigann-throughput-rankings)|[MSTuring](#msturing-throughput-rankings)|[MSSpace](#msspace-throughput-rankings)|[Text2Image](#text2image-throughput-rankings)|[FBSSNet](#fbsimsearchnet-throughput-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**821550.201**|[184,490.708](eval_2021/optanne_graphann/deep-1B_throughput.png) |[343,727.791](eval_2021/optanne_graphann/bigann-1B_throughput.png) |[157,277.710](eval_2021/optanne_graphann/msturing-1B_throughput.png)   |[139,612.021](eval_2021/optanne_graphann/msspacev-1B_throughput.png)  |[10,838.358](eval_2021/optanne_graphann/text2image-1B_throughput.png)     |-         |
|   2|[diskann](../t3/diskann-bare-metal/README.md)|Microsoft Research(*org*)|Dell PowerEdge |inprog|**50635.296**|[12,926.890](eval_2021/diskann-bare-metal/deep-1B_throughput.png) |[19,094.371](eval_2021/diskann-bare-metal/bigann-1B_throughput.png) |[17,200.601](eval_2021/diskann-bare-metal/msturing-1B_throughput.png)   |[6,503.212](eval_2021/diskann-bare-metal/msspacev-1B_throughput.png)  |[9,306.610](eval_2021/diskann-bare-metal/text2image-1B_throughput.png)     |-         | 
|   3|[gemini](../t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**34209.040**|[9,150.271](eval_2021/gemini/deep-1B_throughput.png) |[9,504.865](eval_2021/gemini/bigann-1B_throughput.png) |[20,166.678](eval_2021/gemini/msturing-1B_throughput.png)   |[8,587.024](eval_2021/gemini/msspacev-1B_throughput.png)  |[1,196.589](eval_2021/gemini/text2image-1B_throughput.png)     |-         | 
|   4|[faiss_t3](../t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[4,417.036](eval_2021/faiss_t3/deep-1B_throughput.png) |[3,086.656](eval_2021/faiss_t3/bigann-1B_throughput.png) |[2,359.485](eval_2021/faiss_t3/msturing-1B_throughput.png)   |[2,770.848](eval_2021/faiss_t3/msspacev-1B_throughput.png)  |[1,762.363](eval_2021/faiss_t3/text2image-1B_throughput.png)     |[5,572.272](eval_2021/faiss_t3/ssnpp-1B_throughput.png)         | 
|   5|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   6|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   7|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   8|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   9|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|  10|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Power Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-power-rankings)|[BigANN](#bigann-power-rankings)|[MSTuring](#msturing-power-rankings)|[MSSpace](#msspace-power-rankings)|[Text2Image](#text2image-power-rankings)|[FBSSNet](#fbsimsearchnet-power-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|-----|-----|
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**-0.687**|[0.004](eval_2021/optanne_graphann/deep-1B_power.png) |[0.002](eval_2021/optanne_graphann/bigann-1B_power.png) |[0.005](eval_2021/optanne_graphann/msturing-1B_power.png)   |[0.005](eval_2021/optanne_graphann/msspacev-1B_power.png)  |[0.070](eval_2021/optanne_graphann/text2image-1B_power.png)|-|
|   2|[gemini](../t3/diskann-bare-metal/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**-0.121**|[0.040](eval_2021/gemini/deep-1B_power.png) |[0.039](eval_2021/gemini/bigann-1B_power.png) |[0.023](eval_2021/gemini/msturing-1B_power.png)   |[0.048](eval_2021/gemini/msspacev-1B_power.png)  |[0.503](eval_2021/gemini/text2image-1B_power.png)|-| 
|   3|[faiss_t3](../t3/gemini/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|[0.113](eval_2021/faiss_t3/deep-1B_power.png) |[0.167](eval_2021/faiss_t3/bigann-1B_power.png) |[0.204](eval_2021/faiss_t3/msturing-1B_power.png)   |[0.167](eval_2021/faiss_t3/msspacev-1B_power.png)  |[0.123](eval_2021/faiss_t3/text2image-1B_power.png)|[0.095](eval_2021/faiss_t3/ssnpp-1B_power.png)| 
|   4|[-](../t3/faiss_t3/README.md)|-|- |-|**-**|- |- |-   |-  |-|-| 
|   5|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|
|   6|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|
|   7|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|
|   8|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|
|   9|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|
|  10|                 -|      -|       -|      -|          -|     -|     -|       -|      -|    -|    -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Cost Rankings 

|Rank|Submission        |Team   |Hardware|Status |Score      |[Deep1B](#deep1B-cost-rankings)|[BigANN](#bigann-cost-rankings)|[MSTuring](#msturing-cost-rankings)|[MSSpace](#msspace-cost-rankings)|[Text2Image](#text2image-cost-rankings)|[FBSSNet](#fbsimsearchnet-cost-rankings)|
|----|------------------|-------|--------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)|Intel|Intel Optane |inprog|**$-4,285,768.44**|$16,082.49 |$15,407.15 |$16,397.80   |$16,563.61  |$171,244.96     |-         |
|   2|[faiss_t3](../t3/faiss_t3/README.md)|Facebook Research(*org*)|NVidia GPU |final|**baseline**|$545,952.10 |$785,282.45 |$1,018,332.30   |$873,460.84  |$1,298,436.77     |$429,634.84         |
|   3|[gemini](../t3/gemini/README.md)|GSI Technology(*org*)|LedaE APU |inprog|**$2,561,786.18**|$626,932.94 |$626,785.91 |$286,578.81   |$685,704.76  |$4,857,248.23     |-         |
|   4|[-](-)|-|- |-|**-**|- |- |-   |-  |-     |-         |
|   5|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   6|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   7|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   8|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|   9|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|
|  10|                 -|      -|       -|      -|          -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

### Rankings Per Database

#### Deep1B

##### Deep1B Recall Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[diskann](../t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[0.99821](eval_2021/diskann-bare-metal/deep-1B_recall.png)**|       
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.98871](eval_2021/gemini/deep-1B_recall.png)**|       
|   3|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.98264](eval_2021/optanne_graphann/deep-1B_recall.png)**|       
|   4|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.94275](eval_2021/faiss_t3/deep-1B_recall.png)**|       
|   5|                                                      -|                             -|                      -|       -|          -|       
|   6|                                                      -|                             -|                      -|       -|          -|       
|   7|                                                      -|                             -|                      -|       -|          -|       
|   8|                                                      -|                             -|                      -|       -|          -|       
|   9|                                                      -|                             -|                      -|       -|          -|       
|  10|                                                      -|                             -|                      -|       -|          -|       

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Throughput Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S        |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[184,490.708](eval_2021/optanne_graphann/deep-1B_throughput.png)**|
|   2|[diskann](../t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[12,926.890](eval_2021/diskann-bare-metal/deep-1B_throughput.png)**|
|   3|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[9,150.271](eval_2021/gemini/deep-1B_throughput.png)**|
|   4|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[4,417.036](eval_2021/faiss_t3/deep-1B_throughput.png)**|
|   3|                                                      -|                             -|                      -|       -|          -|    
|   4|                                                      -|                             -|                      -|       -|          -|    
|   5|                                                      -|                             -|                      -|       -|          -|    
|   6|                                                      -|                             -|                      -|       -|          -|    
|   7|                                                      -|                             -|                      -|       -|          -|    
|   8|                                                      -|                             -|                      -|       -|          -|    
|   9|                                                      -|                             -|                      -|       -|          -|    
|  10|                                                      -|                             -|                      -|       -|          -|    

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Power Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.004](eval_2021/optanne_graphann/deep-1B_power.png)**|
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.040](eval_2021/gemini/deep-1B_power.png)**|
|   3|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.113](eval_2021/faiss_t3/deep-1B_power.png)**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   4|                                                      -|                             -|                      -|       -|          -|
|   5|                                                      -|                             -|                      -|       -|          -|
|   6|                                                      -|                             -|                      -|       -|          -|
|   7|                                                      -|                             -|                      -|       -|          -|
|   8|                                                      -|                             -|                      -|       -|          -|
|   9|                                                      -|                             -|                      -|       -|          -|
|  10|                                                      -|                             -|                      -|       -|          -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Cost Rankings 

|Rank|Submission          |Team     |Hardware               |Status  |Cost         |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|---------|-----------------------|--------|-------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)|Intel |Intel Optane               |inprog|**$16,082.49**  |$14,664.20|$1,418.29|$14,664.20 |-      |-|
|   2|[faiss_t3](../t3/diskann-bare-metal/README.md)|Facebook Research(*org*) |NVidia GPU               |inprog|**$545,952.10**  |$506,503.70|$39,448.40|$22,021.90 |23      |394,484.028|
|   3|[gemini](../t3/diskann-bare-metal/README.md)|GSI Technology(*org*) |LedaE APU               |inprog|**$626,932.94**  |$612,993.26|$13,939.68|$55,726.66 |11      |139,396.812|
|   4|[-](-)|- |-               |-|**-**  |-|-|- |$DP4C_UN      |$DP4C_KWT|
|   5|                   -|        -|                      -|       -|            -|        -|      -|        -|             -|        -|
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
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### BigANN

##### BigANN Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[diskann](../t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[0.99976](eval_2021/diskann-bare-metal/bigann-1B_recall.png)**  |
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.99253](eval_2021/gemini/bigann-1B_recall.png)**  |
|   3|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.99084](eval_2021/optanne_graphann/bigann-1B_recall.png)**  |
|   4|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.92671](eval_2021/faiss_t3/bigann-1B_recall.png)**  |
|   5|                                                      -|                             -|                      -|       -|            -|
|   6|                                                      -|                             -|                      -|       -|            -|
|   7|                                                      -|                             -|                      -|       -|            -|
|   8|                                                      -|                             -|                      -|       -|            -|
|   9|                                                      -|                             -|                      -|       -|            -|
|  10|                                                      -|                             -|                      -|       -|            -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[343,727.791](eval_2021/optanne_graphann/bigann-1B_throughput.png)**  |
|   2|[diskann](../t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[19,094.371](eval_2021/diskann-bare-metal/bigann-1B_throughput.png)**  |
|   3|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[9,504.865](eval_2021/gemini/bigann-1B_throughput.png)**  |
|   4|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[3,086.656](eval_2021/faiss_t3/bigann-1B_throughput.png)**  |
|   5|                                                      -|                             -|                      -|       -|            -|
|   6|                                                      -|                             -|                      -|       -|            -|
|   7|                                                      -|                             -|                      -|       -|            -|
|   8|                                                      -|                             -|                      -|       -|            -|
|   9|                                                      -|                             -|                      -|       -|            -|
|  10|                                                      -|                             -|                      -|       -|            -|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.002](eval_2021/optanne_graphann/bigann-1B_power.png)**|       
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.039](eval_2021/gemini/bigann-1B_power.png)**|       
|   3|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.167](eval_2021/faiss_t3/bigann-1B_power.png)**|      
|   4|[-](-)                                   |-                      |-               |-|**-**|      
|   5|                                                      -|                             -|                      -|       -|          -|
|   6|                                                      -|                             -|                      -|       -|          -|
|   7|                                                      -|                             -|                      -|       -|          -|
|   8|                                                      -|                             -|                      -|       -|          -|
|   9|                                                      -|                             -|                      -|       -|          -|
|  10|                                                      -|                             -|                      -|       -|          -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Cost Rankings

|Rank|Submission          |Team                          |Hardware            |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|------------------------------|--------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)|Intel                      |Intel Optane            |inprog|**$15,407.15**   |$14,664.20|$742.95|$14,664.20 |-      |-|
|   2|[gemini](../t3/diskann-bare-metal/README.md)|GSI Technology(*org*)                      |LedaE APU            |inprog|**$626,785.91**   |$612,993.26|$13,792.65|$55,726.66 |11      |137,926.464|      
|   3|[faiss_t3](../t3/diskann-bare-metal/README.md)|Facebook Research(*org*)                      |NVidia GPU            |inprog|**$785,282.45**   |$726,722.70|$58,559.75|$22,021.90 |33      |585,597.505|  
|   4|[-](-)|-                      |-            |-|**-**   |-|-|- |$BA4C_UN      |$BA4C_KWT|  
|   5|                   -|                             -|                   -|       -|             -|       -|       -|        -|             -|        -|
|   6|                   -|                             -|                   -|       -|             -|       -|       -|        -|             -|        -|
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
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### MSTuring

##### MSTuring Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10           |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------------|
|   1|[diskann](../t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[0.99444](eval_2021/diskann-bare-metal/msturing-1B_recall.png)**    |
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.97841](eval_2021/gemini/msturing-1B_recall.png)**    |
|   3|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.96218](eval_2021/optanne_graphann/msturing-1B_recall.png)**    |
|   4|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.90900](eval_2021/faiss_t3/msturing-1B_recall.png)**    |
|   5|                                                      -|                             -|                      -|       -|              -|
|   6|                                                      -|                             -|                      -|       -|              -|
|   7|                                                      -|                             -|                      -|       -|              -|       
|   8|                                                      -|                             -|                      -|       -|              -|       
|   9|                                                      -|                             -|                      -|       -|              -|       
|  10|                                                      -|                             -|                      -|       -|              -|       

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[157,277.710](eval_2021/optanne_graphann/msturing-1B_throughput.png)** |
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[20,166.678](eval_2021/gemini/msturing-1B_throughput.png)** |
|   3|[diskann](../t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[17,200.601](eval_2021/diskann-bare-metal/msturing-1B_throughput.png)** |
|   4|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[2,359.485](eval_2021/faiss_t3/msturing-1B_throughput.png)** |
|   5|                                                      -|                             -|                      -|       -|           -|
|   6|                                                      -|                             -|                      -|       -|           -|
|   7|                                                      -|                             -|                      -|       -|           -|
|   8|                                                      -|                             -|                      -|       -|           -|
|   9|                                                      -|                             -|                      -|       -|           -|
|  10|                                                      -|                             -|                      -|       -|           -|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q         |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.005](eval_2021/optanne_graphann/msturing-1B_power.png)** |
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.023](eval_2021/gemini/msturing-1B_power.png)** |
|   3|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.204](eval_2021/faiss_t3/msturing-1B_power.png)** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|                                                      -|                             -|                      -|       -|           -|
|   6|                                                      -|                             -|                      -|       -|           -|
|   7|                                                      -|                             -|                      -|       -|           -|
|   8|                                                      -|                             -|                      -|       -|           -|
|   9|                                                      -|                             -|                      -|       -|           -|
|  10|                                                      -|                             -|                      -|       -|           -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Cost Rankings

|Rank|Submission                          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|------------------------------------|------------------------------|-----------------------|--------|--------------|--------|--------|---------|--------------|----------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                |Intel                      |Intel Optane               |inprog|**$16,397.80**   |$14,664.20|$1,733.60|$14,664.20 |-      |- |
|   2|[gemini](../t3/diskann-bare-metal/README.md)                |GSI Technology(*org*)                      |LedaE APU               |inprog|**$286,578.81**   |$278,633.30|$7,945.51|$55,726.66 |5      |79,455.069 |         
|   3|[faiss_t3](../t3/diskann-bare-metal/README.md)                |Facebook Research(*org*)                      |NVidia GPU               |inprog|**$1,018,332.30**   |$946,941.70|$71,390.60|$22,021.90 |43      |713,905.964 |       
|   4|[-](-)                |-                      |-               |-|**-**   |-|-|- |$MT4C_UN      |$MT4C_KWT |       
|   5|                                   -|                             -|                      -|       -|             -|       -|        -|       -|             -|         -|
|   6|                                   -|                             -|                      -|       -|             -|       -|        -|       -|             -|         -|
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
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### MSSpace

##### MSSpace Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10     |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.005](eval_2021/optanne_graphann/msspacev-1B_power.png)** |
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.048](eval_2021/gemini/msspacev-1B_power.png)** |
|   3|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.167](eval_2021/faiss_t3/msspacev-1B_power.png)** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|                                                      -|                             -|                      -|       -|        -|
|   6|                                                      -|                             -|                      -|       -|        -|
|   7|                                                      -|                             -|                      -|       -|        -|
|   8|                                                      -|                             -|                      -|       -|        -|
|   9|                                                      -|                             -|                      -|       -|        -|
|  10|                                                      -|                             -|                      -|       -|        -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[139,612.021](eval_2021/optanne_graphann/msspacev-1B_throughput.png)** |
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[8,587.024](eval_2021/gemini/msspacev-1B_throughput.png)** |
|   3|[diskann](../t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[6,503.212](eval_2021/diskann-bare-metal/msspacev-1B_throughput.png)** |
|   4|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[2,770.848](eval_2021/faiss_t3/msspacev-1B_throughput.png)** |
|   5|                                                      -|                             -|                      -|       -|           -|    
|   6|                                                      -|                             -|                      -|       -|           -|   
|   7|                                                      -|                             -|                      -|       -|           -|    
|   8|                                                      -|                             -|                      -|       -|           -|    
|   9|                                                      -|                             -|                      -|       -|           -|   
|  10|                                                      -|                             -|                      -|       -|           -|    

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.005](eval_2021/optanne_graphann/msspacev-1B_power.png)** |
|   2|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.048](eval_2021/gemini/msspacev-1B_power.png)** |
|   3|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.167](eval_2021/faiss_t3/msspacev-1B_power.png)** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|                                                      -|                             -|                      -|       -|           -|
|   6|                                                      -|                             -|                      -|       -|           -|
|   7|                                                      -|                             -|                      -|       -|           -|
|   8|                                                      -|                             -|                      -|       -|           -|
|   9|                                                      -|                             -|                      -|       -|           -|
|  10|                                                      -|                             -|                      -|       -|           -|

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Cost Rankings

|Rank|Submission          |Team                          |Hardware               |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs  |
|----|--------------------|------------------------------|-----------------------|------- |--------------|--------|--------|---------|--------------|----------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)|Intel                      |Intel Optane               |inprog|**$16,563.61**   |$14,664.20|$1,899.41|$14,664.20 |-      |- |
|   2|[gemini](../t3/diskann-bare-metal/README.md)|GSI Technology(*org*)                      |LedaE APU               |inprog|**$685,704.76**   |$668,719.92|$16,984.84|$55,726.66 |12      |169,848.419 |
|   3|[faiss_t3](../t3/diskann-bare-metal/README.md)|Facebook Research(*org*)                      |NVidia GPU               |inprog|**$873,460.84**   |$814,810.30|$58,650.54|$22,021.90 |37      |586,505.424 |
|   4|[-](-)|-                      |-               |-|**-**   |-|-|- |$MS4C_UN      |$MS4C_KWT |
|   5|                   -|                             -|                      -|       -|             -|       -|       -|        -|             -|         -|        
|   6|                   -|                             -|                      -|       -|             -|       -|       -|        -|             -|         -|        
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
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Text2Image

##### Text2Image Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[diskann](../t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[0.98130](eval_2021/diskann-bare-metal/text2image-1B_recall.png)**  |
|   2|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.90277](eval_2021/optanne_graphann/text2image-1B_recall.png)**  |
|   3|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.88163](eval_2021/gemini/text2image-1B_recall.png)**  |
|   4|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.86028](eval_2021/faiss_t3/text2image-1B_recall.png)**  |
|   5|                                                      -|                             -|                      -|       -|            -|
|   6|                                                      -|                             -|                      -|       -|            -|
|   7|                                                      -|                             -|                      -|       -|            -|
|   8|                                                      -|                             -|                      -|       -|            -|
|   9|                                                      -|                             -|                      -|       -|            -|
|  10|                                                      -|                             -|                      -|       -|            -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[10,838.358](eval_2021/optanne_graphann/text2image-1B_throughput.png)** |
|   2|[diskann](../t3/diskann-bare-metal/README.md)                                   |Microsoft Research(*org*)                      |Dell PowerEdge               |inprog|**[9,306.610](eval_2021/diskann-bare-metal/text2image-1B_throughput.png)** |
|   3|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[1,762.363](eval_2021/faiss_t3/text2image-1B_throughput.png)** |
|   4|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[1,196.589](eval_2021/gemini/text2image-1B_throughput.png)** |
|   5|                                                      -|                             -|                      -|       -|           -|   
|   6|                                                      -|                             -|                      -|       -|           -|    
|   7|                                                      -|                             -|                      -|       -|           -|    
|   8|                                                      -|                             -|                      -|       -|           -|    
|   9|                                                      -|                             -|                      -|       -|           -|    
|  10|                                                      -|                             -|                      -|       -|           -|    

* The operational point for ranking is 0.860 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.860 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.070](eval_2021/optanne_graphann/text2image-1B_power.png)**|
|   2|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.123](eval_2021/faiss_t3/text2image-1B_power.png)**|
|   3|[gemini](../t3/diskann-bare-metal/README.md)                                   |GSI Technology(*org*)                      |LedaE APU               |inprog|**[0.503](eval_2021/gemini/text2image-1B_power.png)**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   4|                                                      -|                             -|                      -|       -|        -|
|   5|                                                      -|                             -|                      -|       -|        -|
|   6|                                                      -|                             -|                      -|       -|        -|
|   7|                                                      -|                             -|                      -|       -|        -|
|   8|                                                      -|                             -|                      -|       -|        -|
|   9|                                                      -|                             -|                      -|       -|        -|
|  10|                                                      -|                             -|                      -|       -|        -|

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.86 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Cost Rankings

|Rank|Submission           |Team                          |Hardware             |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|---------------------|------------------------------|---------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[optanne_graphann](../t3/diskann-bare-metal/README.md) |Intel                      |Intel Optane             |inprog|**$171,244.96**   |$146,642.00|$24,602.96|$14,664.20 |-      |-|
|   2|[faiss_t3](../t3/diskann-bare-metal/README.md) |Facebook Research(*org*)                      |NVidia GPU             |inprog|**$1,298,436.77**   |$1,255,248.30|$43,188.47|$22,021.90 |57      |431,884.673| 
|   3|[gemini](../t3/diskann-bare-metal/README.md) |GSI Technology(*org*)                      |LedaE APU             |inprog|**$4,857,248.23**   |$4,681,039.44|$176,208.79|$55,726.66 |84      |1,762,087.853| 
|   4|[-](-) |-                      |-             |-|**-**   |-|-|- |$TI4C_UN      |$TI4C_KWT| 
|   5|                    -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
|   6|                    -|                             -|                    -|       -|             -|       -|       -|        -|             -|        -|       
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
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### FBSimSearchNet

##### FBSimSearchNet Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.97863](eval_2021/faiss_t3/ssnpp-1B_recall.png)**  |
|   2|[-](-)                                   |-                      |-               |-|**-**  |
|   3|[-](-)                                   |-                      |-               |-|**-**  |
|   4|[-](-)                                   |-                      |-               |-|**-**  |
|   5|                                                      -|                             -|                      -|       -|            -|
|   6|                                                      -|                             -|                      -|       -|            -|
|   7|                                                      -|                             -|                      -|       -|            -|
|   8|                                                      -|                             -|                      -|       -|            -|
|   9|                                                      -|                             -|                      -|       -|            -|
|  10|                                                      -|                             -|                      -|       -|            -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### FBSimSearchNet Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[5,572.272](eval_2021/faiss_t3/ssnpp-1B_throughput.png)** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|[-](-)                                   |-                      |-               |-|**-** |
|   5|                                                      -|                             -|                      -|       -|           -|
|   6|                                                      -|                             -|                      -|       -|           -|
|   7|                                                      -|                             -|                      -|       -|           -|
|   8|                                                      -|                             -|                      -|       -|           -|
|   9|                                                      -|                             -|                      -|       -|           -|
|  10|                                                      -|                             -|                      -|       -|           -|

* The operational point for ranking is 0.9 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.9 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress


##### FBSimSearchNet Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[faiss_t3](../t3/diskann-bare-metal/README.md)                                   |Facebook Research(*org*)                      |NVidia GPU               |inprog|**[0.095](eval_2021/faiss_t3/ssnpp-1B_power.png)**|
|   2|[-](-)                                   |-                      |-               |-|**-**|
|   3|[-](-)                                   |-                      |-               |-|**-**|
|   4|[-](-)                                   |-                      |-               |-|**-**|
|   5|                                                      -|                             -|                      -|       -|          -|
|   6|                                                      -|                             -|                      -|       -|          -|
|   7|                                                      -|                             -|                      -|       -|          -|
|   8|                                                      -|                             -|                      -|       -|          -|
|   9|                                                      -|                             -|                      -|       -|          -|
|  10|                                                      -|                             -|                      -|       -|          -|

* The operational point for ranking is 0.9 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.9 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### FBSimSearchNet Cost Rankings

|Rank|Submission          |Team                          |Hardware             |Status  |Cost          |capex   |opex    |unit cost|units@100K qps|KwH*4yrs |
|----|--------------------|------------------------------|---------------------|--------|--------------|--------|--------|---------|--------------|---------|
|   1|[faiss_t3](../t3/diskann-bare-metal/README.md)|Facebook Research(*org*)                      |NVidia GPU             |inprog|**$429,634.84**   |$396,394.20|$33,240.64|$22,021.90 |-      |-|
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
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

