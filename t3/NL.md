# T3 Track Leaderboards 

## Final Rankings On Private Query Set

*Available December 2021*
 
## Rankings On Public Query Set

### Rankings By Submission Name (alphabetical)

|Submission                                             |Team                             |Hardware                 |Status|[Recall Rank](#recall-rankings)|[Throughput Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)| 
|-------------------------------------------------------|---------------------------------|-------------------------|------|-------------------------------|---------------------------------------|-----------------------------|---------------------------|
|DeepGram                                               |DeepGram                         |<nobr>NVidia GPU</nobr>  |     -|                              -|                                      -|                            -|                          -|
|DiskANN                                                |<nobr>Microsoft (org)</nobr>     |<nobr>Intel Optane</nobr>|     -|                              -|                                      -|                            -|                          -|
|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>   |<nobr>NVidia GPU</nobr>  |final |3                         |3                                 |3                       |1                    |
|[Gemini](../t3/gemini/README.md)                       |<nobr>GSI Technology (org)</nobr>|<nobr>LedaE APU</nobr>   |inprog|1                        |2                                |2                      |2                   |
|KANNDI                                                 |Silo.ai                          |<nobr>LedaE APU</nobr>   |     -|                              -|                                      -|                            -|                          -|
|<nobr>NVidia Single GPU</nobr>                         |NVidia                           |<nobr>NVidia GPU</nobr>  |     -|                              -|                                      -|                            -|                          -|
|<nobr>NVidia Multi GPU</nobr>                          |NVidia                           |<nobr>NVidia GPU</nobr>  |     -|                              -|                                      -|                            -|                          -|
|OptANNe-1                                              |Intel                            |<nobr>Intel Optane</nobr>|inprog|2                      |1                               |1                     |NQ                  |
|OptANNE-2                                              |Intel                            |<nobr>Intel Optane</nobr>|     -|                              -|                                      -|                            -|                          -|
|Vector-T3                                              |<nobr>Vector Institute</nobr>    |<nobr>NVidia GPU</nobr>  |     _|                              -|                                      -|                            -|                          -|

* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

### Rankings Per Metric

#### Recall Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status|Score  |Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-------------------------------------------------------|------------------------------|-----------------------|-------|-------|------|------|--------|-------|----------|--------------|
|   1|[gemini](../t3/gemini/README.md)                                     |gemini                       |Gemini APU                |inprog|0.2802369519716198|     -|     -|       -|      -|         -|             -|
|   2|[optanne_graphann](../t3/optanne_graphann/README.md)                                     |optanne_graphann                       |Optane                |inprog|0.2790678608268525|     -|     -|       -|      -|         -|             -|
|   3|[faiss_t3](../t3/faiss_t3/README.md)                                     |faiss_t3                       |NVidia GPU                |final|0.0|     -|     -|       -|      -|         -|             -|
|   4|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|    
|   5|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|   
|   6|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   7|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   8|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   9|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|  10|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

#### Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Score  |Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-------------------------------------------------------|------------------------------|-----------------------|------|-------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)                                     |optanne_graphann                       |Optane                |inprog|821550.2011633916|     -|     -|       -|      -|         -|             -|
|   2|[gemini](../t3/gemini/README.md)                                     |gemini                       |Gemini APU                |inprog|34209.03953669113|     -|     -|       -|      -|         -|             -|
|   3|[faiss_t3](../t3/faiss_t3/README.md)                                     |faiss_t3                       |NVidia GPU                |final|0.0|     -|     -|       -|      -|         -|             -|
|   4|                                                      -|                             -|                      -|     -|       -|     -|     -|       -|      -|         -|             -|
|   5|                                                      -|                             -|                      -|     -|       -|     -|     -|       -|      -|         -|             -|
|   6|                                                      -|                             -|                      -|     -|       -|     -|     -|       -|      -|         -|             -|
|   7|                                                      -|                             -|                      -|     -|       -|     -|     -|       -|      -|         -|             -|
|   8|                                                      -|                             -|                      -|     -|       -|     -|     -|       -|      -|         -|             -|
|   9|                                                      -|                             -|                      -|     -|       -|     -|     -|       -|      -|         -|             -|
|  10|                                                      -|                             -|                      -|     -|       -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

#### Power Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status |Score  |Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-------------------------------------------------------|------------------------------|-----------------------|-------|-------|------|------|--------|-------|----------|--------------|
|   1|[optanne_graphann](../t3/optanne_graphann/README.md)                                     |optanne_graphann                       |Optane                |inprog|-0.6873303114624362|     -|     -|       -|      -|         -|             -|
|   2|[gemini](../t3/gemini/README.md)                                     |gemini                       |Gemini APU                |inprog|-0.12090838376879062|     -|     -|       -|      -|         -|             -|
|   3|[faiss_t3](../t3/faiss_t3/README.md)                                     |faiss_t3                       |NVidia GPU                |final|0.0|     -|     -|       -|      -|         -|             -|
|   4|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   5|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   6|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   7|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   8|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   9|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|  10|                                                      -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress
  * *NQ* = not qualified

#### Cost Rankings 

|Rank|Submission                                          |Team                          |Hardware               |Status |Score  |Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|----------------------------------------------------|------------------------------|-----------------------|-------|-------|------|------|--------|-------|----------|--------------|
|   1|[faiss_t3](../t3/faiss_t3/README.md)                                  |faiss_t3                       |NVidia GPU                |final|&#36;0.0|     -|     -|       -|      -|         -|             -|
|   2|[gemini](../t3/gemini/README.md)                                  |gemini                       |Gemini APU                |inprog|&#36;2561736.982327416|     -|     -|       -|      -|         -|             -|
|   3|[$CR3_TM]($CR3_RD)                                  |$CR3_TM                       |$CR3_HW                |$CR3_ST|$CR3_SC|     -|     -|       -|      -|         -|             -|
|   4|                                                   -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   5|                                                   -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   6|                                                   -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   7|                                                   -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   8|                                                   -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|   9|                                                   -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|
|  10|                                                   -|                             -|                      -|      -|      -|     -|     -|       -|      -|         -|             -|

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

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.942**|2002.490|
|   2|                                                      -|                             -|                      -|     -|        -|       -|
|   3|                                                      -|                             -|                      -|     -|        -|       -|
|   4|                                                      -|                             -|                      -|     -|        -|       -|
|   5|                                                      -|                             -|                      -|     -|        -|       -|
|   6|                                                      -|                             -|                      -|     -|        -|       -|
|   7|                                                      -|                             -|                      -|     -|        -|       -|
|   8|                                                      -|                             -|                      -|     -|        -|       -|
|   9|                                                      -|                             -|                      -|     -|        -|       -|
|  10|                                                      -|                             -|                      -|     -|        -|       -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Throughput Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status|Q/S         |R@10 |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|------------|-----|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**3422.473**|0.916|
|   2|                                                      -|                             -|                      -|     -|           -|    -|
|   3|                                                      -|                             -|                      -|     -|           -|    -|
|   4|                                                      -|                             -|                      -|     -|           -|    -|
|   5|                                                      -|                             -|                      -|     -|           -|    -|
|   6|                                                      -|                             -|                      -|     -|           -|    -|
|   7|                                                      -|                             -|                      -|     -|           -|    -|
|   8|                                                      -|                             -|                      -|     -|           -|    -|
|   9|                                                      -|                             -|                      -|     -|           -|    -|
|  10|                                                      -|                             -|                      -|     -|           -|    -|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Power Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q    |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.158**|
|   2|                                                      -|                             -|                      -|     -|        -|
|   3|                                                      -|                             -|                      -|     -|        -|
|   4|                                                      -|                             -|                      -|     -|        -|
|   5|                                                      -|                             -|                      -|     -|        -|
|   6|                                                      -|                             -|                      -|     -|        -|
|   7|                                                      -|                             -|                      -|     -|        -|
|   8|                                                      -|                             -|                      -|     -|        -|
|   9|                                                      -|                             -|                      -|     -|        -|
|  10|                                                      -|                             -|                      -|     -|        -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Cost Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status|Cost         |capex    |opex   |unit cost|units@100K qps|KwH*4yrs |KwH cost|
|----|-------------------------------------------------------|------------------------------|-----------------------|------|-------------|---------|-------|---------|--------------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**$716010.0**|$660657.0| $55353|$22021.90|            30|$553632.0|$55353.0|
|   2|                                                      -|                             -|                      -|     -|            -|        -|      -|        -|             -|        -|       -|
|   3|                                                      -|                             -|                      -|     -|            -|        -|      -|        -|             -|        -|       -|
|   4|                                                      -|                             -|                      -|     -|            -|        -|      -|        -|             -|        -|       -|
|   5|                                                      -|                             -|                      -|     -|            -|        -|      -|        -|             -|        -|       -|
|   6|                                                      -|                             -|                      -|     -|            -|        -|      -|        -|             -|        -|       -|
|   7|                                                      -|                             -|                      -|     -|            -|        -|      -|        -|             -|        -|       -|
|   8|                                                      -|                             -|                      -|     -|            -|        -|      -|        -|             -|        -|       -|
|   9|                                                      -|                             -|                      -|     -|            -|        -|      -|        -|             -|        -|       -|
|  10|                                                      -|                             -|                      -|     -|            -|        -|      -|        -|             -|        -|       -|

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

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.927**|2058.950|
|   2|                                                      -|                             -|                      -|     -|        -|       -|
|   3|                                                      -|                             -|                      -|     -|        -|       -|
|   4|                                                      -|                             -|                      -|     -|        -|       -|
|   5|                                                      -|                             -|                      -|     -|        -|       -|
|   6|                                                      -|                             -|                      -|     -|        -|       -|
|   7|                                                      -|                             -|                      -|     -|        -|       -|
|   8|                                                      -|                             -|                      -|     -|        -|       -|
|   9|                                                      -|                             -|                      -|     -|        -|       -|
|  10|                                                      -|                             -|                      -|     -|        -|       -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Q/S         |R@10 |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|------------|-----|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**2186.755**|0.905|
|   2|                                                      -|                             -|                      -|     -|           -|    -|
|   3|                                                      -|                             -|                      -|     -|           -|    -|
|   4|                                                      -|                             -|                      -|     -|           -|    -|
|   5|                                                      -|                             -|                      -|     -|           -|    -|
|   6|                                                      -|                             -|                      -|     -|           -|    -|
|   7|                                                      -|                             -|                      -|     -|           -|    -|
|   8|                                                      -|                             -|                      -|     -|           -|    -|
|   9|                                                      -|                             -|                      -|     -|           -|    -|
|  10|                                                      -|                             -|                      -|     -|           -|    -|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q   |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.19**|
|   2|                                                      -|                             -|                      -|     -|       -|
|   3|                                                      -|                             -|                      -|     -|       -|
|   4|                                                      -|                             -|                      -|     -|       -|
|   5|                                                      -|                             -|                      -|     -|       -|
|   6|                                                      -|                             -|                      -|     -|       -|
|   7|                                                      -|                             -|                      -|     -|       -|
|   8|                                                      -|                             -|                      -|     -|       -|
|   9|                                                      -|                             -|                      -|     -|       -|
|  10|                                                      -|                             -|                      -|     -|       -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Cost Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Cost          |capex     |opex    |unit cost|units@100K qps|KwH*4yrs |KwH cost|
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|----------|--------|---------|--------------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**$1079583.4**|$1013007.4|$66576.0|$22021.90|            46|$665760.0|$66576.0|
|   2|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   3|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   4|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   5|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   6|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   7|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   8|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   9|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|  10|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|

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

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.910**|2011.542|
|   2|                                                      -|                             -|                      -|     -|        -|       -|
|   3|                                                      -|                             -|                      -|     -|        -|       -|
|   4|                                                      -|                             -|                      -|     -|        -|       -|
|   5|                                                      -|                             -|                      -|     -|        -|       -|
|   6|                                                      -|                             -|                      -|     -|        -|       -|
|   7|                                                      -|                             -|                      -|     -|        -|       -|
|   8|                                                      -|                             -|                      -|     -|        -|       -|
|   9|                                                      -|                             -|                      -|     -|        -|       -|
|  10|                                                      -|                             -|                      -|     -|        -|       -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Q/S         |R@10 |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|------------|-----|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**2421.856**|0.902|
|   2|                                                      -|                             -|                      -|     -|           -|    -|
|   3|                                                      -|                             -|                      -|     -|           -|    -|
|   4|                                                      -|                             -|                      -|     -|           -|    -|
|   5|                                                      -|                             -|                      -|     -|           -|    -|
|   6|                                                      -|                             -|                      -|     -|           -|    -|
|   7|                                                      -|                             -|                      -|     -|           -|    -|
|   8|                                                      -|                             -|                      -|     -|           -|    -|
|   9|                                                      -|                             -|                      -|     -|           -|    -|
|  10|                                                      -|                             -|                      -|     -|           -|    -|

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q   |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.51**|
|   2|                                                      -|                             -|                      -|     -|       -|
|   3|                                                      -|                             -|                      -|     -|       -|
|   4|                                                      -|                             -|                      -|     -|       -|
|   5|                                                      -|                             -|                      -|     -|       -|
|   6|                                                      -|                             -|                      -|     -|       -|
|   7|                                                      -|                             -|                      -|     -|       -|
|   8|                                                      -|                             -|                      -|     -|       -|
|   9|                                                      -|                             -|                      -|     -|       -|
|  10|                                                      -|                             -|                      -|     -|       -|

* The operational point for ranking is 0.90 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Cost Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Cost          |capex     |opex     |unit cost|units@100K qps|KwH*4yrs  |KwH cost |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|----------|---------|---------|--------------|----------|---------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**$1279799.0**|$1101095.0|$178704.0|$22021.90|            50|$1787040.0|$178704.0|
|   2|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   3|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   4|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   5|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   6|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   7|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   8|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   9|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|  10|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|

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

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.850**|2190.829|
|   2|                                                      -|                             -|                      -|     -|        -|       -|
|   3|                                                      -|                             -|                      -|     -|        -|       -|
|   4|                                                      -|                             -|                      -|     -|        -|       -|
|   5|                                                      -|                             -|                      -|     -|        -|       -|
|   6|                                                      -|                             -|                      -|     -|        -|       -|
|   7|                                                      -|                             -|                      -|     -|        -|       -|
|   8|                                                      -|                             -|                      -|     -|        -|       -|
|   9|                                                      -|                             -|                      -|     -|        -|       -|
|  10|                                                      -|                             -|                      -|     -|        -|       -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Q/S         |R@10 |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|------------|-----|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**1484.217**|0.869|
|   2|                                                      -|                             -|                      -|     -|           -|    -|
|   3|                                                      -|                             -|                      -|     -|           -|    -|
|   4|                                                      -|                             -|                      -|     -|           -|    -|
|   5|                                                      -|                             -|                      -|     -|           -|    -|
|   6|                                                      -|                             -|                      -|     -|           -|    -|
|   7|                                                      -|                             -|                      -|     -|           -|    -|
|   8|                                                      -|                             -|                      -|     -|           -|    -|
|   9|                                                      -|                             -|                      -|     -|           -|    -|
|  10|                                                      -|                             -|                      -|     -|           -|    -|

* The operational point for ranking is 0.86 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.86 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q   |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.65**|
|   2|                                                      -|                             -|                      -|     -|       -|
|   3|                                                      -|                             -|                      -|     -|       -|
|   4|                                                      -|                             -|                      -|     -|       -|
|   5|                                                      -|                             -|                      -|     -|       -|
|   6|                                                      -|                             -|                      -|     -|       -|
|   7|                                                      -|                             -|                      -|     -|       -|
|   8|                                                      -|                             -|                      -|     -|       -|
|   9|                                                      -|                             -|                      -|     -|       -|
|  10|                                                      -|                             -|                      -|     -|       -|

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.86 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Cost Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Cost          |capex     |opex     |unit cost|units@100K qps|KwH*4yrs  |KwH cost |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|----------|---------|---------|--------------|----------|---------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**$1725249.2**|$1497489.2|$227760.0|$22021.90|            68|$2277600.0|$227760.0|
|   2|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   3|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   4|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   5|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   6|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   7|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   8|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|   9|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|
|  10|                                                      -|                             -|                      -|     -|             -|         -|        -|        -|             -|         -|        -|

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

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.860**|2120.635|
|   2|                                                      -|                             -|                      -|     -|        -|       -|
|   3|                                                      -|                             -|                      -|     -|        -|       -|
|   4|                                                      -|                             -|                      -|     -|        -|       -|
|   5|                                                      -|                             -|                      -|     -|        -|       -|
|   6|                                                      -|                             -|                      -|     -|        -|       -|
|   7|                                                      -|                             -|                      -|     -|        -|       -|
|   8|                                                      -|                             -|                      -|     -|        -|       -|
|   9|                                                      -|                             -|                      -|     -|        -|       -|
|  10|                                                      -|                             -|                      -|     -|        -|       -|

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Q/S         |R@10 |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|------------|-----|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**1510.624**|0.882|
|   2|                                                      -|                             -|                      -|     -|           -|    -|
|   3|                                                      -|                             -|                      -|     -|           -|    -|
|   4|                                                      -|                             -|                      -|     -|           -|    -|
|   5|                                                      -|                             -|                      -|     -|           -|    -|
|   6|                                                      -|                             -|                      -|     -|           -|    -|
|   7|                                                      -|                             -|                      -|     -|           -|    -|
|   8|                                                      -|                             -|                      -|     -|           -|    -|
|   9|                                                      -|                             -|                      -|     -|           -|    -|
|  10|                                                      -|                             -|                      -|     -|           -|    -|

* The operational point for ranking is 0.875 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.875 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Power Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|W*S/Q    |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.195**|
|   2|                                                      -|                             -|                      -|     -|        -|
|   3|                                                      -|                             -|                      -|     -|        -|
|   4|                                                      -|                             -|                      -|     -|        -|
|   5|                                                      -|                             -|                      -|     -|        -|
|   6|                                                      -|                             -|                      -|     -|        -|
|   7|                                                      -|                             -|                      -|     -|        -|
|   8|                                                      -|                             -|                      -|     -|        -|
|   9|                                                      -|                             -|                      -|     -|        -|
|  10|                                                      -|                             -|                      -|     -|        -|

* The operational point for ranking is 0.86 recall@10. We will use the lowest power consumption for the search parameters that meet or exceed 0.86 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Cost Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Cost          |capex     |opex    |unit cost|units@100K qps|KwH*4yrs |KwH cost|
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------------|----------|--------|---------|--------------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**$1125379.2**|$1057051.2|$68328.0|$22021.90|            48|$683280.0|$68328.0|
|   2|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   3|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   4|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   5|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   6|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   7|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   8|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|   9|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|
|  10|                                                      -|                             -|                      -|     -|             -|         -|       -|        -|             -|        -|       -|

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

#### FBSimSearchNet

##### FBSimSearchNet Recall Rankings

[TBD]

##### FBSimSearchNet Throughput Rankings

[TBD]

##### FBSimSearchNet Power Rankings

[TBD]

##### FBSimSearchNet Cost Rankings

[TBD]
