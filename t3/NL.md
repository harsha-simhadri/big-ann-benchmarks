# T3 Track Leaderboards 

## Final Rankings On Private Query Set

*Available December 2021*
 
## Rankings On Public Query Set

### Rankings By Submission Name (alphabetical)

|Submission          |Team       |Hardware  |Status |[Recall Rank](#recall-rankings)|[Throughput Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)| 
|--------------------|-----------|----------|-------|-------------------------------|---------------------------------------|-----------------------------|---------------------------|
|deepgram            |DeepGram   |NVidia GPU|inprog |                              -|                                      -|                            -|                          -|
|diskANN             |Microsoft  |Intel Optane  |inprog |                              -|                                      -|                            -|                          -|
|[faiss_t3](../t3/faiss_t3/README.md)    |Facebook Research     |NVidia GPU    |final  |[3](#recall-rankings)                         |[3](#throughput-rankings)                                 |[3](#power-rankings)                       |[2](#cost-rankings)                     |
|[gemini](../t3/gemini/README.md)  |GSI Technology    |LedaE APU   |inprog |[1](#recall-rankings)                        |[2](#throughput-rankings)                                |[2](#power-rankings)                      |[3](#cost-rankings)                    |
|kanndi              |Silo.ai    |LedaE APU   |inprog |                              -|                                      -|                            -|                          -|
|nvidia_single_gpu   |NVidia     |NVidia GPU|inprog |                              -|                                      -|                            -|                          -|
|nvidia_multi_gpu    |NVidia     |NVidia GPU|inprog |                              -|                                      -|                            -|                          -|
|[optanne_graphann](../t3/optanne_graphann/README.md)|Intel   |Intel Optane  |inprog|[2](#recall-rankings)                       |[1](#throughput-rankings)                               |[1](#power-rankings)                     |[1](#cost-rankings)                   |
|optanne_diskann     |Intel   |Intel Optane  |inprog |                              -|                                      -|                            -|                          -|
|vector_t3           |Vector Inst|NVidia GPU|inprog |                              -|                                      -|                            -|                          -|



* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

### Rankings Per Metric

#### Recall Rankings 

|Rank|Submission                                         |Team                          |Hardware               |Status |Score      |Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|---------------------------------------------------|------------------------------|-----------------------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[gemini](../t3/gemini/README.md)                                 |GSI Technology                       |LedaE APU                |inprog|**0.280**|[0.989](eval_2021/gemini/deep-1B_recall.png) |[0.993](eval_2021/gemini/bigann-1B_recall.png) |[0.978](eval_2021/gemini/msturing-1B_recall.png)   |[0.986](eval_2021/gemini/msspacev-1B_recall.png)  |[0.882](eval_2021/gemini/text2image-1B_recall.png)     |-         |
|   2|[optanne_graphann](../t3/optanne_graphann/README.md)                                 |Intel                       |Intel Optane                |inprog|**0.279**|[0.983](eval_2021/optanne_graphann/deep-1B_recall.png) |[0.991](eval_2021/optanne_graphann/bigann-1B_recall.png) |[0.962](eval_2021/optanne_graphann/msturing-1B_recall.png)   |[0.988](eval_2021/optanne_graphann/msspacev-1B_recall.png)  |[0.903](eval_2021/optanne_graphann/text2image-1B_recall.png)     |-         |
|   3|[faiss_t3](../t3/faiss_t3/README.md)                                 |Facebook Research                       |NVidia GPU                |final|**baseline**|[0.943](eval_2021/faiss_t3/deep-1B_recall.png) |[0.927](eval_2021/faiss_t3/bigann-1B_recall.png) |[0.909](eval_2021/faiss_t3/msturing-1B_recall.png)   |[0.909](eval_2021/faiss_t3/msspacev-1B_recall.png)  |[0.860](eval_2021/faiss_t3/text2image-1B_recall.png)     |[0.979](eval_2021/faiss_t3/ssnpp-1B_recall.png)         |
|   4|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|    
|   5|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|   
|   6|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   7|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   8|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   9|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|  10|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

#### Throughput Rankings

|Rank|Submission                                         |Team                          |Hardware               |Status |Score      |Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|---------------------------------------------------|------------------------------|-----------------------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)                                 |Intel                       |Intel Optane                |inprog|**821550.201**|[184,490.708](eval_2021/optanne_graphann/deep-1B_throughput.png) |[343,727.791](eval_2021/optanne_graphann/bigann-1B_throughput.png) |[157,277.710](eval_2021/optanne_graphann/msturing-1B_throughput.png)   |[139,612.021](eval_2021/optanne_graphann/msspacev-1B_throughput.png)  |[10,838.358](eval_2021/optanne_graphann/text2image-1B_throughput.png)     |-         |
|   2|[gemini](../t3/gemini/README.md)                                 |GSI Technology                       |LedaE APU                |inprog|**34209.040**|[9,150.271](eval_2021/gemini/deep-1B_throughput.png) |[9,504.865](eval_2021/gemini/bigann-1B_throughput.png) |[20,166.678](eval_2021/gemini/msturing-1B_throughput.png)   |[8,587.024](eval_2021/gemini/msspacev-1B_throughput.png)  |[1,196.589](eval_2021/gemini/text2image-1B_throughput.png)     |-         | 
|   3|[faiss_t3](../t3/faiss_t3/README.md)                                 |Facebook Research                       |NVidia GPU                |final|**baseline**|[4,417.036](eval_2021/faiss_t3/deep-1B_throughput.png) |[3,086.656](eval_2021/faiss_t3/bigann-1B_throughput.png) |[2,359.485](eval_2021/faiss_t3/msturing-1B_throughput.png)   |[2,770.848](eval_2021/faiss_t3/msspacev-1B_throughput.png)  |[1,762.363](eval_2021/faiss_t3/text2image-1B_throughput.png)     |[5,572.272](eval_2021/faiss_t3/ssnpp-1B_throughput.png)         | 
|   4|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   5|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   6|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   7|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   8|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   9|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|  10|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

#### Power Rankings 

|Rank|Submission                                         |Team                          |Hardware               |Status |Score      |Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|---------------------------------------------------|------------------------------|-----------------------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)                                 |Intel                       |Intel Optane                |inprog|**-0.687**|[0.004](eval_2021/optanne_graphann/deep-1B_power.png) |[0.002](eval_2021/optanne_graphann/bigann-1B_power.png) |[0.005](eval_2021/optanne_graphann/msturing-1B_power.png)   |[0.005](eval_2021/optanne_graphann/msspacev-1B_power.png)  |[0.070](eval_2021/optanne_graphann/text2image-1B_power.png)     |-         |
|   2|[gemini](../t3/gemini/README.md)                                 |GSI Technology                       |LedaE APU                |inprog|**-0.121**|[0.040](eval_2021/gemini/deep-1B_power.png) |[0.039](eval_2021/gemini/bigann-1B_power.png) |[0.023](eval_2021/gemini/msturing-1B_power.png)   |[0.048](eval_2021/gemini/msspacev-1B_power.png)  |[0.503](eval_2021/gemini/text2image-1B_power.png)     |-         | 
|   3|[faiss_t3](../t3/faiss_t3/README.md)                                 |Facebook Research                       |NVidia GPU                |final|**baseline**|[0.113](eval_2021/faiss_t3/deep-1B_power.png) |[0.167](eval_2021/faiss_t3/bigann-1B_power.png) |[0.204](eval_2021/faiss_t3/msturing-1B_power.png)   |[0.167](eval_2021/faiss_t3/msspacev-1B_power.png)  |[0.123](eval_2021/faiss_t3/text2image-1B_power.png)     |[0.095](eval_2021/faiss_t3/ssnpp-1B_power.png)         | 
|   4|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   5|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   6|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   7|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   8|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   9|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|  10|                                                  -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

#### Cost Rankings 

|Rank|Submission                                          |Team                          |Hardware               |Status |Score      |Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|----------------------------------------------------|------------------------------|-----------------------|-------|-----------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)                                  |Intel                       |Intel Optane                |inprog|**$-4,285,768.44**|$16,082.49 |$15,407.15 |$16,397.80   |$16,563.61  |$171,244.96     |-         |
|   2|[faiss_t3](../t3/faiss_t3/README.md)                                  |Facebook Research                       |NVidia GPU                |final|**baseline**|$545,952.10 |$785,282.45 |$1,018,332.30   |$873,460.84  |$1,298,436.77     |$429,634.84         |
|   3|[gemini](../t3/gemini/README.md)                                  |GSI Technology                       |LedaE APU                |inprog|**$2,561,786.18**|$626,932.94 |$626,785.91 |$286,578.81   |$685,704.76  |$4,857,248.23     |-         |
|   4|                                                   -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   5|                                                   -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   6|                                                   -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   7|                                                   -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   8|                                                   -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|   9|                                                   -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|
|  10|                                                   -|                             -|                      -|      -|          -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

### Rankings Per Database

#### Deep1B

##### Deep1B Recall Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.989](eval_2021/gemini/deep-1B_recall.png)**|       
|   2|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.983](eval_2021/optanne_graphann/deep-1B_recall.png)**|       
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.943](eval_2021/faiss_t3/deep-1B_recall.png)**|       
|   4|                                                      -|                             -|                      -|       -|          -|       
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
  * *NQ* = not qualified

##### Deep1B Throughput Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S        |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[184,490.708](eval_2021/optanne_graphann/deep-1B_throughput.png)**|
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[9,150.271](eval_2021/gemini/deep-1B_throughput.png)**|
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[4,417.036](eval_2021/faiss_t3/deep-1B_throughput.png)**|
|   2|                                                      -|                             -|                      -|       -|          -|    
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
  * *NQ* = not qualified

##### Deep1B Power Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.004](eval_2021/optanne_graphann/deep-1B_power.png)**|
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.040](eval_2021/gemini/deep-1B_power.png)**|
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.113](eval_2021/faiss_t3/deep-1B_power.png)**|
|   2|                                                      -|                             -|                      -|       -|          -|
|   3|                                                      -|                             -|                      -|       -|          -|
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
  * *NQ* = not qualified

##### Deep1B Cost Rankings 

|Rank|Submission                                     |Team                          |Hardware               |Status  |Cost         |capex    |opex   |unit cost|units@100K qps|KwH*4yrs |KwH cost|
|----|-----------------------------------------------|------------------------------|-----------------------|--------|-------------|---------|-------|---------|--------------|---------|--------|
|   1|[optanne_graphann](../t3/gemini/README.md)                           |Intel                      |Intel Optane               |inprog|**$16,082.49**  |        -|      -|        -|             -|        -|       -|
|   2|[faiss_t3](../t3/gemini/README.md)                           |Facebook Research                      |NVidia GPU               |inprog|**$545,952.10**  |        -|      -|        -|             -|        -|       -|
|   3|[gemini](../t3/gemini/README.md)                           |GSI Technology                      |LedaE APU               |inprog|**$626,932.94**  |        -|      -|        -|             -|        -|       -|
|   4|                                              -|                             -|                      -|       -|            -|        -|      -|        -|             -|        -|       -|
|   5|                                              -|                             -|                      -|       -|            -|        -|      -|        -|             -|        -|       -|
|   6|                                              -|                             -|                      -|       -|            -|        -|      -|        -|             -|        -|       -|
|   7|                                              -|                             -|                      -|       -|            -|        -|      -|        -|             -|        -|       -|
|   8|                                              -|                             -|                      -|       -|            -|        -|      -|        -|             -|        -|       -|
|   9|                                              -|                             -|                      -|       -|            -|        -|      -|        -|             -|        -|       -|
|  10|                                              -|                             -|                      -|       -|            -|        -|      -|        -|             -|        -|       -|

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
  * *NQ* = not qualified

#### BigANN

##### BigANN Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.993](eval_2021/gemini/bigann-1B_recall.png)**  |
|   2|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.991](eval_2021/optanne_graphann/bigann-1B_recall.png)**  |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.927](eval_2021/faiss_t3/bigann-1B_recall.png)**  |
|   3|                                                      -|                             -|                      -|       -|            -|
|   4|                                                      -|                             -|                      -|       -|            -|
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
  * *NQ* = not qualified

##### BigANN Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S          |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[343,727.791](eval_2021/optanne_graphann/bigann-1B_throughput.png)**  |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[9,504.865](eval_2021/gemini/bigann-1B_throughput.png)**  |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[3,086.656](eval_2021/faiss_t3/bigann-1B_throughput.png)**  |
|   4|                                                      -|                             -|                      -|       -|            -|
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
  * *NQ* = not qualified

##### BigANN Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.002](eval_2021/optanne_graphann/bigann-1B_power.png)**|       
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.039](eval_2021/gemini/bigann-1B_power.png)**|       
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.167](eval_2021/faiss_t3/bigann-1B_power.png)**|      
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
  * *NQ* = not qualified

##### BigANN Cost Rankings

|Rank|Submission                                      |Team                          |Hardware            |Status  |Cost          |capex     |opex    |unit cost|units@100K qps|KwH*4yrs |KwH cost|
|----|------------------------------------------------|------------------------------|--------------------|--------|--------------|----------|--------|---------|--------------|---------|--------|
|   1|[optanne_graphann](../t3/gemini/README.md)                            |Intel                      |Intel Optane            |inprog|**$15,407.15**   |         -|       -|        -|             -|        -|       -|
|   2|[gemini](../t3/gemini/README.md)                            |GSI Technology                      |LedaE APU            |inprog|**$626,785.91**   |         -|       -|        -|             -|        -|       -|
|   3|[faiss_t3](../t3/gemini/README.md)                            |Facebook Research                      |NVidia GPU            |inprog|**$785,282.45**   |         -|       -|        -|             -|        -|       -|
|   2|                                               -|                             -|                   -|       -|             -|         -|       -|        -|             -|        -|       -|
|   3|                                               -|                             -|                   -|       -|             -|         -|       -|        -|             -|        -|       -|
|   4|                                               -|                             -|                   -|       -|             -|         -|       -|        -|             -|        -|       -|
|   5|                                               -|                             -|                   -|       -|             -|         -|       -|        -|             -|        -|       -|
|   6|                                               -|                             -|                   -|       -|             -|         -|       -|        -|             -|        -|       -|
|   7|                                               -|                             -|                   -|       -|             -|         -|       -|        -|             -|        -|       -|
|   8|                                               -|                             -|                   -|       -|             -|         -|       -|        -|             -|        -|       -|
|   9|                                               -|                             -|                   -|       -|             -|         -|       -|        -|             -|        -|       -|
|  10|                                               -|                             -|                   -|       -|             -|         -|       -|        -|             -|        -|       -|

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
  * *NQ* = not qualified

#### MSTuring

##### MSTuring Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10           |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------------|
|   1|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.978](eval_2021/gemini/msturing-1B_recall.png)**    |
|   2|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.962](eval_2021/optanne_graphann/msturing-1B_recall.png)**    |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.909](eval_2021/faiss_t3/msturing-1B_recall.png)**    |
|   4|                                                      -|                             -|                      -|       -|              -|
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
  * *NQ* = not qualified

##### MSTuring Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[157,277.710](eval_2021/optanne_graphann/msturing-1B_throughput.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[20,166.678](eval_2021/gemini/msturing-1B_throughput.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[2,359.485](eval_2021/faiss_t3/msturing-1B_throughput.png)** |
|   4|                                                      -|                             -|                      -|       -|           -|
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
  * *NQ* = not qualified

##### MSTuring Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q         |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.005](eval_2021/optanne_graphann/msturing-1B_power.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.023](eval_2021/gemini/msturing-1B_power.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.204](eval_2021/faiss_t3/msturing-1B_power.png)** |
|   4|                                                      -|                             -|                      -|       -|           -|
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
  * *NQ* = not qualified

##### MSTuring Cost Rankings

|Rank|Submission                          |Team                          |Hardware               |Status  |Cost          |capex     |opex     |unit cost|units@100K qps|KwH*4yrs  |KwH cost |
|----|------------------------------------|------------------------------|-----------------------|--------|--------------|----------|---------|---------|--------------|----------|---------|
|   1|[optanne_graphann](../t3/gemini/README.md)                |Intel                      |Intel Optane               |inprog|**$16,397.80**   |         -|        -|        -|             -|         -|        -|
|   2|[gemini](../t3/gemini/README.md)                |GSI Technology                      |LedaE APU               |inprog|**$286,578.81**   |         -|        -|        -|             -|         -|        -|
|   3|[faiss_t3](../t3/gemini/README.md)                |Facebook Research                      |NVidia GPU               |inprog|**$1,018,332.30**   |         -|        -|        -|             -|         -|        -|
|   4|                                   -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   5|                                   -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   6|                                   -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   7|                                   -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   8|                                   -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   9|                                   -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|  10|                                   -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|

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
  * *NQ* = not qualified

#### MSSpace

##### MSSpace Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10     |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|---------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.005](eval_2021/optanne_graphann/msspacev-1B_power.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.048](eval_2021/gemini/msspacev-1B_power.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.167](eval_2021/faiss_t3/msspacev-1B_power.png)** |
|   4|                                                      -|                             -|                      -|       -|        -|
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
  * *NQ* = not qualified

##### MSSpace Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[139,612.021](eval_2021/optanne_graphann/msspacev-1B_throughput.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[8,587.024](eval_2021/gemini/msspacev-1B_throughput.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[2,770.848](eval_2021/faiss_t3/msspacev-1B_throughput.png)** |
|   2|                                                      -|                             -|                      -|       -|           -|    
|   3|                                                      -|                             -|                      -|       -|           -|   
|   4|                                                      -|                             -|                      -|       -|           -|   
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
  * *NQ* = not qualified

##### MSSpace Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.005](eval_2021/optanne_graphann/msspacev-1B_power.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.048](eval_2021/gemini/msspacev-1B_power.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.167](eval_2021/faiss_t3/msspacev-1B_power.png)** |
|   4|                                                      -|                             -|                      -|       -|           -|
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
  * *NQ* = not qualified

##### MSSpace Cost Rankings

|Rank|Submission                             |Team                          |Hardware               |Status  |Cost          |capex     |opex     |unit cost|units@100K qps|KwH*4yrs  |KwH cost |
|----|---------------------------------------|------------------------------|-----------------------|------- |--------------|----------|---------|---------|--------------|----------|---------|
|   1|[optanne_graphann](../t3/gemini/README.md)                   |Intel                      |Intel Optane               |inprog|**$16,563.61**   |         -|        -|        -|             -|         -|        -|
|   2|[gemini](../t3/gemini/README.md)                   |GSI Technology                      |LedaE APU               |inprog|**$685,704.76**   |         -|        -|        -|             -|         -|        -|
|   3|[faiss_t3](../t3/gemini/README.md)                   |Facebook Research                      |NVidia GPU               |inprog|**$873,460.84**   |         -|        -|        -|             -|         -|        -|
|   4|                                      -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   5|                                      -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   6|                                      -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   7|                                      -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   8|                                      -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|   9|                                      -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|
|  10|                                      -|                             -|                      -|       -|             -|         -|        -|        -|             -|         -|        -|

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
  * *NQ* = not qualified

#### Text2Image

##### Text2Image Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.903](eval_2021/optanne_graphann/text2image-1B_recall.png)**  |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.882](eval_2021/gemini/text2image-1B_recall.png)**  |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.860](eval_2021/faiss_t3/text2image-1B_recall.png)**  |
|   4|                                                      -|                             -|                      -|       -|            -|
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
  * *NQ* = not qualified

##### Text2Image Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[10,838.358](eval_2021/optanne_graphann/text2image-1B_throughput.png)** |
|   2|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[1,762.363](eval_2021/faiss_t3/text2image-1B_throughput.png)** |
|   3|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[1,196.589](eval_2021/gemini/text2image-1B_throughput.png)** |
|   4|                                                      -|                             -|                      -|       -|           -|    
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
  * *NQ* = not qualified

##### Text2Image Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |Intel Optane               |inprog|**[0.070](eval_2021/optanne_graphann/text2image-1B_power.png)**|
|   2|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.123](eval_2021/faiss_t3/text2image-1B_power.png)**|
|   3|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.503](eval_2021/gemini/text2image-1B_power.png)**|
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
  * *NQ* = not qualified

##### Text2Image Cost Rankings

|Rank|Submission                                     |Team                          |Hardware             |Status  |Cost          |capex     |opex    |unit cost|units@100K qps|KwH*4yrs |KwH cost|
|----|-----------------------------------------------|------------------------------|---------------------|--------|--------------|----------|--------|---------|--------------|---------|--------|
|   1|[optanne_graphann](../t3/gemini/README.md)                           |Intel                      |Intel Optane             |inprog|**$171,244.96**   |         -|       -|        -|             -|        -|       -|
|   2|[faiss_t3](../t3/gemini/README.md)                           |Facebook Research                      |NVidia GPU             |inprog|**$1,298,436.77**   |         -|       -|        -|             -|        -|       -|
|   3|[gemini](../t3/gemini/README.md)                           |GSI Technology                      |LedaE APU             |inprog|**$4,857,248.23**   |         -|       -|        -|             -|        -|       -|
|   4|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   5|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   6|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   7|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   8|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   9|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|  10|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|

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
  * *NQ* = not qualified

#### FBSimSearchNet

##### FBSimSearchNet Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-------------|
|   1|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.979](eval_2021/faiss_t3/ssnpp-1B_recall.png)**  |
|   2|[-](-)                                   |-                      |-               |-|**-**  |
|   3|[-](-)                                   |-                      |-               |-|**-**  |
|   4|                                                      -|                             -|                      -|       -|            -|
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
  * *NQ* = not qualified

##### FBSimSearchNet Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |Q/S         |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[5,572.272](eval_2021/faiss_t3/ssnpp-1B_throughput.png)** |
|   2|[-](-)                                   |-                      |-               |-|**-** |
|   3|[-](-)                                   |-                      |-               |-|**-** |
|   4|                                                      -|                             -|                      -|       -|           -|
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
  * *NQ* = not qualified


##### FBSimSearchNet Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |NVidia GPU               |inprog|**[0.095](eval_2021/faiss_t3/ssnpp-1B_power.png)**|
|   2|[-](-)                                   |-                      |-               |-|**-**|
|   3|[-](-)                                   |-                      |-               |-|**-**|
|   4|                                                      -|                             -|                      -|       -|          -|
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
  * *NQ* = not qualified

##### FBSimSearchNet Cost Rankings

|Rank|Submission                                     |Team                          |Hardware             |Status  |Cost          |capex     |opex    |unit cost|units@100K qps|KwH*4yrs |KwH cost|
|----|-----------------------------------------------|------------------------------|---------------------|--------|--------------|----------|--------|---------|--------------|---------|--------|
|   1|[faiss_t3](../t3/gemini/README.md)                           |Facebook Research                      |NVidia GPU             |inprog|**$429,634.84**   |         -|       -|        -|             -|        -|       -|
|   2|[-](-)                           |-                      |-             |-|**-**   |         -|       -|        -|             -|        -|       -|
|   3|[-](-)                           |-                      |-             |-|**-**   |         -|       -|        -|             -|        -|       -|
|   4|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   5|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   6|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   7|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   8|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   9|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|  10|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|

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
  * *NQ* = not qualified

