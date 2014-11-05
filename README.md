# Table of Contents
 * [What is it](#what-is-it)
 * [Why was it created](#why-was-it-created)
 * [Things it can do right now](#things-it-can-not-do-right-now)
 * [Things it can NOT do right now](#things-it-can-not-do-right-now)
 * [How it has been tested](#how-it-has-been-tested)
 * [Groups interested in it](#groups-interested-in-it)
 * [How do I install it](#how-do-i-install-it)
  * [Windows Installation](#windows-installation)
  * [OS X Installation](#os-x-installation)
  * [Linux Installation](#linux-installation)
 * [How do I use it](#how-do-i-use-it)
  * [Windows Usage](#windows-usage)
  * [OS X and Linux Usage](#os-x-and-linux-usage)

----

[..TOC..](#table-of-contents)
# What is it

PyTan is a Python library that provides a simple way for programmatically interfacing with Tanium's SOAP API. It also has command line scripts that make it easy for non-programmers to utilize PyTan's library.

[..TOC..](#table-of-contents)
# Why was it created

PyTan was created to solve for the following needs:
  1. Create a python library to provide an easy set of methods for programmatically interfacing with Tanium via the SOAP API
  2. Create a set of command line scripts that utilize the python library that handle the argument parsing, thereby providing non-python users with command line access to the functionality provided by the methods inside of the python library
  4. Original Design Goals ([Original Design Approach Doc](doc/DESIGN.md)):
    * Provide a command line method for asking a question and getting a result
    * Provide a command line method for asking all questions and getting all results
    * Make above methods produce output in programmatic output (i.e. CSV)
    * Make a self contained package with as little external dependencies as possible
    * Make a self contained package with as little setup required as possible

[..TOC..](#table-of-contents)
# Things it can do right now

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

[..TOC..](#table-of-contents)
# Things it can NOT do right now

  1. Pass parameters for parsed questions
  2. Pass parameters for manual questions
  3. Pass filters for manual questions
  4. Pass Options for anything
  5. Add object for saved question, sensor, package, action, group
  6. Deploy actions
  7. Deploy packages
  8. See [TODO.md](doc/TODO.md) for the list of things that need to be done and their priority
 
[..TOC..](#table-of-contents)
# How it has been tested

  * To date, PyTan has only been tested to run on OS X 10.10 and Windows 2008 R2
  * To date, the only Tanium installation PyTan has been tested to run against is the following:
   * Tanium Server version: 6.2.314.3258
   * SQL Server version: SQL Server 2012 Express with Tools
   * Host OS: Windows 2008 R2 SP1 x64 with all Windows Updates applied, running inside a VMWare Fusion 7 Virtual Machine on OS X 10.10 - both the Tanium Server and the SQL Server reside on the same host
   * Tanium Clients: 2
     * One windows (installed on the Tanium Server itself)
     * One OS X (installed on the OS X 10.10 running VMWare Fusion 7)

[..TOC..](#table-of-contents)
# Groups interested in it

  * Tanium TAM's (for automating Sensor testing)
  * Potential Client in Fed

[..TOC..](#table-of-contents)
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

[..TOC..](#table-of-contents)
# How do I use it

## Windows Usage
  * Use ```pytan\winbin\ask_parsed_question.bat``` to ask a parsed question of Tanium
  * Use ```pytan\winbin\ask_manual_question.bat``` to ask a manual question of Tanium
  * Use ```pytan\winbin\get_objects.bat``` to get object data from Tanium
  * Use ```pytan\winbin\get_question_results.bat``` to get results from a question ID that has already been asked
  * Use ```pytan\winbin\get_server_info.bat``` to get print out the return of GetServerInfo from the API
  * Use ```pytan\winbin\sw_shell.bat``` to enter into a python console that has access to the PyTan Library as **sw**
  * Run any of the commands above with **-h/--help** to get usage information
  * See ```pytan\winbin\EXAMPLE``` for a set of batch scripts that use the various command line scripts to do things. Ensure you update ```pytan\winbin\EXAMPLE\API_INFO.bat``` with username, password, and host for your Tanium server
 
## OS X and Linux Usage
  * Use ```pytan\bin\ask_parsed_question.py``` to ask a parsed question of Tanium
  * Use ```pytan\bin\ask_manual_question.py``` to ask a manual question of Tanium
  * Use ```pytan\bin\get_objects.py``` to get object data from Tanium
  * Use ```pytan\bin\get_question_results.py``` to get results from a question ID that has already been asked
  * Use ```pytan\bin\get_server_info.py``` to get print out the return of GetServerInfo from the API
  * Use ```pytan\bin\sw_shell.py``` to enter into a python console that has access to the PyTan Library as **sw**
  * Run any of the commands above with **-h/--help** to get usage information
  * See ```pytan\bin\EXAMPLE``` for a set of bash scripts that use the various command line scripts to do things. Ensure you update ```pytan\bin\EXAMPLE\API_INFO.sh``` with username, password, and host for your Tanium server
  
[..TOC..](#table-of-contents)
## API Usage

[..TOC..](#table-of-contents)
### Create a connection

  * This python script will create a connection to the SOAP API on a Tanium server. Change PYTAN_PATH, USERNAME, PASSWORD, and HOST accordingly.

```python
#!/usr/bin/env python
PYTAN_PATH = '/opt/pytan'
USERNAME = 'Tanium User'
PASSWORD = 'T@n!um'
HOST = '172.16.31.128'

import sys
sys.path.insert(0, '%s/lib' % PYTAN_PATH)

import SoapWrap

sw = SoapWrap.SoapWrap(USERNAME, PASSWORD, HOST)
print sw
'''
Should produce the following output:

SoapWrap to https://172.16.31.128:443/soap, Version: 6.2.314.3258
'''
```

[..TOC..](#table-of-contents)
### Ask a parsed question

  * This python script will create a connection to the SOAP API on a Tanium server, and ask a parsed question and store the return in ```response```. Change PYTAN_PATH, USERNAME, PASSWORD, HOST, and QUESTION accordingly.

```python
#!/usr/bin/env python
PYTAN_PATH = '/opt/pytan'
USERNAME = 'Tanium User'
PASSWORD = 'T@n!um'
HOST = '172.16.31.128'
QUESTION = 'Get Computer Name from all machines'

import sys
sys.path.insert(0, '%s/lib' % PYTAN_PATH)

import SoapWrap
import json

sw = SoapWrap.SoapWrap(USERNAME, PASSWORD, HOST)
response = sw.ask_parsed_question(QUESTION)
print response
'''
Should produce the following output:

SoapResponse from: https://172.16.31.128:443/soap, len: 1640, on: 2014_11_05-11_09_55-EST, SoapRequest for 'get_parse_groups'/'AddObject' of '{"parse_job": {"question_text": "Get Computer Name from all machines"}}', Sent: 2014_11_05-11_09_40-EST, Auth: session
'''
print json.dumps(response.inner_return, indent=2)
'''
Should produce the following output:

{
  "result_sets": {
    "now": "2014/11/03 11:02:28 GMT-0000",
    "result_set": {
      "age": 0,
      "archived_question_id": 0,
      "saved_question_id": 0,
      "question_id": 22636,
      "report_count": 2,
      "seconds_since_issued": 0,
      "issue_seconds": 0,
      "expire_seconds": 0,
      "tested": 2,
      "passed": 2,
      "mr_tested": 2,
      "mr_passed": 2,
      "estimated_total": 2,
      "select_count": 1,
      "cs": {
        "c": [
          {
            "wh": 3409330187,
            "dn": "Computer Name",
            "rt": 1
          },
          {
            "wh": 0,
            "dn": "Count",
            "rt": 3
          }
        ]
      },
      "filtered_row_count": 2,
      "filtered_row_count_machines": 2,
      "item_count": 2,
      "rs": {
        "r": [
          {
            "id": 510214322,
            "cid": 0,
            "c": [
              {
                "v": "Casus-Belli.local"
              },
              {
                "v": 1
              }
            ]
          },
          {
            "id": 911171945,
            "cid": 0,
            "c": [
              {
                "v": "jtanium1.localdomain"
              },
              {
                "v": 1
              }
            ]
          }
        ]
      }
    }
  }
}
'''
```

[..TOC..](#table-of-contents)
### Ask a parsed question and save as CSV

  * This python script will create a connection to the SOAP API on a Tanium server, and ask a parsed question and store the return in ```response```, then use the SoapTransform class to write the response as a CSV file. Change PYTAN_PATH, USERNAME, PASSWORD, HOST, QUESTION, and FTYPE accordingly. See the dictionary ```TRANSFORM_FORMATS``` in ```pytan/lib/SoapConstants.py``` for all of the supported formats for FTYPE.

```python
#!/usr/bin/env python
PYTAN_PATH = '/opt/pytan'
USERNAME = 'Tanium User'
PASSWORD = 'T@n!um'
HOST = '172.16.31.128'
QUESTION = 'Get Computer Name from all machines'
FTYPE = 'csv'

import sys
sys.path.insert(0, '%s/lib' % PYTAN_PATH)

import SoapWrap

sw = SoapWrap.SoapWrap(USERNAME, PASSWORD, HOST)
response = sw.ask_parsed_question(QUESTION)
st = SoapWrap.SoapTransform()
response_filename = st.write_response(response, ftype=FTYPE)
print response_filename
'''
Should produce the following output:

./get_parse_groups__parse_job_question_text_GetComputerNamefromallmachines__2014_11_05-11_16_22-EST.csv
'''
```

  * Contents of the transformed CSV file:

```csv
"Computer Name"
"Casus-Belli.local"
"jtanium1.localdomain"
```

[..TOC..](#table-of-contents)
