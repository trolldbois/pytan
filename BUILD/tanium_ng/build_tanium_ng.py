#!/usr/bin/env python3
"""Builds the ../../pytan/tanium_ng directory from the ../../doc/console.wsdl file"""

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

from pytan import utils
from pytan import version as pytan_version
from pytan.utils.argparsers import ShellParser

import re
import logging
import string
import shutil
import tempfile

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET


logname = 'build.tanium_ng'
mylog = logging.getLogger(logname)
mylog.setLevel(logging.INFO)
utils.log.install_console(logger_name=logname)


class WsdlParser(object):

    EXCLUDE_TYPES = ['auth', 'TaniumSOAPRequest', 'TaniumSOAPResult']
    NAMESPACES = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    XSD_MAP = {
        'xsd:int': 'int',
        'xsd:string': 'text_type',
        'xsd:long': 'int'
    }

    HEADER_STRING = ('''"""${desc}

* License: ${pytan_license}
* Copyright: ${pytan_copyright}
* Generated from ``console.wsdl`` by ``${script_name}`` on ${now}
* Version of ``console.wsdl``: ${wsdl_version}
* Tanium Server version of ``console.wsdl``: ${tanium_version}
* Version of PyTan: ${pytan_version}

"""''')

    INIT_STRING = HEADER_STRING + (
        '''
${imports}

OBJECT_TYPES = {
${object_types}
}

__all__ = [
    'OBJECT_TYPES',
${alls}
]
''')

    CODE_STRING = HEADER_STRING + (
        '''
from .base import BaseType


class ${py_type}(BaseType):

    _soap_tag = '${soap_tag}'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        ${simple_properties}
        ${complex_properties}
        ${list_properties}
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


${imports}

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)
import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
${SIMPLE_ARGS}

COMPLEX_ARGS = {}
${COMPLEX_ARGS}

LIST_ARGS = {}
${LIST_ARGS}
''')

    INIT_TEMPLATE = string.Template(INIT_STRING)
    CODE_TEMPLATE = string.Template(CODE_STRING)

    STATICS = [
        {
            'file': 'base.py',
            'py_type': 'BaseType',
            'desc': '''The BaseType used by (almost) all tanium_ng objects.

Handles the serialization and deserialization of objects to / from XML and Python''',
        },
        {'file': 'column.py', 'py_type': 'Column'},
        {'file': 'column_set.py', 'py_type': 'ColumnSet'},
        {'file': 'result_info.py', 'py_type': 'ResultInfo'},
        {'file': 'result_set.py', 'py_type': 'ResultSet'},
        {'file': 'row.py', 'py_type': 'Row'},
    ]

    def __init__(self, args):
        self.args = args
        self.capcase = utils.tools.capcase
        self.wsdl_file = os.path.abspath(os.path.expanduser(self.args.input))
        self.wsdl_contents = utils.tools.read_file(self.wsdl_file)
        self.wsdl_version = self.get_wsdl_version()
        self.tanium_version = self.get_tanium_version()
        self.wsdl_dom = self.parse_wsdl()
        self.object_types = self.find_types()

        if self.args.run:
            self.check_output_dir()

        self.object_maps = [self.write_static(x) for x in self.STATICS]
        self.object_maps += [self.parse_type(x) for x in self.object_types]
        self.write_init()

    def write_static(self, static):
        result = {}
        result.update(static)
        result['type_name'] = os.path.splitext(static['file'])[0]

        filepath = os.path.join(my_dir, 'statics', static['file'])
        code = utils.tools.read_file(filepath)

        desc = 'Static object Serializer/Deserializer for Tanium SOAP XML types: ``{py_type}``'
        desc = desc.format(**result)

        if 'desc' not in result:
            result['desc'] = desc

        result.update(self.general_subs())
        header = string.Template(self.HEADER_STRING)
        header = header.substitute(result)
        result['code'] = '\n'.join([header, code])
        self.write_file(result['file'], result['code'])
        return result

    def check_output_dir(self):
        output_dir = self.get_output_dir()
        output_exists = os.path.isdir(output_dir)

        if output_exists and not self.args.force:
            err = "Output dir: '{}' exists and -f/--force not supplied!"
            err = err.format(output_dir)
            raise Exception(err)

        if output_exists and self.args.force:
            tempdir = tempfile.gettempdir()
            output_base = os.path.basename(output_dir) + '_backup'
            output_dst = os.path.join(tempdir, output_base)
            utils.tools.clean_it(output_dst, mylog)
            shutil.move(output_dir, output_dst)
            m = "Moved old output dir '{}' to '{}'"
            m = m.format(output_dir, output_dst)
            mylog.info(m)

    def write_init(self):
        filename = '__init__.py'
        subs = {}

        impt = "from .{type_name} import {py_type}".format
        t = "imports"
        a = [impt(**x) for x in self.object_maps]
        subs[t] = '\n'.join(a)

        allt = "    '{py_type}',".format
        t = "alls"
        a = [allt(**x) for x in self.object_maps]
        subs[t] = '\n'.join(a)

        typet = "    '{soap_tag}': {py_type},".format
        t = "object_types"
        a = [typet(**x) for x in self.object_maps if 'soap_tag' in x]
        subs[t] = '\n'.join(a)

        subs['desc'] = (
            'Tanium NG: An object Serializer/Deserializer for the XML used by the Tanium SOAP API'
        )
        subs.update(self.general_subs())

        code = self.INIT_TEMPLATE.substitute(subs)
        self.write_file(filename, code)

    def get_output_dir(self):
        result = os.path.abspath(os.path.expanduser(self.args.output))
        return result

    def write_file(self, filename, filecode):
        h = '#' * 10
        m = '{0} {1}:\n{2}\n{0}'
        m = m.format(h, filename, filecode)
        mylog.debug(m)

        if self.args.run:
            output = self.get_output_dir()
            filepath = os.path.join(output, filename)
            utils.tools.write_file(filepath, filecode, mylog)
        else:
            m = "-r/--run not provided, not writing code - generated {} bytes of code for '{}'"
            m = m.format(len(filecode), filename)
            mylog.info(m)

    def parse_type(self, type_name):
        result = {}
        result['type_name'] = type_name
        result['soap_tag'] = self.get_soap_tag(type_name)
        result['py_type'] = self.capcase(result['type_name'])
        result['type_els'] = self.find_type_els(result['type_name'])
        result['stypes_list'] = self.get_simpleattrs(result['type_els'])
        result['ctypes_list'] = self.get_complexattrs(result['type_els'])
        result['ltypes_list'] = self.get_listattrs(result['type_els'])
        result['deps_list'] = self.get_deps(result['type_els'])
        result['file_name'] = self.get_file_name(result['type_name'])

        m = "{!r} simple: {}, complex: {}, list: {}, deps: {}, tag: {}, py: {}"
        m = m.format(
            result['type_name'],
            len(result['stypes_list']),
            len(result['ctypes_list']),
            len(result['ltypes_list']),
            len(result['deps_list']),
            result['soap_tag'],
            result['py_type'],
        )
        mylog.debug(m)

        result = self.get_type_code(result)
        self.write_file(result['file_name'], result['code'])
        return result

    def get_file_name(self, type_name):
        result = '{}.py'.format(type_name)
        return result

    def parse_wsdl(self):
        wsdl_dom = ET.fromstring(self.wsdl_contents)
        return wsdl_dom

    def search_wsdl(self, xpath, **kwargs):
        single = kwargs.get('single', False)
        namespaces = kwargs.get('namespaces', self.NAMESPACES)
        if single:
            result = self.wsdl_dom.find(xpath, namespaces)
            m = "Found single {} element using xpath {!r}"
            m = m.format(result, xpath)
        else:
            result = self.wsdl_dom.findall(xpath, namespaces)
            m = "Found {} elements using xpath {!r}"
            m = m.format(len(result), xpath)
        mylog.debug(m)
        return result

    def find_types(self, **kwargs):
        type_elements = self.search_wsdl(xpath=".//xsd:complexType[@name]", **kwargs)
        result = [
            t.attrib['name'] for t in type_elements
            if t.attrib['name'] not in self.EXCLUDE_TYPES
        ]
        result = sorted(list(set(result)))
        m = "Found {} object types in WSDL File"
        m = m.format(len(result))
        mylog.info(m)
        return result

    def find_type_els(self, type_name, **kwargs):
        find_tpl = ".//xsd:complexType[@name='{}']/*/xsd:element[@type]".format(type_name)
        type_els = self.search_wsdl(xpath=find_tpl, **kwargs)
        return type_els

    def get_simpleattrs(self, type_els):
        els = [
            x for x in type_els
            if x.attrib['type'].startswith('xsd:')
            and x.attrib.get('maxOccurs') != 'unbounded'
        ]
        result = [(x.attrib['name'], self.XSD_MAP[x.attrib['type']]) for x in els]
        return result

    def get_complexattrs(self, type_els):
        els = [
            x for x in type_els
            if not x.attrib['type'].startswith('xsd:')
            and not x.attrib.get('maxOccurs') == 'unbounded'
        ]
        result = [(x.attrib['name'], x.attrib['type']) for x in els]
        return result

    def _get_el_listtype(self, el):
        if el.attrib['type'].startswith('xsd'):
            result = self.XSD_MAP[el.attrib['type']]
        else:
            result = self.capcase(el.attrib['type'])
        return result

    def get_listattrs(self, type_els):
        els = [
            x for x in type_els
            if x.attrib.get('maxOccurs') == 'unbounded'
        ]
        result = [(x.attrib['name'], self._get_el_listtype(x)) for x in els]
        return result

    def get_soap_tag(self, type_name, **kwargs):
        find_tpl = ".//xsd:complexType/xsd:sequence/xsd:element[@type='{0}']".format(type_name)
        usage = self.search_wsdl(xpath=find_tpl, single=True, **kwargs)
        if usage is None:
            find_tpl = ".//xsd:complexType/xsd:all/xsd:element[@type='{0}']".format(type_name)
            usage = self.search_wsdl(xpath=find_tpl, single=True, **kwargs)

        result = usage.attrib['name'] if usage is not None else type_name
        return result

    def get_deps(self, type_els):
        result = [x.attrib['type'] for x in type_els if not x.attrib['type'].startswith('xsd:')]
        result = list(set(result))
        return result

    def get_tanium_version(self):
        """ElementTree exludes comments, just find the line with regex"""
        pattern = r'<!-- From Tanium Server Version\: ([0-9\.]+) -->'
        result = self.search_wsdl_contents(pattern, 'tanium_version')
        return result

    def get_wsdl_version(self):
        """ElementTree exludes comments, just find the line with regex"""
        pattern = r'<!-- Version\: ([0-9\.]+) -->'
        result = self.search_wsdl_contents(pattern, 'wsdl_version')
        return result

    def search_wsdl_contents(self, pattern, name):
        result = re.search(pattern, self.wsdl_contents)

        if not result:
            err = "Unable to find {!r} using pattern {!r} in {!r}"
            err = err.format(name, pattern, self.wsdl_file)
            raise Exception(err)

        result = str(result.groups()[0]).strip()
        m = "Parsed {!r} from WSDL file: {!r}"
        m = m.format(name, result)
        mylog.info(m)
        return result

    def general_subs(self):
        result = {}
        result['now'] = utils.calc.get_now()
        result['tanium_version'] = self.tanium_version
        result['wsdl_version'] = self.wsdl_version
        result['pytan_version'] = pytan_version.__version__
        result['pytan_codename'] = pytan_version.__codename__
        result['pytan_title'] = pytan_version.__title__
        result['pytan_url'] = pytan_version.__url__
        result['pytan_author'] = pytan_version.__author__
        result['pytan_email'] = pytan_version.__email__
        result['pytan_description'] = pytan_version.__description__
        result['pytan_license'] = pytan_version.__license__
        result['pytan_copyright'] = pytan_version.__copyright__
        result['pytan_status'] = pytan_version.__status__
        result['script_name'] = my_file
        return result

    def get_type_code(self, type_dict):
        argt = "{}['{}'] = {}".format
        linej = '\n'
        nullt = '# no {} defined'.format

        t = 'SIMPLE_ARGS'
        a = [argt(t, p[0], p[1]) for p in type_dict['stypes_list']] or [nullt(t)]
        type_dict[t] = linej.join(a)

        t = 'COMPLEX_ARGS'
        a = [argt(t, p[0], self.capcase(p[1])) for p in type_dict['ctypes_list']] or [nullt(t)]
        type_dict[t] = linej.join(a)

        t = 'LIST_ARGS'
        a = [argt(t, p[0], p[1]) for p in type_dict['ltypes_list']] or [nullt(t)]
        type_dict[t] = linej.join(a)

        simple_def = "self.{} = None".format
        list_def = "self.{} = []".format
        propj = '\n        '

        t = 'simple_properties'
        a = [simple_def(p[0]) for p in type_dict['stypes_list']] or [nullt(t)]
        type_dict[t] = propj.join(a)

        t = 'complex_properties'
        a = [simple_def(p[0]) for p in type_dict['ctypes_list']] or [nullt(t)]
        type_dict[t] = propj.join(a)

        t = 'list_properties'
        a = [list_def(p[0]) for p in type_dict['ltypes_list']] or [nullt(t)]
        type_dict[t] = propj.join(a)

        dept = "from .{} import {}".format
        nulld = "# no extra imports used"

        t = "imports"
        a = [dept(d, self.capcase(d)) for d in type_dict['deps_list']] or [nulld]
        type_dict[t] = linej.join(a)

        desc = 'Object Serializer/Deserializer for Tanium SOAP XML tag: ``{soap_tag}``'
        desc = desc.format(**type_dict)
        type_dict['desc'] = desc

        type_dict.update(self.general_subs())

        t = 'code'
        type_dict[t] = self.CODE_TEMPLATE.substitute(type_dict)
        return type_dict

if __name__ == '__main__':
    pytan_dir = os.path.join(os.pardir, os.pardir)
    default_wsdl_file = os.path.join(pytan_dir, "doc", "console.wsdl")
    default_output_dir = os.path.join(pytan_dir, "pytan", "tanium_ng")
    # default_output_dir = "/tmp/tanium_ng"

    parser = ShellParser(my_file=my_file, description=__doc__)
    parser.add_argument(
        '-i', '--input',
        required=False, action='store', dest='input', default=default_wsdl_file,
        help='Tanium Server WSDL File to generate tanium_ng from',
    )
    parser.add_argument(
        '-o', '--output',
        required=False, action='store', dest='output', default=default_output_dir,
        help='Directory to generate tanium_ng in',
    )
    parser.add_argument(
        '-r', '--run',
        required=False, action='store_true', dest='run', default=False,
        help='Actually generate the tanium_ng directory instead of just previewing the changes',
    )
    parser.add_argument(
        '-f', '--force',
        required=False, action='store_true', dest='force', default=False,
        help='If --output dir exists and --run, move the dir to the temp folder',
    )
    parser.add_argument(
        '-v', '--verbose',
        required=False, action='store_true', dest='verbose', default=False,
        help='Show verbose messages',
    )

    args = parser.parse_args()
    if args.verbose:
        mylog.setLevel(logging.DEBUG)

    wsdl_parser = WsdlParser(args=args)
