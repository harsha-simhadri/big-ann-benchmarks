
import sys
from subprocess import Popen
import subprocess

if sys.argv[-1] == "parent":
    p = Popen(["python", __file__, "child"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1,
              universal_newlines=True)
    p.stdin.write("echo 1\n")
    line = p.stdout.readline()
    print(1, line.strip(), flush=True)
    p.stdin.write("echo 2\n")
    line = p.stdout.readline()
    print(2, line.strip(), flush=True)

elif sys.argv[-1] == "child":
    line = sys.stdin.readline()
    print(f"Received {line.strip()}", flush=True)
    line = sys.stdin.readline()
    print(f"Received {line.strip()}", flush=True)
