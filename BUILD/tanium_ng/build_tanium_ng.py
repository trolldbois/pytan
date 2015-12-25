#!/usr/bin/env python3
"""Builds the file ``../../pytan/tanium_ng.py`` from the file ``../../doc/console.wsdl``"""

# BEGIN BOOTSTRAP CODE
# statically defined path
PYTAN_PATH = "~/gh/pytan/pytan"

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
pytan_root = os.path.dirname(parent_dir)
pytan_dir = os.path.join(pytan_root, 'pytan')
path_adds.append(pytan_dir)

# if OS Environment "PYTAN_PATH" is set, add that to path_adds
if 'PYTAN_PATH' in os.environ:
    path_adds.append(os.environ['PYTAN_PATH'])

# expand user directories and get the absolute path of all path_adds
path_adds = [os.path.abspath(os.path.expanduser(aa)) for aa in path_adds]
print(path_adds)
# add the path_adds to beginning of PYTHONPATH
[sys.path.insert(0, aa) for aa in path_adds if aa not in sys.path]

# END BOOTSTRAP CODE

import utils

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
    NAMESPACES = {
        'xsd': 'http://www.w3.org/2001/XMLSchema',
        't': 'urn:TaniumSOAP'
    }
    XSD_MAP = {
        'xsd:int': 'int',
        'xsd:string': 'text_type',
        'xsd:long': 'int'
    }

    HEADER_STRING = (
        '''"""Tanium NG: A Python object representation layer for the XML used by the Tanium SOAP API.

* License: ${pytan_license}
* Copyright: ${pytan_copyright}
* Generated from ``console.wsdl`` by ``${script_name}`` on ${now}
* Version of ``console.wsdl``: ${wsdl_version}
* Tanium Server version of ``console.wsdl``: ${tanium_version}
* Version of PyTan: ${pytan_version}

"""
# BEGIN STATIC CODE
${STATIC_CODE}

# END STATIC CODE
# BEGIN DYNAMIC CODE
''')

    CODE_STRING = (
        '''

class ${py_type}(BaseType):
    """${desc}.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = '${soap_tag}'

    CONSTANTS = [
        ${CONSTANTS}
    ]

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                ${SIMPLE_ARGS}
            },
            complex_properties={
                ${COMPLEX_ARGS}
            },
            list_properties={
                ${LIST_ARGS}
            },
            **kwargs
        )
        ${SIMPLE_PROPS}
        ${COMPLEX_PROPS}
        ${LIST_PROPS}
        self._set_init_values()
''')

    FOOTER_STRING = (
        '''

BASE_TYPES = {}
"""Maps Tanium XML soap tags to the Tanium NG Python BaseType object"""
BASE_TYPES['result_infos'] = ResultInfoList  # static
BASE_TYPES['result_info'] = ResultInfo  # static
BASE_TYPES['result_sets'] = ResultSetList  # static
BASE_TYPES['result_set'] = ResultSet  # static
BASE_TYPES['cs'] = ColumnList  # static
BASE_TYPES['c'] = Column  # static
BASE_TYPES['rs'] = RowList  # static
BASE_TYPES['r'] = Row  # static

${BASE_TYPES}

# END DYNAMIC CODE
''')
    HEADER_TEMPLATE = string.Template(HEADER_STRING)
    CODE_TEMPLATE = string.Template(CODE_STRING)
    FOOTER_TEMPLATE = string.Template(FOOTER_STRING)
    STATIC_FILE = 'static_tanium_ng.py'

    def __init__(self, args):
        self.args = args
        self.capcase = utils.tools.capcase
        self.wsdl_file = os.path.abspath(os.path.expanduser(self.args.input))
        self.ng_file = os.path.abspath(os.path.expanduser(self.args.output))
        self.ng_static_file = os.path.join(my_dir, self.STATIC_FILE)
        self.ng_statics = self.read_file(self.ng_static_file)
        self.wsdl_contents = self.read_file(self.wsdl_file)
        self.wsdl_version = self.get_wsdl_version()
        self.tanium_version = self.get_tanium_version()
        self.wsdl_dom = self.parse_wsdl()
        self.object_types = self.find_types()
        self.object_maps = [self.parse_type(x) for x in self.object_types]
        self.write_tanium_ng()

    def read_file(self, f):
        result = utils.tools.read_file(f)
        m = "Read {} bytes from file: '{}'"
        m = m.format(len(result), f)
        mylog.info(m)
        return result

    def write_tanium_ng(self):
        filename = '__init__.py'
        subs = {}
        subs.update(self.general_subs())
        subs['STATIC_CODE'] = self.ng_statics

        typet = "BASE_TYPES['{soap_tag}'] = {py_type}".format
        a = [typet(**x) for x in self.object_maps if 'soap_tag' in x]
        subs['BASE_TYPES'] = '\n'.join(a)

        header = self.HEADER_TEMPLATE.substitute(subs)
        footer = self.FOOTER_TEMPLATE.substitute(subs)

        filecode = [header] + [x['code'] for x in self.object_maps] + [footer]
        filecode = ''.join(filecode)
        filename = self.ng_file

        m = '{0} {1}:\n{2}\n{0}'
        m = m.format('#' * 30, filename, filecode)
        mylog.debug(m)

        if self.args.run:
            if os.path.exists(filename):
                tempdir = tempfile.gettempdir()
                output_base = os.path.basename(filename) + '_backup'
                backupname = os.path.join(tempdir, output_base)
                if os.path.exists(backupname):
                    os.remove(backupname)
                    m = "Removed old backup: {}"
                    m = m.format(backupname)
                    mylog.info(m)

                shutil.move(filename, backupname)
                m = "Moved current tanium_ng from '{}' to '{}'"
                m = m.format(filename, backupname)
                mylog.info(m)

            utils.tools.write_file(filename, filecode, mylog)
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
        result['constants'] = self.find_constants(result['type_name'])
        result['simples'] = self.get_simples(result['type_els'])
        result['complexes'] = self.get_complexes(result['type_els'])
        result['lists'] = self.get_lists(result['type_els'])
        result['file_name'] = self.get_file_name(result['type_name'])

        t = "pyobject: {py_type!r}, xml tag: {soap_tag!r}".format(**result)
        mi = []
        for k in ['simples', 'complexes', 'lists', 'constants']:
            mi.append("{}: {}".format(k, len(result[k])))
            md = "    {}: {}".format(k, result[k])
            mylog.debug(md)

        mylog.info("{}: {}".format(t, ', '.join(mi)))

        result = self.get_type_code(result)
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

    def find_constants(self, type_name, **kwargs):
        find_tpl = ".//xsd:complexType[@name='{}']/xsd:annotation//t:constant".format(type_name)
        els = self.search_wsdl(find_tpl, **kwargs)
        if els:
            # keys = ['name', 'value', 'type']
            result = [(i[0].text, i[1].text, self.XSD_MAP[i[1].attrib['type']]) for i in els]
            # result = [dict(zip(keys, i)) for i in vals]
        else:
            result = []
        return result

    def find_type_els(self, type_name, **kwargs):
        find_tpl = ".//xsd:complexType[@name='{}']/*/xsd:element[@type]".format(type_name)
        type_els = self.search_wsdl(xpath=find_tpl, **kwargs)
        return type_els

    def get_simples(self, type_els):
        els = [
            x for x in type_els
            if x.attrib['type'].startswith('xsd:')
            and x.attrib.get('maxOccurs') != 'unbounded'
        ]
        result = [(x.attrib['name'], self.XSD_MAP[x.attrib['type']]) for x in els]
        result = dict(result)
        return result

    def get_complexes(self, type_els):
        els = [
            x for x in type_els
            if not x.attrib['type'].startswith('xsd:')
            and not x.attrib.get('maxOccurs') == 'unbounded'
        ]
        result = [(x.attrib['name'], x.attrib['type']) for x in els]
        result = dict(result)
        return result

    def _get_el_listtype(self, el):
        if el.attrib['type'].startswith('xsd'):
            result = self.XSD_MAP[el.attrib['type']]
        else:
            result = self.capcase(el.attrib['type'])
        return result

    def get_lists(self, type_els):
        els = [
            x for x in type_els
            if x.attrib.get('maxOccurs') == 'unbounded'
        ]
        result = [(x.attrib['name'], self._get_el_listtype(x)) for x in els]
        result = dict(result)
        return result

    def get_soap_tag(self, type_name, **kwargs):
        find_tpl = ".//xsd:complexType/xsd:sequence/xsd:element[@type='{0}']".format(type_name)
        usage = self.search_wsdl(xpath=find_tpl, single=True, **kwargs)
        if usage is None:
            find_tpl = ".//xsd:complexType/xsd:all/xsd:element[@type='{0}']".format(type_name)
            usage = self.search_wsdl(xpath=find_tpl, single=True, **kwargs)

        result = usage.attrib['name'] if usage is not None else type_name
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
        result['now'] = utils.tools.get_now()
        result['tanium_version'] = self.tanium_version
        result['wsdl_version'] = self.wsdl_version
        result['pytan_version'] = utils.__version__
        result['pytan_codename'] = utils.__codename__
        result['pytan_title'] = utils.__title__
        result['pytan_url'] = utils.__url__
        result['pytan_author'] = utils.__author__
        result['pytan_email'] = utils.__email__
        result['pytan_description'] = utils.__description__
        result['pytan_license'] = utils.__license__
        result['pytan_copyright'] = utils.__copyright__
        result['pytan_status'] = utils.__status__
        result['script_name'] = my_file
        return result

    def get_type_code(self, type_dict):
        argt = "'{}': {},".format
        argj = '\n                '.join
        propj = '\n        '.join
        conj = "\n        ".join

        nullt = ['# no constants defined in console.wsdl']
        con_def = "{{'name': '{}', 'value': '{}', 'type': {}}},".format
        p = type_dict['constants']
        type_dict['CONSTANTS'] = conj([con_def(*k) for k in p] or nullt)

        nullt = ['# no simple properties defined in console.wsdl']
        attr_def = "self.{} = None".format
        p = type_dict['simples'].items()
        type_dict['SIMPLE_ARGS'] = argj([argt(k, v) for k, v in p] or nullt)
        type_dict['SIMPLE_PROPS'] = propj([attr_def(k) for k, v in p] or nullt)

        nullt = ['# no complex properties defined in console.wsdl']
        attr_def = "self.{} = None".format
        p = type_dict['complexes'].items()
        type_dict['COMPLEX_ARGS'] = argj([argt(k, self.capcase(v)) for k, v in p] or nullt)
        type_dict['COMPLEX_PROPS'] = propj([attr_def(k) for k, v in p] or nullt)

        nullt = ['# no list properties defined in console.wsdl']
        attr_def = "self.{} = []".format
        p = type_dict['lists'].items()
        type_dict['LIST_ARGS'] = argj([argt(k, v) for k, v in p] or nullt)
        type_dict['LIST_PROPS'] = propj([attr_def(k) for k, v in p] or nullt)

        desc = 'Python Object representation for Tanium SOAP XML tag: ``{soap_tag}``'
        type_dict['desc'] = desc.format(**type_dict)
        type_dict['code'] = self.CODE_TEMPLATE.substitute(type_dict)
        return type_dict

if __name__ == '__main__':
    pytan_dir = os.path.join(os.pardir, os.pardir)
    default_wsdl_file = os.path.join(pytan_root, "doc", "console.wsdl")
    default_output_file = os.path.join(pytan_root, "pytan", "tanium_ng.py")

    parser = utils.ShellParser(my_file=my_file, description=__doc__)
    parser.add_argument(
        '-i', '--input',
        required=False, action='store', dest='input', default=default_wsdl_file,
        help='Tanium Server console.wsdl file to generate tanium_ng from',
    )
    parser.add_argument(
        '-o', '--output',
        required=False, action='store', dest='output', default=default_output_file,
        help='File to create tanium_ng as',
    )
    parser.add_argument(
        '-r', '--run',
        required=False, action='store_true', dest='run', default=False,
        help='Actually generate the tanium_ng file instead of just previewing the changes',
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

type_name = 'sensor'
find_tpl = ".//xsd:complexType[@name='{}']/xsd:annotation/xsd:appinfo/".format(type_name)
x = wsdl_parser.search_wsdl(find_tpl)
