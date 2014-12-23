#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''generates all of the examples from the test/ddt JSON files'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.0'

import os
import sys
import json
import StringIO
import contextlib
import glob
import pprint

sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

# import pytan
from pytan import utils

utils.version_check(__version__)


def read_file(f):
    with open(f) as fh:
        out = fh.read()
    return out


def json_read(f):
    return json.loads(read_file(f))


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def get_exec_output(c):
    print "executing code block:\n{}".format(c)
    with stdoutIO() as s:
        exec(c)
    return s.getvalue()


def indent_block(c):
    return '\n    ' + '\n    '.join(c.splitlines())


def get_name_title(t):
    return t.replace('_', ' ').capitalize()


def write_file(f, c):
    with open(f, 'w') as fh:
        fh.write(c)
    print "Wrote file: {}".format(f)


rst_name_template = "\n{{}}\n{}\n".format("=" * 90).format
rst_desc_template = "{}\n".format

example_py_out = '''
"""
{0}
"""
{1}
\'\'\'Output from running this:
{2}
\'\'\'
'''.format

example_index_rst_out = """
{}
----------------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 3
   :numbered:

   {}
""".format


def rst_code_block(c, out):
    base_block = """
{}
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: {}
    :linenos:

{}
""".format
    c_block = indent_block(c)
    code_block = base_block('Example Python Code', 'python', c_block)

    out_block = indent_block(out)
    output_block = base_block('Output from Python Code', 'none', out_block)
    ret = "{}\n{}".format(code_block, output_block)
    return ret

#####

test_dir = os.path.join(parent_dir, 'test')
ddt_dir = os.path.join(test_dir, 'ddt')
rst_out_dir = os.path.join(parent_dir, 'BUILD', 'doc', 'source', 'examples')
example_out_dir = os.path.join(parent_dir, 'EXAMPLES', 'API')
if not os.path.isdir(example_out_dir):
    os.makedirs(example_out_dir)

####################### BASE EXAMPLE

base_example = """# Path to lib directory which contains pytan package
PYTAN_LIB_PATH = '../lib'

# connection info for Tanium Server
USERNAME = "Tanium User"
PASSWORD = "T@n!um"
HOST = "172.16.31.128"
PORT = "444"

# Logging conrols
LOGLEVEL = 2
DEBUGFORMAT = False

import sys, tempfile
sys.path.append(PYTAN_LIB_PATH)

import pytan
handler = pytan.Handler(
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    loglevel=LOGLEVEL,
    debugformat=DEBUGFORMAT,
)

print handler
"""

old_files = glob.glob(rst_out_dir + '/*.*')
if old_files:
    for x in old_files:
        print "Cleaning up old example RST file {}".format(x)
        os.unlink(x)

old_files = glob.glob(example_out_dir + '/*.*')
if old_files:
    for x in old_files:
        print "Cleaning up old example RST file {}".format(x)
        os.unlink(x)

examples = []

base_name = "pytan_api_basic_handler_example"
base_desc = """Here is an example for how to instantiate a :class:`pytan.Handler` object.

The username, password, host, and maybe port as well need to be provided on a per Tanium server basis.
"""
out = get_exec_output(base_example)
example_rst_out = "{}{}{}".format(
    rst_name_template(get_name_title(base_name)),
    rst_desc_template(base_desc),
    rst_code_block(base_example, out)
)

example_rst_file = base_name + '.rst'
example_py_file = base_name + '.py'

examples.append(example_rst_file)
write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
write_file(
    os.path.join(example_out_dir, example_py_file), example_py_out(base_desc, base_example, out))


####################### VALID QUESTION DDT

ddt = os.path.join(ddt_dir, 'ddt_valid_questions.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):

    q_kwargs = ''.join([
        'kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the arguments for the handler method
kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """
# call the handler with the {0} method, passing in kwargs for arguments
response = handler.{0}(**kwargs)
""".format(qinfo['method'])

    q_response = """import pprint, io

print ""
print "Type of response: ", type(response)

print ""
print "Pretty print of response:"
print pprint.pformat(response)

print ""
print "Equivalent Question if it were to be asked in the Tanium Console: "
print response['question_object'].query_text

# create an IO stream to store CSV results to
out = io.BytesIO()

# call the write_csv() method to convert response to CSV and store it in out
response['question_results'].write_csv(out, response['question_results'])

print ""
print "CSV Results of response: "
out = out.getvalue()
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)
print out
"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'
    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'valid_questions.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Valid Question Examples', '\n   '.join(q_examples)))
examples.append('valid_questions')

####################### INVALID QUESTION DDT

ddt = os.path.join(ddt_dir, 'ddt_invalid_questions.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):

    q_kwargs = ''.join([
        'kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the arguments for the handler method
kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """

# call the handler with the {0} method, passing in kwargs for arguments
# this should throw an exception: {1}
import traceback
try:
    handler.{0}(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)

""".format(qinfo['method'], qinfo['exception'])

    q_response = """"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'invalid_questions.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Invalid Question Examples', '\n   '.join(q_examples)))
examples.append('invalid_questions')

####################### VALID GET OBJECT DDT

ddt = os.path.join(ddt_dir, 'ddt_valid_get_object.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):

    q_kwargs = ''.join([
        'kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the arguments for the handler method
kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """
# call the handler with the {0} method, passing in kwargs for arguments
response = handler.{0}(**kwargs)
""".format(qinfo['method'])

    q_response = """
print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "length of response (number of objects returned): "
print len(response)

print ""
print "print the first object returned in JSON format:"
out = response.to_json(response[0])
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)

print out

"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'valid_get_objects.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Valid Get Object Examples', '\n   '.join(q_examples)))
examples.append('valid_get_objects')

####################### INVALID GET OBJECT DDT

ddt = os.path.join(ddt_dir, 'ddt_invalid_get_object.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):

    q_kwargs = ''.join([
        'kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the arguments for the handler method
kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """

# call the handler with the {0} method, passing in kwargs for arguments
# this should throw an exception: {1}
import traceback
try:
    handler.{0}(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)

""".format(qinfo['method'], qinfo['exception'])

    q_response = """"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'invalid_get_objects.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Invalid Get Object Examples', '\n   '.join(q_examples)))
examples.append('invalid_get_objects')

####################### VALID DEPLOY ACTION DDT

ddt = os.path.join(ddt_dir, 'ddt_valid_deploy_action.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):

    q_kwargs = ''.join([
        'kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the arguments for the handler method
kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """
# call the handler with the {0} method, passing in kwargs for arguments
response = handler.{0}(**kwargs)
""".format(qinfo['method'])

    q_response = """import pprint, io

print ""
print "Type of response: ", type(response)

print ""
print "Pretty print of response:"
print pprint.pformat(response)

print ""
print "Print of action object: "
print response['action_object']

# create an IO stream to store CSV results to
out = io.BytesIO()

# if results were returned (i.e. get_results=True was one of the kwargs passed in):
if response['action_results']:
    # call the write_csv() method to convert response to CSV and store it in out
    response['action_results'].write_csv(out, response['action_results'])

    print ""
    print "CSV Results of response: "
    print out.getvalue()

"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'valid_deploy_actions.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Valid Deploy Action Examples', '\n   '.join(q_examples)))
examples.append('valid_deploy_actions')

####################### INVALID DEPLOY ACTION DDT

ddt = os.path.join(ddt_dir, 'ddt_invalid_deploy_action.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):

    q_kwargs = ''.join([
        'kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the arguments for the handler method
kwargs = {{}}
kwargs['report_dir'] = tempfile.gettempdir()
{}""".format(q_kwargs)

    q_method = """

# call the handler with the {0} method, passing in kwargs for arguments
# this should throw an exception: {1}
import traceback
try:
    handler.{0}(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)

""".format(qinfo['method'], qinfo['exception'])

    q_response = """"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'invalid_deploy_actions.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Invalid Deploy Action Examples', '\n   '.join(q_examples)))
examples.append('invalid_deploy_actions')

####################### VALID CREATE OBJECT DDT

ddt = os.path.join(ddt_dir, 'ddt_valid_create_object.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):
    delete_args = {str(k): str(v) for k, v in qinfo['delete'].iteritems()}
    q_delete_args = ''.join([
        'delete_kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in delete_args.iteritems()
    ])

    q_kwargs = ''.join([
        'kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the arguments for the delete method (to remove the package in case it exists)
delete_kwargs = {{}}
{}

# setup the arguments for the handler method
kwargs = {{}}
{}""".format(q_delete_args, q_kwargs)

    q_method = """
# delete the object in case it already exists
try:
    handler.delete(**delete_kwargs)
except Exception as e:
    print e

# call the handler with the {0} method, passing in kwargs for arguments
response = handler.{0}(**kwargs)

""".format(qinfo['method'])

    q_response = """
print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "print the object returned in JSON format:"
print response.to_json(response)

# delete the object, we are done with it now
try:
    handler.delete(**delete_kwargs)
except Exception as e:
    print e

"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'valid_create_objects.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Valid Create Object Examples', '\n   '.join(q_examples)))
examples.append('valid_create_objects')

####################### INVALID CREATE OBJECT DDT

ddt = os.path.join(ddt_dir, 'ddt_invalid_create_object.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):

    q_kwargs = ''.join([
        'kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the arguments for the handler method
kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """

# call the handler with the {0} method, passing in kwargs for arguments
# this should throw an exception: {1}
import traceback
try:
    handler.{0}(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)

""".format(qinfo['method'], qinfo['exception'])

    q_response = """"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'invalid_create_objects.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Invalid Create Object Examples', '\n   '.join(q_examples)))
examples.append('invalid_create_objects')

####################### VALID CREATE OBJECT FROM JSON DDT

ddt = os.path.join(ddt_dir, 'ddt_valid_create_object_from_json.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):
    aname = ''
    avalue = ''

    if qinfo['transform']:
        aname = qinfo['transform'][0]
        avalue = qinfo['transform'][1]

    q_kwargs = ''.join([
        'get_kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['get'].iteritems()
    ])
    q_kwargs = """
# set the attribute name and value we want to add to the original object (if any)
attr_name = "{}"
attr_add = "{}"

# delete object before creating it?
delete = {}

# setup the arguments for getting an object to export as json file
get_kwargs = {{}}
{}""".format(aname, avalue, qinfo['delete'], q_kwargs)

    q_method = """

# get objects to use as an export to JSON file
orig_objs = handler.get(**get_kwargs)

# if attr_name and attr_add exists, modify the orig_objs to add attr_add to the attribute
# attr_name
if attr_name:
    for x in orig_objs:
        new_attr = getattr(x, attr_name)
        new_attr += attr_add
        setattr(x, attr_name, new_attr)
        if delete:
            # delete the object in case it already exists
            del_kwargs = {{}}
            del_kwargs[attr_name] = new_attr
            del_kwargs['objtype'] = {0!r}
            try:
                handler.delete(**del_kwargs)
            except Exception as e:
                print e

# export orig_objs to a json file
json_file, results = handler.export_to_report_file(
    obj=orig_objs,
    export_format='json',
    report_dir=tempfile.gettempdir(),
)

# create the object from the exported JSON file
create_kwargs = {{'objtype': {0!r}, 'json_file': json_file}}
response = handler.create_from_json(**create_kwargs)

""".format(qinfo['objtype'])

    q_response = """
print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "print the object returned in JSON format:"
print response.to_json(response)
"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'valid_create_objects_from_json.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Valid Create Object From JSON Examples', '\n   '.join(q_examples)))
examples.append('valid_create_objects_from_json')

####################### INVALID CREATE OBJECT FROM JSON DDT

ddt = os.path.join(ddt_dir, 'ddt_invalid_create_object_from_json.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):
    q_kwargs = ''.join([
        'get_kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['get'].iteritems()
    ])
    q_kwargs = """
# setup the arguments for getting an object to export as json file
get_kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """
# get objects to use as an export to JSON file
orig_objs = handler.get(**get_kwargs)

# export orig_objs to a json file
json_file, results = handler.export_to_report_file(
    obj=orig_objs,
    export_format='json',
    report_dir=tempfile.gettempdir(),
)

# call the handler with the create_from_json method, passing in kwargs for arguments
# this should throw an exception: {1}
import traceback

# create the object from the exported JSON file
create_kwargs = {{'objtype': {0!r}, 'json_file': json_file}}
try:
    response = handler.create_from_json(**create_kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)

""".format(qinfo['objtype'], qinfo['exception'])

    q_response = """"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'invalid_create_objects_from_json.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Invalid Create Object From JSON Examples', '\n   '.join(q_examples)))
examples.append('invalid_create_objects_from_json')

####################### VALID EXPORT RESULTSET DDT

ddt = os.path.join(ddt_dir, 'ddt_valid_export_resultset.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):
    q_kwargs = ''.join([
        'export_kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the export_obj kwargs for later
export_kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """
# ask the question that will provide the resultset that we want to use
ask_kwargs = {{
    'qtype': 'manual_human',
    'sensors': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match{{dirname=Program Files,regex=.*Shared.*}}',
    ],
}}
response = handler.ask(**ask_kwargs)

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
export_kwargs['obj'] = response['question_results']
export_str = handler.export_obj(**export_kwargs)

""".format()

    q_response = """
print ""
print "print the export_str returned from export_obj():"
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)

print out
"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'valid_export_resultset.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Valid Export ResultSet Examples', '\n   '.join(q_examples)))
examples.append('valid_export_resultset')

####################### INVALID EXPORT RESULTSET DDT

ddt = os.path.join(ddt_dir, 'ddt_invalid_export_resultset.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):
    q_kwargs = ''.join([
        'export_kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the export_obj kwargs for later
export_kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """
# ask the question that will provide the resultset that we want to use
ask_kwargs = {{
    'qtype': 'manual_human',
    'sensors': [
        "Computer Name"
    ],
}}
response = handler.ask(**ask_kwargs)
export_kwargs['obj'] = response['question_results']

# export the object to a string
# this should throw an exception: {0}
import traceback

try:
    handler.export_obj(**export_kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)

""".format(qinfo['exception'])

    q_response = """"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'invalid_export_resultset.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Invalid Export ResultSet Examples', '\n   '.join(q_examples)))
examples.append('invalid_export_resultset')

####################### VALID EXPORT BASETYPE DDT

ddt = os.path.join(ddt_dir, 'ddt_valid_export_basetype.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):
    q_kwargs = ''.join([
        'export_kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the export_obj kwargs for later
export_kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """
# get the objects that will provide the basetype that we want to use
get_kwargs = {{
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match',
    ],
    'objtype': 'sensor',
}}
response = handler.get(**get_kwargs)

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
export_kwargs['obj'] = response
export_str = handler.export_obj(**export_kwargs)

""".format()

    q_response = """
print ""
print "print the export_str returned from export_obj():"

out = export_str
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)

print out
"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'valid_export_basetype.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Valid Export BaseType Examples', '\n   '.join(q_examples)))
examples.append('valid_export_basetype')

####################### INVALID EXPORT BASETYPE DDT

ddt = os.path.join(ddt_dir, 'ddt_invalid_export_basetype.json')
ddt_objs = json_read(ddt)

q_examples = []
for qname, qinfo in sorted(ddt_objs.items(), key=lambda x: x[1]['priority']):
    q_kwargs = ''.join([
        'export_kwargs["{}"] = {}\n'.format(k, pprint.pformat(v))
        for k, v in qinfo['args'].iteritems()
    ])
    q_kwargs = """
# setup the export_obj kwargs for later
export_kwargs = {{}}
{}""".format(q_kwargs)

    q_method = """
# get the objects that will provide the basetype that we want to use
get_kwargs = {{
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match',
    ],
    'objtype': 'sensor',
}}
response = handler.get(**get_kwargs)
export_kwargs['obj'] = response

# export the object to a string
# this should throw an exception: {0}
import traceback

try:
    handler.export_obj(**export_kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)

""".format(qinfo['exception'])

    q_response = """"""
    q_code = '{}{}{}{}\n'.format(base_example, q_kwargs, q_method, q_response)
    example_rst_file = qname + '.rst'
    example_py_file = qname + '.py'

    out = get_exec_output(q_code)
    example_rst_out = "{}{}{}".format(
        rst_name_template(get_name_title(qname)),
        rst_desc_template(qinfo['desc']),
        rst_code_block(q_code, out)
    )
    q_examples.append(example_rst_file)
    write_file(os.path.join(rst_out_dir, example_rst_file), example_rst_out)
    write_file(
        os.path.join(example_out_dir, example_py_file), example_py_out(qinfo['desc'], q_code, out))

q_examples_rst = os.path.join(rst_out_dir, 'invalid_export_basetype.rst')
write_file(q_examples_rst, example_index_rst_out(
    'pytan API Invalid Export BaseType Examples', '\n   '.join(q_examples)))
examples.append('invalid_export_basetype')

####################### EXAMPLE INDEX

examples_rst = os.path.join(rst_out_dir, 'pytan_examples.rst')

write_file(examples_rst, example_index_rst_out('pytan API examples', '\n   '.join(examples)))
