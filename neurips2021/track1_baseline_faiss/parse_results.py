"""
Parse log files from baseline_faiss.py

"""
import os
import numpy as np



def parse_result_file(fname):
    # print fname
    st = 0
    res = []
    keys = []
    stats = {}
    stats['run_version'] = fname[-8]
    indexkey = None
    for l in open(fname):
        if l.startswith("srun:"):
            # looks like a crash...
            if indexkey is None:
                raise RuntimeError("instant crash")
            break
        elif st == 0:
            if l.startswith("dataset in dimension"):
                fi = l.split()
                stats["d"] = int(fi[3][:-1])
                stats["nq"] = int(fi[9])
                stats["nb"] = int(fi[11])
                stats["nt"] = int(fi[13])
            if l.startswith('index size on disk:'):
                stats['index_size'] = int(l.split()[-1])
            if l.startswith('current RSS:'):
                stats['RSS'] = int(l.split()[-1])
            if l.startswith('precomputed tables size:'):
                stats['tables_size'] = int(l.split()[-1])
            if l.startswith('Setting nb of threads to'):
                stats['n_threads'] = int(l.split()[-1])
            if l.startswith('  add in'):
                stats['add_time'] = float(l.split()[-2])
            if l.startswith('args:'):
                args = eval(l[l.find(' '):])
                indexkey = args.indexkey
            if l.startswith('build index, key='):
                indexkey = l.split()[-1]
            elif "time(ms/q)" in l:
                # result header
                if 'R@1   R@10  R@100' in l:
                    stats["measure"] = "recall"
                    stats["ranks"] = [1, 10, 100]
                elif 'I@1   I@10  I@100' in l:
                    stats["measure"] = "inter"
                    stats["ranks"] = [1, 10, 100]
                elif 'inter@' in l:
                    stats["measure"] = "inter"
                    fi = l.split()
                    if fi[1] == "inter@":
                        rank = int(fi[2])
                    else:
                        rank = int(fi[1][len("inter@"):])
                    stats["ranks"] = [rank]
                elif 'AP' in l:
                    stats["measure"] = "average_precision"
                else:
                    assert False
                st = 1
            elif 'index size on disk:' in l:
                stats["index_size"] = int(l.split()[-1])
        elif st == 1:
            st = 2
        elif st == 2:
            fi = l.split()
            if l[0] == " ":
                # means there are 0 parameters
                fi = [""] + fi
            keys.append(fi[0])
            if len(fi[1:]) > 0:
                res.append([float(x) for x in fi[1:]])
    return indexkey, np.array(res), keys, stats


def find_latest_version(fname):
    """ all log files are called
    XX.a.log
    XX.b.log

    Where XX is the experiment id and a, b... are versions.
    The version is used when the same experiment needs to be
    redone because it failed. This function returns the latest version
    """
    assert fname.endswith(".log")
    pref = fname[:-5]
    lv = ""
    for suf in "abcdefghijklmnopqrs":
        fname = pref + suf + '.log'
        if os.path.exists(fname):
            lv = fname
    assert lv
    return lv