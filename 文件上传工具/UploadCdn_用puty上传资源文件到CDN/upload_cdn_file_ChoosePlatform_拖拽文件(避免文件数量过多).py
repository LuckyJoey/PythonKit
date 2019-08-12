import sys
import os
import json
import hashlib
from urllib import request

if len(sys.argv) < 2:
    input('将要提交的文件拖放到该工具上，可以选择多个文件\n')
    exit(0)


print('选择的文件:')
platform =  input('\n选择平台: 1.PC  2.安卓 3.iOS\n')
cdndir = ''
for i in range(1,len(sys.argv)):
    filepath = sys.argv[i]
    print(filepath)

    resdir = ''
    if filepath.endswith('.bin'):
        resdir = 'bin'
    elif filepath.endswith('.json'):
        resdir = 'json'
    elif filepath.endswith('.asset') or filepath.endswith('.atlas'):
        if platform == "1":
           resdir = 'asset/pc'
           print('PC平台')
        elif platform == "2":
           resdir = 'asset/android'
           print('Android平台')
        elif platform == "3":
           resdir = 'asset/ios'
           print('iOS平台')
        else:
           print('平台输入错误\n')
           exit(0)           
    else:
        input('文件类型错误\n')
        exit(0)

    if cdndir == '':
        cdndir = resdir
    elif cdndir != resdir:
        input('一次只能上传同一目录的文件\n')
        exit(0)


puttycmd = 'echo y | "' + os.getcwd() + '/putty/pscp.exe" -r -q -pw %s %s %s@%s/%s'

def uploadfiles(filelisturl, serverdatapath, u, p):
    fileliststr = request.urlopen(filelisturl).read()
    filelistcdn = json.loads(fileliststr)

    files = ''
    for i in range(1,len(sys.argv)):
        fp = open(sys.argv[i], 'rb')
        filemd5 = hashlib.md5(fp.read()).hexdigest()
        fp.close()
        filename = os.path.basename(sys.argv[i])
        changed = False
        if filename in filelistcdn:
            if filelistcdn[filename] != filemd5:
                changed = True
                print('modify:', filename)
                filelistcdn[filename] = filemd5
            else:
                print('no change:', filename)
        else:
            changed = True
            print('new:', filename)
            filelistcdn[filename] = filemd5

        if changed:
            if files != '':
                files += ' '
            files += sys.argv[i]

    if files != '':
        fp = open('filelist.json', 'w')
        fp.write(json.dumps(filelistcdn).replace(' ',''))
        fp.close()
        files += ' ' + os.getcwd() + '/filelist.json'
        cmd = puttycmd % (p, files, u, serverdatapath, cdndir)
        os.system(cmd)
        os.system('del /q filelist.json')


def uploadserver(serverid):
    print('serverid', serverid)
    if serverid == '1':
        print('开发服上传中...')
        uploadfiles('http://192.168.0.49/aden1_data/%s/filelist.json' % cdndir, '192.168.0.49:/opt/cdn/aden_data1', 'aden', 'adenxxx')

    elif serverid == '2':
        print('体验服上传中...')
        uploadfiles('http://192.168.0.49/aden2_data/%s/filelist.json' % cdndir, '192.168.0.49:/opt/cdn/aden_data2', 'aden2', 'aden321')

    elif serverid == '3':
        print('测试服上传中...')
        uploadfiles('http://192.168.0.49/aden3_data/%s/filelist.json' % cdndir, '192.168.0.49:/opt/cdn/aden_data3', 'aden3', 'aden321')
        
    else:
        print('输入错误')

serv = input('\n选择服务器: 1.开发服  2.体验服 3.测试服  4.全部\n')
if serv != '4':
    uploadserver(serv)
else:
    for i in range(1,4):
        uploadserver(str(i))

input('finished!')
