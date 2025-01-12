from smtplib import quotedata

from benchmark.datasets import DATASETS, RandomDS, RandomRangeDS, RandomPlus
import re
import os
import yaml


def normalize_dataset_name(dataset_name):
    return re.sub(r"\(.*\)", "", dataset_name)

def parse_dataset(args):
    if args.dataset in DATASETS:
        dataset = DATASETS[args.dataset]()

        streaming_runbook_file, congestion_runbook_file = get_runbook_paths(args)
        update_runbook_for_dataset(args, dataset.nb, streaming_runbook_file, congestion_runbook_file)

        return dataset

    elif args.dataset.startswith("random-plus"):
        return custom_random_plus(args)

    elif args.dataset.startswith("random-xs") or args.dataset.startswith("random-s"):
        return custom_random_ds(args)

    elif args.dataset.startswith("random-range-xs") or args.dataset.startswith("random-range-s"):
        return custom_random_range_ds(args)

    else:
        raise ValueError(f"Dataset: {args.dataset} not found!")


def custom_random_plus(args):
    dataset_name = args.dataset
    match = re.match(r"random-plus\((\d+),(\d+),(\d+)(?:,(\d*))?(?:,(\d*))?(?:,(\d*))?(?:,(\d*))?(?:,(\S*))?\)", dataset_name)
    if match:
        nb, nq, d = map(int, match.groups()[:3])
        seed = int(match.group(4)) if match.group(4) else 7758258
        drift_position = float(match.group(5)) if match.group(5) else 0
        drift_offset = float(match.group(6)) if match.group(6) else 0.5
        query_noise_fraction = float(match.group(7)) if match.group(7) else 0
        basedir = match.group(8) if match.group(8) else "randomplus"
        add_dataset(dataset_name, f'RandomPlus({nb}, {nq}, {d}, {seed}, {drift_position}, {drift_offset}, {query_noise_fraction}, "{basedir}")')
        DATASETS[dataset_name] = lambda : RandomPlus(nb, nq, d, seed, drift_position, drift_offset, query_noise_fraction, basedir)

        streaming_runbook_file, congestion_runbook_file = get_runbook_paths(args)
        update_runbook_for_dataset(args, nb, streaming_runbook_file, congestion_runbook_file)

        return RandomPlus(nb, nq, d, seed, drift_position, drift_offset, query_noise_fraction, basedir)
    else:
        raise ValueError(f"Invalid dataset format: {dataset_name}")


def custom_random_ds(args):
    dataset_name = args.dataset
    match = re.match(r"(random-xs|random-s)\((\d+),(\d+),(\d+)(?:,(\S+))?\)", dataset_name)
    if match:
        nb, nq, d = map(int, match.groups()[1:4])
        basedir = match.group(5) if match.group(5) else "random"
        add_dataset(dataset_name, f'RandomDS({nb}, {nq}, {d}, "{basedir}")')
        DATASETS[dataset_name] = lambda: RandomDS(nb, nq, d, basedir)

        streaming_runbook_file, congestion_runbook_file = get_runbook_paths(args)
        update_runbook_for_dataset(args, nb, streaming_runbook_file, congestion_runbook_file)

        return RandomDS(nb, nq, d, basedir)
    else:
        raise ValueError(f"Invalid dataset format for random-xs or random-s: {dataset_name}")


def custom_random_range_ds(args):
    dataset_name = args.dataset
    match = re.match(r"(random-range-xs|random-range-s)\((\d+),(\d+),(\d+)\)", dataset_name)
    if match:
        nb, nq, d = map(int, match.groups()[1:4])
        add_dataset(dataset_name, f'RandomRangeDS({nb}, {nq}, {d})')
        DATASETS[dataset_name] = lambda: RandomRangeDS(nb, nq, d)

        streaming_runbook_file, congestion_runbook_file = get_runbook_paths(args)
        update_runbook_for_dataset(args, nb, streaming_runbook_file, congestion_runbook_file)

        return RandomRangeDS(nb, nq, d)
    else:
        raise ValueError(f"Invalid dataset format for random-range-xs or random-range-s: {dataset_name}")


def add_dataset(dataset_name, dataset_func, file_path='benchmark/datasets.py'):
    # Write to the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    insert_position = -1
    for i, line in enumerate(lines):
        if 'DATASETS =' in line:
            insert_position = i
            break

    if insert_position == -1:
        raise RuntimeError(f"{file_path} doesn't contain a 'DATASETS =' assignment")

    new_dataset_code = f"    '{dataset_name}': lambda : {dataset_func},\n"
    lines.insert(insert_position + 1, new_dataset_code)

    with open(file_path, 'w') as file:
        file.writelines(lines)

    print(f"Successfully added {dataset_name} to {file_path}")


def generate_Streaming_runbook_yaml(dataset, max_pts, runbook_file='neurips23/runbooks/streaming/simple_runbook.yaml'):

    def custom_operation_representer(dumper, value):
        quoted_operations = ["insert", "search", "delete", "none"]
        if value in quoted_operations:
            return dumper.represent_scalar('tag:yaml.org,2002:str', value, style='"')
        else:
            return dumper.represent_scalar('tag:yaml.org,2002:str', value)

    yaml.add_representer(str, custom_operation_representer)

    dataset_info = {
        "max_pts": max_pts,
        1: {"operation": "insert",
            "start": 0,
            "end": max_pts
        },
        2: {"operation": "search"},
        3: {"operation": "delete",
            "start": 0,
            "end": max_pts // 2
        },
        4: {"operation": "search"},
        5: {"operation": "insert",
            "start": 0,
            "end": max_pts // 2
        },
        6: {"operation": "search"},
        "gt_url": "none"
    }

    with open(runbook_file, "a") as f:
        f.write("\n")
        yaml.dump({dataset: dataset_info}, f, default_flow_style=False, sort_keys=False)

    print(f"Streaming Runbook updated successfully for dataset: {dataset}")


def generate_congestion_runbook_yaml(dataset, max_pts, runbook_file, batch_size, event_rate):

    def custom_operation_representer(dumper, value):
        quoted_operations = ["search", "startHPC", "initial", "batch_insert", "waitPending", "delete", "endHPC", "none"]
        if value in quoted_operations:
            return dumper.represent_scalar('tag:yaml.org,2002:str', value, style='"')
        else:
            return dumper.represent_scalar('tag:yaml.org,2002:str', value)

    yaml.add_representer(str, custom_operation_representer)

    dataset_info = {
        "max_pts": max_pts,
        1: {"operation": "startHPC"},
        2: {"operation": "initial",
            "start": 0,
            "end": 5000
        },
        3: {
            "operation": "batch_insert",
            "start": 5000,
            "end": max_pts,
            "batchSize": batch_size,
            "eventRate": event_rate,
        },
        4: {"operation": "search"},
        5: {"operation": "waitPending"},
        6: {"operation": "delete",
            "start": 0,
            "end": max_pts // 2
        },
        7: {"operation": "waitPending"},
        8: {"operation": "search"},
        9: {
            "operation": "batch_insert",
            "start": 0,
            "end": max_pts // 2,
            "batchSize": batch_size,
            "eventRate": event_rate,
        },
        10: {"operation": "waitPending"},
        11: {"operation": "search"},
        12: {"operation": "endHPC"},
        "gt_url": "none",
    }

    with open(runbook_file, "a") as f:
        f.write("\n")
        yaml.dump({dataset: dataset_info}, f, default_flow_style=False, sort_keys=False)

    print(f"Congestion Runbook updated successfully for dataset: {dataset}")


def read_runbook(runbook_file):
    try:
        with open(runbook_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}


def is_dataset_in_runbook(runbook_data, dataset):
    return dataset in runbook_data


def update_streaming_runbook(dataset, max_pts, runbook_file):
    runbook_data = read_runbook(runbook_file)

    if is_dataset_in_runbook(runbook_data, dataset):
        print(f"Dataset '{dataset}' already exists in the streaming runbook.")
    else:
        generate_Streaming_runbook_yaml(dataset, max_pts, runbook_file)


def update_congestion_runbook(dataset, max_pts, runbook_file, batch_size, event_rate):
    runbook_data = read_runbook(runbook_file)

    if is_dataset_in_runbook(runbook_data, dataset):
        print(f"Dataset '{dataset}' already exists in the congestion runbook.")
    else:
        generate_congestion_runbook_yaml(dataset, max_pts, runbook_file, batch_size, event_rate)

def update_runbook_for_dataset(args,
                               max_pts,
                               streaming_runbook_file='neurips23/runbooks/streaming/simple_runbook.yaml',
                               congestion_runbook_file='neurips23/runbooks/congestion/simple_runbook.yaml',):
    update_streaming_runbook(args.dataset, max_pts, streaming_runbook_file)

    if args.batchsize is not None and args.eventrate is not None:
        if hasattr(args, 'neurips23track'):
            if args.neurips23track == 'congestion':
                update_congestion_runbook(args.dataset, max_pts, congestion_runbook_file, args.batchsize, args.eventrate)
        else:
            update_congestion_runbook(args.dataset, max_pts, congestion_runbook_file, args.batchsize, args.eventrate)

def get_runbook_paths(args):
    default_streaming_path = 'neurips23/runbooks/streaming/simple_runbook.yaml'
    default_congestion_path = 'neurips23/runbooks/congestion/simple_runbook.yaml'

    if hasattr(args, 'runbook_path'):
        if args.neurips23track == 'congestion':
            return default_streaming_path, args.runbook_path
        else:
            return args.runbook_path, default_congestion_path
    else:
        return default_streaming_path, default_congestion_path