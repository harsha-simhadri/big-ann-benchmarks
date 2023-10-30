# Submission for NeurIPS'23 Big-ANN Filter Track of team rubignn

Our method improves the Filtered-DiskANN to support thousands attributes and multi-filter search.

Here is the repo for our complete code: [https://github.com/rutgers-db/ru-bignn-23](https://github.com/rutgers-db/ru-bignn-23)

## Run Searching on Docker

1. Download the index file (TODO: script for download)

2. Build docker through `python install.py --neurips23track filter --algorithm rubignn`

3. Execute searching in docker:

      run `docker_run_container_search.sh`. **Note: may need to modify the directory path(CONTEST_REPO_PATH and INDEX_FILE_PATH)**

TODO: Transfer the result to hdf5 file