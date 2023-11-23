CONTEST_REPO_PATH=/home/ubuntu/big-ann-benchmarks #path to big-ann-benchmarks directory
INDEX_FILE_PATH=/home/ubuntu/built_index #path to index_file directory

mkdir -p $INDEX_FILE_PATH/index_file_docker_build # make sure index file directory exist

docker container run -it  --mount type=bind,src=$CONTEST_REPO_PATH/results,dst=/home/app/results --mount type=bind,src=$INDEX_FILE_PATH/index_file_docker_build,dst=/home/app/index_file --read-only --mount type=bind,src=$CONTEST_REPO_PATH/data,dst=/home/app/data  neurips23-filter-rubignn  /bin/bash -c 'cd /home/app/ru-bignn-23/build &&
./apps/base_label_to_label_file /home/app/data/random-filter100000/data_metadata_100000_50 /home/app/index_file/label_file_base_random-filter-s_filter.txt && 
./apps/build_stitched_index --data_type float --data_path /home/app/data/random-filter100000/data_100000_50 --index_path_prefix /home/app/index_file/random-filter-s_R16_L80_SR96_stitched_index_label -R 16 -L 80 --stitched_R 96 --alpha 1.2 --label_file /home/app/index_file/label_file_base_random-filter-s_filter.txt --universal_label 0'



docker container run -it  --mount type=bind,src=$CONTEST_REPO_PATH/results,dst=/home/app/results --mount type=bind,src=$INDEX_FILE_PATH/index_file_docker_build,dst=/home/app/index_file --read-only --mount type=bind,src=$CONTEST_REPO_PATH/data,dst=/home/app/data  neurips23-filter-rubignn  /bin/bash -c 'mkdir -p /home/app/results/neurips23/filter/random-filter-s/10/rubignn && 
cd /home/app/ru-bignn-23/build &&
./apps/search_contest --index_path_prefix /home/app/index_file/random-filter-s_R16_L80_SR96_stitched_index_label --query_file /home/app/data/random-filter100000/queries_1000_50 --search_list 50 80 100 --query_filters_file /home/app/data/random-filter100000/queries_metadata_100000_50 --result_path_prefix /home/app/results/neurips23/filter/random-filter-s/10/rubignn/rubignn --runs 2 --dataset random-filter-s --data_type float &&
python3 ../contest-scripts/output_bin_to_hdf5.py /home/app/results/neurips23/filter/random-filter-s/10/rubignn/rubignn_search_metadata.txt /home/app'