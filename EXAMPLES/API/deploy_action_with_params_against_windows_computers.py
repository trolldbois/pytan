
"""
Deploy an action with parameters against only windows computers using human strings.

This will use the Package 'Custom Tagging - Add Tags' and supply two parameters. The second parameter will be ignored because the package in question only requires one parameter.
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
kwargs["run"] = True
kwargs["action_filters"] = u'Operating System, that contains:Windows'
kwargs["package"] = u'Custom Tagging - Add Tags{$1=tag_should_be_added,$2=tag_should_be_ignore}'

# call the handler with the deploy_action method, passing in kwargs for arguments
response = handler.deploy_action(**kwargs)
import pprint, io

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



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: Not yet determined!
2015-08-06 14:52:41,683 DEBUG    pytan.handler.ActionPoller: ID 36370: id resolved to 36370
2015-08-06 14:52:41,683 DEBUG    pytan.handler.ActionPoller: ID 36370: package_spec resolved to PackageSpec, name: 'Custom Tagging - Add Tags', id: 9342
2015-08-06 14:52:41,688 DEBUG    pytan.handler.ActionPoller: ID 36370: target_group resolved to Group, name: 'Default', id: 27376
2015-08-06 14:52:41,705 DEBUG    pytan.handler.ActionPoller: ID 36370: Result Map resolved to {'failed': {'36370:Expired.': [], 'total': 0, '36370:NotSucceeded.': [], '36370:Stopped.': [], '36370:Failed.': []}, 'finished': {'36370:NotSucceeded.': [], '36370:Completed.': [], '36370:Verified.': [], '36370:Stopped.': [], '36370:Succeeded.': [], '36370:Expired.': [], 'total': 0, '36370:Failed.': []}, 'running': {'36370:Downloading.': [], '36370:Running.': [], '36370:PendingVerification.': [], '36370:Waiting.': [], 'total': 0, '36370:Copying.': []}, 'success': {'36370:Completed.': [], 'total': 0, '36370:Verified.': []}, 'unknown': {'total': 0}}
2015-08-06 14:52:41,705 DEBUG    pytan.handler.ActionPoller: ID 36370: expiration_time resolved to 2015-08-06T15:04:42
2015-08-06 14:52:41,705 DEBUG    pytan.handler.ActionPoller: ID 36370: status resolved to Active
2015-08-06 14:52:41,705 DEBUG    pytan.handler.ActionPoller: ID 36370: stopped_flag resolved to 0
2015-08-06 14:52:41,705 DEBUG    pytan.handler.ActionPoller: ID 36370: Object Info resolved to ID 36370: Package: 'Custom Tagging - Add Tags', Target: ' Operating System contains "Windows"', Verify: False, Stopped: False, Status: Active
2015-08-06 14:52:41,705 DEBUG    pytan.handler.ActionPoller: ID 36370: Adding Question to derive passed count
2015-08-06 14:52:41,853 DEBUG    pytan.handler.QuestionPoller: ID 86269: id resolved to 86269
2015-08-06 14:52:41,853 DEBUG    pytan.handler.QuestionPoller: ID 86269: expiration resolved to 2015-08-06T15:02:42
2015-08-06 14:52:41,853 DEBUG    pytan.handler.QuestionPoller: ID 86269: query_text resolved to Get number of machines where Operating System contains "Windows"
2015-08-06 14:52:41,853 DEBUG    pytan.handler.QuestionPoller: ID 86269: id resolved to 86269
2015-08-06 14:52:41,853 DEBUG    pytan.handler.QuestionPoller: ID 86269: Object Info resolved to Question ID: 86269, Query: Get number of machines where Operating System contains "Windows"
2015-08-06 14:52:41,859 DEBUG    pytan.handler.QuestionPoller: ID 86269: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:52:41,860 DEBUG    pytan.handler.QuestionPoller: ID 86269: Timing: Started: 2015-08-06 14:52:41.853478, Expiration: 2015-08-06 15:02:42, Override Timeout: None, Elapsed Time: 0:00:00.006548, Left till expiry: 0:10:00.139976, Loop Count: 1
2015-08-06 14:52:41,860 INFO     pytan.handler.QuestionPoller: ID 86269: Progress Changed 0% (0 of 2)
2015-08-06 14:52:46,867 DEBUG    pytan.handler.QuestionPoller: ID 86269: Progress: Tested: 0, Passed: 0, MR Tested: 0, MR Passed: 0, Est Total: 2, Row Count: 0
2015-08-06 14:52:46,867 DEBUG    pytan.handler.QuestionPoller: ID 86269: Timing: Started: 2015-08-06 14:52:41.853478, Expiration: 2015-08-06 15:02:42, Override Timeout: None, Elapsed Time: 0:00:05.013759, Left till expiry: 0:09:55.132766, Loop Count: 2
2015-08-06 14:52:51,877 DEBUG    pytan.handler.QuestionPoller: ID 86269: Progress: Tested: 2, Passed: 1, MR Tested: 2, MR Passed: 2, Est Total: 2, Row Count: 0
2015-08-06 14:52:51,877 DEBUG    pytan.handler.QuestionPoller: ID 86269: Timing: Started: 2015-08-06 14:52:41.853478, Expiration: 2015-08-06 15:02:42, Override Timeout: None, Elapsed Time: 0:00:10.023802, Left till expiry: 0:09:50.122722, Loop Count: 3
2015-08-06 14:52:51,877 INFO     pytan.handler.QuestionPoller: ID 86269: Progress Changed 100% (2 of 2)
2015-08-06 14:52:51,877 INFO     pytan.handler.QuestionPoller: ID 86269: Reached Threshold of 99% (2 of 2)
2015-08-06 14:52:51,877 DEBUG    pytan.handler.ActionPoller: ID 36370: Passed Count resolved to 1
2015-08-06 14:52:51,950 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:52:51,951 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:10.245228, Left till expiry: 0:11:50.049011, Loop Count: 1
2015-08-06 14:52:51,951 INFO     pytan.handler.ActionPoller: ID 36370: Progress Changed for Seen Count 0% (0 of 1)
2015-08-06 14:52:57,174 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:52:57,174 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:15.468750, Left till expiry: 0:11:44.825489, Loop Count: 2
2015-08-06 14:53:02,344 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:02,345 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:20.639259, Left till expiry: 0:11:39.654981, Loop Count: 3
2015-08-06 14:53:07,939 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:07,939 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:26.234047, Left till expiry: 0:11:34.060192, Loop Count: 4
2015-08-06 14:53:13,140 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:13,140 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:31.435135, Left till expiry: 0:11:28.859104, Loop Count: 5
2015-08-06 14:53:18,318 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:18,319 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:36.613304, Left till expiry: 0:11:23.680935, Loop Count: 6
2015-08-06 14:53:23,333 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:23,333 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:41.627753, Left till expiry: 0:11:18.666486, Loop Count: 7
2015-08-06 14:53:28,498 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:28,498 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:46.793044, Left till expiry: 0:11:13.501195, Loop Count: 8
2015-08-06 14:53:33,766 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:33,766 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:52.061176, Left till expiry: 0:11:08.233063, Loop Count: 9
2015-08-06 14:53:39,070 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:39,070 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:00:57.364464, Left till expiry: 0:11:02.929776, Loop Count: 10
2015-08-06 14:53:44,086 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:44,086 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:02.380713, Left till expiry: 0:10:57.913527, Loop Count: 11
2015-08-06 14:53:49,150 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:49,150 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:07.445167, Left till expiry: 0:10:52.849072, Loop Count: 12
2015-08-06 14:53:54,334 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:54,334 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:12.628763, Left till expiry: 0:10:47.665476, Loop Count: 13
2015-08-06 14:53:59,432 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:53:59,432 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:17.726705, Left till expiry: 0:10:42.567534, Loop Count: 14
2015-08-06 14:54:04,756 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:04,756 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:23.051122, Left till expiry: 0:10:37.243117, Loop Count: 15
2015-08-06 14:54:09,863 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:09,863 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:28.157595, Left till expiry: 0:10:32.136645, Loop Count: 16
2015-08-06 14:54:15,131 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:15,132 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:33.426231, Left till expiry: 0:10:26.868008, Loop Count: 17
2015-08-06 14:54:20,148 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:20,148 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:38.442357, Left till expiry: 0:10:21.851882, Loop Count: 18
2015-08-06 14:54:25,165 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:25,165 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:43.460210, Left till expiry: 0:10:16.834029, Loop Count: 19
2015-08-06 14:54:30,181 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:30,181 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:48.475814, Left till expiry: 0:10:11.818426, Loop Count: 20
2015-08-06 14:54:35,199 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:35,199 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:53.493881, Left till expiry: 0:10:06.800359, Loop Count: 21
2015-08-06 14:54:40,213 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:40,213 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:01:58.508115, Left till expiry: 0:10:01.786124, Loop Count: 22
2015-08-06 14:54:45,806 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:45,806 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:04.100524, Left till expiry: 0:09:56.193715, Loop Count: 23
2015-08-06 14:54:51,010 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:51,010 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:09.305214, Left till expiry: 0:09:50.989026, Loop Count: 24
2015-08-06 14:54:56,024 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:54:56,024 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:14.318896, Left till expiry: 0:09:45.975343, Loop Count: 25
2015-08-06 14:55:01,072 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:01,072 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:19.366844, Left till expiry: 0:09:40.927395, Loop Count: 26
2015-08-06 14:55:06,372 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:06,372 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:24.666628, Left till expiry: 0:09:35.627611, Loop Count: 27
2015-08-06 14:55:12,607 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:12,607 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:30.901715, Left till expiry: 0:09:29.392525, Loop Count: 28
2015-08-06 14:55:17,649 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:17,649 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:35.943412, Left till expiry: 0:09:24.350827, Loop Count: 29
2015-08-06 14:55:22,662 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:22,662 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:40.956995, Left till expiry: 0:09:19.337245, Loop Count: 30
2015-08-06 14:55:27,780 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:27,780 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:46.075194, Left till expiry: 0:09:14.219047, Loop Count: 31
2015-08-06 14:55:32,797 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:32,797 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:51.091632, Left till expiry: 0:09:09.202607, Loop Count: 32
2015-08-06 14:55:38,078 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:38,078 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:02:56.372384, Left till expiry: 0:09:03.921857, Loop Count: 33
2015-08-06 14:55:43,164 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:43,164 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:03:01.458491, Left till expiry: 0:08:58.835748, Loop Count: 34
2015-08-06 14:55:48,181 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:48,181 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:03:06.475858, Left till expiry: 0:08:53.818381, Loop Count: 35
2015-08-06 14:55:53,340 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 0, Expected Seen: 1, Percent: 0%
2015-08-06 14:55:53,340 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:03:11.635073, Left till expiry: 0:08:48.659166, Loop Count: 36
2015-08-06 14:55:59,240 DEBUG    pytan.handler.ActionPoller: ID 36370: Progress: Seen Action: 1, Expected Seen: 1, Percent: 100%
2015-08-06 14:55:59,240 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:03:17.534463, Left till expiry: 0:08:42.759776, Loop Count: 37
2015-08-06 14:55:59,240 INFO     pytan.handler.ActionPoller: ID 36370: Progress Changed for Seen Count 100% (1 of 1)
2015-08-06 14:55:59,240 INFO     pytan.handler.ActionPoller: ID 36370: Reached Threshold for Seen Count of 100% (1 of 1)
2015-08-06 14:55:59,253 DEBUG    pytan.handler.ActionPoller: ID 36370: failed: 0, finished: 1, running: 0, success: 1, unknown: 0, Done Key: success, Passed Count: 1
2015-08-06 14:55:59,253 DEBUG    pytan.handler.ActionPoller: ID 36370: Timing: Started: 2015-08-06 14:52:41.705763, Expiration: 2015-08-06 15:04:42, Override Timeout: None, Elapsed Time: 0:03:17.547920, Left till expiry: 0:08:42.746319, Loop Count: 1
2015-08-06 14:55:59,253 INFO     pytan.handler.ActionPoller: ID 36370: Progress Changed for Finished Count 100% (1 of 1)
2015-08-06 14:55:59,253 INFO     pytan.handler.ActionPoller: ID 36370: Reached Threshold for Finished Count of 100% (1 of 1)

Type of response:  <type 'dict'>

Pretty print of response:
{'action_info': <taniumpy.object_types.result_info.ResultInfo object at 0x122cdda50>,
 'action_object': <taniumpy.object_types.action.Action object at 0x122cdd8d0>,
 'action_result_map': {'failed': {'36370:Expired.': [],
                                  '36370:Failed.': [],
                                  '36370:NotSucceeded.': [],
                                  '36370:Stopped.': [],
                                  'total': 0},
                       'finished': {'36370:Completed.': ['jtanium1.localdomain'],
                                    '36370:Expired.': [],
                                    '36370:Failed.': [],
                                    '36370:NotSucceeded.': [],
                                    '36370:Stopped.': [],
                                    '36370:Succeeded.': [],
                                    '36370:Verified.': [],
                                    'total': 1},
                       'running': {'36370:Copying.': [],
                                   '36370:Downloading.': [],
                                   '36370:PendingVerification.': [],
                                   '36370:Running.': [],
                                   '36370:Waiting.': [],
                                   'total': 0},
                       'success': {'36370:Completed.': ['jtanium1.localdomain'],
                                   '36370:Verified.': [],
                                   'total': 1},
                       'unknown': {'total': 0}},
 'action_results': <taniumpy.object_types.result_set.ResultSet object at 0x11d003210>,
 'group_object': <taniumpy.object_types.group.Group object at 0x122cdd210>,
 'package_object': <taniumpy.object_types.package_spec.PackageSpec object at 0x122cddd90>,
 'poller_object': <pytan.pollers.ActionPoller object at 0x111540610>,
 'poller_success': True,
 'saved_action_object': None}

Print of action object: 
Action, name: 'API Deploy Custom Tagging - Add Tags', id: 36370

CSV Results of response: 
Action Statuses,Computer Name
36370:Completed.,jtanium1.localdomain


'''
