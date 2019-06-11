
set AppIntgTool=D:\Jenkins_Tools\Aden\Run\AppIntgTool_TC.exe

for %%F in ("*.apk") do (
    set FileNameExt="%%~nxF"
    %AppIntgTool% -h %%~nxF com.netmarbleasia.aden > %%~nxF.txt
)