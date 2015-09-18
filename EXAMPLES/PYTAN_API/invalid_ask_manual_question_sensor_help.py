#!/usr/bin/env python
"""
Have ask_manual() return the help for sensors
"""
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

# setup the arguments for the handler() class
kwargs = {}
kwargs["qtype"] = u'manual'
kwargs["sensors_help"] = True

print "...CALLING: handler.ask() with args: {}".format(kwargs)
try:
    handler.ask(**kwargs)
except Exception as e:
    print "...EXCEPTION: {}".format(e)
    # this should throw an exception of type: pytan.exceptions.PytanHelp
    # uncomment to see full exception
    # traceback.print_exc(file=sys.stdout)
'''STDOUT from running this:
...CALLING: pytan.handler() with args: {'username': 'Administrator', 'record_all_requests': True, 'loglevel': 1, 'debugformat': False, 'host': '10.0.1.240', 'password': 'Tanium2015!', 'port': '443'}
...OUTPUT: handler string: PyTan v2.1.4 Handler for Session to 10.0.1.240:443, Authenticated: True, Platform Version: 6.5.314.4301
...CALLING: handler.ask() with args: {'qtype': u'manual', 'sensors_help': True}
...EXCEPTION: 
Sensors Help
============

Supplying sensors controls what columns will be showed when you ask a
question.

A sensor string is a human string that describes, at a minimum, a sensor.
It can also optionally define a selector for the sensor, parameters for
the sensor, a filter for the sensor, and options for the filter for the
sensor. Sensors can be provided as a string or a list of strings.

Examples for basic sensors
---------------------------------

Supplying a single sensor:

    'Computer Name'

Supplying two sensors in a list of strings:

    ['Computer Name', 'IP Route Details']

Supplying multiple sensors with selectors (name is the default
selector if none is supplied):

    [
        'Computer Name',
        'name:Computer Name',
        'id:1',
        'hash:123456789',
    ]

Sensor Parameters
-----------------

Supplying parameters to a sensor can control the arguments that are
supplied to a sensor, if that sensor takes any arguments.

Sensor parameters must be surrounded with curly braces '{}',
and must have a key and value specified that is separated by
an equals '='. Multiple parameters must be seperated by
a comma ','. The key should match up to a valid parameter key
for the sensor in question.

If a parameter is supplied and the sensor doesn't have a
corresponding key name, it will be ignored. If the sensor has
parameters and a parameter is NOT supplied then one of two
paths will be taken:

    * if the parameter does not require a default value, the
    parameter is left blank and not supplied.
    * if the parameter does require a value (pulldowns, for
    example), a default value is derived (for pulldowns,
    the first value available as a pulldown entry is used).

Examples for sensors with parameters
------------------------------------

Supplying a single sensor with a single parameter 'dirname':

    'Sensor With Params{dirname=Program Files}'

Supplying a single sensor with two parameters, 'param1' and
'param2':

    'Sensor With Params{param1=value1,param2=value2}'

Sensor Filters
--------------

Supplying a filter to a sensor controls what data will be shown in
those columns (sensors) you've provided.

Sensor filters can be supplied by adding ', that FILTER:VALUE',
where FILTER is a valid filter string, and VALUE is the string
that you want FILTER to match on.

See filter help for a list of all possible FILTER strings.

See options help for a list of options that can control how
the filter works.

Examples for sensors with filters
---------------------------------

Supplying a sensor with a filter that limits the results to only
show column data that matches the regular expression
'.*Windows.*' (Tanium does a case insensitive match by default):

    'Computer Name, that contains:Windows'

Supplying a sensor with a filter that limits the results to only
show column data that matches the regular expression
'Microsoft.*':

    'Computer Name, that starts with:Microsoft'

Supply a sensor with a filter that limits the results to only
show column data that has a version greater or equal to
'39.0.0.0'. Since this sensor uses Version as its default result
type, there is no need to change the value type using filter
options.

    'Installed Application Version' \
    '{Application Name=Google Chrome}, that =>:39.0.0.0'

Sensor Options
--------------

Supplying options to a sensor can change how the filter for
that sensor works.

Sensor options can be supplied by adding ', opt:OPTION' or
', opt:OPTION:VALUE' for those options that require values,
where OPTION is a valid option string, and VALUE is the
appropriate value required by accordant OPTION.

See options help for a list of options that can control how
the filter works.

Examples for sensors with options
---------------------------------

Supplying a sensor with an option that forces tanium to
re-fetch any cached column data that is older than 1 minute:

    'Computer Name, opt:max_data_age:60'

Supplying a sensor with filter and an option that causes
Tanium to match case for the filter value:

    'Computer Name, that contains:Windows, opt:match_case'

Supplying a sensor with a filter and an option that causes
Tanium to match all values supplied:

    'Computer Name, that contains:Windows, opt:match_all_values'

Supplying a sensor with a filter and a set of options that
causes Tanium to recognize the value type as String (which is
the default type for most sensors), re-fetch data older than
10 minutes, match any values, and match case:

    'Computer Name', that contains:Windows, ' \
    opt:value_type:string, opt:max_data_age:600, ' \
    'opt:match_any_value, opt:match_case'


'''

'''STDERR from running this:

'''
