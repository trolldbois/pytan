#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Build the bin/ and winbin/ scripts'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.1.0'

import sys
sys.dont_write_bytecode = True

import os
import glob
import string

my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

import pytan
import pytan.binsupport

py_file = "${name}.py"
bat_file = "${name}.bat"

py_template = """#!/usr/bin/env python${pyopts}
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''${docstring}'''
__author__ = '${author}'
__version__ = '${version}'

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

bat_template = """@echo off
set my_dir=%~dp0%
call %my_dir%\CONFIG.bat
set my_script_name=%~n0%
%PYTHON%${pyopts} %my_dir%\\..\\bin\\%my_script_name%.py %*
"""

config_bat_template = '''@echo off
set PYTHON=C:\Python27\python.exe
'''

map_template = """#!/usr/bin/env python${pyopts}
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''${docstring}'''
__author__ = '${author}'
__version__ = '${version}'

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
        parser=parser, handler=handler, obj='${objname}', all_args=all_args,
    )
"""

get_report_parser = "    pytan.binsupport.add_get_object_report_argparser(parser=parser)\n"

scripts = [
    {
        'docstring': 'Ask a manual question and save the results as a report format',
        'name': 'ask_manual',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Ask a parsed question and save the results as a report format',
        'name': 'ask_parsed',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Ask a saved question and save the results as a report format',
        'name': 'ask_saved',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Create a group object from command line arguments',
        'name': 'create_group',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Create a package object from command line arguments',
        'name': 'create_package',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Create a sensor object from command line arguments (Not supported)',
        'name': 'create_sensor',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Create a sensor object from command line arguments (Not supported)',
        'name': 'create_sensor',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Create a user object from command line arguments',
        'name': 'create_user',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Create a Whitelisted URL object from command line arguments',
        'name': 'create_whitelisted_url',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Deploy an action and save the results as a report format',
        'name': 'deploy_action',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Get results from a deploy action, saved question, or question',
        'name': 'get_results',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Prints sensor information to stdout',
        'name': 'print_sensors',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Prints server information to stdout',
        'name': 'print_server_info',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Provides an interactive console with pytan available as handler',
        'name': 'pytan_shell',
        'pyopts': ' -i',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Stop an action by ID',
        'name': 'stop_action',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'docstring': 'Tanium Sensor Analysis Tool: asks a question for every sensor and saves the results as CSV reports',
        'name': 'tsat',
        'pyopts': '',
        'py_template': py_template,
        'bat_template': bat_template,
    },
    {
        'name': 'CONFIG',
        'bat_template': config_bat_template,
    },
]

other_subs = {
    'author': __author__,
    'version': __version__,
}

for i in pytan.constants.GET_OBJ_MAP:
    d = {}
    d['name'] = "get_{}".format(i)
    d['pyopts'] = ''
    d['objname'] = i
    d['docstring'] = "Get an object of type: {} and save the object to a report file".format(i)
    d['py_template'] = map_template
    d['bat_template'] = bat_template
    d['reportparser'] = get_report_parser
    d['maptype'] = 'get_object'
    scripts.append(d)

for i in pytan.constants.GET_OBJ_MAP:
    if not pytan.constants.GET_OBJ_MAP[i]['delete']:
        continue
    d = {}
    d['name'] = "delete_{}".format(i)
    d['pyopts'] = ''
    d['objname'] = i
    d['docstring'] = "Delete an object of type: {}".format(i)
    d['py_template'] = map_template
    d['bat_template'] = bat_template
    d['reportparser'] = ''
    d['maptype'] = 'delete_object'
    scripts.append(d)

for i in pytan.constants.GET_OBJ_MAP:
    if not pytan.constants.GET_OBJ_MAP[i]['create_json']:
        continue
    d = {}
    d['name'] = "create_{}_from_json".format(i)
    d['pyopts'] = ''
    d['objname'] = i
    d['docstring'] = "Create an object of type: {} from a JSON file".format(i)
    d['py_template'] = map_template
    d['bat_template'] = bat_template
    d['reportparser'] = ''
    d['maptype'] = 'create_json_object'
    scripts.append(d)


def clean_it(f):
    if os.path.exists(f):
        os.unlink(f)
        print "Removed {}".format(f)


def clean_up(p, pattern):
    print "## Cleaning up scripts in {}".format(p)
    for i in get_files(p, pattern):
        clean_it(i)


def get_files(p, pattern='*'):
    return glob.glob(os.path.join(p, pattern))


def write_file(f, c):
    with open(f, 'w') as fh:
        fh.write(c)
    print "Wrote file: {}".format(f)
    os.chmod(f, 0755)


if __name__ == "__main__":
    pytan.binsupport.version_check(reqver=__version__)

    output_bin = os.path.join(parent_dir, 'bin')
    output_winbin = os.path.join(parent_dir, 'winbin')

    clean_up(output_bin, '*.py')
    clean_up(output_winbin, '*.bat')

    for i in scripts:
        i.update(other_subs)
        if i.get('py_template'):
            script_out = string.Template(i['py_template']).safe_substitute(**i)
            script_file = string.Template(py_file).safe_substitute(**i)
            script_path = os.path.join(output_bin, script_file)
            write_file(script_path, script_out)
        if i.get('bat_template'):
            script_out = string.Template(i['bat_template']).safe_substitute(**i)
            script_file = string.Template(bat_file).safe_substitute(**i)
            script_path = os.path.join(output_winbin, script_file)
            write_file(script_path, script_out)
