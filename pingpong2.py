
import sys
from subprocess import Popen
import subprocess

if sys.argv[-1] == "parent":
    p = Popen(["python", __file__, "child"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1,
              universal_newlines=True)
    for i in range(10):
        p.stdin.write(f"ping {i}\n")
        response = p.stdout.readline().strip()
        print(i, response, flush=True)
    p.stdin.write("done\n")
elif sys.argv[-1] == "child":
    while True:
        msg = sys.stdin.readline().strip()
        if msg == "done":
            sys.stderr.write("exiting\n")
            sys.stderr.flush()
            sys.exit(0)
        else:
            print(f"ack: {msg}", flush=True)
