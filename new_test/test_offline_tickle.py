import os
import sys

try:
    import pytan  # noqa
except Exception as e:
    print("ERROR: Unable to import pytan package, error: '{}'".format(e))
    print("Full PYTHONPATH: {}".format(', '.join(sys.path)))
    sys.exit(99)

import pytest
from pytan import text_type
from pytan import tickle
from pytan import tanium_ng
from pytan import utils

my_dir = sys.path[0]
xml_dir = os.path.join(my_dir, 'tanium_objects')

action_statuses = {
    'name': 'Action Statuses',
    'category': 'Reserved',
    'hash': 1792443391,
}

computer_name = {
    'name': 'Computer Name',
    'category': 'Reserved',
    'hash': 3409330187,
}

tanium_action_log = {
    'name': 'Tanium Action Log',
    'category': 'Tanium Diagnostics',
    'hash': 969736519,
}

operating_system_boot_directory = {
    'name': 'Operating System Boot Directory',
    'category': 'Operating System',
    'hash': 1544486184,
}

operating_system_temp_directory = {
    'name': 'Operating System Temp Directory',
    'category': 'Operating System',
    'hash': 2222730558,
}

questionlist_last_5_minutes = [
    {'name': 'Disabled Firewall Profiles'},
    {'name': 'Running Applications'},
    {'name': 'Local User Information'},
    {'name': 'Application Crashes Yesterday'},
    {'name': 'Running Applications'},
]

raw_tanium_xmls = [
    {
        'xml_file': 'Action Statuses.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
        'child_attrs': [action_statuses],
    },
    {
        'xml_file': 'Computer Name.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
        'child_attrs': [computer_name],
    },
    {
        'xml_file': 'Tanium Action Log.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
        'child_attrs': [tanium_action_log],
    },
    {
        'xml_file': 'Operating System Boot Directory and Operating System Temp Directory.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
        'child_attrs': [operating_system_boot_directory, operating_system_temp_directory],
    },
    {
        'xml_file': 'QuestionList_last_5_minutes.xml',
        'obj_type': tanium_ng.QuestionList,
        'obj_tag': 'questions',
        'child_type': tanium_ng.Question,
        'child_tag': 'question',
        'child_attrs': questionlist_last_5_minutes,
    },

]

'''
UserList with 2
ActionList with 2
'''

pytest_raw_tanium_xmls = pytest.mark.parametrize("xml_dict", raw_tanium_xmls)


@pytest_raw_tanium_xmls
def test_from_xml_raw_tanium(xml_dict):
    xml_path = os.path.join(xml_dir, 'raw_tanium_response', xml_dict['xml_file'])
    xml = utils.read_file(xml_path)
    obj = tickle.from_xml(xml)
    assert isinstance(obj, tanium_ng.BaseType)
    assert isinstance(obj, xml_dict['obj_type'])
    assert obj._SOAP_TAG == xml_dict['obj_tag']
    for idx, a in enumerate(xml_dict['child_attrs']):
        assert obj[idx]._SOAP_TAG == xml_dict['child_tag']
        assert isinstance(obj[idx], xml_dict['child_type'])
        for k, v in a.items():
            assert getattr(obj[idx], k) == v
        if getattr(obj[idx], 'parameter_definition', ''):
            assert isinstance(obj[idx].parameter_definition, text_type)
            assert isinstance(obj[idx].parameter_definition_dict, dict)
