@echo off

set my_dir=%~dp0%
call %my_dir%\CONFIG.bat
set cmdline=
IF DEFINED username set cmdline=%cmdline% --username "%username%"
IF DEFINED password set cmdline=%cmdline% --password "%password%"
IF DEFINED host set cmdline=%cmdline% --host "%host%"
IF DEFINED port set cmdline=%cmdline% --port "%port%"
IF DEFINED loglevel set cmdline=%cmdline% --loglevel "%loglevel%"
IF DEFINED output_dir set cmdline=%cmdline% --output_dir "%output_dir%"
IF DEFINED sleep set cmdline=%cmdline% --sleep "%sleep%"
IF DEFINED pct set cmdline=%cmdline% --pct "%pct%"
IF DEFINED timeout set cmdline=%cmdline% --timeout "%timeout%"
IF "%debugformat%" == "true" set cmdline=%cmdline% --debugformat

SETLOCAL ENABLEDELAYEDEXPANSION
IF DEFINED platforms for %%a in (%platforms%) do (set cmdline=!cmdline! --platform "%%a")
IF DEFINED categories for %%a in (%categories%) do (set cmdline=!cmdline! --category "%%a")

cd %my_dir%
Tanium_Sensor_Analysis_Tool.exe !cmdline!
ENDLOCAL
