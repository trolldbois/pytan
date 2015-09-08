@echo off
set my_dir=%~dp0%
call %my_dir%\CONFIG.bat
cd %my_dir%
%PYTHON% setup_Tanium_Sensor_Analysis_Tool.py py2exe
