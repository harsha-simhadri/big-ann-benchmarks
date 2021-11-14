# Explanation of T3 Ranking Method

This readme outlines the ranking logic used for the T3 track of this competition.

## Benchmarks

We measure participants on 4 benchmarks and we maintain a leaderboard for each:
* recall/average precision -  recall is based on recall@10 accounting for distance ties
* throughput - based on queries/second
* power consumption - based on measuring watt*seconds/query
* cost - based on a projection of capex + opex

## Ranking Score

For each benchmark/leaderboard, we will compute an aggregate score based on the teams's performance on each participating dataset.

A team must participate in at least 3 datasets to qualify for the competition. 

A team fails to qualify for a dataset if either 1) their algorithm does not support that dataset 2) the performance of their algorithm does not meet the threshold for that dataset (see below) for a benchmark that implements thresholds.

The score on each participating dataset is based on the difference between the team's performance on that dataset and the performance of the baseline (see below).

The team's final ranking score for a benchmark is the sum of individual participating dataset scores.

In this way, teams that participate in more datasets can get an advantage.

## Thresholds

We implement thresholds for the recall/average precision and throughput benchmark/leaderboards.

The thresholds are listed below for each dataset:

|Dataset            |R@10/AP    |Throughput(qps) |
|-------------------|-----------|----------------|
|deep-1B            |0.9        |2000            |                                 
|bigann-1B          |0.9        |2000            |                                 
|msturing-1B        |0.9        |2000            |                                 
|msspacev-1B        |0.85       |1484.217        |                                 
|text2image-1B      |0.86       |1510.624        |                                 
|ssnpp-1B           |0.9        |2000            |

## Thresholds Explained

We had to decide very early in the planning of this competition reasonable performance thresholds to implement.  

We observed that the performance of the T3 baseline algorithm (see below) was achieving at least 90% recall@10 at 2000qps for several datasets, so we decided to bake this into the competition rules.  As our internal testing evolved we discovered that two datasets (msspacev-1B and text2image-1B) could not achieve those thresholds, and so we decided to lower the threshold based on the baseline performance we observed at that time.

Fast forward several months, we improved the baseline performance of both msspacev-1B and text2image-1B as well as changed the recall computation to account for ties (see below).  We decided that it would not be fair to participants to change the thresholds that were already established, so we kept the thresholds shown in the table above.  In the baseline section below, you will see results of the original experiments that established the track thresholds, as well as the most recent benchmarks that indeed improve on those thresholds.

# Baseline

## Algorithm and Hardware

The baseline algorithm is based on FAISS library version 1.7.1.  The FAISS library provides several ANN approaches and the baselined leverages the FAISS index called "IVF1048576,SQ8." The choice of this index was based on experimentation and consultation with Mathijs Douje of Facebook, one of the competition organizers.  You can view the algorithm [here].

The hardware is 1 PCIe V100 NVidia GPU attached to an Advantech SKY motherboard with 768 GB RAM.  More details about the hardware can be found [here].

## Threshold

The baseline algorithm informed the track thresholds as explained in the Thresholds section above.

## Scoring

The performance of the baseline algorithm factors into the scoring used to rank participants, as explained in the Ranking Score section above.

The benchmarks used in the score calculation are listed below for each dataset:

|Dataset            |Recall@10  |Throughput(qps) |
|-------------------|-----------|----------------|
|deep-1B            |0.942      |3422.473        |
|bigann-1B          |0.927      |2186.755        |
|msturing-1B        |0.910      |2421.856        |
|msspacev-1B        |0.850      |1484.217        |
|text2image-1B      |0.860      |1510.624        |
|ssnpp-1B           |0.979      |5572.272        |

## Measurements

The baseline benchmarks used for the score calculation in the table above was based on very early experiments.  The full results of those benchmarks are shown in Appendix A below.

The decision point was based on the following:
* for recall/average precision, we chose the highest recall/average precision that exceeded the threshold minimum for that dataset ( see Threshold section above. )
* for throughput, we chose the highest qps that exceeded the threshold minimum for that dataset ( see Threshold section above. )

As mentioned previously, the recall/average precision and throughput benchmarks on the baseline improved since the original measurements, but we decided not to change either the thresholds or scoring benchmarks out of fairness to participants.  That said, you can view those most recent baseline benchmarks in Appendix B.  In future competitions, we will likely update the thresholds and scoring benchmarks based on the most recent baseline measurements. 

# Appendix

## Appendix A

The following table lists the full results for baseline performance:

|              dbase|    throughtput(qps)|            recall@10|
|-------------------|--------------------|---------------------|
|          bigann-1B|         2186.754570|             0.904860|
|          bigann-1B|         1926.901416|             0.911140|
|          bigann-1B|         1657.226695|             0.919860|
|          bigann-1B|         2058.950046|             0.926560|
|          bigann-1B|         1931.042641|             0.932450|
|          bigann-1B|         1770.748406|             0.937190|
|          bigann-1B|         1609.052224|             0.941330|
|          bigann-1B|         1504.748288|             0.943890|
|      text2image-1B|         2607.779941|             0.834820|
|      text2image-1B|         2456.621393|             0.841845|
|      text2image-1B|         2285.966847|             0.851920|
|      text2image-1B|         2120.635218|             0.860156|
|      text2image-1B|         1917.445903|             0.867244|
|      text2image-1B|         1748.662912|             0.873469|
|      text2image-1B|         1612.313130|             0.878757|
|      text2image-1B|         1510.624227|             0.882487|
|        msspacev-1B|         2465.473370|             0.844805|
|        msspacev-1B|         2190.828587|             0.850205|
|        msspacev-1B|         1935.385102|             0.854864|
|        msspacev-1B|         1931.506970|             0.858998|
|        msspacev-1B|         1748.525911|             0.862437|
|        msspacev-1B|         1585.766679|             0.865152|
|        msspacev-1B|         1477.389358|             0.867912|
|        msspacev-1B|         1484.216732|             0.868812|
|        msturing-1B|         3625.040250|             0.881202|
|        msturing-1B|         3197.403722|             0.888140|
|        msturing-1B|         2907.993722|             0.893669|
|        msturing-1B|         2655.951474|             0.898400|
|        msturing-1B|         2421.855941|             0.902413|
|        msturing-1B|         2233.241641|             0.905846|
|        msturing-1B|         2070.942269|             0.908949|
|        msturing-1B|         2011.542149|             0.910115|
|            deep-1B|         3422.472565|             0.915540|
|            deep-1B|         2732.133452|             0.920430|
|            deep-1B|         2507.486404|             0.927790|
|            deep-1B|         1992.323615|             0.932950|
|            deep-1B|         2037.783443|             0.937940|
|            deep-1B|         2002.489712|             0.941740|
|            deep-1B|         1967.826369|             0.945130|
|            deep-1B|         1874.898854|             0.947430|

These baseline numbers were performed on the machine configuration used for the T3 faiss baseline.

An older (now obsolete) code framework was used to determine these thresholds, not the existing evaluation framework so unfortunately there is no algos.yaml configuration file.

The following shows the meaurements used to acquire the range search baseline [ TODO ]

## Appendix B

The following show the most recent baseline performance, which improve on the original measurements take that were used to inform the track thresholds and scoring benchmarks:

[TODO]


