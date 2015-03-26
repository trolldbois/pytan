@echo off
set my_dir=%~dp0%
call %my_dir%\CONFIG.bat
cd %my_dir%
%PYTHON% setup_Tanium_Unmanaged_Asset_Tracker.py py2exe
