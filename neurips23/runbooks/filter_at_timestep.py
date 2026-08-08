import yaml
import argparse
import struct
import mmap

DATA_TYPE_SIZES = { "float": 4, "int": 4, "uint8": 1 }

# Merges consecutive or overlapping intervals
def merge_intervals(intervals):
    if not intervals:
        return []
    
    intervals.sort()
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged

# Returns a list of active intervals of vectors after a given timestep
def get_vectors_at_timestep(runbook_path, timestep):
    # Only uses the first dataset in the runbook
    with open(runbook_path, "r") as file:
        data = yaml.safe_load(file)
    
    if not data:
        raise Exception("Error: The runbook file is empty or invalid.")
    dataset_name = list(data.keys())[0]
    runbook = data[dataset_name]
    active_intervals = []

    numeric_steps = [int(k) for k in runbook.keys() if str(k).isdigit()]
    
    for step in sorted(numeric_steps):
        if step > timestep:
            break

        entry = runbook[step]
        op_type = entry["operation"]

        if op_type == "insert":
            start, end = entry["start"], entry["end"]
            active_intervals.append((start, end))
            active_intervals = merge_intervals(active_intervals)

        elif op_type == "delete":
            start, end = entry["start"], entry["end"]
            new_intervals = []
            
            for s, e in active_intervals:
                if e <= start or s >= end:
                    new_intervals.append((s, e))
                else:
                    if s < start:
                        new_intervals.append((s, start))
                    if e > end:
                        new_intervals.append((end, e))
            active_intervals = new_intervals

    return active_intervals

# Filters vectors in a binary file based on the active intervals after a given timestep
def filter_vectors_in_file(runbook_path, timestep, datatype, in_path, out_path):
    active_intervals = merge_intervals(get_vectors_at_timestep(runbook_path, timestep))

    print(f"Active vector intervals at time step {timestep}:")
    for start, end in active_intervals:
        print(f"  [{start}, {end})")
    num_output_vectors = sum(end - start for start, end in active_intervals)

    with open(in_path, "rb") as in_file:
        with mmap.mmap(in_file.fileno(), 0, access=mmap.ACCESS_READ) as in_mm:
            num_input_vectors, dims = struct.unpack("II", in_mm[:8])
            print(f"\nOriginal file contains {num_input_vectors} vectors of dimension {dims}.")
            print(f"Output file will contain {num_output_vectors} vectors of dimension {dims}.")
            if active_intervals and active_intervals[-1][1] > num_input_vectors:
                raise Exception(f"Error: The last interval end exceeds the number of vectors in the original file.")

            with open(out_path, "r+b") as out_file:
                total_bytes = 8 + num_output_vectors * dims * DATA_TYPE_SIZES[datatype]
                print(f"Total bytes to write: {total_bytes}")
                out_file.truncate(total_bytes)
                out_file.seek(total_bytes - 1)
                out_file.write(b"\x00")

                with mmap.mmap(out_file.fileno(), total_bytes, access=mmap.ACCESS_WRITE) as out_mm:
                    out_mm[:8] = struct.pack("II", num_output_vectors, dims)

                    offset = 8
                    for interval in active_intervals:
                        bytes_in_interval = (interval[1] - interval[0]) * dims * DATA_TYPE_SIZES[datatype]
                        out_mm[offset : offset + bytes_in_interval] = in_mm[8 + interval[0] * dims * DATA_TYPE_SIZES[datatype] : 8 + interval[1] * dims * DATA_TYPE_SIZES[datatype]]
                        offset += bytes_in_interval

    print(f"Filtered vectors written to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Filter vectors in a binary file based on the state of a runbook after a certain time step."
    )

    parser.add_argument("-r", "--runbook", required=True, help="Path to the runbook (.yaml).")
    parser.add_argument("-t", "--timestep", type=int, required=True, help="Time step to filter vectors by.")
    parser.add_argument("-i", "--infile", required=True, help="Path to the input binary vector file.")
    parser.add_argument("-o", "--outfile", required=True, help="Path to the output filtered binary file.")
    parser.add_argument(
        "-d", "--datatype", choices=["float", "int", "uint8"], default="float",
        help="Data type of vectors: 'float' (4 bytes), 'int' (4 bytes), or 'uint8' (1 byte)."
    )

    args = parser.parse_args()

    filter_vectors_in_file(args.runbook, args.timestep, args.datatype, args.infile, args.outfile)
