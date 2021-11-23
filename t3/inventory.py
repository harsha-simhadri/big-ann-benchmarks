import sys
import os


def get_issue(hw_dir_path):
    '''get /etc/issue contents'''
    cmd = "cat /etc/issue >  %s" % ( os.path.join(hw_dir_path, "etc_issue") )
    print("running command=", cmd)
    stream = os.popen(cmd)
    print("result of cmd=", stream.read())

def get_lshw(hw_dir_path):
    '''get output of lshw'''
    cmd = "lshw >  %s" % ( os.path.join(hw_dir_path, "lshw") )
    print("running command=", cmd)
    stream = os.popen(cmd)
    print("result of cmd=", stream.read())

def get_proc_meminfo(hw_dir_path):
    '''get output of /proc/meminfo'''
    cmd = "cat /proc/meminfo >  %s" % ( os.path.join(hw_dir_path, "proc_meminfo") )
    print("running command=", cmd)
    stream = os.popen(cmd)
    print("result of cmd=", stream.read())

def get_df(hw_dir_path):
    '''get output of df -h'''
    cmd = "df -h >  %s" % ( os.path.join(hw_dir_path, "df") )
    print("running command=", cmd)
    stream = os.popen(cmd)
    print("result of cmd=", stream.read())

def get_uname(hw_dir_path):
    '''get output of uname -a'''
    cmd = "uname -a >  %s" % ( os.path.join(hw_dir_path, "uname") )
    print("running command=", cmd)
    stream = os.popen(cmd)
    print("result of cmd=", stream.read())

if __name__ == "__main__":
    hw_dir_path = sys.argv[1]
 
    if os.path.exists( hw_dir_path ):
        print("Error the path already exists->", sys.argv[1])
        sys.exit(1)

    print("Creating directory->", hw_dir_path )
    os.mkdir( hw_dir_path )
   
    get_issue( hw_dir_path )
    get_lshw( hw_dir_path )
    get_proc_meminfo( hw_dir_path )
    get_df( hw_dir_path )
    get_uname( hw_dir_path )
 
