#!/usr/bin/env python

import argparse
import datetime
import errno
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET


EXCLUDE_TYPE_LIST = ['auth', 'TaniumSOAPRequest', 'TaniumSOAPResult']

XSD_TO_PYTHON_TYPES = {
    'xsd:int': 'int',
    'xsd:string': 'str',
    'xsd:long': 'int'
}

FILE_HEADER_TEMPLATE = """

# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version {0:<10}
#
#
"""

wsdl_version = None

def get_file_header():
    if not wsdl_version:
        raise Exception('wsdl_version not set')
    return FILE_HEADER_TEMPLATE.format(wsdl_version, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def dashcase(val):
    """convert a string to - separated, idempotent"""
    return '-'.join(re.split('[-_]', val))

def capcase(val):
    """convert some_string or some-string to SomeString"""
    return ''.join([a[0].upper() + (a[1:] if len(a) > 0 else '') for a in re.split('[-_]', val)])

class Type(object):

    # Template for simple type.
    # Expanded with {0} = type name, {1} = properties
    SIMPLE_PROPERTY_TEMPLATE     = "                    this.{0: <30}     = {1}"
    COMPLEX_PROPERTY_TEMPLATE    = "                    this.{0: <30}     = None"

    TYPE_TEMPLATE = """

from .base import BaseType

class {0}(BaseType):

    OBJECT_LIST_TAG = {1}

    def __init__(self):
        BaseType.__init__(self,
            soap_tag='{2}',
            simple_properties={{ {3} }},
            complex_properties={{ {4} }},
            list_properties={{ {5} }},
        )
        {6}
        {7}
        {8}

{9}

"""

    def __init__(self, wsdl_dom, namespaces, wsdl_type, simple_properties, complex_properties, list_properties, property_values, depends_list, soap_tag, force, preview, verbose):
        self.wsdl_dom = wsdl_dom
        self.namespaces = namespaces
        self.wsdl_type = wsdl_type
        self.pytype = capcase(wsdl_type)
        self.simple_properties = simple_properties
        self.complex_properties = complex_properties
        self.list_properties = list_properties
        self.property_values = property_values
        self.depends_list = depends_list
        self.soap_tag = soap_tag
        self.force = force
        self.preview = preview
        self.verbose = verbose

    @property
    def is_list(self):
        return self.wsdl_type.endswith('_list') or self.wsdl_type == 'user_permissions'

    @property
    def list_type(self):
        if not self.is_list:
            raise Exception('{} is not a list type'.format(self.wsdl_type))
        if self.wsdl_type == 'user_permissions':
            return 'permission'
        elif self.is_list_of_value:
            return self.wsdl_type[:-5] 
        else:
            el = self.wsdl_dom.find(".//xsd:complexType[@name='{}']/xsd:sequence/xsd:element[@type]".format(self.wsdl_type), self.namespaces)
            if el is None:
                raise Exception('Could not find {} list type in wsdl'.format(self.wsdl_type))
            return el.attrib['type']
            
    @property
    def is_list_of_value(self):
        return self.wsdl_dom.find(".//xsd:complexType[@name='{}']/xsd:sequence/xsd:element[@type]".format(self.wsdl_type), self.namespaces).attrib['type'].startswith('xsd:')

    @property
    def type_dependencies(self):
        return [d for d in self.depends_list if d not in EXCLUDE_TYPE_LIST]

    @staticmethod
    def load(wsdl_dom, namespaces, type_name, force, preview, verbose):
        """Use the WSDL to lookup the definition and usage of type_name."""
        type_element = wsdl_dom.find(".//xsd:complexType[@name='{}']".format(type_name), namespaces)
        usage_elements = wsdl_dom.findall(".//xsd:element[@type='{}']/../..[@name]".format(type_name), namespaces)
        # built-in property types
        simple_properties = [(el.attrib['name'], XSD_TO_PYTHON_TYPES[el.attrib['type']]) for el in wsdl_dom.findall(".//xsd:complexType[@name='{}']/*/xsd:element[@type]".format(type_name),
            namespaces) if el.attrib['type'].startswith('xsd:')]
        # complex property types
        complex_properties = [(el.attrib['name'], el.attrib['type']) for el in wsdl_dom.findall(".//xsd:complexType[@name='{}']/*/xsd:element[@type]".format(type_name),
            namespaces) if not el.attrib['type'].startswith('xsd:') and not el.attrib.get('maxOccurs') == 'unbounded']
        list_properties = [(el.attrib['name'], capcase(el.attrib['type'])) for el in wsdl_dom.findall(".//xsd:complexType[@name='{}']/*/xsd:element[@type]".format(type_name),
            namespaces) if not el.attrib['type'].startswith('xsd:') and el.attrib.get('maxOccurs') == 'unbounded']


        property_values = {}
        for el in wsdl_dom.findall(".//xsd:complexType[@name='{}']/*/xsd:element[@type]".format(type_name), namespaces):
            if not el.attrib['type'].startswith('xsd:'):
                continue
            if 'default' in el.attrib:
                property_values[el.attrib['name']] = '"{}"'.format(el.attrib['default']) if el.attrib['type'] == 'xsd:string' else '{}'.format(el.attrib['default'])
            else:
                property_values[el.attrib['name']] = 'null' if el.attrib['type'] != 'xsd:int' else 'Number.NaN'
        property_values.update({el.attrib['name']: '[]' for el in wsdl_dom.findall(".//xsd:complexType[@name='{}']/*/xsd:element[@type]".format(type_name),
            namespaces) if not el.attrib['type'].startswith('xsd:')})
        # determine dependencies
        depends_list = [el.attrib['type'] for el in wsdl_dom.findall(".//xsd:complexType[@name='{}']/*/xsd:element[@type]".format(type_name),
            namespaces) if not el.attrib['type'].startswith('xsd:')]
        # generate the soap tag. If this is a type used in a list, use what 
        # the list attribute name is. If not, use the type name.
        usage = wsdl_dom.find(".//xsd:complexType/xsd:sequence/xsd:element[@type='{0}']".format(type_name), namespaces)
        soap_tag = usage.attrib['name'] if usage is not None else type_name
        return Type(
            wsdl_dom=wsdl_dom,
            namespaces=namespaces,
            wsdl_type=type_name,
            simple_properties=simple_properties,
            complex_properties=complex_properties,
            list_properties=list_properties,
            property_values=property_values,
            depends_list=depends_list,
            soap_tag=soap_tag,
            force=force,
            preview=preview,
            verbose=verbose)

    def __str__(self):
        return """WSDL type: {0}
Simple Properties: {1}
Complex Properties: {2}
Dependencies: {3}
""".format(self.wsdl_type,
    ', '.join(['{0}:{1}'.format(p[0], p[1]) for p in self.simple_properties]),
    ', '.join(['{0}:{1}'.format(p[0], p[1]) for p in self.complex_properties]),
    ', '.join(self.depends_list))

    @property
    def fname(self):
        return os.path.join(self.pathname,
            '{}.py'.format(self.wsdl_type))

    @property
    def pathname(self):
        return os.path.join(os.path.dirname(__file__),
            '..',
            'object_types')

    @property
    def object_list_tag(self):
        # find the tag used in TaniumSOAPRequest
        if self.wsdl_type in EXCLUDE_TYPE_LIST:
            return None
        el = self.wsdl_dom.find(".//xsd:complexType[@name='object_list']/xsd:sequence/xsd:element[@type='{}']".format(self.wsdl_type), self.namespaces)
        if el is not None:
            return "'{}'".format(el.attrib['name'])
        return None

    @property
    def code(self):
        return self.TYPE_TEMPLATE.format(
            self.pytype,
            self.object_list_tag,
            self.soap_tag,
            ',\n                        '.join(["'{}': {}".format(p[0], p[1]) for p in self.simple_properties]),
            ',\n                        '.join(["'{}': {}".format(p[0], capcase(p[1])) for p in self.complex_properties]),
            ',\n                        '.join(["'{}': {}".format(p[0], p[1]) for p in self.list_properties]),
            '\n        '.join(["self.{} = None".format(p[0]) for p in self.simple_properties]),
            '\n        '.join(["self.{} = None".format(p[0]) for p in self.complex_properties]),
            '\n        '.join(["self.{} = []".format(p[0]) for p in self.list_properties]),
            '\n'.join(["from {} import {}".format(d, capcase(d)) for d in self.depends_list]),
         )

    def write(self):
        if self.wsdl_type in EXCLUDE_TYPE_LIST:
            return
        if self.preview:
            print 'FILE: {}'.format(self.fname)
            print self.code
        else:
            try:
                os.makedirs(self.pathname)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
            with open(self.fname, 'w') as fd:
                fd.write(get_file_header())
                fd.write(self.code)

class ValueType(Type):

    BUILTIN_TYPE_TEMPLATE = """

from xml.etree import ElementTree as ET

class {0}:
    def __init__(self, val=None):
        self.val = val

    def toSOAPElement(
        el = ET.Element('{1}')
        el.text = str(val)
        return el
"""

    def __init__(self, wsdl_dom, namespaces, type_name, force, preview, verbose):
        Type.__init__(self,
            wsdl_dom=wsdl_dom,
            namespaces=namespaces,
            wsdl_type=type_name,
            simple_properties=[],
            complex_properties=[],
            list_properties=[],
            property_values=[],
            depends_list=[],
            soap_tag=type_name,
            force=force,
            preview=preview,
            verbose=verbose)
    
    @staticmethod
    def load(wsdl_dom, namespaces, type_name, force, preview, verbose):
        return ValueType(wsdl_dom, namespaces, type_name, force, preview, verbose)

    @property
    def code(self):
        return self.BUILTIN_TYPE_TEMPLATE.format(capcase(self.wsdl_type), self.wsdl_type)

def generate_type(wsdlDom, namespaces, typeName, force, preview, verbose):
    if verbose:
        print 'Generating {}'.format(typeName)
    t = Type.load(wsdlDom, namespaces, typeName, force, preview, verbose);
    return t

def generate_value_type(wsdlDom, namespaces, type_name, force, preview, verbose):
    t = ValueType.load(wsdlDom, namespaces, type_name, force, preview, verbose)
    return t
        
def get_namespaces(wsdl_dom, verbose):
    # these are hard-coded for now - had issues pulling from
    # wsdlDom.find('../definitions').attrib
    return {'xsd': 'http://www.w3.org/2001/XMLSchema'}

def get_wsdl_version(input):
    """ElementTree exludes comments, just find the line with regex"""
    with open(input) as fd:
        lines = fd.readlines()
    pattern = r'<!-- Version\: ([0-9\.]+) -->'
    return ''.join([re.match(pattern, line).group(1) for line in lines if re.match(pattern, line)])

def generate_object_list_types(object_list_types):
    with open(os.path.join(os.path.dirname(__file__), '..', 'object_types', 'object_list_types.py'), 'w') as fd:
        for t in sorted(object_list_types):
            clazz = object_list_types[t]
            fd.write('from {0} import {1}\n'.format(
                clazz.wsdl_type,
                capcase(clazz.wsdl_type)))
        fd.write("\n\nOBJECT_LIST_TYPES = {\n")
        for t in sorted(object_list_types):
            clazz = object_list_types[t]
            fd.write("\t{}: {},\n".format(
                clazz.object_list_tag,
                capcase(clazz.wsdl_type)))
        fd.write("}")

def main(wsdlDom, force, preview, verbose):
    namespaces = get_namespaces(wsdlDom, verbose)
    # if no type was passed, find all types and generate them all
    typeElements = wsdlDom.findall(".//xsd:complexType[@name]", namespaces)
    types = set([t.attrib['name'] for t in typeElements if t not in EXCLUDE_TYPE_LIST])
    # while generating types, build a mapping of request object_list tag to class
    object_list_types = {}
    for type_name in sorted(types):
        t = generate_type(wsdlDom, namespaces, type_name, force, preview, verbose)
        t.write()
        if t.is_list and t.is_list_of_value:
            generate_value_type(wsdlDom, namespaces, t.list_type, force, preview, verbose).write()
        if t.object_list_tag:
            object_list_types[t.object_list_tag] = t
    generate_object_list_types(object_list_types)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate Python code from types in WSDL')
    parser.add_argument('-i', '--input', help='WSDL file name', required=True)
    parser.add_argument('-p', '--preview', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    parser.add_argument('-f', '--force', action='store_true', default=False)
    args = parser.parse_args()
    wsdl_version = get_wsdl_version(args.input)
    main(ET.parse(args.input), args.force, args.preview, args.verbose)
