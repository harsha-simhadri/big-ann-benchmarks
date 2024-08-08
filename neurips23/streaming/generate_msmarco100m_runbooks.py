import yaml
import os
import random

dataset_name="msmarco-100M"

total_points=101070374
max_t=1000
# insert the points in 1000 steps

data = {dataset_name: {}}

max_num_points=0
num_points=0

to_delete=[[] for _ in range(max_t+300)]

t=1
for i in range(max_t): 

    data[dataset_name][t]={
        'operation': 'insert',
        'start': i*(total_points//max_t),
        'end': (i+1)*(total_points//max_t)
    }
    t+=1

    num_points+=total_points//max_t

    max_num_points=max(max_num_points,num_points)

    data_type = random.randint(0, 25)
    if data_type == 0:
        pass
        # with probability 1/26, the inserted point always stay in the index
    elif data_type >0 and data_type < 6:
        to_delete[i+200].append(i)
        # with probability 5/26, the inserted point always stay in the index for 200 steps
    elif data_type >=6 and data_type:
        to_delete[i+50].append(i)
        # with probability 20/26, the inserted point always stay in the index for 50 steps


    for x in to_delete[i]:
        data[dataset_name][t]={
            'operation': 'delete',
            'start': x*(total_points//max_t),
            'end': (x+1)*(total_points//max_t)
        }
        t+=1
        num_points-=total_points//max_t

    data[dataset_name][t]={
        'operation': 'search',
    }
    t+=1


data[dataset_name]["max_pts"]=max_num_points

run_book_name=dataset_name+"_"+"expirationtime_runbook.yaml"

with open(run_book_name, 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)

