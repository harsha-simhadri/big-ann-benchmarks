import yaml

def load_runbook(dataset_name, max_pts, runbook_file):
    with open(runbook_file) as fd:
        runbook = yaml.safe_load(fd)[dataset_name]
        i=1
        run_list = []
        while i in runbook:
            entry = runbook.get(i)
            if entry['operation'] not in {'insert', 'delete', 'search', 'replace'}:
                raise Exception('Undefined runbook operation')
            if entry['operation']  in {'insert', 'delete'}:
                if 'start' not in entry:
                    raise Exception('Start not speficied in runbook')
                if 'end' not in entry:
                    raise Exception('End not specified in runbook')
                if entry['start'] < 0 or entry['start'] >= max_pts:
                    raise Exception('Start out of range in runbook')
                if entry['end'] < 0 or entry['end'] > max_pts:
                    raise Exception('End out of range in runbook')
            if entry['operation'] in {'replace'}:
                if 'to_replace_start' not in entry:
                    raise Exception('Start of indices to be replaced not specified in runbook')
                if 'to_replace_end' not in entry:
                    raise Exception('End of indices to be replaced not specified in runbook')
                if 'replace_ids_start' not in entry:
                    raise Exception('Start of indices to replace not specified in runbook')
                if 'replace_ids_end' not in entry:
                    raise Exception('End of indices to replace not specified in runbook')
                if entry['to_replace_start'] < 0 or entry ['to_replace_start'] >= max_pts:
                    raise Exception('Start of indices to be replaced out of range in runbook') 
                if entry['to_replace_end'] < 0 or entry ['to_replace_end'] > max_pts:
                    raise Exception('End of indices to be replaced out of range in runbook') 
                if entry['replace_ids_start'] < 0 or entry ['replace_ids_start'] >= max_pts:
                    raise Exception('Start of indices to replace out of range in runbook') 
                if entry['replace_ids_end'] < 0 or entry ['replace_ids_end'] > max_pts:
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