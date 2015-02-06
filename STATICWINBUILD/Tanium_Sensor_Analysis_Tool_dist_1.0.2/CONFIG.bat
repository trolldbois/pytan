@echo off

REM if username is not set here, it will be prompted for on the command line
set username=

REM if password is not set here, it will be prompted for on the command line
set password=

REM if host is not set here, it will be prompted for on the command line
set host=

REM optionally control which port to connect to (integer)
set port=

REM optionally control the logging / verbosity level (integer)
set loglevel=

REM optionally set the logging format to a more verbose logging format (true to enable)
set debugformat=false

REM optionally only ask questions for sensors that are in the given platforms
REM space separated, i.e. Linux Mac Windows
set platforms=

REM optionally only ask questions for sensors that are in the given categories
REM space separated, i.e. Reserved Tanium
set categories=

REM optionally control the output directory
set output_dir=

REM optionally override the default number of seconds to wait between asking questions
set sleep=

REM optionally override the default percent to consider question data complete
set pct=

REM optionally override the default number of seconds before questions timeout
set timeout=
