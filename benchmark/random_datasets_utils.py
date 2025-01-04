from benchmark.datasets import DATASETS, RandomDS, RandomRangeDS, RandomPlus
import re
import os
import yaml


def normalize_dataset_name(dataset_name):
    return re.sub(r"\(.*\)", "", dataset_name)

def parse_dataset(args):
    if args.dataset in DATASETS:
        dataset = DATASETS[args.dataset]()
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
        if hasattr(args, 'runbook_path'):
            generate_runbook_yaml(dataset_name, nb, args.runbook_path)
        else:
            generate_runbook_yaml(dataset_name, nb, 'neurips23/runbooks/simple_runbook.yaml')
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
        if hasattr(args, 'runbook_path'):
            generate_runbook_yaml(dataset_name, nb, args.runbook_path)
        else:
            generate_runbook_yaml(dataset_name, nb, 'neurips23/runbooks/simple_runbook.yaml')
        return RandomDS(nb, nq, d, basedir)
    else:
        raise ValueError(f"Invalid dataset format for random-xs or random-s: {dataset_name}")


def custom_random_range_ds(args):
    dataset_name = args.dataset
    match = re.match(r"(random-range-xs|random-range-s)\((\d+),(\d+),(\d+)\)", dataset_name)
    if match:
        nb, nq, d = map(int, match.groups()[1:4])
        add_dataset(dataset_name, f'RandomRangeDS({nb}, {nq}, {d})')
        if hasattr(args, 'runbook_path'):
            generate_runbook_yaml(dataset_name, nb, args.runbook_path)
        else:
            generate_runbook_yaml(dataset_name, nb, 'neurips23/runbooks/simple_runbook.yaml')
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


def generate_runbook_yaml(dataset, max_pts, runbook_file):
    if os.path.exists(runbook_file):
        with open(runbook_file, "r") as f:
            runbook_content = yaml.safe_load(f) or {}
    else:
        runbook_content = {}

    dataset_info = {
        "max_pts": max_pts,
        1: {"operation": "insert", "start": 0, "end": max_pts},
        2: {"operation": "search"},
        3: {"operation": "delete", "start": 0, "end": max_pts // 2},
        4: {"operation": "search"},
        5: {"operation": "insert", "start": 0, "end": max_pts // 2},
        6: {"operation": "search"},
        "gt_url": "https://comp21storage.z5.web.core.windows.net/comp23/str_gt/random10000/10000/simple_runbook.yaml"
    }

    runbook_content[dataset] = dataset_info
    print(runbook_file)
    with open(runbook_file, "w") as f:
        yaml.dump(runbook_content, f, default_flow_style=False, sort_keys=False)

    print(f"Runbook updated successfully for dataset: {dataset}")