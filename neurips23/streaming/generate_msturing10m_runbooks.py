import yaml
import os


dataset_name="msturing-10M"

data = {dataset_name: {}}

total_points=10000000

num_points=0
max_num_points=0


max_t=200
# insert 10000000/200 points per step
# start deleting points after 100 steps

t=1
for i in range(max_t): 
    if i>=max_t//2:
        data[dataset_name][t]={
            'operation': 'search',
        }
        t+=1
        data[dataset_name][t]={
            'operation': 'delete',
            'start': (i-max_t//2)*(total_points//max_t),
            'end': (i-max_t//2+1)*(total_points//max_t)
        }
        t+=1
        num_points-=total_points//max_t
    data[dataset_name][t]={
            'operation': 'insert',
            'start': i*(total_points//max_t),
            'end': (i+1)*(total_points//max_t)
        }
    t+=1

    num_points+=total_points//max_t
    max_num_points=max(max_num_points,num_points)

data[dataset_name]["max_pts"]=max_num_points

run_book_name=dataset_name+"_"+"slidingwindow_runbook.yaml"

with open(run_book_name, 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)


