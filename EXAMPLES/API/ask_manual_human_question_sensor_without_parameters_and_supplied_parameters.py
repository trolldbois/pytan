
"""
Ask a manual question using human strings by referencing the name of a single sensor that does NOT take parameters, but supplying parameters anyways (which will be ignored since the sensor does not take parameters).

No sensor filters, sensor filter options, question filters, or question options supplied.
"""

import os
import sys
sys.dont_write_bytecode = True

# Determine our script name, script dir
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)

# determine the pytan lib dir and add it to the path
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)


# connection info for Tanium Server
USERNAME = "Tanium User"
PASSWORD = "T@n!um"
HOST = "172.16.31.128"
PORT = "444"

# Logging conrols
LOGLEVEL = 2
DEBUGFORMAT = False

import tempfile

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

# setup the arguments for the handler method
kwargs = {}
kwargs["sensors"] = u'Computer Name{fake=Dweedle}'
kwargs["qtype"] = u'manual_human'

# call the handler with the ask method, passing in kwargs for arguments
response = handler.ask(**kwargs)
import pprint, io

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
    out = '\n'.join(out)
print out


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
2015-03-26 11:39:40,593 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:39:45,610 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:39:50,628 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:39:55,642 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:00,657 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:05,675 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:10,689 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:15,705 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:20,718 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:25,732 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:30,747 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:35,763 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:40,778 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:45,791 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:50,806 INFO     question_progress: Results 0% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:40:55,823 INFO     question_progress: Results 50% (Get Computer Name[Dweedle] from all machines)
2015-03-26 11:41:00,839 INFO     question_progress: Results 100% (Get Computer Name[Dweedle] from all machines)

Type of response:  <type 'dict'>

Pretty print of response:
{'question_object': <taniumpy.object_types.question.Question object at 0x10762aa10>,
 'question_results': <taniumpy.object_types.result_set.ResultSet object at 0x10760f290>}

Equivalent Question if it were to be asked in the Tanium Console: 
Get Computer Name[Dweedle] from all machines

CSV Results of response: 
Computer Name[Dweedle]
[no results]
JTANIUM1


'''
