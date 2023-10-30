CONTEST_REPO_PATH=/home/ubuntu/big-ann-benchmarks #path to big-ann-benchmarks directory
INDEX_FILE_PATH=/home/ubuntu/built_index #path to index_file directory

docker container run -it  --mount type=bind,src=$CONTEST_REPO_PATH/results,dst=/home/app/results --mount type=bind,src=$INDEX_FILE_PATH/index_file_96,dst=/home/app/index_file --read-only --mount type=bind,src=$CONTEST_REPO_PATH/data,dst=/home/app/data  neurips23-filter-rubignn  /bin/bash -c 'mkdir -p /home/app/results/neurips23/filter/yfcc-10M/10/rubignn && 
cd /home/app/ru-bignn-23/build &&
./apps/search_contest --index_path_prefix /home/app/index_file/yfcc_R16_L80_SR96_stitched_index_label --query_file /home/app/data/yfcc100M/query.public.100K.u8bin --search_list 80 90 95 100 105 110 120 130 --query_filters_file /home/app/data/yfcc100M/query.metadata.public.100K.spmat --result_path_prefix /home/app/results/neurips23/filter/yfcc-10M/10/rubignn/rubignn --runs 5 &&
python3 ../contest-scripts/output_bin_to_hdf5.py /home/app/results/neurips23/filter/yfcc-10M/10/rubignn/rubignn_search_metadata.txt /home/app'