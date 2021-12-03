import os
import argparse
import hashlib as hash
import sys

BLOCKSIZE = 65536

def collect_files( path ):
    '''recursively get all files under a directory'''
    #print("path=",path)
    if os.path.isfile( path ):
        # print("is file", path)
        return [ path ]
    elif os.path.isdir( path ):
        # print("is dir", path )
        files = []
        items = os.listdir(path)
        # print("items=",items)
        for item in items:
            pth = os.path.join( path, item ) 
            # print("pth=",pth)
            files += collect_files(pth)
        return files
    else:
        print("what is this?", path, os.path.exists(path), os.path.isfile(path), os.path.isdir(path))
        sys.exit(1)

def get_signature( file ):
    '''produce a SHA256 hash of a (possible really large) file'''
    sha = hash.sha256()
    try:
        with open(file, 'rb') as kali_file:
            file_buffer = kali_file.read(BLOCKSIZE)
            while len(file_buffer) > 0:
                sha.update(file_buffer)
                file_buffer = kali_file.read(BLOCKSIZE)
        return sha.hexdigest()
    except:
        print("Problem with file", file)
        return "-1"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        help='Path to the output file',
        required=True)
    parser.add_argument(
        '--path',
        help='Path to the file which contains a file or directory on each line to process',
        required=True)
    args = parser.parse_args()

    # get the input paths
    f = open( args.path )
    paths =  [ ln.strip() for ln in f.readlines() ]
    f.close()
    print("Input paths", paths)

    # collect all the files for signature
    files = []
    for p in paths:
        files = files + collect_files( p  )
    if len(files)==0:
        print("No files for signatures.")
        sys.exit(1)
    print("Found files for signatures =", files)

    # Compute the signatures for the file list
    print("Computing signatures for the files...")
    sigs = {}
    for idx, file in enumerate(files):
        print("Getting signature for file (%d/%d)" % (idx+1, len(files)), file)
        sig = get_signature( file )
        #print("file %s sig= %s" % (file, sig))
        sigs[file] = sig

    # Write the output file
    wf = open(args.output,"w")
    for file in files:
        sig = sigs[file]
        wf.write("%s,%s\n" % ( sig, file ) )
    wf.flush()
    wf.close()
    print("Wrote output file at", args.output )

    
