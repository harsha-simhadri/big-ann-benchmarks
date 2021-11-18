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
|msspacev-1B        |0.0        |2000            |                                 
|text2image-1B      |0.86       |1762.363        |                                 
|ssnpp-1B           |0.9        |2000            |

## Thresholds Explained

We had to decide very early in the planning of this competition reasonable performance thresholds to implement.  

We observed that the performance of the T3 baseline algorithm (see below) was achieving at least 90% recall@10 at 2000qps for several datasets, so we decided to bake this into the competition rules.  As our internal testing evolved we discovered that 1 dataset (text2image-1B) could not achieve those thresholds, and so we decided to lower the threshold based on the baseline performance we observed at that time.

# Baseline

## Algorithm and Hardware

The baseline algorithm is based on FAISS library version 1.7.1.  The FAISS library provides several ANN approaches and the baselined leverages the FAISS index called "IVF1048576,SQ8." The choice of this index was based on experimentation and consultation with Mathijs Douje of Facebook, one of the competition organizers.  You can view the algorithm [here].

The hardware is 1 PCIe V100 NVidia GPU attached to an Advantech SKY motherboard with 768 GB RAM.  More details about the hardware can be found [here](faiss_t3/README.md).

## Threshold

The baseline algorithm informed the track thresholds as explained in the Thresholds section above.

## Scoring

The performance of the baseline algorithm factors into the scoring used to rank participants, as explained in the Ranking Score section above.

The benchmarks used in the score calculation are listed below for each dataset:

|Dataset            |Recall@10/AP|Throughput(qps) |Cost(wspq) |
|-------------------|------------|----------------|-----------|
|deep-1B            |0.943       |4417.036        |0.113      |
|bigann-1B          |0.927       |3086.656        |0.167      |
|msturing-1B        |0.909       |2359.485        |0.204      |
|msspacev-1B        |0.909       |2770.848        |0.167      |
|text2image-1B      |0.860       |1762.363        |0.123      |
|ssnpp-1B           |0.979       |5572.272        |0.095      |

## Measurements

The baseline benchmarks are based on the most recent measurements.  At the start, and during the competition, we had published different numbers.  The reason for the changes are described in [Appendix A](#appendix-a) below.

# Appendix

## Appendix A

At the start of the competition, we had release the following thresholds:

|Dataset            |R@10/AP    |Throughput(qps) |
|-------------------|-----------|----------------|
|deep-1B            |0.9        |2000            |
|bigann-1B          |0.9        |2000            |
|msturing-1B        |0.9        |2000            |
|msspacev-1B        |0.85       |1484.217        |
|text2image-1B      |0.86       |1510.624        |
|ssnpp-1B           |0.9        |2000            |

The most recent thresholds have changed from the original for the following reasons:
* Changes in how recall was computing to deal with ties in distance.
* Changes in the radius for the range search dataset
* Also we decided to re-run the measurements of the baseline algorithm on the T3 baseline machine using the current evaluation framework.  The original baselines were measured using a different software framework
* The original baselines published did not calculate and report baseline cost.

The original baselines that were published are shown below. For recall:

|   dataset    |    qps   | recall@10 |
| ------------ | -------- | --------- |
| msturing-1B  | 2011.542 |   0.910   |
| bigann-1B    | 2058.950 |   0.927   |
| text2image-1B| 2120.635 |   0.860   |
| deep-1B      | 2002.490 |   0.942   |
| msspacev-1B  | 2190.829 |   0.850   |

And for throughput:

|   dataset    |    qps   | recall@10 |
| ------------ | -------- | --------- |
| msturing-1B  | 2421.856 |   0.902   |
| bigann-1B    | 2186.755 |   0.905   |
| text2image-1B| 1510.624 |   0.882   |
| deep-1B      | 3422.473 |   0.916   |
| msspacev-1B  | 1484.217 |   0.869   |

The following tables show the baseline performance on the range search dataset:

Instead of recall, the range search dataset utilizes average precision:

|   dataset  |    qps   |    ap
| -----------| ---------| ---------
| ssnpp-1B   | 2907.414 |   0.979

For throughput:

|   dataset  |    qps   |    ap     |
| -----------| -------- | --------- |
| ssnpp-1B   | 5572.272 |   0.910   |

Here were the published baselines for power:

|   dataset    | power(wspq) |
| ------------ | ------------|
| msturing-1B  | 0.203740    |
| bigann-1B    | 0.167123    |
| text2image-1B| 0.089675    |
| deep-1B      | 0.112581    |
| msspacev-1B  | 0.099569    |
| ssnpp-1B     | 0.0944865   |


The following table lists the full measurements for baseline performance experiments that informed the original baselines (only recall and throughput are shown.)

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



