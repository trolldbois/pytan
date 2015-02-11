
"""
Export a ResultSet from asking a question as CSV with true for header_add_type
"""
# Path to lib directory which contains pytan package
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

# setup the export_obj kwargs for later
export_kwargs = {}
export_kwargs["export_format"] = u'csv'
export_kwargs["header_add_type"] = True

# ask the question that will provide the resultset that we want to use
ask_kwargs = {
    'qtype': 'manual_human',
    'sensors': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match{dirname=Program Files,regex=.*Shared.*}',
    ],
}
response = handler.ask(**ask_kwargs)

# export the object to a string
# (we could just as easily export to a file using export_to_report_file)
export_kwargs['obj'] = response['question_results']
export_str = handler.export_obj(**export_kwargs)


print ""
print "print the export_str returned from export_obj():"
if len(out.splitlines()) > 15:
    out = out.splitlines()[0:15]
    out.append('..trimmed for brevity..')
    out = '\n'.join(out)

print out


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2015-02-11 12:16:26,062 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:31,087 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:36,112 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:41,134 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:46,162 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:51,189 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:56,214 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:17:01,240 INFO     question_progress: Results 100% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2015-02-11 12:16:05,799 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:10,824 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:15,849 INFO     question_progress: Results 50% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:20,872 INFO     question_progress: Results 50% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:25,895 INFO     question_progress: Results 100% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2015-02-11 12:15:40,504 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:15:45,534 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:15:50,556 INFO     question_progress: Results 50% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:15:55,584 INFO     question_progress: Results 50% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:00,610 INFO     question_progress: Results 50% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2015-02-11 12:16:05,637 INFO     question_progress: Results 100% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
..trimmed for brevity..

'''
