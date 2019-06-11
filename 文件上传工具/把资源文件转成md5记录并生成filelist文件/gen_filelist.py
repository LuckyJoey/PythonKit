import os
import hashlib
import sys
#拖拽文件夹到此文件，将此文件夹下的文件转成md5记录在filelist.json文件
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

