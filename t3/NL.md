# T3 Track Leaderboards 

## Final Rankings On Private Query Set

*Available December 2021*
 
## Rankings On Public Query Set

### Rankings By Submission Name (alphabetical)

|Submission          |Team       |Hardware  |Status |[Recall Rank](#recall-rankings)|[Throughput Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)| 
|--------------------|-----------|----------|-------|-------------------------------|---------------------------------------|-----------------------------|---------------------------|
|deepgram            |DeepGram   |NVidia GPU|inprog |                              -|                                      -|                            -|                          -|
|diskANN             |Microsoft  |Intel Optane  |inprog |                              -|                                      -|                            -|                          -|
|[faiss_t3](../t3/faiss_t3/README.md)    |Facebook Research     |NVidia GPU    |final  |3                         |3                                 |3                       |1                     |
|[gemini](../t3/gemini/README.md)  |GSI Technology    |LedaE APU   |inprog |1                        |2                                |2                      |2                    |
|kanndi              |Silo.ai    |LedaE APU   |inprog |                              -|                                      -|                            -|                          -|
|nvidia_single_gpu   |NVidia     |NVidia GPU|inprog |                              -|                                      -|                            -|                          -|
|nvidia_multi_gpu    |NVidia     |NVidia GPU|inprog |                              -|                                      -|                            -|                          -|
|[optanne_graphann](../t3/optanne_graphann/README.md)|Intel   |Intel Optane  |inprog|2                       |1                               |1                     |NQ                   |
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
|   1|[gemini](../t3/gemini/README.md)                                 |GSI Technology                       |LedaE APU                |inprog|**0.280**|0.989 |0.993 |0.978   |0.986  |0.882     |-         |
|   2|[optanne_graphann](../t3/optanne_graphann/README.md)                                 |Intel                       |Intel Optane                |inprog|**0.279**|0.983 |0.991 |0.962   |0.988  |0.903     |-         |
|   3|[faiss_t3](../t3/faiss_t3/README.md)                                 |Facebook Research                       |NVidia GPU                |final|**baseline**|0.943 |0.927 |0.909   |0.909  |0.860     |0.979         |
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
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)                                 |Intel                       |Intel Optane                |inprog|**821550.201**|184,490.708 |343,727.791 |157,277.710   |139,612.021  |10,838.358     |-         |
|   2|[gemini](../t3/gemini/README.md)                                 |GSI Technology                       |LedaE APU                |inprog|**34209.040**|9,150.271 |9,504.865 |20,166.678   |8,587.024  |1,196.589     |-         | 
|   3|[faiss_t3](../t3/faiss_t3/README.md)                                 |Facebook Research                       |NVidia GPU                |final|**baseline**|4,417.036 |3,086.656 |2,359.485   |2,770.848  |1,762.363     |5,572.272         | 
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
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)                                 |Intel                       |Intel Optane                |inprog|**-0.687**|0.004 |0.002 |0.005   |0.005  |0.070     |-         |
|   2|[gemini](../t3/gemini/README.md)                                 |GSI Technology                       |LedaE APU                |inprog|**-0.121**|0.040 |0.039 |0.023   |0.048  |0.503     |-         | 
|   3|[faiss_t3](../t3/faiss_t3/README.md)                                 |Facebook Research                       |NVidia GPU                |final|**baseline**|0.113 |0.167 |0.204   |0.167  |0.123     |0.095         | 
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
|   1|[faiss_t3](../t3/faiss_t3/README.md)                                  |Facebook Research                       |NVidia GPU                |final|**baseline**|$545,952.10 |$785,282.45 |$1,018,332.30   |$873,460.84  |$1,298,436.77     |$429,634.84         |
|   2|[gemini](../t3/gemini/README.md)                                  |GSI Technology                       |LedaE APU                |inprog|**$2,561,736.98**|$626,932.94 |$626,785.91 |$286,578.81   |$685,704.76  |$4,857,248.23     |-         |
|   3|[-](-)                                  |-                       |-                |-|**-**|- |- |-   |-  |-     |-         |
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

|Rank|Submission                                             |Team                          |Hardware               |Status  |R@10       |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|--------|
|   1|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.9887100000000001](eval_2021/gemini/deep-1B_recall.png)**|       -|
|   2|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.98264](eval_2021/gemini/deep-1B_recall.png)**|       -|
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.94275](eval_2021/gemini/deep-1B_recall.png)**|       -|
|   4|                                                      -|                             -|                      -|       -|          -|       -|
|   5|                                                      -|                             -|                      -|       -|          -|       -|
|   6|                                                      -|                             -|                      -|       -|          -|       -|
|   7|                                                      -|                             -|                      -|       -|          -|       -|
|   8|                                                      -|                             -|                      -|       -|          -|       -|
|   9|                                                      -|                             -|                      -|       -|          -|       -|
|  10|                                                      -|                             -|                      -|       -|          -|       -|

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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[184490.7079548704](eval_2021/gemini/deep-1B_throughput.png)**|
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[9150.271074040484](eval_2021/gemini/deep-1B_throughput.png)**|
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[4417.035674087254](eval_2021/gemini/deep-1B_throughput.png)**|
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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.004047640826756757](eval_2021/gemini/deep-1B_power.png)**|
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.0397821952](eval_2021/gemini/deep-1B_power.png)**|
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.11258105824](eval_2021/gemini/deep-1B_power.png)**|
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
|   1|[faiss_t3](../t3/gemini/README.md)                           |Facebook Research                      |LedaE APU               |inprog|**$545,952.10**  |        -|      -|        -|             -|        -|       -|
|   2|[gemini](../t3/gemini/README.md)                           |GSI Technology                      |LedaE APU               |inprog|**$626,932.94**  |        -|      -|        -|             -|        -|       -|
|   3|[-](-)                           |-                      |-               |-|**-**  |        -|      -|        -|             -|        -|       -|
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
|   1|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.9925299999999999](eval_2021/gemini/bigann-1B_recall.png)**  |
|   2|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.9908399999999999](eval_2021/gemini/bigann-1B_recall.png)**  |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.92671](eval_2021/gemini/bigann-1B_recall.png)**  |
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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[343727.7912541795](eval_2021/gemini/bigann-1B_throughput.png)**  |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[9504.865054975337](eval_2021/gemini/bigann-1B_throughput.png)**  |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[3086.6559639930956](eval_2021/gemini/bigann-1B_throughput.png)**  |
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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.002120302399273256](eval_2021/gemini/bigann-1B_power.png)**|       
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.039362575359999985](eval_2021/gemini/bigann-1B_power.png)**|       
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.16712257560000002](eval_2021/gemini/bigann-1B_power.png)**|      
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
|   1|[gemini](../t3/gemini/README.md)                            |GSI Technology                      |LedaE APU            |inprog|**$626,785.91**   |         -|       -|        -|             -|        -|       -|
|   2|[faiss_t3](../t3/gemini/README.md)                            |Facebook Research                      |LedaE APU            |inprog|**$785,282.45**   |         -|       -|        -|             -|        -|       -|
|   3|[-](-)                            |-                      |-            |-|**-**   |         -|       -|        -|             -|        -|       -|
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
|   1|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.97841](eval_2021/gemini/msturing-1B_recall.png)**    |
|   2|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.9621770000000001](eval_2021/gemini/msturing-1B_recall.png)**    |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.908996](eval_2021/gemini/msturing-1B_recall.png)**    |
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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[157277.71040650006](eval_2021/gemini/msturing-1B_throughput.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[20166.677965726823](eval_2021/gemini/msturing-1B_throughput.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[2359.4845936035667](eval_2021/gemini/msturing-1B_throughput.png)** |
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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.0049474815059375](eval_2021/gemini/msturing-1B_power.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.02267553344](eval_2021/gemini/msturing-1B_power.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.2037402864](eval_2021/gemini/msturing-1B_power.png)** |
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
|   1|[gemini](../t3/gemini/README.md)                |GSI Technology                      |LedaE APU               |inprog|**$286,578.81**   |         -|        -|        -|             -|         -|        -|
|   2|[faiss_t3](../t3/gemini/README.md)                |Facebook Research                      |LedaE APU               |inprog|**$1,018,332.30**   |         -|        -|        -|             -|         -|        -|
|   3|[-](-)                |-                      |-               |-|**-**   |         -|        -|        -|             -|         -|        -|
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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.005420693346849843](eval_2021/gemini/msspacev-1B_power.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.048472722244962935](eval_2021/gemini/msspacev-1B_power.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.16738168481375354](eval_2021/gemini/msspacev-1B_power.png)** |
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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[139612.021037142](eval_2021/gemini/msspacev-1B_throughput.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[8587.024025537552](eval_2021/gemini/msspacev-1B_throughput.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[2770.848339473574](eval_2021/gemini/msspacev-1B_throughput.png)** |
|   2|                                                      -|                             -|                      -|       -|           -|    
|   3|                                                      -|                             -|                      -|       -|           -|   
|   4|                                                      -|                             -|                      -|       -|           -|   
|   5|                                                      -|                             -|                      -|       -|           -|    
|   6|                                                      -|                             -|                      -|       -|           -|   
|   7|                                                      -|                             -|                      -|       -|           -|    
|   8|                                                      -|                             -|                      -|       -|           -|    
|   9|                                                      -|                             -|                      -|       -|           -|   
|  10|                                                      -|                             -|                      -|       -|           -|    

* The operational point for ranking is 0.86 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.86 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

##### MSSpace Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q       |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|------------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.005420693346849843](eval_2021/gemini/msspacev-1B_power.png)** |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.048472722244962935](eval_2021/gemini/msspacev-1B_power.png)** |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.16738168481375354](eval_2021/gemini/msspacev-1B_power.png)** |
|   4|                                                      -|                             -|                      -|       -|           -|
|   5|                                                      -|                             -|                      -|       -|           -|
|   6|                                                      -|                             -|                      -|       -|           -|
|   7|                                                      -|                             -|                      -|       -|           -|
|   8|                                                      -|                             -|                      -|       -|           -|
|   9|                                                      -|                             -|                      -|       -|           -|
|  10|                                                      -|                             -|                      -|       -|           -|

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.86 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

##### MSSpace Cost Rankings

|Rank|Submission                             |Team                          |Hardware               |Status  |Cost          |capex     |opex     |unit cost|units@100K qps|KwH*4yrs  |KwH cost |
|----|---------------------------------------|------------------------------|-----------------------|------- |--------------|----------|---------|---------|--------------|----------|---------|
|   1|[gemini](../t3/gemini/README.md)                   |GSI Technology                      |LedaE APU               |inprog|**$685,704.76**   |         -|        -|        -|             -|         -|        -|
|   2|[faiss_t3](../t3/gemini/README.md)                   |Facebook Research                      |LedaE APU               |inprog|**$873,460.84**   |         -|        -|        -|             -|         -|        -|
|   3|[-](-)                   |-                      |-               |-|**-**   |         -|        -|        -|             -|         -|        -|
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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.902765](eval_2021/gemini/text2image-1B_recall.png)**  |
|   2|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.8816330000000001](eval_2021/gemini/text2image-1B_recall.png)**  |
|   3|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.8602779999999999](eval_2021/gemini/text2image-1B_recall.png)**  |
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
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[10838.358351140563](eval_2021/gemini/text2image-1B_throughput.png)** |
|   2|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[1762.3632692835652](eval_2021/gemini/text2image-1B_throughput.png)** |
|   3|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[1196.589256851994](eval_2021/gemini/text2image-1B_throughput.png)** |
|   4|                                                      -|                             -|                      -|       -|           -|    
|   5|                                                      -|                             -|                      -|       -|           -|   
|   6|                                                      -|                             -|                      -|       -|           -|    
|   7|                                                      -|                             -|                      -|       -|           -|    
|   8|                                                      -|                             -|                      -|       -|           -|    
|   9|                                                      -|                             -|                      -|       -|           -|    
|  10|                                                      -|                             -|                      -|       -|           -|    

* The operational point for ranking is 0.875 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.875 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

##### Text2Image Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status  |W*S/Q      |
|----|-------------------------------------------------------|------------------------------|-----------------------|--------|-----------|
|   1|[optanne_graphann](../t3/gemini/README.md)                                   |Intel                      |LedaE APU               |inprog|**[0.07021393391250001](eval_2021/gemini/text2image-1B_power.png)**|
|   2|[faiss_t3](../t3/gemini/README.md)                                   |Facebook Research                      |LedaE APU               |inprog|**[0.1232547584](eval_2021/gemini/text2image-1B_power.png)**|
|   3|[gemini](../t3/gemini/README.md)                                   |GSI Technology                      |LedaE APU               |inprog|**[0.50287895344](eval_2021/gemini/text2image-1B_power.png)**|
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
|   1|[faiss_t3](../t3/gemini/README.md)                           |Facebook Research                      |LedaE APU             |inprog|**$1,298,436.77**   |         -|       -|        -|             -|        -|       -|
|   2|[gemini](../t3/gemini/README.md)                           |GSI Technology                      |LedaE APU             |inprog|**$4,857,248.23**   |         -|       -|        -|             -|        -|       -|
|   3|[-](-)                           |-                      |-             |-|**-**   |         -|       -|        -|             -|        -|       -|
|   4|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   5|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   6|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   7|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   8|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|   9|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|
|  10|                                              -|                             -|                    -|       -|             -|         -|       -|        -|             -|        -|       -|

* The operational point for ranking is 0.875 recall@10. We will use the lowest power consumption/query for the search parameters that meet or exceed 0.875 recall@10.
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

[TBD]

##### FBSimSearchNet Throughput Rankings

[TBD]

##### FBSimSearchNet Power Rankings

[TBD]

##### FBSimSearchNet Cost Rankings

[TBD]
