
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
<table id="T_5e37f">
  <thead>
    <tr>
      <th id="T_5e37f_level0_col0" class="col_heading level0 col0" colspan="3">filter</th>
      <th id="T_5e37f_level0_col3" class="col_heading level0 col3" colspan="3">sparse</th>
      <th id="T_5e37f_level0_col6" class="col_heading level0 col6" colspan="3">ood</th>
    </tr>
    <tr>
      <th id="T_5e37f_level1_col0" class="col_heading level1 col0" >rank</th>
      <th id="T_5e37f_level1_col1" class="col_heading level1 col1" >algorithm</th>
      <th id="T_5e37f_level1_col2" class="col_heading level1 col2" >qps</th>
      <th id="T_5e37f_level1_col3" class="col_heading level1 col3" >rank</th>
      <th id="T_5e37f_level1_col4" class="col_heading level1 col4" >algorithm</th>
      <th id="T_5e37f_level1_col5" class="col_heading level1 col5" >qps</th>
      <th id="T_5e37f_level1_col6" class="col_heading level1 col6" >rank</th>
      <th id="T_5e37f_level1_col7" class="col_heading level1 col7" >algorithm</th>
      <th id="T_5e37f_level1_col8" class="col_heading level1 col8" >qps</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="T_5e37f_row0_col0" class="data row0 col0" >1</td>
      <td id="T_5e37f_row0_col1" class="data row0 col1" ><a href="latitude/commands/filter__zilliz.sh"><div style="height:100%;width:100%">zilliz</div></a></td>
      <td id="T_5e37f_row0_col2" class="data row0 col2" >               213.3K</td>
      <td id="T_5e37f_row0_col3" class="data row0 col3" >1</td>
      <td id="T_5e37f_row0_col4" class="data row0 col4" ><a href="latitude/commands/sparse__zilliz.sh"><div style="height:100%;width:100%">zilliz</div></a></td>
      <td id="T_5e37f_row0_col5" class="data row0 col5" >                34.8K</td>
      <td id="T_5e37f_row0_col6" class="data row0 col6" >1</td>
      <td id="T_5e37f_row0_col7" class="data row0 col7" ><a href="latitude/commands/ood__pinecone-ood.sh"><div style="height:100%;width:100%">pinecone-ood</div></a></td>
      <td id="T_5e37f_row0_col8" class="data row0 col8" >                76.9K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row1_col0" class="data row1 col0" >2</td>
      <td id="T_5e37f_row1_col1" class="data row1 col1" ><a href="latitude/commands/filter__pinecone.sh"><div style="height:100%;width:100%">pinecone</div></a></td>
      <td id="T_5e37f_row1_col2" class="data row1 col2" >               146.7K</td>
      <td id="T_5e37f_row1_col3" class="data row1 col3" >2</td>
      <td id="T_5e37f_row1_col4" class="data row1 col4" ><a href="latitude/commands/sparse__pyanns.sh"><div style="height:100%;width:100%">pyanns</div></a></td>
      <td id="T_5e37f_row1_col5" class="data row1 col5" >                26.9K</td>
      <td id="T_5e37f_row1_col6" class="data row1 col6" >2</td>
      <td id="T_5e37f_row1_col7" class="data row1 col7" ><a href="latitude/commands/ood__zilliz.sh"><div style="height:100%;width:100%">zilliz</div></a></td>
      <td id="T_5e37f_row1_col8" class="data row1 col8" >                73.5K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row2_col0" class="data row2 col0" >3</td>
      <td id="T_5e37f_row2_col1" class="data row2 col1" ><a href="latitude/commands/filter__puck.sh"><div style="height:100%;width:100%">puck</div></a></td>
      <td id="T_5e37f_row2_col2" class="data row2 col2" >                62.3K</td>
      <td id="T_5e37f_row2_col3" class="data row2 col3" >3</td>
      <td id="T_5e37f_row2_col4" class="data row2 col4" ><a href="latitude/commands/sparse__pinecone_smips.sh"><div style="height:100%;width:100%">pinecone_smips</div></a></td>
      <td id="T_5e37f_row2_col5" class="data row2 col5" >                12.0K</td>
      <td id="T_5e37f_row2_col6" class="data row2 col6" >3</td>
      <td id="T_5e37f_row2_col7" class="data row2 col7" ><a href="latitude/commands/ood__pyanns.sh"><div style="height:100%;width:100%">pyanns</div></a></td>
      <td id="T_5e37f_row2_col8" class="data row2 col8" >                55.5K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row3_col0" class="data row3 col0" >4</td>
      <td id="T_5e37f_row3_col1" class="data row3 col1" ><a href="latitude/commands/filter__parlayivf.sh"><div style="height:100%;width:100%">parlayivf</div></a></td>
      <td id="T_5e37f_row3_col2" class="data row3 col2" >                55.0K</td>
      <td id="T_5e37f_row3_col3" class="data row3 col3" >4</td>
      <td id="T_5e37f_row3_col4" class="data row3 col4" ><a href="latitude/commands/sparse__shnsw.sh"><div style="height:100%;width:100%">shnsw</div></a></td>
      <td id="T_5e37f_row3_col5" class="data row3 col5" >                 8.2K</td>
      <td id="T_5e37f_row3_col6" class="data row3 col6" >4</td>
      <td id="T_5e37f_row3_col7" class="data row3 col7" ><a href="latitude/commands/ood__scann.sh"><div style="height:100%;width:100%">scann</div></a></td>
      <td id="T_5e37f_row3_col8" class="data row3 col8" >                32.3K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row4_col0" class="data row4 col0" >5</td>
      <td id="T_5e37f_row4_col1" class="data row4 col1" ><a href="latitude/commands/filter__wm_filter.sh"><div style="height:100%;width:100%">wm_filter</div></a></td>
      <td id="T_5e37f_row4_col2" class="data row4 col2" >                20.9K</td>
      <td id="T_5e37f_row4_col3" class="data row4 col3" >5</td>
      <td id="T_5e37f_row4_col4" class="data row4 col4" ><a href="latitude/commands/sparse__nle.sh"><div style="height:100%;width:100%">nle</div></a></td>
      <td id="T_5e37f_row4_col5" class="data row4 col5" >                 2.9K</td>
      <td id="T_5e37f_row4_col6" class="data row4 col6" >5</td>
      <td id="T_5e37f_row4_col7" class="data row4 col7" ><a href="latitude/commands/ood__sustech-ood.sh"><div style="height:100%;width:100%">sustech-ood</div></a></td>
      <td id="T_5e37f_row4_col8" class="data row4 col8" >                28.5K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row5_col0" class="data row5 col0" >6</td>
      <td id="T_5e37f_row5_col1" class="data row5 col1" ><a href="latitude/commands/filter__pyanns.sh"><div style="height:100%;width:100%">pyanns</div></a></td>
      <td id="T_5e37f_row5_col2" class="data row5 col2" >                 9.0K</td>
      <td id="T_5e37f_row5_col3" class="data row5 col3" >6</td>
      <td id="T_5e37f_row5_col4" class="data row5 col4" ><a href="latitude/commands/sparse__cufe.sh"><div style="height:100%;width:100%">cufe</div></a></td>
      <td id="T_5e37f_row5_col5" class="data row5 col5" >                 0.1K</td>
      <td id="T_5e37f_row5_col6" class="data row5 col6" >6</td>
      <td id="T_5e37f_row5_col7" class="data row5 col7" ><a href="latitude/commands/ood__mysteryann-dif.sh"><div style="height:100%;width:100%">mysteryann-dif</div></a></td>
      <td id="T_5e37f_row5_col8" class="data row5 col8" >                27.9K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row6_col0" class="data row6 col0" >7</td>
      <td id="T_5e37f_row6_col1" class="data row6 col1" ><a href="latitude/commands/filter__faissplus.sh"><div style="height:100%;width:100%">faissplus</div></a></td>
      <td id="T_5e37f_row6_col2" class="data row6 col2" >                 8.5K</td>
      <td id="T_5e37f_row6_col3" class="data row6 col3" >7</td>
      <td id="T_5e37f_row6_col4" class="data row6 col4" ><a href="latitude/commands/sparse__linscan.sh"><div style="height:100%;width:100%">linscan</div></a></td>
      <td id="T_5e37f_row6_col5" class="data row6 col5" >                 0.1K</td>
      <td id="T_5e37f_row6_col6" class="data row6 col6" >7</td>
      <td id="T_5e37f_row6_col7" class="data row6 col7" ><a href="latitude/commands/ood__mysteryann.sh"><div style="height:100%;width:100%">mysteryann</div></a></td>
      <td id="T_5e37f_row6_col8" class="data row6 col8" >                26.6K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row7_col0" class="data row7 col0" >8</td>
      <td id="T_5e37f_row7_col1" class="data row7 col1" ><a href="latitude/commands/filter__faiss.sh"><div style="height:100%;width:100%">faiss</div></a></td>
      <td id="T_5e37f_row7_col2" class="data row7 col2" >                 7.3K</td>
      <td id="T_5e37f_row7_col3" class="data row7 col3" ><NA></td>
      <td id="T_5e37f_row7_col4" class="data row7 col4" ><a href="latitude/errors/sparse__spmat.txt"><div style="height:100%;width:100%">spmat</div></a></td>
      <td id="T_5e37f_row7_col5" class="data row7 col5" ></td>
      <td id="T_5e37f_row7_col6" class="data row7 col6" >8</td>
      <td id="T_5e37f_row7_col7" class="data row7 col7" ><a href="latitude/commands/ood__vamana.sh"><div style="height:100%;width:100%">vamana</div></a></td>
      <td id="T_5e37f_row7_col8" class="data row7 col8" >                20.0K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row8_col0" class="data row8 col0" >9</td>
      <td id="T_5e37f_row8_col1" class="data row8 col1" ><a href="latitude/commands/filter__cufe.sh"><div style="height:100%;width:100%">cufe</div></a></td>
      <td id="T_5e37f_row8_col2" class="data row8 col2" >                 6.3K</td>
      <td id="T_5e37f_row8_col3" class="data row8 col3" ><NA></td>
      <td id="T_5e37f_row8_col4" class="data row8 col4" ><a href="latitude/errors/sparse__sustech-whu.txt"><div style="height:100%;width:100%">sustech-whu</div></a></td>
      <td id="T_5e37f_row8_col5" class="data row8 col5" ></td>
      <td id="T_5e37f_row8_col6" class="data row8 col6" >9</td>
      <td id="T_5e37f_row8_col7" class="data row8 col7" ><a href="latitude/commands/ood__puck.sh"><div style="height:100%;width:100%">puck</div></a></td>
      <td id="T_5e37f_row8_col8" class="data row8 col8" >                19.0K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row9_col0" class="data row9 col0" ><NA></td>
      <td id="T_5e37f_row9_col1" class="data row9 col1" ><a href="latitude/errors/filter__fdufilterdiskann.txt"><div style="height:100%;width:100%">fdufilterdiskann</div></a></td>
      <td id="T_5e37f_row9_col2" class="data row9 col2" ></td>
      <td id="T_5e37f_row9_col3" class="data row9 col3" ><NA></td>
      <td id="T_5e37f_row9_col4" class="data row9 col4" ></td>
      <td id="T_5e37f_row9_col5" class="data row9 col5" ></td>
      <td id="T_5e37f_row9_col6" class="data row9 col6" >10</td>
      <td id="T_5e37f_row9_col7" class="data row9 col7" ><a href="latitude/commands/ood__ngt.sh"><div style="height:100%;width:100%">ngt</div></a></td>
      <td id="T_5e37f_row9_col8" class="data row9 col8" >                11.9K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row10_col0" class="data row10 col0" ><NA></td>
      <td id="T_5e37f_row10_col1" class="data row10 col1" ><a href="latitude/errors/filter__hwtl_sdu_anns_filter.txt"><div style="height:100%;width:100%">hwtl_sdu_anns_filter</div></a></td>
      <td id="T_5e37f_row10_col2" class="data row10 col2" ></td>
      <td id="T_5e37f_row10_col3" class="data row10 col3" ><NA></td>
      <td id="T_5e37f_row10_col4" class="data row10 col4" ></td>
      <td id="T_5e37f_row10_col5" class="data row10 col5" ></td>
      <td id="T_5e37f_row10_col6" class="data row10 col6" >11</td>
      <td id="T_5e37f_row10_col7" class="data row10 col7" ><a href="latitude/commands/ood__epsearch.sh"><div style="height:100%;width:100%">epsearch</div></a></td>
      <td id="T_5e37f_row10_col8" class="data row10 col8" >                 7.7K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row11_col0" class="data row11 col0" ><NA></td>
      <td id="T_5e37f_row11_col1" class="data row11 col1" ><a href="latitude/errors/filter__dhq.txt"><div style="height:100%;width:100%">dhq</div></a></td>
      <td id="T_5e37f_row11_col2" class="data row11 col2" ></td>
      <td id="T_5e37f_row11_col3" class="data row11 col3" ><NA></td>
      <td id="T_5e37f_row11_col4" class="data row11 col4" ></td>
      <td id="T_5e37f_row11_col5" class="data row11 col5" ></td>
      <td id="T_5e37f_row11_col6" class="data row11 col6" >12</td>
      <td id="T_5e37f_row11_col7" class="data row11 col7" ><a href="latitude/commands/ood__diskann.sh"><div style="height:100%;width:100%">diskann</div></a></td>
      <td id="T_5e37f_row11_col8" class="data row11 col8" >                 6.4K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row12_col0" class="data row12 col0" ><NA></td>
      <td id="T_5e37f_row12_col1" class="data row12 col1" ></td>
      <td id="T_5e37f_row12_col2" class="data row12 col2" ></td>
      <td id="T_5e37f_row12_col3" class="data row12 col3" ><NA></td>
      <td id="T_5e37f_row12_col4" class="data row12 col4" ></td>
      <td id="T_5e37f_row12_col5" class="data row12 col5" ></td>
      <td id="T_5e37f_row12_col6" class="data row12 col6" >13</td>
      <td id="T_5e37f_row12_col7" class="data row12 col7" ><a href="latitude/commands/ood__cufe.sh"><div style="height:100%;width:100%">cufe</div></a></td>
      <td id="T_5e37f_row12_col8" class="data row12 col8" >                 5.4K</td>
    </tr>
    <tr>
      <td id="T_5e37f_row13_col0" class="data row13 col0" ><NA></td>
      <td id="T_5e37f_row13_col1" class="data row13 col1" ></td>
      <td id="T_5e37f_row13_col2" class="data row13 col2" ></td>
      <td id="T_5e37f_row13_col3" class="data row13 col3" ><NA></td>
      <td id="T_5e37f_row13_col4" class="data row13 col4" ></td>
      <td id="T_5e37f_row13_col5" class="data row13 col5" ></td>
      <td id="T_5e37f_row13_col6" class="data row13 col6" ><NA></td>
      <td id="T_5e37f_row13_col7" class="data row13 col7" ><a href="latitude/errors/ood__puck-fizz.txt"><div style="height:100%;width:100%">puck-fizz</div></a></td>
      <td id="T_5e37f_row13_col8" class="data row13 col8" ></td>
    </tr>
  </tbody>
</table>
 

Notes:
* Evaluations were run in late August 2024
* In the table, each track algorithm links to the build and run commmand used (and errors if any).
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
