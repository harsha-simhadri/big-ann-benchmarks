import yaml

def load_runbook_congestion(dataset_name, max_pts, runbook_file):


    with open(runbook_file) as fd:
        runbook = yaml.safe_load(fd)[dataset_name]
        i=1
        run_list = []
        while i in runbook:
            entry = runbook.get(i)
            if entry['operation'] not in {'initial','insert', 'delete', 'search', 'replace', 'batch_insert','startHPC', 'endHPC', 'waitPending', 'enableScenario'}:
                raise Exception('Undefined runbook operation')
            if entry['operation'] in {'batch_insert'}:
                if 'start' not in entry:
                    raise Exception('Start not speficied in runbook')
                if 'end' not in entry:
                    raise Exception('End not specified in runbook')
                if 'batchSize' not in entry:
                    raise Exception('batchSize not specified in runbook')
            if entry['operation']  in {'initial','insert', 'delete'}:
                if 'start' not in entry:
                    raise Exception('Start not speficied in runbook')
                if 'end' not in entry:
                    raise Exception('End not specified in runbook')
                if entry['start'] < 0 or entry['start'] >= max_pts:
                    raise Exception('Start out of range in runbook')
                if entry['end'] < 0 or entry['end'] > max_pts:
                    raise Exception('End out of range in runbook')
            if entry['operation'] in {'replace'}:
                if 'tags_start' not in entry:
                    raise Exception('Start of indices to be replaced not specified in runbook')
                if 'tags_end' not in entry:
                    raise Exception('End of indices to be replaced not specified in runbook')
                if 'ids_start' not in entry:
                    raise Exception('Start of indices to replace not specified in runbook')
                if 'ids_end' not in entry:
                    raise Exception('End of indices to replace not specified in runbook')
                if entry['tags_start'] < 0 or entry ['tags_start'] >= max_pts:
                    raise Exception('Start of indices to be replaced out of range in runbook') 
                if entry['tags_end'] < 0 or entry ['tags_end'] > max_pts:
                    print(entry['tags_end'])
                    raise Exception('End of indices to be replaced out of range in runbook') 
                if entry['ids_start'] < 0 or entry ['ids_start'] >= max_pts:
                    raise Exception('Start of indices to replace out of range in runbook') 
                if entry['ids_end'] < 0 or entry ['ids_end'] > max_pts:
                    raise Exception('End of indices to replace out of range in runbook') 
            i += 1
            run_list.append(entry)
        
        max_pts = runbook.get('max_pts')
        if max_pts == None:
            raise Exception('max points not listed for dataset in runbook')
        return max_pts, run_list

def get_gt_url(dataset_name, runbook_file):
    with open(runbook_file) as fd:
        runbook = yaml.safe_load(fd)[dataset_name]
        return runbook['gt_url']