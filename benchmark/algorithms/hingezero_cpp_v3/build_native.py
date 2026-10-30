from pathlib import Path
import hashlib
import json
import os
import platform
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
FLAGS = ['-O3','-march=native','-ffp-contract=off','-std=c++17','-fopenmp','-fPIC','-shared','-DNDEBUG']

def build():
    compiler = shutil.which(os.environ.get('HINGEZERO_CXX','g++'))
    if compiler is None:
        raise RuntimeError('C++ compiler missing. On Pop!_OS run: sudo apt install g++')
    version = subprocess.check_output([compiler,'--version'],text=True).splitlines()[0]
    cpu = ''
    if Path('/proc/cpuinfo').is_file():
        cpu = '\n'.join(x for x in Path('/proc/cpuinfo').read_text().splitlines() if x.startswith(('model name','flags')))
    info = dict(source_sha256=hashlib.sha256((ROOT/'native.cpp').read_bytes()).hexdigest(),
                flags=FLAGS,compiler=version,machine=platform.machine(),cpu_sha256=hashlib.sha256(cpu.encode()).hexdigest())
    library = ROOT/'libhingezero.so'
    metadata = ROOT/'native-build.json'
    if library.is_file() and metadata.is_file() and json.loads(metadata.read_text())==info:
        return library, info
    temporary = ROOT/f'libhingezero.pending.{os.getpid()}.so'
    print('[HZ C++] Compiling native kernel for this CPU...',flush=True)
    try:
        subprocess.run([compiler,*FLAGS,str(ROOT/'native.cpp'),'-o',str(temporary)],check=True)
        os.replace(temporary,library)
        metadata.write_text(json.dumps(info,indent=2)+'\n')
    finally:
        temporary.unlink(missing_ok=True)
    print('[HZ C++] Native kernel ready.',flush=True)
    return library, info

if __name__=='__main__':
    path, info = build()
    print(path)
