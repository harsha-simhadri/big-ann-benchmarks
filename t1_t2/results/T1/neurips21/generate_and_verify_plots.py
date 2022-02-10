import glob
import os


fns = glob.glob(os.path.join(".", "*.tex.template"))

missing = []

for fn in fns:
    with open(fn) as f:
        with open(fn[:-9], "w") as g:
            for line in f:
                if "%%PROCESS" not in line:
                    g.write(line)
                else:
                    line = line.strip()[10:]
                    label, attributes = None, None
                    if "[" in line:
                        other, attributes = line.split("[")
                        attributes = attributes[:-1]
                        gn, label = other.split()
                    else:
                        if " " in line:
                            gn, *label = line.split()
                            label = " ".join(label)
                        else:
                            gn = line
                    if os.path.exists(os.path.join(".", gn)):
                        s = "\\addplot"
                        if attributes:
                            s += "[" + attributes + "]"
                        s += " table {" + gn + "};"
                        g.write(s + "\n")
                        if label:
                            g.write("\\addlegendentry{%s};\n" % label)
                    else:
                        missing.append(gn)

print("Done processing all files. %d files were missing." % len(missing))

if len(missing) > 0:

    print(missing)
    missing_exps = set()
    for fn in missing:
        res = fn.split("/")[-1].split("_")
        if len(res) == 5:
            ds, count, algo, _, _ = res
            if not algo.isdigit():
                missing_exps.add((ds, algo, count))

    print("The following experiments have missing results:")
    for ds, algo, count in sorted(missing_exps, key=lambda x:x[0]):
        print("python3 run.py --algorithm %s --dataset %s --count %s" % (ds, algo, count))



