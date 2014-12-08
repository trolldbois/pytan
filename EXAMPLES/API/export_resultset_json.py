
"""
Export a ResultSet from asking a question as JSON with the default options
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
export_kwargs["export_format"] = u'json'

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
2014-12-08 16:31:37,503 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:42,529 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:47,559 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:52,587 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:57,615 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:02,640 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:07,665 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:12,693 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:17,719 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:22,747 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:27,775 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:32,805 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:37,831 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:42,858 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:47,887 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:52,922 INFO     question_progress: Results 17% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:32:57,948 INFO     question_progress: Results 50% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:33:02,976 INFO     question_progress: Results 100% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2014-12-08 16:30:56,943 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:01,971 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:07,002 INFO     question_progress: Results 33% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:12,030 INFO     question_progress: Results 67% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:17,058 INFO     question_progress: Results 83% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:22,085 INFO     question_progress: Results 83% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:27,114 INFO     question_progress: Results 83% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:32,138 INFO     question_progress: Results 83% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:31:37,164 INFO     question_progress: Results 100% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)

print the export_str returned from export_obj():
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
2014-12-08 16:30:31,572 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
2014-12-08 16:30:36,599 INFO     question_progress: Results 0% (Get Computer Name and IP Route Details and IP Address and Folder Name Search with RegEx Match[No, Program Files, No, ] from all machines)
..trimmed for brevity..

'''
