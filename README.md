# Table of Contents
 * [What is it](#what-is-it)
 * [How do I install it](#how-do-i-install-it)
  * [Windows Installation](#windows-installation)
  * [OS X Installation](#os-x-installation)
  * [Linux Installation](#linux-installation)
 * [How do I use it](#how-do-i-use-it)
  * [Windows Usage](#windows-usage)
  * [OS X and Linux Usage](#os-x-and-linux-usage)

# What is it

PyTan was created to solve for the following needs:
  1. Create a python library to provide an easy set of methods for programmatically interfacing with Tanium via the SOAP API
  2. Create a set of command line scripts that utilize the python library that handle the argument parsing, thereby providing non-python users with command line access to the functionality provided by the methods inside of the python library
  3. [Original Design Approach Doc](doc/DESIGN.md)
  4. Original Design Goals:
    * Provide a command line method for asking a question and getting a result
    * Provide a command line method for asking all questions and getting all results
    * Make above methods produce output in programmatic output (i.e. CSV)
    * Make a self contained package with as little external dependencies as possible
    * Make a self contained package with as little setup required as possible

Things PyTan can do right now:
  1. Ask parsed questions (just like in the console)
  2. Ask manually built questions
  3. Get object data for the following object types: saved question, question, sensor, package, action, group
  4. Transform the data and save the transformation into a file for any response into the following types: 
    1. csv: will transform the response from Tanium into a CSV document
    7. json: will transform the response from Tanium into a JSON document
    4. xml: will transform the response from Tanium into an XML document
    2. raw.xml: will save the raw XML response from Tanium with no transformation
    3. raw.response: will save the raw HTTP response from Tanium with no transformation
    5. raw.request: will save the raw HTTP request to Tanium with no transformation

Things PyTan can **NOT** do right now:
  1. Pass parameters for parsed questions
  2. Pass parameters for manual questions
  3. Pass filters for manual questions
  4. Pass Options for anything
  5. Add object for saved question, sensor, package, action, group
  6. See [TODO.md](doc/TODO.md) for the list of things that need to be done and their priority
 
How PyTan has been tested so far:
  * To date, PyTan has only been tested to run on OS X 10.10 and Windows 2008 R2
  * To date, the only Tanium installation PyTan has been tested to run against is the following:
   * Tanium Server version: 6.2.314.3258
   * SQL Server version: SQL Server 2012 Express with Tools
   * Host OS: Windows 2008 R2 SP1 x64 with all Windows Updates applied, running inside a VMWare Fusion 7 Virtual Machine on OS X 10.10 - both the Tanium Server and the SQL Server reside on the same host
   * Tanium Clients:
     * One windows (installed on the Tanium Server itself)
     * One OS X (installed on the OS X 10.10 running VMWare Fusion 7)

Groups interested in PyTan thus far:
  * Tanium TAM's (for automating Sensor testing)
  * Potential Client in Fed

[TOC](#table-of-contents)

# How do I install it

## Windows Installation
  * Download Python 2.7 from https://www.python.org/downloads/windows/
  * Install Python 2.7 -- if you accept the default paths it will install to C:\Python27
  * Copy this distro to your local machine somewhere
  * If you did not accept the default install path for Python 2.7, edit ```pytan\winbin\CONFIG.bat``` to change the *PYTHON* variable to point to the full path of *python.exe*
  
## OS X Installation
  * OS X 10.8 and higher come with Python 2.7 out of the box
  * Copy this distro to your local machine somewhere

## Linux Installation
  * Ensure Python 2.7 is installed
  * Ensure the first *python* binary in your path points to your Python 2.7 installation
  * Copy this distro to your local machine somewhere

[TOC](#table-of-contents)

# How do I use it

## Windows Usage
  * See ```pytan\winbin\EXAMPLE``` for a set of batch scripts that use the various command line scripts to do things. Ensure you update ```pytan\winbin\EXAMPLE\API_INFO.bat``` with username, password, and host for your Tanium server
  * Use ```pytan\winbin\ask_parsed_question.bat``` to ask a parsed question of Tanium
  * Use ```pytan\winbin\ask_manual_question.bat``` to ask a manual question of Tanium
  * Use ```pytan\winbin\get_objects.bat``` to get object data from Tanium
  * Use ```pytan\winbin\get_question_results.bat``` to get results from a question ID that has already been asked
  * Use ```pytan\winbin\get_server_info.bat``` to get print out the return of GetServerInfo from the API
  * Use ```pytan\winbin\sw_shell.bat``` to enter into a python console that has access to the PyTan Library as **sw**
  * Run any of the commands above with **-h/--help** to get usage information
 
## OS X and Linux Usage
  * See ```pytan\bin\EXAMPLE``` for a set of bash scripts that use the various command line scripts to do things. Ensure you update ```pytan\bin\EXAMPLE\API_INFO.sh``` with username, password, and host for your Tanium server
  * Use ```pytan\bin\ask_parsed_question.py``` to ask a parsed question of Tanium
  * Use ```pytan\bin\ask_manual_question.py``` to ask a manual question of Tanium
  * Use ```pytan\bin\get_objects.py``` to get object data from Tanium
  * Use ```pytan\bin\get_question_results.py``` to get results from a question ID that has already been asked
  * Use ```pytan\bin\get_server_info.py``` to get print out the return of GetServerInfo from the API
  * Use ```pytan\bin\sw_shell.py``` to enter into a python console that has access to the PyTan Library as **sw**
  * Run any of the commands above with **-h/--help** to get usage information
  
  
[TOC](#table-of-contents)
