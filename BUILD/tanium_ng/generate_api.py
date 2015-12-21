#!/usr/bin/env python

import datetime
import errno
# import glob
import shutil
import os
import re
import sys
import xml.etree.ElementTree as ET

my_dir = os.path.dirname(__file__)
pname = os.path.splitext(os.path.basename(sys.argv[0]))[0]

def_output_dir = os.path.join(my_dir, '..')

EXCLUDE_TYPE_LIST = ['auth', 'TaniumSOAPRequest', 'TaniumSOAPResult']

XSD_TO_PYTHON_TYPES = {
    'xsd:int': 'int',
    'xsd:string': 'str',
    'xsd:long': 'int'
}

FILE_HEADER_TEMPLATE = """
# Copyright (c) 2015 Tanium Inc
#
# Generated from console.wsdl version {0:<10}
#
#
"""

wsdl_version = None


def get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_file_header():
    if not wsdl_version:
        raise Exception('wsdl_version not set')
    return FILE_HEADER_TEMPLATE.format(wsdl_version, get_now())


def dashcase(val):
    """convert a string to - separated, idempotent"""
    return '-'.join(re.split('[-_]', val))


def capcase(val):
    """convert some_string or some-string to SomeString"""
    val = [
        a[0].upper() + (a[1:]if len(a) > 0 else '')
        for a in re.split('[-_]', val)
    ]
    return ''.join(val)


class Type(object):

    # Template for simple type.
    # Expanded with {0} = type name, {1} = properties
    SIMPLE_PROPERTY_TEMPLATE = (
        "                    this.{0: <30}     = {1}"
    )
    COMPLEX_PROPERTY_TEMPLATE = (
        "                    this.{0: <30}     = None"
    )

    TYPE_TEMPLATE = """
from .base import BaseType


class {0}(BaseType):

    _soap_tag = '{1}'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={{{2}}},
            complex_properties={{{3}}},
            list_properties={{{4}}},
        )
        {5}
        {6}
        {7}

{8}

"""

    def __init__(self, wsdl_dom, namespaces, wsdl_type, simple_properties,
                 complex_properties, list_properties, property_values,
                 depends_list, soap_tag, force, preview, verbose):
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
        c1 = '_list'
        c2 = 'user_permissions'
        return self.wsdl_type.endswith(c1) or self.wsdl_type == c2

    @property
    def list_type(self):
        if not self.is_list:
            raise Exception('{} is not a list type'.format(self.wsdl_type))
        if self.wsdl_type == 'user_permissions':
            return 'permission'
        elif self.is_list_of_value:
            print('list of value: {}'.format(self.wsdl_type))
            return self.wsdl_type[:-5]
        else:
            find_tpl = (
                ".//xsd:complexType[@name='{}']/xsd:sequence/xsd:element"
                "[@type]"
            ).format(self.wsdl_type)
            el = self.wsdl_dom.find(find_tpl, self.namespaces)
            if el is None:
                exc_tpl = (
                    'Could not find {} list type in wsdl'
                ).format(self.wsdl_type)
                raise Exception(exc_tpl)
            return el.attrib['type']

    @property
    def is_list_of_value(self):
        find_tpl = (
            ".//xsd:complexType[@name='{}']/xsd:sequence/xsd:element[@type]"
        ).format(self.wsdl_type)
        el = self.wsdl_dom.find(find_tpl, self.namespaces)
        return el.attrib['type'].startswith('xsd:')

    @property
    def type_dependencies(self):
        return [d for d in self.depends_list if d not in EXCLUDE_TYPE_LIST]

    @staticmethod
    def load(wsdl_dom, namespaces, type_name, force, preview, verbose):
        """Use the WSDL to lookup the definition and usage of type_name."""
        # find_tpl = ".//xsd:complexType[@name='{}']".format(type_name)
        # type_element = wsdl_dom.find(find_tpl, namespaces)

        # find_tpl = (
        # ".//xsd:element[@type='{}']/../..[@name]"
        # ).format(type_name)
        # usage_elements = wsdl_dom.findall(find_tpl, namespaces)

        # built-in property types
        find_tpl = (
            ".//xsd:complexType[@name='{}']/*/xsd:element[@type]"
        ).format(type_name)
        simple_properties = [
            (el.attrib['name'], XSD_TO_PYTHON_TYPES[el.attrib['type']])
            for el in wsdl_dom.findall(find_tpl, namespaces)
            if el.attrib['type'].startswith('xsd:') and
            el.attrib.get('maxOccurs') != 'unbounded'
        ]

        # complex property types
        find_tpl = (
            ".//xsd:complexType[@name='{}']/*/xsd:element[@type]"
        ).format(type_name)
        complex_properties = [
            (el.attrib['name'], el.attrib['type'])
            for el in wsdl_dom.findall(find_tpl, namespaces)
            if not el.attrib['type'].startswith('xsd:')
            and not el.attrib.get('maxOccurs') == 'unbounded'
        ]

        find_tpl = (
            ".//xsd:complexType[@name='{}']/*/xsd:element[@type]"
        ).format(type_name)
        list_properties = [
            (
                el.attrib['name'], XSD_TO_PYTHON_TYPES[el.attrib['type']]
                if el.attrib['type'].startswith('xsd') else capcase(el.attrib['type'])
            )
            for el in wsdl_dom.findall(find_tpl, namespaces)
            if el.attrib.get('maxOccurs') == 'unbounded'
        ]
        print('{}:{}'.format(type_name, list_properties))
        find_tpl = (
            ".//xsd:complexType[@name='{}']/*/xsd:element[@type]"
        ).format(type_name)
        property_values = {}
        for el in wsdl_dom.findall(find_tpl, namespaces):
            if not el.attrib['type'].startswith('xsd:'):
                continue
            if 'default' in el.attrib:
                if el.attrib['type'] == 'xsd:string':
                    el_val = '"{}"'.format(el.attrib['default'])
                else:
                    el_val = '{}'.format(el.attrib['default'])
                property_values[el.attrib['name']] = el_val

            else:
                if el.attrib['type'] != 'xsd:int':
                    el_val = 'null'
                else:
                    el_val = 'Number.NaN'
                property_values[el.attrib['name']] = el_val

        find_tpl = (
            ".//xsd:complexType[@name='{}']/*/xsd:element[@type]"
        ).format(type_name)
        property_values.update({
            el.attrib['name']: '[]'
            for el in wsdl_dom.findall(find_tpl, namespaces)
            if not el.attrib['type'].startswith('xsd:')
        })

        # determine dependencies
        find_tpl = (
            ".//xsd:complexType[@name='{}']/*/xsd:element[@type]"
        ).format(type_name)
        depends_list = [
            el.attrib['type']
            for el in wsdl_dom.findall(find_tpl, namespaces)
            if not el.attrib['type'].startswith('xsd:')
        ]

        # generate the soap tag. If this is a type used in a list, use what
        # the list attribute name is. If not, use the type name. Look
        # for usage in an xsd:sequence or xsd:all for another type
        find_tpl = (
            ".//xsd:complexType/xsd:sequence/xsd:element[@type='{0}']"
        ).format(type_name)
        usage = wsdl_dom.find(find_tpl, namespaces)
        if usage is None:
            find_tpl = (
                ".//xsd:complexType/xsd:all/xsd:element[@type='{0}']"
            ).format(type_name)
            usage = wsdl_dom.find(find_tpl, namespaces)

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
        simple_properties = ', '.join(
            ['{0}:{1}'.format(p[0], p[1]) for p in self.simple_properties]
        )
        complex_properties = ', '.join(
            ['{0}:{1}'.format(p[0], p[1]) for p in self.complex_properties]
        )
        depends_list = ', '.join(self.depends_list)
        s = (
            "WSDL type: {0}\n"
            "Simple Properties: {1}\n"
            "Complex Properties: {2}\n"
            "Dependencies: {3}\n"
        ).format(
            self.wsdl_type,
            simple_properties,
            complex_properties,
            depends_list,
        )
        return s

    def fname(self, output):
        return os.path.join(
            self.pathname(output), '{}.py'.format(self.wsdl_type)
        )

    def pathname(self, output):
        return os.path.join(output, 'api', 'object_types')

    @property
    def code(self):
        simple_args = ',\n                        '.join(
            ["'{}': {}".format(p[0], p[1]) for p in self.simple_properties]
        )
        complex_args = ',\n                        '.join(
            [
                "'{}': {}".format(p[0], capcase(p[1]))
                for p in self.complex_properties
            ]
        )
        list_args = ',\n                        '.join(
            ["'{}': {}".format(p[0], p[1]) for p in self.list_properties]
        )
        simple_properties = '\n        '.join(
            ["self.{} = None".format(p[0]) for p in self.simple_properties]
        )
        complex_properties = '\n        '.join(
            ["self.{} = None".format(p[0]) for p in self.complex_properties]
        )
        list_properties = '\n        '.join(
            ["self.{} = []".format(p[0]) for p in self.list_properties]
        )
        depends_list = '\n'.join(
            [
                "from {} import {}".format(d, capcase(d))
                for d in self.depends_list
            ]
        )
        s = self.TYPE_TEMPLATE.format(
            self.pytype,
            self.soap_tag,
            simple_args,
            complex_args,
            list_args,
            simple_properties,
            complex_properties,
            list_properties,
            depends_list,
        )
        return s

    def write(self, output):
        if self.wsdl_type in EXCLUDE_TYPE_LIST:
            return
        if self.preview:
            print('FILE: {}'.format(self.fname(output)))
            print(self.code)
        else:
            try:
                os.makedirs(self.pathname(output))
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
            with open(self.fname(output), 'w') as fd:
                fd.write(get_file_header())
                fd.write(self.code)


def generate_type(wsdlDom, namespaces, typeName, force, preview, output,
                  verbose):
    if verbose:
        print('Generating {}'.format(typeName))
    t = Type.load(wsdlDom, namespaces, typeName, force, preview, verbose)  # ;
    if verbose:
        print('Generated {}'.format(t.fname(output)))
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
    patterns = [
        re.match(pattern, line).group(1)
        for line in lines if re.match(pattern, line)
    ]
    return ''.join(patterns)


def print_out(s):
    print(s)


def generate_object_list_types(soap_tags, preview, verbose, output):
    fpath = os.path.join(output, 'api', 'object_types', 'object_list_types.py')
    if verbose:
        print('Generating {}'.format(fpath))
    if preview:
        writer = print_out
    else:
        fd = open(fpath, 'w')
        writer = fd.write

    for t in sorted(soap_tags):
        clazz = soap_tags[t]
        writer('from {0} import {1}\n'.format(
            clazz.wsdl_type,
            capcase(clazz.wsdl_type)))
    writer("\n\nOBJECT_LIST_TYPES = {\n")
    for t in sorted(soap_tags):
        clazz = soap_tags[t]
        writer("\t'{}': {},\n".format(
            clazz.soap_tag,
            capcase(clazz.wsdl_type)))
    writer("}")
    if verbose:
        print('Generated {}'.format(fpath))


def main(args):

    force = args.force
    preview = args.preview
    verbose = args.verbose
    output = args.output
    input = args.input

    api_dir = os.path.join(output, 'api')
    statics_dir = os.path.join(my_dir, 'statics')

    if not preview:
        if os.path.isdir(api_dir):
            if not force:
                raise Exception((
                    "Directory {} already exists! Remove/rename"
                ).format(api_dir))
            else:
                old_api_dir = "{}.{}".format(
                    api_dir,
                    datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                )
                print("Renaming {} to {}".format(api_dir, old_api_dir))
                os.rename(api_dir, old_api_dir)
        shutil.copytree(statics_dir, api_dir, symlinks=True)

    wsdlDom = ET.parse(input)

    namespaces = get_namespaces(wsdlDom, verbose)

    # if no type was passed, find all types and generate them all
    typeElements = wsdlDom.findall(".//xsd:complexType[@name]", namespaces)
    types = set([
        t.attrib['name'] for t in typeElements if t not in EXCLUDE_TYPE_LIST
    ])

    # while generating types, build a mapping of soap tag to class
    all_obj = []
    soap_tags = {}
    for type_name in sorted(types):

        t = generate_type(
            wsdlDom,
            namespaces,
            type_name,
            force,
            preview,
            output,
            verbose,
        )
        t.write(output)
        all_obj.append(t)
        if t.wsdl_type not in EXCLUDE_TYPE_LIST:
            soap_tags[t.soap_tag] = t

    fpath = os.path.join(output, 'api', 'object_types', 'all_objects.py')

    if verbose:
        print('Generating {}'.format(fpath))
    if preview:
        writer = print_out
    else:
        fd = open(fpath, 'w')
        writer = fd.write

    for t in [x for x in all_obj if x.wsdl_type not in EXCLUDE_TYPE_LIST]:
        writer('from {0} import {1}\n'.format(
            t.wsdl_type,
            capcase(t.wsdl_type)))

    if verbose:
        print('Generated {}'.format(fpath))

    generate_object_list_types(soap_tags, preview, verbose, output)


if __name__ == '__main__':
    import argparse
    from argparse import ArgumentDefaultsHelpFormatter as A1
    from argparse import RawDescriptionHelpFormatter as A2

    class CustomFormatter(A1, A2):
        pass

    class CustomParser(argparse.ArgumentParser):
        def __init__(self, *args, **kwargs):
            if 'formatter_class' not in kwargs:
                kwargs['formatter_class'] = CustomFormatter
            argparse.ArgumentParser.__init__(self, *args, **kwargs)

        def error(self, message):
            self.print_help()
            print('ERROR:{}:{}\n'.format(pname, message))
            sys.exit(2)

    parser = CustomParser(
        description='Generate Python code from types in WSDL',
        formatter_class=CustomFormatter,
    )
    parser.add_argument(
        '-i', '--input', help='WSDL file name', required=True,
    )
    parser.add_argument(
        '-o', '--output', help='output directory', default=def_output_dir,
    )
    parser.add_argument(
        '-p', '--preview', action='store_true', default=False,
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
    )
    parser.add_argument(
        '-f', '--force', action='store_true', default=False,
    )
    args = parser.parse_args()
    wsdl_version = get_wsdl_version(args.input)
    main(args)
