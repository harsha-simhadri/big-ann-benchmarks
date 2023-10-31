# Submission for NeurIPS'23 Big-ANN Filter Track of team rubignn

Our method improves the Filtered-DiskANN to support thousands attributes and multi-filter search.

Here is the repo for our complete code: [https://github.com/rutgers-db/ru-bignn-23](https://github.com/rutgers-db/ru-bignn-23)

## Download prebuilt index file

sas_string: `sp=rl&st=2023-10-31T01:24:17Z&se=2023-12-01T10:24:17Z&spr=https&sv=2022-11-02&sr=c&sig=1Gk9nCu3%2FdvHZ4IyldHo161Swb5eCaRs%2FXXCnz5JEaU%3D'`

sal_url: `https://rubignn.blob.core.windows.net/biganncontest-96?sp=rl&st=2023-10-31T01:24:17Z&se=2023-12-01T10:24:17Z&spr=https&sv=2022-11-02&sr=c&sig=1Gk9nCu3%2FdvHZ4IyldHo161Swb5eCaRs%2FXXCnz5JEaU%3D`

blob_prefix: `https://rubignn.blob.core.windows.net/biganncontest-96//index_file_96_R10L70`

command for download index files: 

```
INDEX_FILE_PATH=/home/ubuntu/built_index
azcopy copy 'https://rubignn.blob.core.windows.net/biganncontest-96//index_file_96_R10L70?sp=rl&st=2023-10-31T01:24:17Z&se=2023-12-01T10:24:17Z&spr=https&sv=2022-11-02&sr=c&sig=1Gk9nCu3%2FdvHZ4IyldHo161Swb5eCaRs%2FXXCnz5JEaU%3D' $INDEX_FILE_PATH --recursive
```

## Run Searching on Docker

1. Download the index file

2. Build docker through `python install.py --neurips23track filter --algorithm rubignn`

3. Execute searching in docker:

      run `docker_run_container_search.sh`. **Note: may need to modify the directory path(CONTEST_REPO_PATH and INDEX_FILE_PATH)**

## docker_run_container_search script

This is the main running script to mount the directory, run the container, conduct searching, and generate results

After build the container, it will execute these commands inside the container:

1. `mkdir -p /home/app/results/neurips23/filter/yfcc-10M/10/rubignn`: generate output directory

2. `cd /home/app/ru-bignn-23/build && ./apps/search_contest --index_path_prefix /home/app/index_file/yfcc_R10_L70_SR96_stitched_index_label --query_file /home/app/data/yfcc100M/query.public.100K.u8bin --L 50 80 90 100 110 120 130 --query_filters_file /home/app/data/yfcc100M/query.metadata.public.100K.spmat --result_path_prefix /home/app/results/neurips23/filter/yfcc-10M/10/rubignn/rubignn --runs 5 `: execute the searching, it contain these parameters: 

        `--index_path_prefix` index files directory and prefix;
        `--query_file` is the path for querys;
        `--query_filters_file` is the path for query filters;
        `--result_path_prefix`: path to store the results;
        `--runs`: run every search multiple times to get best search result as `run.py`
        `--search_list`(or `--L`): search parameters.


3. `python3 ../contest-scripts/output_bin_to_hdf5.py /home/app/results/neurips23/filter/yfcc-10M/10/rubignn/rubignn_search_metadata.txt /home/app`: transfer the original bin result to hdf5 results.

## Build Index on Docker

Execute the build script: `docker_run_container_build.sh`.

## Build and search on random-filter-s

Execute the build script: `docker_run_small_test.sh`.
