#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''All the variables/templates/etc for the build scripts'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.1.5'

import sys
sys.dont_write_bytecode = True
import os

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
pytan_root = os.path.dirname(parent_dir)
pytan_lib_dir = os.path.join(pytan_root, 'lib')
test_dir = os.path.join(pytan_root, 'test')
path_adds = [my_dir, pytan_lib_dir, test_dir]

[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

import pytan
import API_INFO

doc_source = os.path.join(parent_dir, 'doc', 'source')
staticdoc_source = os.path.join(doc_source, '_static')

scripts = {}
sname = 'write_pytan_user_config'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Creates a PyTan User Config based on the current parameters'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'ask_manual'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Ask a manual question and save the results as a report format'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'ask_parsed'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Ask a parsed question and save the results as a report format'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'ask_saved'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Ask a saved question and save the results as a report format'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'create_group'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Create a group object from command line arguments'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'create_package'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Create a package object from command line arguments'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

# sname = 'create_sensor'
# scripts[sname] = {}
# scripts[sname]['docstring'] = 'Create a sensor object from command line arguments (Not supported)'
# scripts[sname]['script_name'] = sname
# scripts[sname]['pyopts'] = ''
# scripts[sname]['py_template'] = '${py_script}'
# scripts[sname]['bat_template'] = '${bat_script}'

sname = 'get_saved_question_history'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Gets the Result Info for all the questions asked for a given saved question, or for all questions asked ever, and exports the question information to a CSV file'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'create_user'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Create a user object from command line arguments'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'create_whitelisted_url'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Create a Whitelisted URL object from command line arguments'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'deploy_action'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Deploy an action and save the results as a report format'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'get_results'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Get results from a deploy action, saved question, or question'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'print_sensors'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Prints sensor information to stdout'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'print_server_info'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Prints server information to stdout'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'pytan_shell'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Provides an interactive console with pytan available as handler'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ' -i'
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'stop_action'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Stop an action by ID'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'approve_saved_action'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Approve a saved action by ID'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'tsat'
scripts[sname] = {}
scripts[sname]['docstring'] = 'Tanium Sensor Analysis Tool: asks a question for every sensor and saves the results as report files'
scripts[sname]['script_name'] = sname
scripts[sname]['pyopts'] = ''
scripts[sname]['py_template'] = '${py_script}'
scripts[sname]['bat_template'] = '${bat_script}'

sname = 'CONFIG'
scripts[sname] = {}
scripts[sname]['script_name'] = sname
scripts[sname]['bat_template'] = '${config_bat_script}'

for i in pytan.constants.GET_OBJ_MAP:
    sname = "get_{}".format(i)
    scripts[sname] = {}
    scripts[sname]['script_name'] = sname
    scripts[sname]['pyopts'] = ''
    scripts[sname]['objname'] = i
    scripts[sname]['docstring'] = "Get an object of type: {} and save the object to a report file".format(i)
    scripts[sname]['py_template'] = '${map_script}'
    scripts[sname]['bat_template'] = '${bat_script}'
    scripts[sname]['reportparser'] = '    pytan.binsupport.add_get_object_report_argparser(parser=parser)\n'
    scripts[sname]['maptype'] = 'get_object'

for i in pytan.constants.GET_OBJ_MAP:
    if not pytan.constants.GET_OBJ_MAP[i]['delete']:
        continue
    sname = "delete_{}".format(i)
    scripts[sname] = {}
    scripts[sname]['script_name'] = sname
    scripts[sname]['pyopts'] = ''
    scripts[sname]['objname'] = i
    scripts[sname]['docstring'] = "Delete an object of type: {}".format(i)
    scripts[sname]['py_template'] = '${map_script}'
    scripts[sname]['bat_template'] = '${bat_script}'
    scripts[sname]['reportparser'] = ''
    scripts[sname]['maptype'] = 'delete_object'

for i in pytan.constants.GET_OBJ_MAP:
    if not pytan.constants.GET_OBJ_MAP[i]['create_json']:
        continue
    sname = "create_{}_from_json".format(i)
    scripts[sname] = {}
    scripts[sname]['script_name'] = sname
    scripts[sname]['pyopts'] = ''
    scripts[sname]['objname'] = i
    scripts[sname]['docstring'] = "Create an object of type: {} from a JSON file".format(i)
    scripts[sname]['py_template'] = '${map_script}'
    scripts[sname]['bat_template'] = '${bat_script}'
    scripts[sname]['reportparser'] = ''
    scripts[sname]['maptype'] = 'create_json_object'


py_file = "${script_name}.py"
bat_file = "${script_name}.bat"

script_templates = {}
script_templates['py_script'] = """#!/usr/bin/env python${pyopts}
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''${docstring}'''
__author__ = '${AUTHOR}'
__version__ = '${VERSION}'

import os
import sys
sys.dont_write_bytecode = True

my_file = os.path.abspath(sys.argv[0])
my_name = os.path.splitext(os.path.basename(my_file))[0]
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

import pytan
import pytan.binsupport

if __name__ == "__main__":
    pytan.binsupport.version_check(reqver=__version__)

    setupmethod = getattr(pytan.binsupport, 'setup_{}_argparser'.format(my_name))
    responsemethod = getattr(pytan.binsupport, 'process_{}_args'.format(my_name))

    parser = setupmethod(doc=__doc__)
    args = parser.parse_args()

    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)
    response = responsemethod(parser=parser, handler=handler, args=args)
"""

script_templates['bat_script'] = """@echo off
set my_dir=%~dp0%
call %my_dir%\CONFIG.bat
set my_script_name=%~n0%
%PYTHON%${pyopts} %my_dir%\\..\\bin\\%my_script_name%.py %*
"""

script_templates['config_bat_script'] = '''@echo off
set PYTHON=C:\Python27\python.exe
'''

script_templates['map_script'] = """#!/usr/bin/env python${pyopts}
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''${docstring}'''
__author__ = '${AUTHOR}'
__version__ = '${VERSION}'

import os
import sys
sys.dont_write_bytecode = True

my_file = os.path.abspath(sys.argv[0])
my_name = os.path.splitext(os.path.basename(my_file))[0]
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

import pytan
import pytan.binsupport

if __name__ == "__main__":
    pytan.binsupport.version_check(reqver=__version__)

    parser = pytan.binsupport.setup_${maptype}_argparser(obj='${objname}', doc=__doc__)
${reportparser}    args = parser.parse_args()

    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)
    response = pytan.binsupport.process_${maptype}_args(
        parser=parser, handler=handler, obj='${objname}', args=args,
    )
"""

RST_INDEX_TEMPLATE = """
{title}
========================================================================================

{desc}

.. toctree::

   {tocitems}
"""

README_MD_TEMPLATE = """
{title}
========================================================================================

This directory contains a number of python scripts that show how to use PyTan in
various ways.

They can be run immediately after changing the username, password, host, and maybe port
variables defined in each.

If you copy them outside of the EXAMPLE/PYTAN_API directory to edit and run them, you will
also need to update the pytan_loc variable to point to the directory where pytan lives.

{tocitems}
"""

EXAMPLE_PY_TEMPLATE = '''#!/usr/bin/env python
"""
{desc}
"""
{py_code}
\'\'\'STDOUT from running this:
{py_stdout}
\'\'\'

\'\'\'STDERR from running this:
{py_stderr}
\'\'\'
'''

VALIDATION_RST_TEMPLATE = """

Tanium: {platform_version}, OS: {os_version}, Python: {python_version_short}
========================================================================================

This is the output from running test/test_pytan_valid_server_tests.py against the following:

* PyTan Version: {pytan_version}
* Tanium Platform Version: {platform_version}
* Test Date: {test_date}
* OS Version running PyTan: {os_version}
* Python version running PyTan: {python_version_full}
* Output from tests: `{stdout_fn} <../_static/{dir_base}/{stdout_fn}>`_

"""

EXAMPLE_RST_TEMPLATE = """
{title}
========================================================================================

{desc}


* `STDOUT from Example Python Code <../_static/pytan_outputs/{inc_stdout}>`_
* `STDERR from Example Python Code <../_static/pytan_outputs/{inc_stderr}>`_
* Example Python Code

.. literalinclude:: {inc_code}
    :linenos:
    :language: python

.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
"""

SOAP_RST_HEAD = """
{title}
==========================================================================================

{desc}

{steps}

.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
"""

SOAP_RST_STEP = """
Step {response.number} - {response.pytan_help}
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: {response.url}
* HTTP Method: {response.request.method}
* Elapsed Time: {response.elapsed}
* `Step {response.number} Request Body <../../_static/soap_outputs/{response.platform_version}/{response.request.inc_file}>`_
* `Step {response.number} Response Body <../../_static/soap_outputs/{response.platform_version}/{response.inc_file}>`_

* Request Headers:

.. code-block:: json
    :linenos:

    {response.request.pretty_headers}

* Response Headers:

.. code-block:: json
    :linenos:

    {response.pretty_headers}
"""

CODE_BLOCK_TEMPLATE = """
{title}
----------------------------------------------------------------------------------------

.. code-block:: {code_type}
    :linenos:
{code_block}
"""

HANDLER_ARGS_TEMPLATE = """
# setup the arguments for the {method}
{args_name} = {{}}
{args_str}"""

METHOD_TEMPLATES = {}

METHOD_TEMPLATES['valid_response'] = """
print "...CALLING: handler.{method} with args: {{}}".format(kwargs)
response = handler.{method}(**kwargs)"""

METHOD_TEMPLATES['invalid_basic'] = """
print "...CALLING: handler.{method}() with args: {{}}".format(kwargs)
try:
    handler.{method}(**kwargs)
except Exception as e:
    print "...EXCEPTION: {{}}".format(e)
    # this should throw an exception of type: {exception}
    # uncomment to see full exception
    # traceback.print_exc(file=sys.stdout)"""

METHOD_TEMPLATES['delete_first'] = """
# delete the object in case it already exists
# catch and print the exception error if it does not exist
print "...CALLING: handler.delete() with args: {{}}".format(delete_kwargs)
try:
    handler.delete(**delete_kwargs)
except Exception as e:
    print "...EXCEPTION: {{}}".format(e)

print "...CALLING: handler.{method}() with args: {{}}".format(kwargs)
response = handler.{method}(**kwargs)"""

METHOD_TEMPLATES['create_from_json'] = """
# get objects to use as an export to JSON file
print "...CALLING: handler.get() with args: {{}}".format(get_kwargs)
orig_objs = handler.get(**get_kwargs)

# export orig_objs to a json file
export_kwargs = {{}}
export_kwargs['obj'] = orig_objs
export_kwargs['export_format'] = 'json'
export_kwargs['report_dir'] = tempfile.gettempdir()

print "...CALLING: handler.export_to_report_file() with args: {{}}".format(export_kwargs)
json_file, results = handler.export_to_report_file(**export_kwargs)

# create the object from the exported JSON file
create_kwargs = {{}}
create_kwargs['objtype'] = {objtype!r}
create_kwargs['json_file'] = json_file

print "...CALLING: handler.create_from_json() with args {{}}".format(create_kwargs)
response = handler.create_from_json(**create_kwargs)"""

METHOD_TEMPLATES['create_from_json_delete_before'] = """
# get objects to use as an export to JSON file
print "...CALLING: handler.get() with args: {{}}".format(get_kwargs)
orig_objs = handler.get(**get_kwargs)

# set the attribute name and value we want to add to the original objects
# this is necessarry to avoid name conflicts when adding the new object
attr_name = {transform_attr!r}
attr_value = {transform_value!r}

# modify the orig_objs to add attr_value to attr_name
for x in orig_objs:
    new_attr = getattr(x, attr_name)
    new_attr += attr_value
    setattr(x, attr_name, new_attr)

    # delete the object in case it already exists
    del_kwargs = {{}}
    del_kwargs[attr_name] = new_attr
    del_kwargs['objtype'] = {objtype!r}

    print "...CALLING: handler.delete() with args: {{}}".format(del_kwargs)
    try:
        handler.delete(**del_kwargs)
    except Exception as e:
        print "...EXCEPTION: {{}}".format(e)

# export orig_objs to a json file
export_kwargs = {{}}
export_kwargs['obj'] = orig_objs
export_kwargs['export_format'] = 'json'
export_kwargs['report_dir'] = tempfile.gettempdir()

print "...CALLING: handler.export_to_report_file() with args: {{}}".format(export_kwargs)
json_file, results = handler.export_to_report_file(**export_kwargs)

# create the object from the exported JSON file
create_kwargs = {{}}
create_kwargs['objtype'] = {objtype!r}
create_kwargs['json_file'] = json_file

print "...CALLING: handler.create_from_json() with args {{}}".format(create_kwargs)
response = handler.create_from_json(**create_kwargs)"""

METHOD_TEMPLATES['invalid_create_from_json'] = """
# get objects to use as an export to JSON file
print "...CALLING: handler.get() with args: {{}}".format(get_kwargs)
orig_objs = handler.get(**get_kwargs)

# export orig_objs to a json file
export_kwargs = {{}}
export_kwargs['obj'] = orig_objs
export_kwargs['export_format'] = 'json'
export_kwargs['report_dir'] = tempfile.gettempdir()

print "...CALLING: handler.export_to_report_file() with args: {{}}".format(export_kwargs)
json_file, results = handler.export_to_report_file(**export_kwargs)

# create the object from the exported JSON file
create_kwargs = {{}}
create_kwargs['objtype'] = {objtype!r}
create_kwargs['json_file'] = json_file

# call the handler with the create_from_json method, passing in kwargs for arguments
print "...CALLING: handler.create_from_json() with args {{}}".format(create_kwargs)
try:
    response = handler.create_from_json(**create_kwargs)
except Exception as e:
    print "...EXCEPTION: {{}}".format(e)
    # this should throw an exception of type: {exception}
    # uncomment to see full exception
    # traceback.print_exc(file=sys.stdout)"""

METHOD_TEMPLATES['export_resultset'] = """
# setup the arguments for handler.ask()
ask_kwargs = {{
    'qtype': 'manual',
    'sensors': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Contents{{folderPath=C:\\Program Files}}',
    ],
}}

# ask the question that will provide the resultset that we want to use
print "...CALLING: handler.ask() with args {{}}".format(ask_kwargs)
response = handler.ask(**ask_kwargs)

# store the resultset object as the obj we want to export into kwargs
kwargs['obj'] = response['question_results']

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
print "...CALLING: handler.export_obj() with args {{}}".format(kwargs)
out = handler.export_obj(**kwargs)"""

METHOD_TEMPLATES['invalid_export_resultset'] = """
# setup the arguments for handler.ask()
ask_kwargs = {{
    'qtype': 'manual',
    'sensors': [
        "Computer Name"
    ],
}}

# ask the question that will provide the resultset that we want to use
print "...CALLING: handler.ask() with args {{}}".format(ask_kwargs)
response = handler.ask(**ask_kwargs)

# store the resultset object as the obj we want to export
kwargs['obj'] = response['question_results']

# export the object to a string
print "...CALLING: handler.export_obj() with args {{}}".format(kwargs)
try:
    handler.export_obj(**kwargs)
except Exception as e:
    print "...EXCEPTION: {{}}".format(e)
    # this should throw an exception of type: {exception}
    # uncomment to see full exception
    # traceback.print_exc(file=sys.stdout)"""

METHOD_TEMPLATES['export_basetype'] = """
# setup the arguments for handler.get()
get_kwargs = {{
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Contents',
    ],
    'objtype': 'sensor',
}}

# get the objects that will provide the basetype that we want to export
print "...CALLING: handler.get() with args: {{}}".format(get_kwargs)
response = handler.get(**get_kwargs)

# store the basetype object as the obj we want to export
kwargs['obj'] = response

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
print "...CALLING: handler.export_obj() with args {{}}".format(kwargs)
out = handler.export_obj(**kwargs)"""

METHOD_TEMPLATES['invalid_export_basetype'] = """
# setup the arguments for handler.get()
get_kwargs = {{
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Contents',
    ],
    'objtype': 'sensor',
}}

# get the objects that will provide the basetype that we want to use
print "...CALLING: handler.get() with args: {{}}".format(get_kwargs)
response = handler.get(**get_kwargs)

# store the basetype object as the obj we want to export
kwargs['obj'] = response

# export the object to a string
print "...CALLING: handler.export_obj() with args {{}}".format(kwargs)
try:
    handler.export_obj(**kwargs)
except Exception as e:
    print "...EXCEPTION: {{}}".format(e)
    # this should throw an exception of type: {exception}
    # uncomment to see full exception
    # traceback.print_exc(file=sys.stdout)"""

RESPONSE_TEMPLATES = {}

RESPONSE_TEMPLATES['question'] = """
print "...OUTPUT: Type of response: ", type(response)

print "...OUTPUT: Pretty print of response:"
print pprint.pformat(response)

print "...OUTPUT: Equivalent Question if it were to be asked in the Tanium Console: "
print response['question_object'].query_text

if response['question_results']:
    # call the export_obj() method to convert response to CSV and store it in out
    export_kwargs = {{}}
    export_kwargs['obj'] = response['question_results']
    export_kwargs['export_format'] = 'csv'

    print "...CALLING: handler.export_obj() with args {{}}".format(export_kwargs)
    out = handler.export_obj(**export_kwargs)

    # trim the output if it is more than 15 lines long
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\\n'.join(out)

    print "...OUTPUT: CSV Results of response: "
    print out
"""

RESPONSE_TEMPLATES['action'] = """
print "...OUTPUT: Type of response: ", type(response)

print "...OUTPUT: Pretty print of response:"
print pprint.pformat(response)

print "...OUTPUT: Print of action object: "
print response['action_object']

# if results were returned (i.e. get_results=True was one of the kwargs passed in):
if response['action_results']:
    # call the export_obj() method to convert response to CSV and store it in out
    export_kwargs = {{}}
    export_kwargs['obj'] = response['action_results']
    export_kwargs['export_format'] = 'csv'
    print "...CALLING: handler.export_obj() with args {{}}".format(export_kwargs)
    out = handler.export_obj(**export_kwargs)

    # trim the output if it is more than 15 lines long
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\\n'.join(out)

    print "...OUTPUT: CSV Results of response: "
    print out
"""

RESPONSE_TEMPLATES['object'] = """
print "...OUTPUT: Type of response: ", type(response)

print "...OUTPUT: print of response:"
print response

# call the export_obj() method to convert response to JSON and store it in out
export_kwargs = {{}}
export_kwargs['obj'] = response
export_kwargs['export_format'] = 'json'

print "...CALLING: handler.export_obj() with args {{}}".format(export_kwargs)
out = handler.export_obj(**export_kwargs)

# trim the output if it is more than 15 lines long
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)

print "...OUTPUT: print the objects returned in JSON format:"
print out
"""

RESPONSE_TEMPLATES['object_delete_after'] = """
print "...OUTPUT: Type of response: ", type(response)
print "...OUTPUT: print of response:"
print response

# call the export_obj() method to convert response to JSON and store it in out
export_kwargs = {{}}
export_kwargs['obj'] = response
export_kwargs['export_format'] = 'json'
print "...CALLING: handler.export_obj() with args {{}}".format(export_kwargs)
out = handler.export_obj(**export_kwargs)

# trim the output if it is more than 15 lines long
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)

print "...OUTPUT: print the objects returned in JSON format:"
print out

# delete the object, we are done with it now
print "...CALLING: handler.delete() with args: {{}}".format(delete_kwargs)
delete_response = handler.delete(**delete_kwargs)

print "...OUTPUT: print the delete response"
print delete_response
"""

RESPONSE_TEMPLATES['export_obj'] = """
# trim the output if it is more than 15 lines long
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)

print "...OUTPUT: print the export_str returned from export_obj():"
print out
"""

BASIC_PY_CODE = """# import the basic python packages we need
import os
import sys
import tempfile
import pprint
import traceback

# disable python from generating a .pyc file
sys.dont_write_bytecode = True

# change me to the path of pytan if this script is not running from EXAMPLES/PYTAN_API
pytan_loc = "~/gh/pytan"
pytan_static_path = os.path.join(os.path.expanduser(pytan_loc), 'lib')

# Determine our script name, script dir
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)

# try to automatically determine the pytan lib directory by assuming it is in '../../lib/'
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')

# add pytan_loc and lib_dir to the PYTHONPATH variable
path_adds = [lib_dir, pytan_static_path]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

# import pytan
import pytan

# create a dictionary of arguments for the pytan handler
handler_args = {{}}

# establish our connection info for the Tanium Server
handler_args['username'] = "{username}"
handler_args['password'] = "{password}"
handler_args['host'] = "{host}"
handler_args['port'] = "{port}"  # optional

# optional, level 0 is no output except warnings/errors
# level 1 through 12 are more and more verbose
handler_args['loglevel'] = 1

# optional, use a debug format for the logging output (uses two lines per log entry)
handler_args['debugformat'] = False

# optional, this saves all response objects to handler.session.ALL_REQUESTS_RESPONSES
# very useful for capturing the full exchange of XML requests and responses
handler_args['record_all_requests'] = True

# instantiate a handler using all of the arguments in the handler_args dictionary
print "...CALLING: pytan.handler() with args: {{}}".format(handler_args)
handler = pytan.Handler(**handler_args)

# print out the handler string
print "...OUTPUT: handler string: {{}}".format(handler)"""

BASIC_NAME = "pytan_api_basic_handler_example"
BASIC_DESC = """This is an example for how to instantiate a :class:`pytan.Handler` object.

The username, password, host, and maybe port as well need to be provided on a per Tanium server basis."""
SOAP_BASIC_NAME = "basic_api_authentication"
SOAP_BASIC_DESC = """This is an example for how to authenticate against the SOAP API"""

RESPONSE_BLOCK_TEMPLATE = """
Request description: {0.pytan_help}
Request URL: {0.request.url}
Request Headers: {0.request.headers}
Request Body: {0.request.body}

Response Headers: {0.headers}
Response Encoding: {0.encoding}
Response Elapsed: {0.elapsed}
Response Body: {0.text}
"""

general_subs = {}
general_subs["API_INFO"] = (
    '''-u {username} -p '{password}' --host {host} --port {port} --loglevel {loglevel}'''
).format(**API_INFO.SERVER_INFO)
general_subs["TANIUM_HOST"] = API_INFO.SERVER_INFO['host']
general_subs["TANIUM_USERNAME"] = API_INFO.SERVER_INFO['username']
general_subs["TANIUM_PASSWORD"] = API_INFO.SERVER_INFO['password']
general_subs["TMPDIR"] = '/tmp'
general_subs['AUTHOR'] = pytan.__author__
general_subs['VERSION'] = pytan.__version__
general_subs['PYTAN_DIR'] = pytan_root

bin_doc_ini = """[CONFIG]
mainheader: ${title_name} Readme
output_blocks: true
valid_blocks: true
basename: ${script_name}
contact: ${AUTHOR}

${sections}
"""

bin_doc_ini_section = """[${name}]
headerdepth: ${depth}
cmd: ${cmd}
validtests: ${tests}
${notes_out}
${others_out}
"""

bin_doc_index = """PyTan Command Line Scripts
==========================

This is the help section for using the Command Line functionality provided by PyTan.

When running these scripts from OS X or Linux, you will want to run the .py scripts from the bin/ directory.

When running these scripts from Windows, you will want to run the .bat scripts from the winbin/ directory. The .bat files in the winbin/ directory handle calling the python binary appropriately. Also, when running these scripts on Windows, ensure arguments that need to be quoted are enclosed in double quotes in order for Windows to properly parse your command line.

{tocitems}
"""
