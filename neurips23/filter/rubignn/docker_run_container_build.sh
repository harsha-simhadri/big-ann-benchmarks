CONTEST_REPO_PATH=/home/ubuntu/big-ann-benchmarks #path to big-ann-benchmarks directory
INDEX_FILE_PATH=/home/ubuntu/built_index #path to index_file directory

docker container run -it  --mount type=bind,src=$CONTEST_REPO_PATH/results,dst=/home/app/results --mount type=bind,src=$INDEX_FILE_PATH/index_file_docker_build,dst=/home/app/index_file --read-only --mount type=bind,src=$CONTEST_REPO_PATH/data,dst=/home/app/data  neurips23-filter-rubignn  /bin/bash -c 'mkdir -p /home/app/index_file/index_file_docker_build && 
cd /home/app/ru-bignn-23/build &&
./apps/base_label_to_label_file /home/app/data/yfcc100M/base.metadata.10M.spmat /home/app/index_file/label_file_base_yfcc10m_filter.txt &&
./apps/build_stitched_index --data_type uint8 --data_path /home/app/data/yfcc100M/base.10M.u8bin.crop_nb_10000000 --index_path_prefix home/app/index_file/index_file_docker_build/yfcc_R16_L80_SR96_stitched_index_label -R 16 -L 80 --stitched_R 96 --alpha 1.2 --label_file /home/app/index_file/label_file_base_yfcc10m_filter.txt --universal_label 0'