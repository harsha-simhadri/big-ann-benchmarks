
# Eval On AMD 3GHz/16-Core + 125GB RAM + NVMe SSD (Bare Metal)

## Table Of Contents

- [Introduction](#introduction)  
- [Results](#results) 
- [Hardware Inventory](#hardware_inventory)
- [How To Reproduce](#how_to_reproduce)
- [Disclaimers And Credits](#disclaimers_and_credits)  

## Introduction

The NeurIPS2023 Practical Vector Search Challenge evaluated participating algorithms on Azure and EC2 CPU-based hardware instances.

In pursuit of expanding the evaluation criteria, we are also running on other generally available hardware configurations.

Shown here are results run on the following hardware:
* AMD EPYC 9124 16-Core 3GHz processor
* 125GB RAM 
* 440GB NVMe SSD
* Bare-metal "m4-metal-medium" instance provided by [Latitude](https://www.latitude.sh/) 

## Results

The calculated rankings are shown at the top.

Notes:
* Evaluations were run in late August 2024.
* In each track, qualifying algorithms are ranked by largest QPS where recall/ap >= 0.9.
* All participating algorithms are shown for each track, but only qualifying algorithms are ranked.
* Each track algorithm links to the build and run commmand used (or disqualifying errors, if any).
* Pareto graphs for each track shown below.

### Track: Filter

![Filter](latitude/filter.png)

### Track: Sparse

![Sparse](latitude/sparse.png)

### Track: OOD

![OOD](latitude/ood.png)

### Track: Streaming

TODO

### Data Export

The full data export CSV file can be found [here.](latitude/data_export_m4-metal-medium.csv)

## Hardware_Inventory

* Via [*lshw*](latitude/m4-metal-medium-lshw.txt)
* Via [*hwinfo*](latitude/m4-metal-medium-hwinfo.txt)
* Via [*procinfo*](latitude/m4-metal-medium-procinfo.txt)

## How_To_Reproduce

This section shows the steps you can use to reproduce the results shown above, from scratch.

### System Preparation

* Signup for/sign into your Latitude account 
* Provision an "m4-metal-medium" instance with at least 100GB NVMe SSD with Linux 20.04.06 LTS
* ssh remotely into the instance
* update Linux via command ```sudo apt-get update```
* install Anaconda for Linux
* run the following commands:
```
git clone git@github.com:harsha-simhadri/big-ann-benchmarks.git
cd big-ann-benchmarks
conda create -n bigann-latitude-m4-metal-medium python=3.10
conda activate bigann-latitude-m4-metal-medium
python -m pip install -r requirements_py3.10.txt 
```

### Sparse Track

Prepare the track dataset by running the following command in the top-level directory of the repository:
```
python create_dataset.py --dataset sparse-full
```

See the [latitude/commands](latitude/commands) directory for individual algorithm scripts.

### Filter Track

Prepare the track dataset by running the following command in the top-level directory of the repository:
```
python create_dataset.py --dataset yfcc-10M
```

See the [latitude/commands](latitude/commands) directory for individual algorithm scripts.

### OOD Track

Prepare the track dataset by running the following command in the top-level directory of the repository:
```
python create_dataset.py --dataset text2image-10M 
```
See the [latitude/commands](latitude/commands) directory for individual algorithm scripts.

### Streaming Track

Prepare the track dataset by running the following command in the top-level directory of the repository:
```
python create_dataset.py --dataset msturing-30M-clustered
python -m benchmark.streaming.download_gt --runbook_file neurips23/streaming/final_runbook.yaml  --dataset msturing-30M-clustered
```

See the [latitude/commands](latitude/commands) directory for individual algorithm scripts.

### Analysis

To extract the data as CSV:
```
sudo chmod ugo+rw -R ./results/ # recursively add read permissions to data files
python data_export.py --recompute --output neurips23/latitude/data_export_m4-metal-medium.csv
```

To plot individual tracks:
```
python plot.py --neurips23track sparse --output neurips23/latitude/sparse.png --raw --recompute --dataset sparse-full
python plot.py --neurips23track filter --output neurips23/latitude/filter.png --raw --recompute --dataset yfcc-10M
python plot.py --neurips23track ood --output neurips23/latitude/ood.png --raw --recompute --dataset text2image-10M
TODO: streaming track
```

To render the ranking table, see this [notebook](latitude/analysis.ipynb).

## Disclaimers_And_Credits

* The hardware systems were graciously donated by [Latitude](https://www.latitude.sh/)
* None of the Neurips2021/23 organizers is an employee or affiliated with Latitude.
* [George Williams](https://github.com/sourcesync), an organizer for both the NeurIPS2021 and NeurIPS2023 Competitions ran the evaluations described above.
* Our main contact from Latitude is [Victor Chiea](victor.chiea@latitude.sh), whom we were introduced by [Harald Carlens](harald@mlcontests.com) from [MLContests](https://mlcontests.com/).
* Latitude logo for sponsorship attribution below (note: it has a transparent background):
<img src="latitude/latitude_logo.png" height="100px">
