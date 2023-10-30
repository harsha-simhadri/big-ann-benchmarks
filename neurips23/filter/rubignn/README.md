# Submission for NeurIPS'23 Big-ANN Filter Track of team rubignn

Our method improves the Filtered-DiskANN to support thousands attributes and multi-filter search.

Here is the repo for our complete code: [https://github.com/rutgers-db/ru-bignn-23](https://github.com/rutgers-db/ru-bignn-23)


## Download prebuilt index file

sas_string: `sp=rl&st=2023-10-30T07:40:31Z&se=2023-12-01T16:40:31Z&spr=https&sv=2022-11-02&sr=c&sig=Xj6pXXVsTMAJ2K7sHX0H3qyqr5E%2BnN%2FOyvczZ3%2Bz2fo%3D`

sal_url: `https://rubignn.blob.core.windows.net/biganncontest-96?sp=rl&st=2023-10-30T07:40:31Z&se=2023-12-01T16:40:31Z&spr=https&sv=2022-11-02&sr=c&sig=Xj6pXXVsTMAJ2K7sHX0H3qyqr5E%2BnN%2FOyvczZ3%2Bz2fo%3D`

blob_prefix: `https://rubignn.blob.core.windows.net/biganncontest-96/index_file_96/`

command for download index files: 

```
INDEX_FILE_PATH=/home/ubuntu/built_index
azcopy copy 'https://rubignn.blob.core.windows.net/biganncontest-96/index_file_96?sp=rl&st=2023-10-30T07:40:31Z&se=2023-12-01T16:40:31Z&spr=https&sv=2022-11-02&sr=c&sig=Xj6pXXVsTMAJ2K7sHX0H3qyqr5E%2BnN%2FOyvczZ3%2Bz2fo%3D' 'INDEX_FILE_PATH' --recursive
```

## Run Searching on Docker

1. Download the index file

2. Build docker through `python install.py --neurips23track filter --algorithm rubignn`

3. Execute searching in docker:

      run `docker_run_container_search.sh`. **Note: may need to modify the directory path(CONTEST_REPO_PATH and INDEX_FILE_PATH)**

TODO: Transfer the result to hdf5 file

TODO: ADD Test on small dataset
