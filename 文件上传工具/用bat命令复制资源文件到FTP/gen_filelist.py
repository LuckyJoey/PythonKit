import os
import hashlib
import sys

if len(sys.argv) < 2:
    exit(0)

dirpath = sys.argv[1]
filelist = open(os.path.join(dirpath, 'filelist.json'), 'w')
filelist.write('{')
start_write = True
for root, dirs, files in os.walk(dirpath):
    for f in files:
        if f == 'filelist.json':
            continue
        
        if start_write:
            start_write = False
        else:
            filelist.write(',')

        fp = open(os.path.join(root, f), 'rb')
        filelist.write('"%s":"%s"' % (f, hashlib.md5(fp.read()).hexdigest()))
        fp.close()
    break
filelist.write('}')
filelist.close()

