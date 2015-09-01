#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''generates all of the examples from the test/ddt JSON files'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.1.0'

import os
import sys
import json
import StringIO
import contextlib
import glob
import pprint
import tempfile

sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan

pytan.utils.version_check(__version__)

EXAMPLE_PY_TEMPLATE = '''
"""
{desc}
"""
{py_code}
\'\'\'Output from running this:
{py_output}
\'\'\'
'''

EXAMPLE_RST_TEMPLATE = """
{title}
========================================================================================

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

If you copy them outside of the EXAMPLE/POC directory to edit and run them, you will
also need to update the pytan_loc variable to point to the directory where pytan lives.

{tocitems}
"""

CODE_BLOCK_TEMPLATE = """
{title}
----------------------------------------------------------------------------------------

.. code-block:: {code_type}
    :linenos:

{code_block}
"""

HANDLER_ARGS_TEMPLATE = """
# setup the arguments for the handler method
{args_name} = {{}}
{args_str}
"""

METHOD_TEMPLATES = {}
METHOD_TEMPLATES['valid_response'] = """
# call the handler with the {method} method, passing in kwargs for arguments
response = handler.{method}(**kwargs)
"""
METHOD_TEMPLATES['invalid_basic'] = """
# call the handler with the {method} method, passing in kwargs for arguments
# this should throw an exception: {exception}
import traceback
try:
    handler.{method}(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)
"""
METHOD_TEMPLATES['delete_first'] = """
# delete the object in case it already exists
try:
    handler.delete(**delete_kwargs)
except Exception as e:
    print e

# call the handler with the {method} method, passing in kwargs for arguments
response = handler.{method}(**kwargs)
"""
METHOD_TEMPLATES['create_from_json'] = """
# set the attribute name and value we want to add to the original object (if any)
attr_name = {transform_attr!r}
attr_value = {transform_value!r}

# delete object before creating it?
delete_before = {delete_before}

# get objects to use as an export to JSON file
orig_objs = handler.get(**get_kwargs)

# if attr_name is set, modify the orig_objs to add attr_value to attr_name
if attr_name:
    for x in orig_objs:
        new_attr = getattr(x, attr_name)
        new_attr += attr_value
        setattr(x, attr_name, new_attr)
        if delete_before:
            # delete the object in case it already exists
            del_kwargs = {{}}
            del_kwargs[attr_name] = new_attr
            del_kwargs['objtype'] = {objtype!r}
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
create_kwargs = {{'objtype': {objtype!r}, 'json_file': json_file}}
response = handler.create_from_json(**create_kwargs)
"""
METHOD_TEMPLATES['invalid_create_from_json'] = """
# get objects to use as an export to JSON file
orig_objs = handler.get(**get_kwargs)

# export orig_objs to a json file
json_file, results = handler.export_to_report_file(
    obj=orig_objs,
    export_format='json',
    report_dir=tempfile.gettempdir(),
)

# call the handler with the create_from_json method, passing in kwargs for arguments
# this should throw an exception: {exception}
import traceback

# create the object from the exported JSON file
create_kwargs = {{'objtype': {objtype!r}, 'json_file': json_file}}
try:
    response = handler.create_from_json(**create_kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)

"""
METHOD_TEMPLATES['export_resultset'] = """
# ask the question that will provide the resultset that we want to use
ask_kwargs = {{
    'qtype': 'manual',
    'sensors': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match{{dirname=Program Files,regex=.*Shared.*}}',
    ],
}}
response = handler.ask(**ask_kwargs)

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
kwargs['obj'] = response['question_results']
out = handler.export_obj(**kwargs)
"""
METHOD_TEMPLATES['invalid_export_resultset'] = """
# ask the question that will provide the resultset that we want to use
ask_kwargs = {{
    'qtype': 'manual',
    'sensors': [
        "Computer Name"
    ],
}}
response = handler.ask(**ask_kwargs)
kwargs['obj'] = response['question_results']

# export the object to a string
# this should throw an exception: {exception}
import traceback

try:
    handler.export_obj(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)
"""
METHOD_TEMPLATES['export_basetype'] = """
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
kwargs['obj'] = response
out = handler.export_obj(**kwargs)
"""
METHOD_TEMPLATES['invalid_export_basetype'] = """
# get the objects that will provide the basetype that we want to use
get_kwargs = {{
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match',
    ],
    'objtype': 'sensor',
}}
response = handler.get(**get_kwargs)
kwargs['obj'] = response

# export the object to a string
# this should throw an exception: {exception}
import traceback

try:
    handler.export_obj(**kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)
"""

RESPONSE_TEMPLATES = {}
RESPONSE_TEMPLATES['question'] = """
print ""
print "Type of response: ", type(response)

print ""
print "Pretty print of response:"
print pprint.pformat(response)

print ""
print "Equivalent Question if it were to be asked in the Tanium Console: "
print response['question_object'].query_text

# call the export_obj() method to convert response to CSV and store it in out
out = handler.export_obj(response['question_results'], 'csv')

print ""
print "CSV Results of response: "
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)
print out
"""
RESPONSE_TEMPLATES['action'] = """
print ""
print "Type of response: ", type(response)

print ""
print "Pretty print of response:"
print pprint.pformat(response)

print ""
print "Print of action object: "
print response['action_object']

# if results were returned (i.e. get_results=True was one of the kwargs passed in):
if response['action_results']:
    # call the export_obj() method to convert response to CSV and store it in out
    out = handler.export_obj(response['action_results'], 'csv')

    print ""
    print "CSV Results of response: "
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\\n'.join(out)
    print out
"""
RESPONSE_TEMPLATES['object'] = """
print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "print the objects returned in JSON format:"
out = handler.export_obj(response, 'json')
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)

print out
"""
RESPONSE_TEMPLATES['object_delete_after'] = """
print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "print the objects returned in JSON format:"
out = handler.export_obj(response, 'json')
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)

print out

# delete the object, we are done with it now
try:
    handler.delete(**delete_kwargs)
except Exception as e:
    print e
"""
RESPONSE_TEMPLATES['export_obj'] = """
print ""
print "print the export_str returned from export_obj():"

if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\\n'.join(out)

print out
"""

BASIC_PY_CODE = """
import os
import sys
import tempfile
import pprint
sys.dont_write_bytecode = True

# change me to the path of pytan if this script is not running from EXAMPLES/PYTAN_API
pytan_loc = "~/gh/pytan"
pytan_static_path = os.path.join(os.path.expanduser(pytan_loc), 'lib')

# Determine our script name, script dir
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)

# determine the pytan lib dir and add it to the path
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')
path_adds = [lib_dir, pytan_static_path]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

# connection info for Tanium Server
USERNAME = "Administrator"
PASSWORD = "Tanium2015!"
HOST = "10.0.1.240"
PORT = "443"  # optional

# Logging controls
LOGLEVEL = 2  # optional
DEBUGFORMAT = False  # optional

# optional, this saves all response objects to handler.session.ALL_REQUESTS_RESPONSES
# very useful for capturing the full exchange of XML requests and responses
RECORD_ALL_REQUESTS = True

import pytan
handler = pytan.Handler(
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    loglevel=LOGLEVEL,
    debugformat=DEBUGFORMAT,
    record_all_requests=RECORD_ALL_REQUESTS,
)

print handler
"""
BASIC_NAME = "pytan_api_basic_handler_example"
BASIC_DESC = """This is an example for how to instantiate a :class:`pytan.Handler` object.

The username, password, host, and maybe port as well need to be provided on a per Tanium server basis.
"""

GET_COMS = "handler.session.ALL_REQUESTS_RESPONSES"

RESPONSE_BLOCK_TEMPLATE = """
Request URL: {0.request.url}
Request Headers: {0.request.headers}
Request Body: {0.request.body}

Response Headers: {0.headers}
Response Body: {0.text}
Response Encoding: {0.encoding}
Response Elapsed: {0.elapsed}
"""


class ExampleProcesser(object):
    rst_examples = []
    py_examples = []
    VERBOSE = False

    def __init__(self):
        self.my_file = os.path.abspath(sys.argv[0])
        self.my_dir = os.path.dirname(self.my_file)
        self.parent_dir = os.path.dirname(self.my_dir)
        self.test_dir = os.path.join(self.parent_dir, 'test')
        self.ddt_dir = os.path.join(self.test_dir, 'ddt')

        # output directory for RST files
        self.rst_out_dir = os.path.join(tempfile.gettempdir(), 'REST_EXAMPLES')
        self.dest_rst_out_dir = os.path.join(parent_dir, 'BUILD', 'doc', 'source', 'examples')

        # output directory for python example files
        self.pytan_example_out_dir = os.path.join(tempfile.gettempdir(), 'PYTAN_API')
        self.dest_pytan_example_out_dir = os.path.join(parent_dir, 'EXAMPLES', 'PYTAN_API')

        # output directory for RST API example files
        self.soap_example_out_dir = os.path.join(tempfile.gettempdir(), 'SOAP_API')
        self.dest_soap_example_out_dir = os.path.join(parent_dir, 'EXAMPLES', 'SOAP_API')

    def clean_up_output_dirs(self):
        for i in [self.rst_out_dir, self.pytan_example_out_dir, self.soap_example_out_dir]:
            if not os.path.isdir(i):
                os.makedirs(i)

            old_files = glob.glob(i + '/*.*')
            if old_files:
                for x in old_files:
                    print "Cleaning up old file {}".format(x)
                    os.unlink(x)

    @contextlib.contextmanager
    def replace_stdout_with_stringio(self, stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO.StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    def get_exec_output(self, name, code_block):
        print "executing code block for {}".format(name)

        if self.VERBOSE:
            print "Code block:\n{}".format(code_block)

        with self.replace_stdout_with_stringio() as s:
            exec(code_block)

        code_output = s.getvalue()

        if self.VERBOSE:
            print "Code output:\n{}".format(code_output)

        response_objects = eval(GET_COMS)
        return code_output, response_objects

    def read_file(self, f):
        with open(f) as fh:
            out = fh.read()
        return out

    def json_read(self, f):
        return json.loads(self.read_file(f))

    def indent_block(self, c):
        return '\n    ' + '\n    '.join(c.splitlines())

    def get_name_title(self, t):
        fixes = {
            'Xml': 'XML',
            'Json': 'JSON',
            'Csv': 'CSV',
            'Pytan': 'PyTan',
            'Api': 'API',
            'Resultset': 'ResultSet',
            'Resultinfo': 'ResultInfo',
        }
        ret = t.replace('_', ' ').strip().title()
        for k, v in fixes.iteritems():
            ret = ret.replace(k, v)
        return ret

    def write_file(self, f, c):
        with open(f, 'w') as fh:
            fh.write(c)
        print "Wrote file: {}".format(f)

    def build_pytan_rst_title(self, name):
        title_sep = "{}".format("=" * 90)
        title_name = self.get_name_title(name)
        ret = "\n{}\n{}\n".format(title_name, title_sep)
        return ret

    def build_pytan_rst_desc(self, desc):
        return "{}\n".format(desc)

    def build_rst_pycode_block(self, py_code, py_output, code_title='Example Python Code',
                               output_title='Output from Python Code'):

        indented_code_block = self.indent_block(py_code)
        code_block = CODE_BLOCK_TEMPLATE.format(
            title=code_title, code_type='python', code_block=indented_code_block)

        indented_output_block = self.indent_block(py_output)
        output_block = CODE_BLOCK_TEMPLATE.format(
            title=output_title, code_type='none', code_block=indented_output_block)

        ret = "{}\n{}".format(code_block, output_block)
        return ret

    def build_response_blocks(self, response_objects):
        out = '\n'.join([RESPONSE_BLOCK_TEMPLATE.format(x) for x in response_objects])
        return out

    def build_pytan_rst_example(self, name, desc, py_code, py_output):
        example_rst_out = "{}\n{}{}".format(
            self.build_pytan_rst_title(name),
            self.build_pytan_rst_desc(desc),
            self.build_rst_pycode_block(py_code, py_output)
        )
        return example_rst_out

    def build_xml_example(self, name, desc, response_objects):
        example_xml_out = "{}\n{}{}".format(
            self.build_pytan_rst_title(name),
            self.build_pytan_rst_desc(desc),
            self.build_response_blocks(response_objects)
        )
        return example_xml_out

    def build_rst_filename(self, name):
        fn = name + '.rst'
        return fn

    def build_md_filename(self, name):
        fn = name + '.md'
        return fn

    def build_py_filename(self, name):
        fn = name + '.py'
        return fn

    def build_xml_filename(self, name):
        fn = name + '.xml'
        return fn

    def write_rst_file(self, name, out):
        filename = self.build_rst_filename(name)
        filepath = os.path.join(self.rst_out_dir, filename)
        self.write_file(filepath, out)

    def write_md_file(self, name, out, out_dir):
        filename = self.build_md_filename(name)
        filepath = os.path.join(out_dir, filename)
        self.write_file(filepath, out)

    def write_py_file(self, name, out, desc):
        filename = self.build_py_filename(name)
        filepath = os.path.join(self.pytan_example_out_dir, filename)
        self.write_file(filepath, out)
        self.py_examples.append({'filename': filename, 'desc': desc})

    def write_xml_file(self, name, out):
        filename = self.build_xml_filename(name)
        filepath = os.path.join(self.soap_example_out_dir, filename)
        self.write_file(filepath, out)

    def make_py_readme(self, name='README.MD'):
        title = "PyTan API Python Examples"
        toc_template = '  * {}: {}'.format
        tocitems = '\n'.join([toc_template(k, v.strip()) for z in self.py_examples for k, v in z])
        out = README_MD_TEMPLATE.format(title=title, tocitems=tocitems)
        self.write_md_file(name, out, self.pytan_example_out_dir)

    def make_rst_index(self, name='pytan_examples'):
        index_title = 'PyTan API Examples'
        index_tocitems = '\n   '.join(self.rst_examples)
        out = EXAMPLE_RST_TEMPLATE.format(title=index_title, tocitems=index_tocitems)
        self.write_rst_file(name, out)

    def make_examples(self, name, desc, py_code):
        py_output, response_objects = self.get_exec_output(name, py_code)
        self.make_rst_example(name, desc, py_code, py_output)
        self.make_py_example(name, desc, py_code, py_output)
        self.make_xml_example(name, desc, response_objects)

    def make_rst_example(self, name, desc, py_code, py_output):
        out = self.build_pytan_rst_example(name, desc, py_code, py_output)
        self.write_rst_file(name, out)

    def make_py_example(self, name, desc, py_code, py_output):
        out = EXAMPLE_PY_TEMPLATE.format(desc=desc, py_code=py_code, py_output=py_output)
        self.write_py_file(name, out, desc)

    def make_xml_example(self, name, desc, response_objects):
        out = self.build_xml_example(name, desc, response_objects)
        self.write_xml_file(name, out)

    def build_args_str(self, args_name, args):
        args_template = '{}["{}"] = {}'.format
        args_str_list = [
            args_template(args_name, k, pprint.pformat(v)) for k, v in args.iteritems()
        ]
        args_str = '\n'.join(args_str_list)
        return args_str

    def build_args_block(self, args_name, info, info_key):
        args_block = ''
        if info.get(info_key, ''):
            args_str = self.build_args_str(args_name, info[info_key])
            args_block = HANDLER_ARGS_TEMPLATE.format(args_name=args_name, args_str=args_str)
        return args_block

    def process_ddt(self, ddt_file):
        ddt_basename = ddt_file.replace('ddt_', '').replace('.json', '')
        ddt = os.path.join(self.ddt_dir, ddt_file)
        ddt_tests = self.json_read(ddt)
        self.ddt_examples = []

        for name, info in sorted(ddt_tests.items(), key=lambda x: x[1]['priority']):

            get_args_block = self.build_args_block('get_kwargs', info, 'get')
            delete_args_block = self.build_args_block('delete_kwargs', info, 'delete')
            args_block = self.build_args_block('kwargs', info, 'args')

            method_template = METHOD_TEMPLATES.get(info['method_template'], '')
            method_block = method_template.format(**info)

            response_template = RESPONSE_TEMPLATES.get(info['response_template'], '')
            response_block = response_template.format(**info)

            py_code_items = [
                BASIC_PY_CODE,
                get_args_block,
                delete_args_block,
                args_block,
                method_block,
                response_block
            ]

            py_code_items = [x for x in py_code_items if x]
            py_code = '\n'.join(py_code_items)

            self.make_examples(name, info['desc'], py_code)

            ddt_example_file = self.build_rst_filename(name)
            self.ddt_examples.append(ddt_example_file)

        index_title = 'PyTan API {} Examples'.format(self.get_name_title(ddt_basename))
        index_tocitems = '\n   '.join(self.ddt_examples)
        index_out = EXAMPLE_RST_TEMPLATE.format(title=index_title, tocitems=index_tocitems)
        self.write_rst_file(ddt_basename, index_out)
        self.rst_examples.append(ddt_basename)

    def main(self):
        self.clean_up_output_dirs()

        self.make_examples(BASIC_NAME, BASIC_DESC, BASIC_PY_CODE)
        self.rst_examples.append(BASIC_NAME)

        valid_json_files = sorted(glob.glob(self.ddt_dir + '/ddt_valid_*.*'))
        invalid_json_files = sorted(glob.glob(self.ddt_dir + '/ddt_invalid_*.*'))

        all_json_files = valid_json_files + invalid_json_files
        all_json_files = [os.path.basename(x) for x in all_json_files]

        skip_json_files = ['ddt_invalid_connects.json']
        all_json_files = [x for x in all_json_files if x not in skip_json_files]

        for x in all_json_files:
            print "Now processing ddt file: {}".format(x)
            self.process_ddt(x)

        self.make_rst_index()
        self.make_py_readme()


ep = ExampleProcesser()

# if __name__ == '__main__':
ep.main()
