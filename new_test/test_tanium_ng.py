#!/usr/bin/env python3

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
path_adds.append(my_dir)
path_adds.append(parent_dir)

# if OS Environment "PYTAN_PATH" is set, add that to path_adds
if 'PYTAN_PATH' in os.environ:
    path_adds.append(os.environ['PYTAN_PATH'])

# expand user directories and get the absolute path of all path_adds
path_adds = [os.path.abspath(os.path.expanduser(aa)) for aa in path_adds]

# add the path_adds to beginning of PYTHONPATH
[sys.path.insert(0, aa) for aa in path_adds if aa not in sys.path]

try:
    import pytan  # noqa
except:
    err = "Unable to import pytan package, looked in paths: '{}', full PYTHONPATH: {}"
    err = err.format(', '.join(path_adds), sys.path)
    raise Exception(err)

# END BOOTSTRAP CODE

import pytest
from pytan import tanium_ng

BASE_TYPES = list(tanium_ng.BASE_TYPES.items())
LIST_TYPES = [x for x in BASE_TYPES if x[1]()._IS_LIST]
HAS_COMPLEX = [x for x in BASE_TYPES if x[1]()._COMPLEX_PROPS]
HAS_SIMPLE = [x for x in BASE_TYPES if x[1]()._SIMPLE_PROPS]
HAS_COMPLEX_NO_LIST = [x for x in HAS_COMPLEX if not x[1]()._IS_LIST]
HAS_SIMPLE_NO_LIST = [x for x in HAS_SIMPLE if not x[1]()._IS_LIST]

base_types = pytest.mark.parametrize("soap_tag,ng_class", BASE_TYPES)
list_types = pytest.mark.parametrize("soap_tag,ng_class", LIST_TYPES)
has_complex = pytest.mark.parametrize("soap_tag,ng_class", HAS_COMPLEX)
has_simple = pytest.mark.parametrize("soap_tag,ng_class", HAS_SIMPLE)
has_complex_no_list = pytest.mark.parametrize("soap_tag,ng_class", HAS_COMPLEX_NO_LIST)
has_simple_no_list = pytest.mark.parametrize("soap_tag,ng_class", HAS_SIMPLE_NO_LIST)


@base_types
def test_instantiate(soap_tag, ng_class):
    '''Test that all Tanium NG objects can be instantiated.'''
    obj = ng_class()
    assert isinstance(obj, tanium_ng.BaseType)
    assert obj._SOAP_TAG


@base_types
def test_empty(soap_tag, ng_class):
    '''Test that a newly created Tanium NG type is empty.'''
    obj = ng_class()
    assert not obj


@list_types
def test_list_attrs(soap_tag, ng_class):
    '''Test that a newly created Tanium NG list type has the list attrs'''
    obj = ng_class()
    assert obj._LIST_ATTR
    assert obj._LIST_TYPE


@list_types
def test_list_one_item(soap_tag, ng_class):
    '''Test that a Tanium NG list type with one item has a length of 1'''
    obj = ng_class()
    item1 = obj._LIST_TYPE()
    obj.append(item1)
    assert len(obj) == 1


@list_types
def test_list_three_items(soap_tag, ng_class):
    '''Test that a Tanium NG list type with 3 items has a length of 3'''
    obj = ng_class()
    assert len(obj) == 0

    items = [obj._LIST_TYPE(), obj._LIST_TYPE(), obj._LIST_TYPE()]
    setattr(obj, obj._LIST_ATTR, items)
    assert len(obj) == 3

    last_item = obj[-1]
    assert isinstance(last_item, obj._LIST_TYPE)


@list_types
def test_list_add(soap_tag, ng_class):
    '''Test that two Tanium NG list type with one item each can be added'''
    obj1 = ng_class()
    item1 = obj1._LIST_TYPE()
    obj1.append(item1)

    obj2 = ng_class()
    item2 = obj2._LIST_TYPE()
    obj2.append(item2)

    obj3 = obj1 + obj2
    assert len(obj3) == 2
    assert isinstance(obj3, ng_class)


@list_types
def test_list_iadd(soap_tag, ng_class):
    '''Test that two Tanium NG list type with one item each can be appended'''
    obj1 = ng_class()
    item1 = obj1._LIST_TYPE()
    obj1.append(item1)

    obj2 = ng_class()
    item2 = obj2._LIST_TYPE()
    obj2.append(item2)

    obj1 += obj2
    assert len(obj1) == 2
    assert isinstance(obj1, ng_class)


@has_complex
def test_complex_assign(soap_tag, ng_class):
    '''Test that all Tanium NG objects with complex attrs can be assigned their complex obj'''
    obj = ng_class()
    for k, v in obj._COMPLEX_PROPS.items():
        complex_item = v()
        setattr(obj, k, complex_item)


@has_simple
def test_simple_assign(soap_tag, ng_class):
    '''Test that all Tanium NG objects with simple attrs can be assigned their simple val'''
    obj = ng_class()
    for k, v in obj._SIMPLE_PROPS.items():
        setattr(obj, k, v('12345'))


@has_complex_no_list
def test_complex_length1(soap_tag, ng_class):
    '''
    Test that all non list Tanium NG objects with complex attrs have a length of one when one
    attribute is set
    '''
    obj = ng_class()
    assert len(obj) == 0

    for k, v in obj._COMPLEX_PROPS.items():
        complex_item = v()
        setattr(obj, k, complex_item)
        break

    assert len(obj) == 1


@has_simple_no_list
def test_simple_length1(soap_tag, ng_class):
    '''
    Test that all non list Tanium NG objects with simple attrs have a length of one when one
    attribute is set
    '''
    obj = ng_class()
    assert len(obj) == 0

    for k, v in obj._SIMPLE_PROPS.items():
        simple_item = v('123456')
        setattr(obj, k, simple_item)
        break

    assert len(obj) == 1


@base_types
def test_invalid_type(soap_tag, ng_class):
    obj = ng_class()
    for k, v in obj._ALL_PROPS.items():
        with pytest.raises(tanium_ng.BadTypeError):
            setattr(obj, k, {})
    assert len(obj) == 0


def test_sensor_init_values():
    obj = tanium_ng.Sensor(values={'id': 1, 'name': 'test123'})
    assert len(obj) == 2
    assert obj.id == 1
    assert obj.name == 'test123'


if __name__ == '__main__':
    pytest.main()
