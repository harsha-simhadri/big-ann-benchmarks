import yaml
import os
import random

dataset_name="wikipedia-35M"

total_points=35000000
max_t=350


data = {dataset_name: {}}

max_num_points=0
num_points=0

to_delete=[[] for _ in range(max_t+100)]

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

    data_type = random.randint(0, 18)
    if data_type == 0:
        pass
        # with probability 1/19, the points added always stay in the index
    elif data_type >0 and data_type < 4:
        to_delete[i+100].append(i)
        # with probability 3/19, the points added stay in the index for 100 steps
    else:
        to_delete[i+20].append(i)
        # with probability 15/19, the points added stay in the index for 20 steps

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
