@echo off

set BuildTarget=%1
set SrcRoot="G:\jenkins\workspace\Aden_Dev_AssetBundle\AssetBundles"
set TarRoot="G:\ftp\Aden\Dev\asset"

if %BuildTarget% == window (
    set SrcDir=%SrcRoot%\Win
    set TarDir=%TarRoot%\pc
)
if %BuildTarget% == android (
    set SrcDir=%SrcRoot%\Android
    set TarDir=%TarRoot%\android
)
if %BuildTarget% == ios (
    set SrcDir=%SrcRoot%\IOS
    set TarDir=%TarRoot%\ios
)

echo [Src] %SrcDir%
echo [Tar] %TarDir%

del /q %TarDir%\*
copy /y %SrcDir%\*.asset %TarDir%\
copy /y %SrcDir%\*.atlas %TarDir%\


C:\Users\Administrator\AppData\Local\Programs\Python\Python36\python.exe G:\jenkins\tools\Aden\gen_filelist.py %TarDir%