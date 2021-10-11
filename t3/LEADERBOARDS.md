# T3 Track Leaderboards 

## Final Rankings On Private Query Set

*Available December 2021*
 
## Rankings On Public Query Set

### Rankings By Submission Name (alphabetical)

|Submission                                             |Team                             |Hardware                 |Status|[Recall Rank](#recall-rankings)|[Throughput Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)| 
|-------------------------------------------------------|---------------------------------|-------------------------|------|-------------------------------|---------------------------------------|-----------------------------|---------------------------|
|DeepGram                                               |DeepGram                         |<nobr>NVidia GPU</nobr>  |     -|                              -|                                      -|                            -|                          -|
|DiskANN                                                |<nobr>Microsoft (org)</nobr>     |<nobr>Intel Optane</nobr>|     -|                              -|                                      -|                            -|                          -|
|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>   |<nobr>NVidia GPU</nobr>  | final|                              1|                                      1|                            1|                          1|
|[Gemini](../t3/gemini/README.md)                       |<nobr>GSI Technology (org)</nobr>|<nobr>LedaE APU</nobr>   |     -|                              -|                                      -|                            -|                          -|
|KANNDI                                                 |Silo.ai                          |<nobr>LedaE APU</nobr>   |     -|                              -|                                      -|                            -|                          -|
|<nobr>NVidia Single GPU</nobr>                         |NVidia                           |<nobr>NVidia GPU</nobr>  |     -|                              -|                                      -|                            -|                          -|
|<nobr>NVidia Multi GPU</nobr>                          |NVidia                           |<nobr>NVidia GPU</nobr>  |     -|                              -|                                      -|                            -|                          -|
|OptANNe-1                                              |Intel                            |<nobr>Intel Optane</nobr>|     -|                              -|                                      -|                            -|                          -|
|OptANNE-2                                              |Intel                            |<nobr>Intel Optane</nobr>|     -|                              -|                                      -|                            -|                          -|
|Vector-T3                                              |<nobr>Vector Institute</nobr>    |<nobr>NVidia GPU</nobr>  |     _|                              -|                                      -|                            -|                          -|

* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

### Rankings Per Metric

#### Recall Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status|Score|Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-------------------------------------------------------|------------------------------|-----------------------|------|-----|------|------|--------|-------|----------|--------------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|    0|     0|     0|       0|      0|         0|             0|
|   2|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -| 
|   3|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|     
|   4|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|    
|   5|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|   
|   6|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   7|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   8|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   9|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|  10|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Throughput Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|Score|Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-------------------------------------------------------|------------------------------|-----------------------|------|-----|------|------|--------|-------|----------|--------------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|    0|     0|     0|       0|      0|         0|             0|
|   2|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   3|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   4|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   5|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   6|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   7|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   8|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   9|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|  10|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Power Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status|Score|Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-------------------------------------------------------|------------------------------|-----------------------|------|-----|------|------|--------|-------|----------|--------------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|    0|     0|     0|       0|      0|         0|             0|
|   2|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   3|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   4|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   5|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   6|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   7|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   8|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   9|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|  10|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Cost Rankings 

|Rank|Submission                                          |Team                          |Hardware                  |Status|Score|Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-------------------------------------------------------|------------------------------|-----------------------|------|-----|------|------|--------|-------|----------|--------------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|    0|     0|     0|       0|      0|         0|             0|
|   2|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   3|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   4|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   5|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   6|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   7|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   8|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|   9|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|
|  10|                                                      -|                             -|                      -|     -|    -|     -|     -|       -|      -|         -|             -|

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

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.942**|2002.490|
|   2|                                                      -|                             -|                      -|     -|        -|        |
|   3|                                                      -|                             -|                      -|     -|        -|        |
|   4|                                                      -|                             -|                      -|     -|        -|        |
|   5|                                                      -|                             -|                      -|     -|        -|        |
|   6|                                                      -|                             -|                      -|     -|        -|        |
|   7|                                                      -|                             -|                      -|     -|        -|        |
|   8|                                                      -|                             -|                      -|     -|        -|        |
|   9|                                                      -|                             -|                      -|     -|        -|        |
|  10|                                                      -|                             -|                      -|     -|        -|        |

* The operational point for ranking is 2000 QPS. We will use the highest recall for the search parameters that meet or exceed 2000 QPS.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Throughput Rankings 

|Rank|Submission                                             |Team                          |Hardware               |Status|Q/S     |R@10 |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|--------|-----|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|3422.473|0.916|
|   2|                                                      -|                             -|                      -|     -|       -|     |
|   3|                                                      -|                             -|                      -|     -|       -|     |
|   4|                                                      -|                             -|                      -|     -|       -|     |
|   5|                                                      -|                             -|                      -|     -|       -|     |
|   6|                                                      -|                             -|                      -|     -|       -|     |
|   7|                                                      -|                             -|                      -|     -|       -|     |
|   8|                                                      -|                             -|                      -|     -|       -|     |
|   9|                                                      -|                             -|                      -|     -|       -|     |
|  10|                                                      -|                             -|                      -|     -|       -|     |

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Power Rankings 

##### Deep1B Cost Rankings 

#### BigANN

##### BigANN Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.927**|2058.950|
|   2|                                                      -|                             -|                      -|     -|        -|        |
|   3|                                                      -|                             -|                      -|     -|        -|        |
|   4|                                                      -|                             -|                      -|     -|        -|        |
|   5|                                                      -|                             -|                      -|     -|        -|        |
|   6|                                                      -|                             -|                      -|     -|        -|        |
|   7|                                                      -|                             -|                      -|     -|        -|        |
|   8|                                                      -|                             -|                      -|     -|        -|        |
|   9|                                                      -|                             -|                      -|     -|        -|        |
|  10|                                                      -|                             -|                      -|     -|        -|        |

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
|   2|                                                      -|                             -|                      -|     -|           -|     |
|   3|                                                      -|                             -|                      -|     -|           -|     |
|   4|                                                      -|                             -|                      -|     -|           -|     |
|   5|                                                      -|                             -|                      -|     -|           -|     |
|   6|                                                      -|                             -|                      -|     -|           -|     |
|   7|                                                      -|                             -|                      -|     -|           -|     |
|   8|                                                      -|                             -|                      -|     -|           -|     |
|   9|                                                      -|                             -|                      -|     -|           -|     |
|  10|                                                      -|                             -|                      -|     -|           -|     |

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### BigANN Power Rankings

##### BigANN Cost Rankings

#### MSTuring

##### MSTuring Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.910**|2011.542|
|   2|                                                      -|                             -|                      -|     -|        -|        |
|   3|                                                      -|                             -|                      -|     -|        -|        |
|   4|                                                      -|                             -|                      -|     -|        -|        |
|   5|                                                      -|                             -|                      -|     -|        -|        |
|   6|                                                      -|                             -|                      -|     -|        -|        |
|   7|                                                      -|                             -|                      -|     -|        -|        |
|   8|                                                      -|                             -|                      -|     -|        -|        |
|   9|                                                      -|                             -|                      -|     -|        -|        |
|  10|                                                      -|                             -|                      -|     -|        -|        |

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
|   2|                                                      -|                             -|                      -|     -|           -|     |
|   3|                                                      -|                             -|                      -|     -|           -|     |
|   4|                                                      -|                             -|                      -|     -|           -|     |
|   5|                                                      -|                             -|                      -|     -|           -|     |
|   6|                                                      -|                             -|                      -|     -|           -|     |
|   7|                                                      -|                             -|                      -|     -|           -|     |
|   8|                                                      -|                             -|                      -|     -|           -|     |
|   9|                                                      -|                             -|                      -|     -|           -|     |
|  10|                                                      -|                             -|                      -|     -|           -|     |

* The operational point for ranking is 0.90 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.90 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSTuring Power Rankings

##### MSTuring Cost Rankings

#### MSSpace

##### MSSpace Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.850**|2190.829|
|   2|                                                      -|                             -|                      -|     -|        -|        |
|   3|                                                      -|                             -|                      -|     -|        -|        |
|   4|                                                      -|                             -|                      -|     -|        -|        |
|   5|                                                      -|                             -|                      -|     -|        -|        |
|   6|                                                      -|                             -|                      -|     -|        -|        |
|   7|                                                      -|                             -|                      -|     -|        -|        |
|   8|                                                      -|                             -|                      -|     -|        -|        |
|   9|                                                      -|                             -|                      -|     -|        -|        |
|  10|                                                      -|                             -|                      -|     -|        -|        |

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
|   2|                                                      -|                             -|                      -|     -|           -|     |
|   3|                                                      -|                             -|                      -|     -|           -|     |
|   4|                                                      -|                             -|                      -|     -|           -|     |
|   5|                                                      -|                             -|                      -|     -|           -|     |
|   6|                                                      -|                             -|                      -|     -|           -|     |
|   7|                                                      -|                             -|                      -|     -|           -|     |
|   8|                                                      -|                             -|                      -|     -|           -|     |
|   9|                                                      -|                             -|                      -|     -|           -|     |
|  10|                                                      -|                             -|                      -|     -|           -|     |

* The operational point for ranking is 0.86 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.86 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### MSSpace Power Rankings

##### MSSpace Cost Rankings

#### Text2Image

##### Text2Image Recall Rankings

|Rank|Submission                                             |Team                          |Hardware               |Status|R@10     |Q/S     |
|----|-------------------------------------------------------|------------------------------|-----------------------|------|---------|--------|
|   1|<nobr>[FAISS Baseline](../t3/faiss_t3/README.md)</nobr>|<nobr>FB Research (org)</nobr>|<nobr>NVidia GPU</nobr>| final|**0.860**|2120.635|
|   2|                                                      -|                             -|                      -|     -|        -|        |
|   3|                                                      -|                             -|                      -|     -|        -|        |
|   4|                                                      -|                             -|                      -|     -|        -|        |
|   5|                                                      -|                             -|                      -|     -|        -|        |
|   6|                                                      -|                             -|                      -|     -|        -|        |
|   7|                                                      -|                             -|                      -|     -|        -|        |
|   8|                                                      -|                             -|                      -|     -|        -|        |
|   9|                                                      -|                             -|                      -|     -|        -|        |
|  10|                                                      -|                             -|                      -|     -|        -|        |

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
|   2|                                                      -|                             -|                      -|     -|           -|     |
|   3|                                                      -|                             -|                      -|     -|           -|     |
|   4|                                                      -|                             -|                      -|     -|           -|     |
|   5|                                                      -|                             -|                      -|     -|           -|     |
|   6|                                                      -|                             -|                      -|     -|           -|     |
|   7|                                                      -|                             -|                      -|     -|           -|     |
|   8|                                                      -|                             -|                      -|     -|           -|     |
|   9|                                                      -|                             -|                      -|     -|           -|     |
|  10|                                                      -|                             -|                      -|     -|           -|     |

* The operational point for ranking is 0.875 recall@10. We will use the highest throughput for the search parameters that meet or exceed 0.875 recall@10.
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Text2Image Power Rankings

##### Text2Image Cost Rankings

#### FBSimSearchNet

##### FBSimSearchNet Recall Rankings

[TBD]

##### FBSimSearchNet Throughput Rankings

[TBD]

##### FBSimSearchNet Power Rankings

[TBD]

##### FBSimSearchNet Cost Rankings

[TBD]
