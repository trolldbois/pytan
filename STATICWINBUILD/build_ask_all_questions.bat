@echo off
set my_dir=%~dp0%
call %my_dir%\CONFIG.bat
cd %my_dir%
%PYTHON% setup_ask_all_questions.py py2exe
