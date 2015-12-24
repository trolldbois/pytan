#!/usr/bin/env python3 -i
"""Python shell for PyTan"""
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '4.0.0'

# BEGIN BOOTSTRAP CODE

# statically defined path
PYTAN_PATH = "~/gh/pytan"

import os
import sys
sys.dont_write_bytecode = True

# list of paths to insert at beginning of PYTHONPATH
path_adds = []

# add PYTAN_PATH to path_adds
path_adds.append(PYTAN_PATH)

# get parent_dir and add to path_adds (allows scripts that live in bin/ to work automatically)
my_filepath = os.path.abspath(sys.argv[0])
my_file = os.path.basename(my_filepath)
my_name = os.path.splitext(my_file)[0]
my_dir = os.path.dirname(my_filepath)
parent_dir = os.path.dirname(my_dir)
path_adds.append(parent_dir)

# if OS Environment "PYTAN_PATH" is set, add that to path_adds
if 'PYTAN_PATH' in os.environ:
    path_adds.append(os.environ['PYTAN_PATH'])

# expand user directories and get the absolute path of all path_adds
path_adds = [os.path.abspath(os.path.expanduser(aa)) for aa in path_adds]

# add the path_adds to beginning of PYTHONPATH
[sys.path.insert(0, aa) for aa in path_adds if aa not in sys.path]

# END BOOTSTRAP CODE

import pytan  # noqa
i = "pytan.shell.{}".format(my_name)
__import__(i)
module = eval(i)
worker = module.Worker()

if __name__ == "__main__":
    version_check = worker.version_check(__version__)
    console = worker.interactive_check()
    check = worker.check()
    setup = worker.setup()
    args = worker.parse_args()
    handler = worker.get_handler()
    result = worker.get_result()
    exec(worker.get_exec())

# from pytan.utils import taniumpy  # noqa
# from pytan.utils import constants  # noqa
# from pytan import utils  # noqa
# self = handler  # noqa


# Computer Name, that =:TPT1.pytanlab.com
spec1 = {
    'sensor': {'value': "Computer Name"},
    # 'sensor_object': {'id': 3, 'hash': "3409330187"},  # NEEDED FROM SENSOR
    'filter': {'value': "TPT1.pytanlab.com", 'operator': 'Equal', 'and_flag': 1},
    # NEEDED FROM USER
    # 'group': {'value': 492},
    # 'group_object': None,  # NEEDED FROM USER
}

# Computer Name
spec2 = {
    'sensor': {'value': "Computer Name"},
    # 'sensor_object': {'id': 3, 'hash': "3409330187"},  # NEEDED FROM SENSOR
}

# Folder Contents{folderPath=C:\\Program Files}, that =:Folder : Windows NT
spec3 = {
    'sensor': {'value': "Folder Contents"},
    # 'sensor_object': {'id': 508, 'hash': "3881863289"},  # NEEDED FROM SENSOR
    'parameters': {'folderPath': 'C:\\Program Files'},  # NEEDED FROM USER
    'filter': {'value': "Folder : Windows NT", 'operator': 'Equal', 'and_flag': 1},
    # NEEDED FROM USER
}

# Folder Contents{folderPath=C:\\Program Files}, that re:Folder : Windows NT
spec5 = {
    'sensor': {'value': "Folder Contents"},
    # 'sensor_object': {'id': 508, 'hash': "3881863289"},  # NEEDED FROM SENSOR
    'parameters': {'folderPath': 'C:\\Program Files'},  # NEEDED FROM USER
    'filter': {'value': ".*", 'operator': 'RegexMatch', 'and_flag': 0},  # NEEDED FROM USER
}

# Folder Contents{folderPath=C:\\Program Files}
spec4 = {
    'sensor': {'value': "Folder Contents"},
    # 'sensor_object': {'id': 508, 'hash': "3881863289"},  # NEEDED FROM SENSOR
    'parameters': {'folderPath': 'C:\\Program Files'},  # NEEDED FROM USER
}

# # left = [spec1, spec4]
# # right = [spec1, spec3, spec5]
# v = handler.ask_manual(left=[spec1, spec4], right=[spec1, spec3, spec5], get_results=False)
# # x = handler.get_groups({'value': 615}, limit_exact=1)

# q = v.question_object
# group = q.group
# pytan.utils.tanium_obj.recurse_group(group)
a = handler.tanium_ng.SensorList()
b = handler.tanium_ng.SensorList()
c = handler.tanium_ng.Sensor()

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

from pytan.tanium_ng import *


ri = '''<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<soap:Body xmlns:t="urn:TaniumSOAP" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<t:return><command>GetResultInfo</command>
<session>1-1175-9d1718ef29cba62801223fb1e0b891841126b8beb2a5d709cbe13dd74ca9ad86c5394e9d77a383351dfb34dbc18422214d03dc9be7dce2c6d7db2dae3a292684</session>
<ID></ID>
<IDType></IDType>
<ContextID></ContextID>
<server_version>6.5.314.4328</server_version>
<object_list><question><id>35133</id>
</question>
</object_list>

<options><suppress_object_list>1</suppress_object_list>
</options>

<ResultXML>
<![CDATA[<result_infos><now>2015/12/23 22:48:30 GMT-0000</now>
<max_available_age>0</max_available_age>
<result_info><age>0</age>
<id>35133</id>
<report_count>0</report_count>
<saved_question_id>0</saved_question_id>
<question_id>35133</question_id>
<archived_question_id>0</archived_question_id><seconds_since_issued>0</seconds_since_issued><issue_seconds>0</issue_seconds><expire_seconds>0</expire_seconds><tested>0</tested><passed>0</passed><mr_tested>0</mr_tested><mr_passed>0</mr_passed><estimated_total>3</estimated_total>
<select_count>0</select_count>
<row_count>0</row_count><error_count>0</error_count><no_results_count>0</no_results_count><row_count_machines>0</row_count_machines><row_count_flag>0</row_count_flag></result_info>
</result_infos>
]]>
</ResultXML>
<result_object></result_object>
</t:return></soap:Body>
</soap:Envelope>
'''

rd = '''<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<soap:Body xmlns:t="urn:TaniumSOAP" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<t:return><command>GetResultData</command>
<session>1-1175-9d1718ef29cba62801223fb1e0b891841126b8beb2a5d709cbe13dd74ca9ad86c5394e9d77a383351dfb34dbc18422214d03dc9be7dce2c6d7db2dae3a292684</session>
<ID></ID>
<IDType></IDType>
<ContextID></ContextID>
<server_version>6.5.314.4328</server_version>
<object_list><question><id>35133</id>
</question>
</object_list>

<options><export_flag>0</export_flag>
<suppress_object_list>1</suppress_object_list>
</options>

<ResultXML>
<![CDATA[<result_sets><now>2015/12/23 22:48:35 GMT-0000</now>
<result_set><age>0</age>
<archived_question_id>0</archived_question_id>
<saved_question_id>0</saved_question_id>
<question_id>35133</question_id>
<report_count>1</report_count>
<seconds_since_issued>0</seconds_since_issued>
<issue_seconds>0</issue_seconds>
<expire_seconds>0</expire_seconds>
<tested>3</tested>
<passed>3</passed>
<mr_tested>3</mr_tested>
<mr_passed>3</mr_passed>
<estimated_total>3</estimated_total>
<select_count>1</select_count>
<cs><c><wh>3409330187</wh><dn>Computer Name</dn><rt>1</rt></c><c><wh>0</wh><dn>Count</dn><rt>3</rt></c></cs><filtered_row_count>3</filtered_row_count><filtered_row_count_machines>3</filtered_row_count_machines><row_count>3</row_count><row_count_machines>3</row_count_machines><item_count>3</item_count><rs><r><id>2099246284</id><cid>0</cid><c><v>WIN-6U71ED4M23D</v></c><c><v>1</v></c></r><r><id>2416794350</id><cid>0</cid><c><v>auth-services.pytanlab.com</v></c><c><v>1</v></c></r><r><id>2447486854</id><cid>0</cid><c><v>TPT1.pytanlab.com</v></c><c><v>1</v></c></r></rs></result_set>
</result_sets>
]]>
</ResultXML>
<result_object></result_object>
</t:return></soap:Body>
</soap:Envelope>
'''
