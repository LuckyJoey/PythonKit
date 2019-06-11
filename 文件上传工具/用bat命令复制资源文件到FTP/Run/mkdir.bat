@set YEAR=%date:~0,4%
@set MONTH=%date:~5,2%
@set DAY=%date:~8,2%

 
@set POSTFIX=%YEAR%%MONTH%%DAY%
 
mkdir D:\Jenkins_Tools\Aden\Run\log_2017-02-27_15-48-58\"log_%POSTFIX%"
::cd "log_%POSTFIX%"