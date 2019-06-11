::
:: APK 검증 작업용
::

set AppIntgTool="D:\Jenkins_Tools\Aden\Run\AppIntgTool.exe"

for %%F in ( "*.apk" ) do (

	:: 확장자 포함한 파일명 "%%~nxF"
	set FileNameExt="%%~nxF"
	
	%AppIntgTool% -h %%~nxF > %%~nxF.txt
)
