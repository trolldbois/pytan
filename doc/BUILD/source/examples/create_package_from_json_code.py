# import the basic python packages we need
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
handler_args = {}

# establish our connection info for the Tanium Server
handler_args['username'] = "Administrator"
handler_args['password'] = "Tanium2015!"
handler_args['host'] = "10.0.1.240"
handler_args['port'] = "443"  # optional

# optional, level 0 is no output except warnings/errors
# level 1 through 12 are more and more verbose
handler_args['loglevel'] = 1

# optional, use a debug format for the logging output (uses two lines per log entry)
handler_args['debugformat'] = False

# optional, this saves all response objects to handler.session.ALL_REQUESTS_RESPONSES
# very useful for capturing the full exchange of XML requests and responses
handler_args['record_all_requests'] = True

# instantiate a handler using all of the arguments in the handler_args dictionary
print "...CALLING: pytan.handler() with args: {}".format(handler_args)
handler = pytan.Handler(**handler_args)

# print out the handler string
print "...OUTPUT: handler string: {}".format(handler)

# setup the arguments for the handler.get() method
get_kwargs = {}
get_kwargs["objtype"] = u'package'
get_kwargs["id"] = 31

# get objects to use as an export to JSON file
print "...CALLING: handler.get() with args: {}".format(get_kwargs)
orig_objs = handler.get(**get_kwargs)

# set the attribute name and value we want to add to the original objects
# this is necessarry to avoid name conflicts when adding the new object
attr_name = u'name'
attr_value = u' API TEST'

# modify the orig_objs to add attr_value to attr_name
for x in orig_objs:
    new_attr = getattr(x, attr_name)
    new_attr += attr_value
    setattr(x, attr_name, new_attr)

    # delete the object in case it already exists
    del_kwargs = {}
    del_kwargs[attr_name] = new_attr
    del_kwargs['objtype'] = u'package'

    print "...CALLING: handler.delete() with args: {}".format(del_kwargs)
    try:
        handler.delete(**del_kwargs)
    except Exception as e:
        print "...EXCEPTION: {}".format(e)

# export orig_objs to a json file
export_kwargs = {}
export_kwargs['obj'] = orig_objs
export_kwargs['export_format'] = 'json'
export_kwargs['report_dir'] = tempfile.gettempdir()

print "...CALLING: handler.export_to_report_file() with args: {}".format(export_kwargs)
json_file, results = handler.export_to_report_file(**export_kwargs)

# create the object from the exported JSON file
create_kwargs = {}
create_kwargs['objtype'] = u'package'
create_kwargs['json_file'] = json_file

print "...CALLING: handler.create_from_json() with args {}".format(create_kwargs)
response = handler.create_from_json(**create_kwargs)

print "...OUTPUT: Type of response: ", type(response)

print "...OUTPUT: print of response:"
print response

# call the export_obj() method to convert response to JSON and store it in out
export_kwargs = {}
export_kwargs['obj'] = response
export_kwargs['export_format'] = 'json'

print "...CALLING: handler.export_obj() with args {}".format(export_kwargs)
out = handler.export_obj(**export_kwargs)

# trim the output if it is more than 15 lines long
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)

print "...OUTPUT: print the objects returned in JSON format:"
print out
