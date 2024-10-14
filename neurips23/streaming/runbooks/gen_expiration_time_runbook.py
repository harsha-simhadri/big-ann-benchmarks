import yaml
import os
import random

'''
dataset_name: dataset key as specified in benchmark/datasets.py
dataset_size: size of datasets
max_t: number of timesteps
runbook_filename: name to save the runbook to
ratios: tuple of three numbers indicating proportion of deletes/replaces assigned to each timestep
timesteps: how long to wait before deleting for each ratio
seed: seed given to random generator
do_replace: whether to include replace in runbook or not
'''
def gen_exp_time_runbook(dataset_name, dataset_size, max_t, runbook_filename, ratios, timesteps, seed = 0, do_replace = False):
    random.seed(seed)
    data = {dataset_name: {}}

    max_num_points=0
    num_points=0

    batch_size = dataset_size//max_t
    to_delete=[[] for _ in range(max_t)]
    to_replace=[[] for _ in range(max_t)]

    t=1

    for i in range(max_t): 
        if do_replace:
            fraction = random.uniform(.5, .9)
        else:
            fraction = 1.0
        end = int(fraction*(i+1)*batch_size)
        ids_start = end
        ids_end = (i+1)*batch_size
        tags_start = i*batch_size
        tags_end = tags_start + (ids_end - ids_start)
        replace_info = (tags_start, tags_end, ids_start, ids_end)
        delete_info = (tags_start, end)
        data[dataset_name][t]={
            'operation': 'insert',
            'start': i*(batch_size),
            'end': end
        }
        t+=1

        num_points+=batch_size

        max_num_points=max(max_num_points,num_points)

        
        data_type = random.randint(0, ratios[2])
        if data_type <= ratios[0]:
            pass
        elif data_type > ratios[0] and data_type < ratios[1]:
            if (i+timesteps[1] < max_t):
                to_delete[i+timesteps[1]].append(delete_info)
        else:
            if (i+timesteps[2] < max_t):
                to_delete[i+timesteps[2]].append(delete_info)

        

        if do_replace:
            if data_type <= ratios[0]:
                remaining_steps = (max_t - t)//2
                to_replace[i+remaining_steps].append(replace_info)
                # with probability 1/19, the points get replaced at t_max-t/2 steps
            elif data_type > ratios[0] and data_type < ratios[1]:
                if (i + timesteps[1]//2 < max_t):
                    to_replace[i+timesteps[1]//2].append(replace_info)
                # with probability 3/19, the points get replaced after 50 steps
            else:
                if (i + timesteps[2]//2 < max_t):
                    to_replace[i+timesteps[2]//2].append(replace_info)
                # with probability 15/19, the points get replaced after 10 steps

        for (start, end) in to_delete[i]:
            data[dataset_name][t]={
                'operation': 'delete',
                'start': start,
                'end': end
            }
            t+=1
            num_points-=batch_size
        
        for (tags_start, tags_end, ids_start, ids_end) in to_replace[i]:
            data[dataset_name][t] ={
                'operation' : 'replace',
                'tags_start': tags_start,
                'tags_end': tags_end,
                'ids_start': ids_start,
                'ids_end': ids_end
            }
            t += 1

        data[dataset_name][t]={
            'operation': 'search',
        }
        t+=1

    data[dataset_name]["max_pts"]=max_num_points

    with open(runbook_filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

ratios = (0, 4, 18)
timesteps = (0, 100, 20)
seed = 809
dataset_file = 'wikipedia-35M_expirationtime_runbook.yaml'
dataset_name = 'wikipedia-35M'
dataset_size = 35000000
max_t = 350
gen_exp_time_runbook(dataset_name, dataset_size, max_t, dataset_file, ratios, timesteps, seed, False)

ratios = (0, 4, 18)
timesteps = (0, 100, 20)
seed = 1232
dataset_file = 'wikipedia-1M_expiration_time_runbook.yaml'
dataset_name = 'wikipedia-1M'
dataset_size = 1000000
max_t = 100
gen_exp_time_runbook(dataset_name, dataset_size, max_t, dataset_file, ratios, timesteps, seed, False)

ratios = (0, 4, 18)
timesteps = (0, 100, 20)
seed = 809
dataset_file = 'wikipedia-35M_expiration_time_replace_runbook.yaml'
dataset_name = 'wikipedia-35M'
dataset_size = 35000000
max_t = 350
gen_exp_time_runbook(dataset_name, dataset_size, max_t, dataset_file, ratios, timesteps, seed, True)

ratios = (0, 6, 25)
timesteps = (0, 200, 50)
seed = 809
dataset_file = 'msmarco-100M_expirationtime_runbook.yaml'
dataset_name = 'msmarco-100M'
dataset_size = 101070374
max_t = 1000
gen_exp_time_runbook(dataset_name, dataset_size, max_t, dataset_file, ratios, timesteps, seed, False)

