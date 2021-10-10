# T3 Track Leaderboards 

## Final Rankings On Private Query Set

*Available December 2021*
 
## Rankings On Public Query Set

### Rankings By Submission Name (alphabetical)

|Submission                                           |Team                   |Hardware    |Status|[Recall Rank](#recall-rankings)|[Throughput Rank](#throughput-rankings)|[Power Rank](#power-rankings)|[Cost Rank](#cost-rankings)| 
|-----------------------------------------------------|-----------------------|------------|------|-------------------------------|---------------------------------------|-----------------------------|---------------------------|
|DeepGram                                             |DeepGram               |NVidia GPU  |     -|                              -|                                      -|                            -|                          -|
|DiskANN                                              |Microsoft (org)        |Intel Optane|     -|                              -|                                      -|                            -|                          -|
|[FAISS Baseline](t3/faiss_t3/README.md)              |Facebook Research (org)|NVidia GPU  | final|                              1|                                      1|                            1|                          1|
|[Gemini](t3/gemini/README.md)                        |GSI Technology (org)   |Leda-E APU  |     -|                              -|                                      -|                            -|                          -|
|KANNDI                                               |Silo.ai                |Leda-E APU  |     -|                              -|                                      -|                            -|                          -|
|NVidia Single                                        |NVidia                 |NVidia GPU  |     -|                              -|                                      -|                            -|                          -|
|NVidia Multi                                         |NVidia                 |NVidia GPU  |     -|                              -|                                      -|                            -|                          -|
|OptANNe 1                                            |Intel                  |Intel Optane|     -|                              -|                                      -|                            -|                          -|
|OptANNE 2                                            |Intel                  |Intel Optane|     -|                              -|                                      -|                            -|                          -|
|Vector T3                                            |Vector Institute       |NVidia GPU  |     _|                              -|                                      -|                            -|                          -|

* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

### Rankings Per Metric

#### Recall Rankings 

|Rank|Submission                                           |Team                   |Hardware  |Status|Score|Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-----------------------------------------------------|-----------------------|----------|------|-----|------|------|--------|-------|----------|--------------|
|   1|[FAISS Baseline](../../../main/t3/faiss_t3/README.md)|Facebook Research (org)|NVidia GPU| final|    0|     0|     0|       0|      0|         0|             0|
|   2|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -| 
|   3|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|     
|   4|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|    
|   5|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|   
|   6|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   7|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   8|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   9|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|  10|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Throughput Rankings

|Rank|Submission                                           |Team                   |Hardware  |Status|Score|Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-----------------------------------------------------|-----------------------|----------|------|-----|------|------|--------|-------|----------|--------------|  
|   1|[FAISS Baseline](../../../main/t3/faiss_t3/README.md)|Facebook Research (org)|NVidia GPU| final|    0|     0|     0|       0|      0|         0|             0|     
|   2|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   3|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   4|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   5|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   6|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   7|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   8|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   9|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|  10|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Power Rankings 

|Rank|Submission                                           |Team                   |Hardware  |Status|Score|Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-----------------------------------------------------|-----------------------|----------|------|-----|------|------|--------|-------|----------|--------------|    
|   1|[FAISS Baseline](../../../main/t3/faiss_t3/README.md)|Facebook Research (org)|NVidia GPU| final|    0|     0|     0|       0|      0|         0|             0|
|   2|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   3|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   4|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   5|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   6|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   7|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   8|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   9|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|  10|                                                    -|                      -|         -|     -|    -|     -|     -|       -|      -|         -|             -|

* A submission must support at least 3 databases to qualify for this ranking.
* The ranking is based on the score, which is the sum of benchmark improvements of qualifying databases (shown in specific database columns after the score column.)
* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

#### Cost Rankings 

|Rank|Submission                                           |Team             |Hardware  |Status|Score|Deep1B|BigANN|MSTuring|MSSpace|Text2Image|FBSimSearchNet|
|----|-----------------------------------------------------|-----------------|----------|------|-----|------|------|--------|-------|----------|--------------|
|   1|[FAISS Baseline](../../../main/t3/faiss_t3/README.md)|Facebook Research|NVidia GPU| final|    0|     0|     0|       0|      0|         0|             0|
|   2|                                                    -|                -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   3|                                                    -|                -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   4|                                                    -|                -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   5|                                                    -|                -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   6|                                                    -|                -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   7|                                                    -|                -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   8|                                                    -|                -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|   9|                                                    -|                -|         -|     -|    -|     -|     -|       -|      -|         -|             -|
|  10|                                                    -|                -|         -|     -|    -|     -|     -|       -|      -|         -|             -|

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

|Rank|Submission                                           |Team                   |Hardware  |Status|R@10|
|----|-----------------------------------------------------|-----------------------|----------|------|----|
|   1|[FAISS Baseline](../../../main/t3/faiss_t3/README.md)|Facebook Research (org)|NVidia GPU| final|   0|
|   2|                                                    -|                      -|         -|     -|   -|
|   3|                                                    -|                      -|         -|     -|   -|
|   4|                                                    -|                      -|         -|     -|   -|
|   5|                                                    -|                      -|         -|     -|   -|
|   6|                                                    -|                      -|         -|     -|   -|
|   7|                                                    -|                      -|         -|     -|   -|
|   8|                                                    -|                      -|         -|     -|   -|
|   9|                                                    -|                      -|         -|     -|   -|
|  10|                                                    -|                      -|         -|     -|   -|

* Rankings are subject to change until all submissions are finalized in Nov/Dec 2021.
* Abbreviations used in chart:
  * *org* = submitted by challenge organizer, so subject to competition restrictions
  * *final* = final submission
  * *inprog* = algorithm development still in progress

##### Deep1B Throughput Rankings 

##### Deep1B Power Rankings 

##### Deep1B Cost Rankings 

#### BigANN

##### BigANN Recall Rankings

##### BigANN Throughput Rankings

##### BigANN Power Rankings

##### BigANN Cost Rankings

#### MSTuring

##### MSTuring Recall Rankings

##### MSTuring Throughput Rankings

##### MSTuring Power Rankings

##### MSTuring Cost Rankings

#### MSSpace

##### MSSpace Recall Rankings

##### MSSpace Throughput Rankings

##### MSSpace Power Rankings

##### MSSpace Cost Rankings

#### Text2Image

##### Text2Image Recall Rankings

##### Text2Image Throughput Rankings

##### Text2Image Power Rankings

##### Text2Image Cost Rankings

#### FBSimSearchNet

##### FBSimSearchNet Recall Rankings

##### FBSimSearchNet Throughput Rankings

##### FBSimSearchNet Power Rankings

##### FBSimSearchNet Cost Rankings

