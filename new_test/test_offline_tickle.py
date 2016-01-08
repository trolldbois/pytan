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
    'id': 1,
    'name': 'Action Statuses',
    'category': 'Reserved',
    'hash': 1792443391,
}

computer_name = {
    'id': 3,
    'name': 'Computer Name',
    'category': 'Reserved',
    'hash': 3409330187,
}

tanium_action_log = {
    'id': 638,
    'name': 'Tanium Action Log',
    'category': 'Tanium Diagnostics',
    'hash': 969736519,
}

raw_tanium_xmls = [
    {
        'xml_file': 'sensors/Action Statuses.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
        'child_attrs': [action_statuses],
    },
    {
        'xml_file': 'sensors/Computer Name.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
        'child_attrs': [computer_name],
    },
    {
        'xml_file': 'sensors/Tanium Action Log.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
        'child_attrs': [tanium_action_log],
    },
]

'''
SensorList with 2
QuestionList with 1
QuestionList with 2
UserList with 1
UserList with 2
ActionList with 2
ActionList with 1
'''

pytest_raw_tanium_xmls = pytest.mark.parametrize("xml_dict", raw_tanium_xmls)


@pytest_raw_tanium_xmls
def test_from_xml_raw_tanium(xml_dict):
    xml_path = os.path.join(xml_dir, xml_dict['xml_file'])
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
        if obj[idx].parameter_definition:
            assert isinstance(obj[idx].parameter_definition, text_type)
            assert isinstance(obj[idx].parameter_definition_dict, dict)
