@echo off
SET my_dir=%~dp0%

CALL %my_dir%\config.bat

SET my_script_name=%~n0%
SET PYTHONINSPECT=-i

%PYTHON% %my_dir%\%my_script_name%.py %*
