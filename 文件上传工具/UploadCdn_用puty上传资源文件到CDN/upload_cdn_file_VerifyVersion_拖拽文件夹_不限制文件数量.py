import sys
import os
import json
import hashlib
from urllib import request

if len(sys.argv) != 2:
    input('将要提交的文件所在文件夹拖放到该工具上\n')
    exit(0)


print('选择的文件:')
platform =  input('\n选择平台: 1.PC  2.安卓 3.iOS\n')
cdndir = ''
allFiles = os.listdir(sys.argv[1]);
for tempFile in allFiles:
    filepath = tempFile #sys.argv[i]
    #print(filepath)

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
        input('一次只能上传同一类型的文件\n')
        exit(0)


puttycmd = 'echo y | "' + os.getcwd() + '/putty/pscp.exe" -r -q -pw %s %s %s@%s/%s'

def uploadfiles(filelisturl, serverdatapath, u, p):
    fileliststr = request.urlopen(filelisturl).read()
    #print('uploadfiles:',fileliststr)
    filelistcdn = json.loads(fileliststr)
    #print('uploadfiles2:',filelistcdn)

    tempI=0
    filesList=[]
    files = ''
    for theFile in allFiles:
        #print(theFile+','+os.path.dirname(theFile)+','+sys.argv[1]+'\\'+theFile)
        fp = open(sys.argv[1]+'\\'+theFile, 'rb')
        filemd5 = hashlib.md5(fp.read()).hexdigest()
        fp.close()
        filename = os.path.basename(theFile)
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
            files += sys.argv[1]+'\\'+theFile#path
            tempI += 1
            #循环
            if tempI >= 30:
                tempI = 0
                filesList.append(files)
                files=''
    if files != '':       
        filesList.append(files)
        files=''
            
    if filesList.count != 0:
        fp = open('filelist.json', 'w')
        fp.write(json.dumps(filelistcdn).replace(' ',''))
        fp.close()
        
        files += ' ' + os.getcwd()+'\\filelist.json'
        filesList.append(files)
        files=''
        for tempFiles in filesList:
            #print('tempFiles:',tempFiles)
            cmd = puttycmd % (p, tempFiles, u, serverdatapath, cdndir)
            os.system(cmd)
        
        #os.system('del /q filelist.json')

def uploadserver():
    print('版号服上传中...')
    uploadfiles('http://115.159.224.43:8081/%s/filelist.json' % cdndir, '115.159.224.43:/data/game/cdn', 'huangxinbei', 'cnJFahtV')

uploadserver()

input('finished!')
