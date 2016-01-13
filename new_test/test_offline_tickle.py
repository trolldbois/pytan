import os
import sys
import pprint

try:
    import pytan  # noqa
except Exception as e:
    print("ERROR: Unable to import pytan package, error: '{}'".format(e))
    print("Full PYTHONPATH: {}".format(', '.join(sys.path)))
    sys.exit(99)

import pytest
from pytan import text_type, string_types
from pytan import tickle
from pytan import tanium_ng
from pytan import utils

my_dir = sys.path[0]
xml_dir = os.path.join(my_dir, 'tanium_objects')


raw_tanium_xmls = [
    {
        'xml_file': 'sensors_Action Statuses_raw.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'len': 1,
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
    },
    {
        'xml_file': 'sensors_Computer Name_raw.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'len': 1,
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
    },
    {
        'xml_file': 'sensors_Tanium Action Log_raw.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'len': 1,
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
    },
    {
        'xml_file': 'sensors_Operating System...Directory_raw.xml',
        'obj_type': tanium_ng.SensorList,
        'obj_tag': 'sensors',
        'len': 2,
        'child_type': tanium_ng.Sensor,
        'child_tag': 'sensor',
    },
    {
        'xml_file': 'questions_Last 20 minutes of questions_raw.xml',
        'obj_type': tanium_ng.QuestionList,
        'obj_tag': 'questions',
        'child_type': tanium_ng.Question,
        'child_tag': 'question',
    },
    {
        'xml_file': 'user_id 1_raw.xml',
        'obj_type': tanium_ng.User,
        'obj_tag': 'user',
    },
    {
        'xml_file': 'users_Administrator_raw.xml',
        'obj_type': tanium_ng.UserList,
        'obj_tag': 'users',
        'child_type': tanium_ng.User,
        'child_tag': 'user',
    },
    {
        'xml_file': 'actions_Last 20 minutes of actions_raw.xml',
        'obj_type': tanium_ng.ActionList,
        'obj_tag': 'actions',
        'child_type': tanium_ng.Action,
        'child_tag': 'action',
    },
]


questions = [
    'Computer Name',
    'Computer Name and IP Address',
    'Computer Name and IP Route Details',
    'Computer Name and IP Route Details and Installed Applications',
    'IP Route Details and Installed Applications',
]

raw_resultset_xmls = []
for q in questions:
    raw_resultset_xmls.append({
        'xml_file': 'resultdata_{}_raw.xml'.format(q),
        'obj_type': tanium_ng.ResultSetList,
        'obj_tag': 'result_sets',
        'complex_type': tanium_ng.ResultSet,
        'complex_tag': 'result_set',
        'complex_attr': 'result_set',
        'len': 2,
    })
    raw_resultset_xmls.append({
        'xml_file': 'resultdata_sse_{}_raw.xml'.format(q),
        'obj_type': tanium_ng.ResultSetList,
        'obj_tag': 'result_sets',
        'complex_type': tanium_ng.ResultSet,
        'complex_tag': 'result_set',
        'complex_attr': 'result_set',
        'len': 1,
    })
    raw_tanium_xmls.append({
        'xml_file': 'resultinfo_{}_raw.xml'.format(q),
        'obj_type': tanium_ng.ResultInfoList,
        'obj_tag': 'result_infos',
        'complex_type': tanium_ng.ResultInfo,
        'complex_tag': 'result_info',
        'complex_attr': 'result_info',
        'len': 2,
    })

raw_tanium_xmls += raw_resultset_xmls


@pytest.fixture(params=raw_tanium_xmls)
def xml_info(request):
    d = request.param
    d['xml_path'] = os.path.join(xml_dir, d['xml_file'])
    d['xml'] = utils.read_file(d['xml_path'])
    return d


@pytest.fixture(params=raw_resultset_xmls)
def resultxml_info(request):
    d = request.param
    d['xml_path'] = os.path.join(xml_dir, d['xml_file'])
    d['xml'] = utils.read_file(d['xml_path'])
    return d


def test_from_xml(xml_info):
    if '_sse_' in xml_info['xml_file']:
        obj = tickle.from_sse_xml(xml_info['xml'])
    else:
        obj = tickle.from_xml(xml_info['xml'])

    assert isinstance(obj, tanium_ng.BaseType)
    assert isinstance(obj, xml_info['obj_type'])
    assert obj._SOAP_TAG == xml_info['obj_tag']
    if xml_info.get('len'):
        assert len(obj) == xml_info['len']
    if xml_info.get('child_type'):
        for child_obj in obj:
            assert child_obj._SOAP_TAG == xml_info['child_tag']
            assert isinstance(child_obj, xml_info['child_type'])
            if getattr(child_obj, 'parameter_definition', ''):
                assert isinstance(child_obj.parameter_definition, text_type)
                assert isinstance(child_obj.parameter_definition_dict, dict)
    if xml_info.get('complex_type'):
        complex_attr = getattr(obj, xml_info.get('complex_attr'))
        assert complex_attr._SOAP_TAG == xml_info['complex_tag']
        assert isinstance(complex_attr, xml_info['complex_type'])
    return obj


def test_to_from_xml(xml_info, report_tmpdir):
    obj1 = test_from_xml(xml_info)
    obj1_xml = tickle.to_xml(obj1)
    assert obj1_xml
    assert isinstance(obj1_xml, string_types)

    fn = 'test_to_from_xml_{}.xml'.format(xml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(obj1_xml)

    xml_info['xml'] = obj1_xml
    obj2 = test_from_xml(xml_info)
    assert len(obj1) == len(obj2)
    assert obj1._SOAP_TAG == obj2._SOAP_TAG
    for k, v in obj1._SIMPLE_PROPS.items():
        assert getattr(obj1, k) == getattr(obj2, k)
    for k, v in obj1._LIST_PROPS.items():
        assert len(getattr(obj1, k)) == len(getattr(obj2, k))


def test_to_from_tree(xml_info):
    obj1 = test_from_xml(xml_info)
    obj1_tree = tickle.to_tree(obj1)
    assert obj1_tree is not None
    assert isinstance(obj1_tree, pytan.tickle.ElementType)
    obj2 = tickle.from_tree(obj1_tree)
    assert len(obj1) == len(obj2)
    assert obj1._SOAP_TAG == obj2._SOAP_TAG
    for k, v in obj1._SIMPLE_PROPS.items():
        assert getattr(obj1, k) == getattr(obj2, k)
    for k, v in obj1._LIST_PROPS.items():
        assert len(getattr(obj1, k)) == len(getattr(obj2, k))


def test_to_from_dict(xml_info, report_tmpdir):
    obj1 = test_from_xml(xml_info)
    obj1_dict = tickle.to_dict(obj1)
    assert obj1_dict
    assert isinstance(obj1_dict, dict)

    fn = 'test_to_from_dict_{}.txt'.format(xml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(pprint.pformat(obj1_dict))

    obj2 = tickle.from_dict(obj1_dict)
    assert len(obj1) == len(obj2)
    assert obj1._SOAP_TAG == obj2._SOAP_TAG
    for k, v in obj1._SIMPLE_PROPS.items():
        assert getattr(obj1, k) == getattr(obj2, k)
    for k, v in obj1._LIST_PROPS.items():
        assert len(getattr(obj1, k)) == len(getattr(obj2, k))


def test_to_from_json(xml_info, report_tmpdir):
    obj1 = test_from_xml(xml_info)
    obj1_json = tickle.to_json(obj1)
    assert obj1_json
    assert isinstance(obj1_json, string_types)

    fn = 'test_to_from_json_{}.json'.format(xml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(obj1_json)

    obj2 = tickle.from_json(obj1_json)
    assert len(obj1) == len(obj2)
    assert obj1._SOAP_TAG == obj2._SOAP_TAG
    for k, v in obj1._SIMPLE_PROPS.items():
        assert getattr(obj1, k) == getattr(obj2, k)
    for k, v in obj1._LIST_PROPS.items():
        assert len(getattr(obj1, k)) == len(getattr(obj2, k))


def test_to_csv(xml_info, report_tmpdir):
    obj1 = test_from_xml(xml_info)
    obj1_csv = tickle.to_csv(obj1)
    assert obj1_csv
    assert isinstance(obj1_csv, string_types)
    fn = 'test_to_csv_{}.csv'.format(xml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(obj1_csv)


def test_to_json_resultset(resultxml_info, report_tmpdir):
    obj1 = test_from_xml(resultxml_info)
    obj1_json = tickle.to_json_resultset(obj1)
    assert obj1_json
    assert isinstance(obj1_json, string_types)
    fn = 'RESULTSET_test_to_json_{}.json'.format(resultxml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(obj1_json)


def test_to_dict_resultset(resultxml_info, report_tmpdir):
    obj1 = test_from_xml(resultxml_info)
    obj1_dict = tickle.to_dict_resultset(obj1)
    assert obj1_dict
    assert isinstance(obj1_dict, list)
    fn = 'RESULTSET_test_to_dict_{}.txt'.format(resultxml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(pprint.pformat(obj1_dict))


def test_to_csv_resultset_xaxis_normal(resultxml_info, report_tmpdir):
    obj1 = test_from_xml(resultxml_info)
    obj1_csv = tickle.to_csv_resultset(obj1)
    assert obj1_csv
    assert isinstance(obj1_csv, string_types)
    fn = 'RESULTSET_test_to_csv_xaxis_normal_{}.csv'.format(resultxml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(obj1_csv)


def test_to_csv_resultset_xaxis_flatten(resultxml_info, report_tmpdir):
    obj1 = test_from_xml(resultxml_info)
    obj1_csv = tickle.to_csv_resultset(obj1, flatten=True)
    assert obj1_csv
    assert isinstance(obj1_csv, string_types)
    fn = 'RESULTSET_test_to_csv_xaxis_flatten_{}.csv'.format(resultxml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(obj1_csv)


def test_to_csv_resultset_yaxis_normal(resultxml_info, report_tmpdir):
    obj1 = test_from_xml(resultxml_info)
    obj1_csv = tickle.to_csv_resultset(obj1, yaxis=True)
    assert obj1_csv
    assert isinstance(obj1_csv, string_types)
    fn = 'RESULTSET_test_to_csv_yaxis_normal_{}.csv'.format(resultxml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(obj1_csv)


def test_to_csv_resultset_yaxis_flatten(resultxml_info, report_tmpdir):
    obj1 = test_from_xml(resultxml_info)
    obj1_csv = tickle.to_csv_resultset(obj1, yaxis=True, flatten=True)
    assert obj1_csv
    assert isinstance(obj1_csv, string_types)
    fn = 'RESULTSET_test_to_csv_yaxis_flatten_{}.csv'.format(resultxml_info['xml_file'])
    p = report_tmpdir.join(fn)
    p.write(obj1_csv)
