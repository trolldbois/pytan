#!/usr/bin/python -i
#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Tanium Python Wrapper Class

Like saran wrap. But not.

This requires Python 2.7

Reference for Tanium's SOAP API: http://kb.tanium.com/SOAP
"""
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.1'

# static variable for how many minutes a session id will be valid
SESSION_TIMEOUT = 5

# static variable to control whether or not SOAP Session IDs are included
# in any outputs
SHOW_SESSION_ID = False

import os
import sys
import logging
import getpass
import traceback
import socket
import time
import csv
import StringIO
import re
import json
from datetime import datetime
from collections import defaultdict
import xml.etree.cElementTree as ET

# ElementTree FUN!
NS_SOAP_ENV = "http://schemas.xmlsoap.org/soap/envelope/"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
NS_XSD = "http://www.w3.org/2001/XMLSchema"
NS_DICT = {"xmlns:xsi": NS_XSI, "xmlns:xsd": NS_XSD}
APP_NS = {'xmlns': "urn:TaniumSOAP"}

# make it so ElementTree produces Elements with soap: prefix instead of ns0:
ET.register_namespace('soap', NS_SOAP_ENV)
for attr, uri in NS_DICT.items():
    ET.register_namespace(attr.split(":")[1], uri)

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
path_adds = [my_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.insert(0, x)

# for debugging support
from console_support import *
import requests

# disable warning messages about insecure HTTPS validation
requests.packages.urllib3.disable_warnings()

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

# debug log format; rather verbose, used for files only unless loglevel >= 1
lfdebug = logging.Formatter(
    '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
    '%(levelname)-8s %(message)s'
)

# info log format; used for console output when loglevel = 0
lfinfo = logging.Formatter('%(levelname)-8s %(message)s')

# create a logger called apiwrap and set it's default level to DEBUG
logger = logging.getLogger("apiwrap")
logger.setLevel(logging.DEBUG)

# create a logger called httplogger and set it's default level to DEBUG
# use httplog to send messages to this logger at the debug level
httplogger = logging.getLogger("http")
httplogger.setLevel(logging.DEBUG)
httplog = httplogger.debug

# create a logger called xmlcreatelogger and set it's default level to DEBUG
# use xmlcreatelog to send messages to this logger at the debug level
xmlcreatelogger = logging.getLogger("xmlcreate")
xmlcreatelogger.setLevel(logging.DEBUG)
xmlcreatelog = xmlcreatelogger.debug

# create a logger called xmlparselogger and set it's default level to DEBUG
# use xmlparselog to send messages to this logger at the debug level
xmlparselogger = logging.getLogger("xmlparse")
xmlparselogger.setLevel(logging.DEBUG)
xmlparselog = xmlparselogger.debug


def version_check(reqver):
    """for scripts using this API to validate the version of the API

    :param reqver: string containing version number to check against
    """
    LOG_TPL = (
        "{}: {} version {}, required {}").format
    if not __version__ >= reqver:
        s = "Script and API Version mismatch!"
        logging.error(LOG_TPL(s, __file__, __version__, reqver))
        sys.exit(100)
    s = "Script and API Version match"
    logging.debug(LOG_TPL(s, __file__, __version__, reqver))


def logging_setup(loglevel=0):
    """setup console logging
    """
    # remove any old handlers, we're going to re-setup new handlers
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers
    [root_logger.removeHandler(x) for x in original_handlers]

    # add a console handler that goes to STDOUT
    console_handler = logging.StreamHandler(sys.__stdout__)
    console_handler.set_name('console')
    if loglevel == 0:
        # if loglevel is 0, set console handler to info level
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(lfinfo)
    else:
        # if loglevel is 1 or higher, set console handler to debug level
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(lfdebug)
    root_logger.addHandler(console_handler)

    log_level_map = {
        # level 1 just turns on debug logging
        # see more details about http communications at lvl 2
        'http': 2,
        # see the XML messages we create at lvl 3
        'xmlcreate': 3,
        # see the XML messages we parse at lvl 4
        'xmlparse': 4,
    }

    for loggername, loggerlvl in log_level_map.iteritems():
        if loglevel >= loggerlvl:
            #print 'setting %s to DEBUG' % loggername
            logging.getLogger(loggername).setLevel(logging.DEBUG)
        else:
            #print 'setting %s to INFO' % loggername
            logging.getLogger(loggername).setLevel(logging.INFO)


def get_caller_method():
    stack = traceback.extract_stack()
    # for x, y in enumerate(stack):
        # print x, y
    caller_stack = stack[-3]
    caller_method = caller_stack[2]
    return caller_method


def get_now():
    """return current time in human friendly format

    :return: :class:`str`
    """
    return human_time(time.localtime())


def human_time(t, format='%Y_%m_%d-%H_%M_%S-%Z'):
    """return time in human friendly format

    :param t: either a epoch or struct_time time object
    :param format: strftime format string
    :return: :class:`str`
    """
    if type(t) in [type(float()), type(int())]:
        t = time.localtime(t)
    return time.strftime(format, t)


def datetime_diff(t=False):
    """Get the dtdiff of now - time

    :param t: either a epoch or datatime object
    :return: :class:`datatime.timedelta`
    """
    now = datetime.now()

    if type(t) in [type(int()), type(float())]:
        dtdiff = now - datetime.fromtimestamp(t)
    elif isinstance(t, datetime):
        dtdiff = now - t
    else:
        dtdiff = now - now

    #second_dtdiff = dtdiff.seconds
    #minute_dtdiff = dtdiff.seconds / 60
    #hour_dtdiff = minute_dtdiff / 60
    #day_dtdiff = dtdiff.days
    return dtdiff


def port_check(address, port, timeout=5):
    """Check if address:port can be reached within timeout

    :param address: string of host to connect to
    :param port: string of port to connect to
    :param timeout: int of seconds to wait until connection fails

    :return: :class:`bool`
    """
    try:
        return socket.create_connection((address, port), timeout)
    except:
        return False


def prompt_username():
    """for scripts using this API to prompt the user for a username

    :return: :class:`str`
    """
    print('Username: '),
    username = sys.stdin.readline()
    return username.strip()


def prompt_password():
    """for scripts using this API to prompt the user for a password

    :return: :class:`str`
    """
    password = getpass.getpass(('Password: '))
    return password.strip()


def ns_urn(ns):
    """return a string wrapped by {}

    :param ns: string to surround by {}
    :return: :class:`str`
    """
    return ('{{{}}}').format(ns)


def ns_prefix(elem, ns):
    """return an element name with a proper {} wrapped namespace prefixed

    :param elem: string of element name to prefix with namespace
    :param ns: string of namespace to prefix to the element name
    :return: :class:`str`
    """
    return ('{}{}').format(ns_urn(ns), elem)


def new_elem(name, value=None, ns=None, attribs=None, parent=None):
    """Create a new XML element

    :param name: string of element to create
    :param value: string of value to set for element, optional
    :param ns: string of namespace to prefix to element, optional
    :param attribs: dict of additional attributes to set on element, optional
    :param parent: ElementTree.Element to create new element under, optional
    :return: :class:`ElementTree.Element` or :class:`ElementTree.SubElement`
    """
    CREATE1_TPL = ("Creating new Element {!r} with attribs {}").format
    CREATE2_TPL = (
        "Creating new Sub Element {!r} under {!r} with attribs {}"
    ).format
    VALUE_TPL = ("Setting Element {!r} value to {!r}").format
    if ns:
        name = ns_prefix(name, ns)
    if attribs is None:
        attribs = {}
    if parent is None:
        xmlcreatelog(CREATE1_TPL(name, attribs))
        elem = ET.Element(name, **attribs)
    else:
        xmlcreatelog(CREATE2_TPL(name, parent.tag, attribs))
        elem = ET.SubElement(parent, name, **attribs)
    if value:
        xmlcreatelog(VALUE_TPL(name, value))
        elem.text = str(value)
    return elem


def xml_indent(elem, level=0):
    """indents an ElementTree object for pretty printing

    :param elem: ElementTree.Element to indent
    :param level: int for indentation level, used for recursion
    :return: :class:`ElementTree.Element`
    """
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            xml_indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    return elem


def xml_clean_ns(elem):
    """removes all namespace qualifiers from ElementTree object

    :param elem: ElementTree.Element to remove namespaces from
    :return: :class:`ElementTree.Element`
    """
    ns_match = re.compile(r'{.*?}')

    for child_elem in elem.getiterator():
        child_elem.tag = re.sub(ns_match, '', child_elem.tag)
        for k in child_elem.attrib.keys():
            if ns_match.search(k):
                del child_elem.attrib[k]
    return elem


def xml_tree(elem):
    """returns the elem object as an ElementTree object

    :param elem: ElementTree.Element or string containing raw XML
    :return: :class:`ElementTree.Element`
    """
    if not ET.iselement(elem):
        elem = ET.fromstring(elem)
    return elem


def xml_pretty(elem):
    """returns the xml for ElementTree object as pretty XML
    string

    :param elem: ElementTree.Element or string containing raw XML
    :return: :class:`str`
    """
    elem = xml_tree(elem)
    elem = xml_indent(elem)
    xml_pretty = ET.tostring(elem)
    return xml_pretty


def gather_keys(obj):
    keys = []
    [keys.append(k) for d in obj for k in d.keys() if k not in keys]
    return keys


def sort_keys(keys, key_priority=None):
    sorted_keys = sorted(keys)
    if key_priority:
        priority_sorted_keys = []
        for kp in key_priority:
            for kidx, k in enumerate(sorted_keys):
                if k.endswith(kp):
                    priority_sorted_keys.append(sorted_keys.pop(kidx))
        priority_sorted_keys += sorted_keys
        return priority_sorted_keys
    else:
        return sorted_keys


def xml_csv(xml_rows_list, header_priority=None):
    """returns the xml for the response as a CSV string"""
    if not xml_rows_list:
        return None
    if type(xml_rows_list) not in [tuple, list]:
        return None
    csv_io = StringIO.StringIO()
    if type(xml_rows_list[0]) in [tuple, list]:
        headers = xml_rows_list.pop(0)
        writer = csv.writer(csv_io, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        writer.writerows(xml_rows_list)
    elif type(xml_rows_list[0]) in [dict]:
        headers = gather_keys(xml_rows_list)
        headers = sort_keys(headers, header_priority)
        writer = csv.DictWriter(
            csv_io, fieldnames=headers, quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writerow(dict((h, h) for h in headers))
        writer.writerows(xml_rows_list)
    else:
        return None
    xml_csv = csv_io.getvalue()
    return xml_csv


def build_dict_from_xml(elem):
    """converts an ElementTree object to a python dict

    :param elem: ElementTree.Element or string containing raw XML
    :return: :class:`dict`
    """
    elem = xml_tree(elem)
    d = {elem.tag: {} if elem.attrib else None}
    #print d
    children = list(elem)
    if children:
        #print 'in children: ', children
        dd = defaultdict(list)
        for dc in map(build_dict_from_xml, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {
            elem.tag: {
                k: v[0] if len(v) == 1 else v for k, v in dd.iteritems()
            }
        }
    if elem.attrib:
        #print 'in elem.attrib: ', elem.attrib
        d[elem.tag].update(('@' + k, v) for k, v in elem.attrib.iteritems())
    if elem.text:
        #print 'in elem.text: ', elem.text
        #print type(elem.text)
        text = elem.text.strip()
        try:
            # sometimes the text of an element is JSON. cool.
            text = json.loads(text)
        except:
            pass
        if children or elem.attrib:
            if text:
                d[elem.tag]['#text'] = text
        else:
            d[elem.tag] = text
    return d


def build_xml_from_dict(parentelem, xml_dict):
    """converts a python dict into an ElementTree.Element object under
    parentelem

    :param parentelem: ElementTree.Element object to create new elements in
        xml_dict under
    :param xml_dict: dict containing info about elements to create
    :return: :class:`ElementTree.Element`
    """
    DICT_TPL = (
        "dict found: creating element {!r} under {!r} with children {}"
    ).format
    LIST_TPL = (
        "list found: creating element {!r} under {!r} with children {}"
    ).format
    STR_TPL = (
        "str found: creating elemnt {!r} under {!r} with value {!r}"
    ).format

    for objname, objvalue in xml_dict.iteritems():
        if type(objvalue) == dict:
            xmlcreatelog(DICT_TPL(objname, parentelem.tag, objvalue))
            objelem = new_elem(objname, parent=parentelem)
            objelem = build_xml_from_dict(objelem, objvalue)
        elif type(objvalue) in [tuple, list]:
            for x in objvalue:
                xmlcreatelog(LIST_TPL(objname, parentelem.tag, x))
                objelem = new_elem(objname, parent=parentelem)
                objelem = build_xml_from_dict(objelem, x)
        else:
            xmlcreatelog(STR_TPL(objname, parentelem.tag, objvalue))
            objelem = new_elem(objname, objvalue, parent=parentelem)
    return parentelem


def flatten_obj(fullobj, prefix=None):
    flat = {}
    #print fullobj, prefix
    if type(fullobj) == dict:
        for k, v in fullobj.iteritems():
            if prefix:
                k = ('{}.{}').format(prefix, k)
            if type(v) == dict:
                #print 'dict found: ', k, v
                flat.update(flatten_obj(v, k))
            elif type(v) in [list, tuple]:
                #print 'list found: ', k, v
                for idx, item in enumerate(v):
                    itempre = ('{}{}').format(k, idx)
                    flat.update(flatten_obj(item, itempre))
            else:
                #print 'other found: ', k, v
                if v and type(v) == str:
                    v = v.replace('\n', '\r\n')
                flat[k] = v
    elif type(fullobj) in [list, tuple]:
        flat[prefix] = ", ".join(fullobj)
    else:
        flat[prefix] = fullobj
    return flat


def parse_result_object(result_object, multi, single):
    """
    example breakdown of result_object for GetObject on sensor:

    single sensor return:
    dict:result_object:
        dict:sensor:
            dict:sensor_details:

    multiple sensors return:
    dict:result_object:
        list:sensor:
            dict:sensor_details:

    all sensors return:
    dict:result_object:
        dict:sensors:
            list:sensor:
                dict:sensor_details:
    """
    items = []
    if single in result_object:
        if type(result_object[single]) in [list, tuple]:
            for item in result_object[single]:
                items.append(flatten_obj(item, prefix=single))
        else:
            items.append(flatten_obj(result_object[single], prefix=single))
    elif multi in result_object:
        multi_list = result_object[multi]
        for item in multi_list[single]:
            items.append(flatten_obj(item, prefix=single))
    return items


def parse_query_args(args, prefixes):
    p = None
    if type(args) == str:
        p_done = False
        for prefix in prefixes:
            if args.startswith(prefix + ':'):
                p_done = True
                p = {prefix: args.lstrip(prefix + ':')}
        if not p_done:
            p = {prefixes[0]: args}
        return p
    elif type(args) in [tuple, list]:
        parsed_args = []
        for i in args:
            parsed_arg = parse_query_args(i, prefixes)
            if parsed_arg:
                parsed_args.append(parsed_arg)
        return parsed_args
    return {}


def check_single_query(query):
    ERR_TPL = (
        "Too many list items!! string or list with single string required, "
        "you passed in {}"
    ).format

    if type(query) in [list, tuple]:
        if len(query) != 1:
            logger.error(ERR_TPL(query))
            return False
    return True


class SoapRequest(object):
    def __init__(self, **kwargs):
        """handles the creation of XML for a SOAP request

        :param auth_dict: dict of authorization info to include in XML
        :param command: string to set command XML element to
        :param objects_dict: dict of objects to include in object_list element
        """
        super(SoapRequest, self).__init__()
        self.__generals(**kwargs)
        try:
            self.caller_method = get_caller_method()
        except:
            self.caller_method = self.command

    def __generals(self, **kwargs):
        self.xml_raw = ''
        # throw an exception if auth_dict not passed in to kwargs
        self.auth_dict = kwargs['auth_dict']

        # throw an exception if object_typ not passed in to kwargs
        self.object_type = kwargs['object_type']

        # optionally get the values for a single object and multiple object
        # types from kwargs
        self._single = kwargs.get('object_single') or self.object_type
        self._multi = kwargs.get('object_multi') or '%ss' % self.object_type

        # optionally get command from kwargs
        self.command = kwargs.get('command')

        # for sorting the xml result
        self.header_priority = []

        self.overrides(**kwargs)

        # build self.objects_dict
        self.__get_objects_dict(**kwargs)

        self.header_priority = [
            '%s.%s' % (self.object_type, x) for x in self.header_priority
        ]

    def __get_objects_dict(self, **kwargs):
        # get either objects_dict from kwargs, or build objects_dict from
        # query_type and query in kwargs
        if not hasattr(self, 'objects_dict'):
            self.objects_dict = kwargs.get('objects_dict')
        if not self.objects_dict:
            # throw an exception if auth_dict not passed in to kwargs
            query_objects = kwargs['query']
            # turn id:value/name:value/hash:value in kwargs['query']
            # to a dictionary {prefix: value}
            arg_prefixes = kwargs.get('arg_prefixes') or ['name', 'id', 'hash']
            parsed_query_objects = parse_query_args(
                query_objects, arg_prefixes,
            )
            self.objects_dict = {self.object_type: parsed_query_objects}

    def overrides(self, **kwargs):
        # these should be over-ridden by a subclass
        # sub classed
        # for sorting the xml result
        self.header_priority = []

    def __str__(self):
        STR_TPL = (
            "{} for {!r} of {!r}, Sent: {}, Auth: {}"
        ).format
        sent = self.sent_human or "Not Yet Sent"
        ret = STR_TPL(
            self.__class__.__name__,
            self.caller_method,
            self.objects_dict,
            sent,
            self.auth_type,
        )
        return ret

    def build_xml(self):
        """builds the xml envelope needed for a SOAP request

        self.command should be a valid SOAP command, i.e. the following:
          GetObject
          GetResultData

        self.auth_dict should be one of the following:
          # session id based auth
          {'session': '$SESSION_ID'}
          # username/password based auth
          {'auth': {'username': '$USERNAME', 'password': '$PASSWORD'}}

        self.objects_dict should be something like one of the following:
          # get a single sensor
          {'sensor': {'name': 'Computer Name'}}
          {'sensor': {'id': '65'}}
          {'sensor': {'hash': '2940242'}}

          # get all sensors
          {'sensor': {'name': ''}}
        """
        DBG_TPL = ('Created XML:\n{}').format
        xmltree = new_elem('Envelope', ns=NS_SOAP_ENV, attribs=NS_DICT)
        body_elem = new_elem('Body', ns=NS_SOAP_ENV, parent=xmltree)
        soap_req_elem = new_elem(
            'tanium_soap_request', parent=body_elem, attribs=APP_NS,
        )
        build_xml_from_dict(soap_req_elem, self.auth_dict)
        new_elem('command', self.command, parent=soap_req_elem)
        objlist_elem = new_elem('object_list', parent=soap_req_elem)
        build_xml_from_dict(objlist_elem, self.objects_dict)
        new_elem('ID', '0', parent=soap_req_elem)
        new_elem('ContextID', '0', parent=soap_req_elem)
        self.xmltree = xmltree
        self.xml_raw = xml_pretty(xmltree)
        xmlcreatelog(DBG_TPL(self.xml_raw))
        return self.xml_raw

    def csv_pre(self, inner_dict_xml):
        """returns the xml for the response as a list of lists or dicts

        needs to be overriden by each sub-class to handle the results specifc
        to that request

        pre_csv should return one of the following:
            * a list of lists, each sub list mapping to a row in CSV, with
            headers in the first sub list
            * a list of dicts, each sub dict mapping to a row in CSV, with
            the headers being extracted from the sub-dict keys
        """
        pre_csv = None
        return pre_csv

    @property
    def auth_type(self):
        """returns the auth type of self.auth_dict"""
        auth_type = "Undefined"
        if not hasattr(self, 'auth_dict'):
            return auth_type

        keys = self.auth_dict.keys()
        if 'auth' in keys:
            auth_type = 'user/pass'
        elif 'session' in keys:
            auth_type = 'session'
        return auth_type

    @property
    def sent_human(self):
        """returns the time the request was sent in human friendly format"""
        if not hasattr(self, '_sent'):
            return None
        return human_time(self._sent)

    @property
    def sent(self):
        """returns the time the request was sent"""
        if not hasattr(self, '_sent'):
            return None
        return self._sent

    @sent.setter
    def sent(self, value):
        """sets the time the request was sent"""
        self._sent = value


class AskSavedQuestionRequest(SoapRequest):
    def overrides(self, **kwargs):
        self.command = 'GetResultData'
        # for sorting the xml result
        self.header_priority = []

    def csv_pre(self, inner_dict_xml):
        """returns the inner_dict_xml for the response as a list of lists, one
        for each row, headers in the first row
        """
        # TODO: MAKE THIS DICT LIKE INSTEAD OF ROW LIKE
        result_sets = inner_dict_xml.get('result_sets', {})
        result_set = result_sets.get('result_set', {})

        # get headers from xml response result_set
        cs = result_set.get('cs', {})
        xml_headers = cs.get('c', [])

        # extract the name for the header of each column
        headers = [dict_get(x, 'dn') for x in xml_headers]

        # get rows from xml response result_set
        rs = result_set.get('rs', {})
        r = rs.get('r', [])
        xml_rows = [x.get('c', []) for x in r]

        # extract the row values for each column
        pre_csv = [
            [dict_get(y, 'v') for y in x] for x in xml_rows
        ]

        # prepend headers to rows
        pre_csv.insert(0, headers)
        return pre_csv


class GetObjectRequest(SoapRequest):
    def overrides(self, **kwargs):
        self.command = 'GetObject'
        # for sorting the xml result
        self.header_priority = [
            'name',
            'id',
            'description',
            'hash',
            'value_type',
        ]

    def csv_pre(self, inner_dict_xml):
        """returns the result_object for the response as a list of dicts, one
        for each row
        """
        if not inner_dict_xml:
            return None
        pre_csv = parse_result_object(
            inner_dict_xml, self._multi, self._single,
        )
        return pre_csv


class ParseQuestionRequest(SoapRequest):
    def overrides(self, **kwargs):
        self.command = 'AddObject'
        self.objects_dict = {
            'parse_job': {'question_text': kwargs['question_request']}
        }


def dict_get(d, k, v='', e='utf-8'):
    v = d.get(k, v)
    if type(v) in [unicode, str]:
        v = v.encode(e)
    return v


class QuestionResults(SoapRequest):
    def overrides(self, **kwargs):
        self.command = 'GetResultData'
        self.objects_dict = {
            'question': {'id': kwargs['question_id']}
        }

    def csv_pre(self, inner_dict_xml):
        """returns the ResultXML_dict for the response as a list of lists, one
        for each row, headers in the first row
        """
        result_sets = inner_dict_xml.get('result_sets', {})
        result_set = result_sets.get('result_set', {})

        # get headers from xml response result_set
        cs = result_set.get('cs', {})
        xml_headers = cs.get('c', [])

        # extract the name for the header of each column
        headers = [dict_get(x, 'dn') for x in xml_headers]

        # get rows from xml response result_set
        rs = result_set.get('rs', {})
        r = rs.get('r', [])
        xml_rows = [x.get('c', []) for x in r]

        # extract the row values for each column
        pre_csv = [
            [dict_get(y, 'v') for y in x] for x in xml_rows
        ]

        # prepend headers to rows
        pre_csv.insert(0, headers)
        return pre_csv


class AskParseQuestionRequest(SoapRequest):
    def overrides(self, **kwargs):
        self.command = 'AddObject'
        self.objects_dict = {
            'parse_result_group': kwargs['parse_result_group'],
        }


class SoapResponse(object):

    def __init__(self, soap_url, request, http_response):
        super(SoapResponse, self).__init__()
        self.received = time.time()

        # URL to SOAP in question
        self.soap_url = soap_url

        # request = SoapRequest object
        self.request = request

        # http_response = requests module object
        self.http_response = http_response

        self.response_ok = self.check_response_ok()

        self.outer_dict_xml = self.get_outer_xml()
        self.outer_return = self.get_outer_return()

        self.command = self.get_command()
        self.auth_ok = self.check_auth_ok()
        self.command_ok = self.check_command_ok()

        self.everything_ok = self.check_everything_ok()

        self.session_id = self.get_session_id()
        self.inner_dict_xml = self.get_inner_xml()
        self.pre_csv = self.consume_inner_xml()
        self.csv = self.get_csv()

    def __str__(self):
        received = self.received_human or "Not Yet Sent"
        STR_TPL = (
            "SoapResponse from {}, len: {}, code {} on: {}, SoapRequest: {}"
        ).format
        ret = STR_TPL(
            self.soap_url,
            len(self.http_response.text),
            self.http_response.status_code,
            received,
            self.request,
        )
        return ret

    def get_outer_xml(self, **kwargs):
        """chew up the raw text from the http_response into XML"""
        NOTEXT_TPL = ("No text converted from HTTP response: {}").format
        OUTER_XML = ('Parsed XML:\n{}').format
        OUTER_ERR = ("Exception while converting outer XML: {}").format
        outer_dict_xml = None

        text = kwargs.get('text') or self.http_response.text
        response_ok = kwargs.get('response_ok') or self.response_ok

        if response_ok:
            text = text.encode('utf-8')

            if not text:
                logger.error(NOTEXT_TPL(self.http_response.text))
            else:
                try:
                    outer_elem_xml = xml_tree(text)
                    outer_elem_xml = xml_clean_ns(outer_elem_xml)
                    outer_raw_xml = xml_pretty(outer_elem_xml)
                    outer_dict_xml = build_dict_from_xml(outer_elem_xml)
                    xmlparselog(OUTER_XML(outer_raw_xml))
                except Exception as e:
                    logger.error(OUTER_ERR(e))

        self.outer_dict_xml = outer_dict_xml
        return outer_dict_xml

    def get_outer_return(self, **kwargs):
        OUTER_ERR = ("Exception while parsing outer XML: {}").format
        outer_return = None
        outer_dict_xml = kwargs.get('outer_dict_xml') or self.outer_dict_xml
        response_ok = kwargs.get('response_ok') or self.response_ok

        if response_ok:
            try:
                outer_envelope = outer_dict_xml['Envelope']
                outer_body = outer_envelope['Body']
                outer_return = outer_body['return']
            except Exception as e:
                logger.error(OUTER_ERR(e))

        self.outer_return = outer_return
        return outer_return

    def get_command(self, **kwargs):
        command = None
        outer_return = kwargs.get('outer_return') or self.outer_return
        response_ok = kwargs.get('response_ok') or self.response_ok

        if response_ok:
            command = outer_return.get('command')
        self.command = command
        return command

    def check_everything_ok(self, **kwargs):
        auth_ok = kwargs.get('auth_ok') or self.auth_ok
        response_ok = kwargs.get('response_ok') or self.response_ok
        command_ok = kwargs.get('command_ok') or self.command_ok
        everything_ok = auth_ok and response_ok and command_ok
        self.everything_ok = everything_ok
        return everything_ok

    def check_auth_ok(self, **kwargs):
        AUTH_ERR = ("Authorization failure in {} (COMMAND: {!r})").format
        command = kwargs.get('command') or self.command
        auth_ok = 'Forbidden' not in command
        if not auth_ok:
            logger.debug(AUTH_ERR(self, command))
        self.auth_ok = auth_ok
        return auth_ok

    def check_response_ok(self, **kwargs):
        NON_200 = ("Non 200 status code in {} (CODE: {!r})").format
        http_response = kwargs.get('http_response') or self.http_response
        valid_codes = [200]
        response_ok = http_response.status_code in valid_codes
        if not response_ok:
            logger.error(NON_200(http_response.status_code, self))
        self.response_ok = response_ok
        return response_ok

    def check_command_ok(self, **kwargs):
        BAD_ERR = ("Bad Command Return in {} (COMMAND: {!r})").format
        command = kwargs.get('command') or self.command
        command_ok = 'Bad Request' not in command
        if not command_ok:
            command = command.replace('\n', '')
            logger.error(BAD_ERR(self, command))
        self.command_ok = command_ok
        return command_ok

    def get_session_id(self, **kwargs):
        session_id = None
        outer_return = kwargs.get('outer_return') or self.outer_return
        everything_ok = kwargs.get('everything_ok') or self.everything_ok
        if everything_ok is True:
            session_id = outer_return['session']

        self.session_id = session_id
        return session_id

    def get_inner_xml(self, **kwargs):
        XML_TPL = ('Inner ResultXML:\n{}').format
        XML_ERR = ("Exception getting inner ResultXML: {}").format
        OBJ_ERR = ("Exception getting inner result_object: {}").format

        inner_dict_xml = None
        result_xml_commands = ['GetResultData', 'GetResultInfo']
        result_obj_commands = ['GetObject', 'AddObject', 'DeleteObject']

        command = kwargs.get('command') or self.command
        outer_return = kwargs.get('outer_return') or self.outer_return
        everything_ok = kwargs.get('everything_ok') or self.everything_ok

        if everything_ok is True:
            if command in result_xml_commands:
                try:
                    inner_raw_xml = outer_return['ResultXML']
                    inner_raw_xml = inner_raw_xml.encode('utf-8')
                    inner_elem_xml = xml_tree(inner_raw_xml)
                    inner_elem_xml = xml_clean_ns(inner_elem_xml)
                    inner_raw_xml = xml_pretty(inner_elem_xml)
                    inner_dict_xml = build_dict_from_xml(inner_elem_xml)
                    xmlparselog(XML_TPL(inner_raw_xml))
                except Exception as e:
                    logger.error(XML_ERR(e))
            elif command in result_obj_commands:
                try:
                    inner_dict_xml = outer_return['result_object']
                except Exception as e:
                    logger.error(OBJ_ERR(e))

        self.inner_dict_xml = inner_dict_xml
        return inner_dict_xml

    def consume_inner_xml(self, **kwargs):
        everything_ok = kwargs.get('everything_ok') or self.everything_ok
        pre_csv = None
        if everything_ok:
            inner_dict_xml = kwargs.get('inner_dict_xml')
            if not inner_dict_xml:
                inner_dict_xml = self.inner_dict_xml
            pre_csv = self.request.csv_pre(inner_dict_xml)
        self.pre_csv = pre_csv
        return pre_csv

    def get_csv(self, **kwargs):
        # grab the pre_csv into an actual csv and store it in csv
        everything_ok = kwargs.get('everything_ok') or self.everything_ok
        pre_csv = kwargs.get('pre_csv') or self.pre_csv
        csv = None
        if everything_ok:
            header_priority = kwargs.get('header_priority')
            if not header_priority:
                header_priority = getattr(
                    self.request, 'header_priority', None,
                )
            csv = xml_csv(pre_csv, header_priority)
        self.csv = csv
        return csv

    def write_csv_file(self, filename=None, dir=None, **kwargs):
        WRITE_TPL = ("Writing CSV to file: {}").format
        NO_CSV_TPL = ("No CSV exists for: {}").format
        csv = kwargs.get('csv') or self.csv
        csv_path = None

        if filename is None:
            filename = str(self.request.objects_dict)
            filename = filename.replace(': ', '.')
            filename = filename.translate(None, '\'{[]}')
            filename = filename.replace(' ', '_')
            filename = filename.replace(',', '+')
            filename = filename.replace('+_', '+')
            filename = filename[0:80]
            filename += '__'
            filename += get_now()
            filename += ".csv"
            filename = ("{}__{}").format(self.request.caller_method, filename)

        if dir is None:
            dir = os.path.curdir

        if csv is None:
            logger.error(NO_CSV_TPL(self))
        else:
            csv_path = os.path.join(dir, filename)
            logger.debug(WRITE_TPL(csv_path))
            x = open(csv_path, 'w+')
            x.write(csv)
            x.close()

        self.csv_path = csv_path
        return csv_path

    @property
    def received_human(self):
        """returns the time the response was received in human friendly format
        """
        return human_time(self.received)


class SoapAuth(object):
    def __init__(self, username, password):
        super(SoapAuth, self).__init__()
        self._username = username
        self._password = password
        self._session_id = None
        self._token = {}
        self.SESSION_TIMEOUT = SESSION_TIMEOUT
        self.SHOW_SESSION_ID = SHOW_SESSION_ID
        self.update_token()

    def __str__(self):
        STR_TPL = (
            "SoapAuth {}"
        ).format
        ret = STR_TPL(self.token_type_details)
        return ret

    def update_token(self):
        """updates self.token with either session ID or user/pass auth"""
        UPD_TPL = ("SOAP Token updated to: {}").format
        if self.session_id_valid:
            token = self.token_session_id
        else:
            token = self.token_userpass
        if self._token != token:
            self._token = token
            logger.debug(UPD_TPL(self.token_type_details))

    def auth_fallback(self):
        """removes the session ID from the token, and reverts back to
        user and password auth"""
        self.session_id = None
        self.update_token()

    def session_id_text(self, session_id):
        """returns session ID if SHOW_SESSION_ID = True"""
        if self.SHOW_SESSION_ID:
            id_text = session_id
        else:
            id_text = "..."
        return id_text

    @property
    def token(self):
        """returns the token"""
        if not hasattr(self, '_token'):
            return None
        return self._token

    @token.setter
    def token(self, value):
        """sets the token"""
        self._token = value

    @property
    def session_id(self):
        """returns the session_id"""
        if not hasattr(self, '_session_id'):
            return None
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        """sets the session_id"""
        if self._session_id != value:
            self._session_id = value
            self._session_id_issued = time.time()
            self.update_token()

        if value is None:
            self._session_id_issued = None

    @property
    def session_id_issued(self):
        """returns the session_id_issued"""
        if not hasattr(self, '_session_id_issued'):
            return None
        return self._session_id_issued

    @session_id_issued.setter
    def session_id_issued(self, value):
        """sets the session_id_issued"""
        self._session_id_issued = value

    @property
    def session_id_valid(self):
        """returns True if self.session_id is not empty and not yet expired,
        False otherwise - expiration is validated by looking at
        self.session_id_issued
        """
        SESSION_TPL = (
            "Session ID {}: issued {}, minutes ago: {}, timeout: {} minutes"
        ).format

        if not self.session_id:
            return False

        dtdiff = datetime_diff(self.session_id_issued)
        minutes_dtdiff = dtdiff.seconds / 60
        hf_issued = human_time(self.session_id_issued)

        if self.SESSION_TIMEOUT < minutes_dtdiff:
            logger.debug(SESSION_TPL(
                'EXPIRED', hf_issued, minutes_dtdiff, self.SESSION_TIMEOUT,
            ))
            self._session_id = None
            self._session_id_issued = None
            return False

        logger.debug(SESSION_TPL(
            'VALID', hf_issued, minutes_dtdiff, self.SESSION_TIMEOUT,
        ))
        return True

    @property
    def via_session_id(self):
        """returns True if self.token dict has 'session' in it"""
        return 'session' in self._token.keys()

    @property
    def via_userpass(self):
        """returns True if token dict has 'auth' in it"""
        return 'auth' in self._token.keys()

    @property
    def token_type_details(self):
        """returns token type and details in text form"""
        TOK_TPL = ('auth type: {} [{}: "{}"]').format
        token_details = "NONE"
        token_type = "UNKNOWN"
        if self.via_session_id:
            token_predetails = 'ID'
            token_details = self.session_id_text(self._token.get('session'))
            token_type = 'session ID'
        elif self.via_userpass:
            token_predetails = 'username'
            token_details = self._token.get('auth').get('username')
            token_type = 'username/password'
        else:
            token_predetails = 'None'
            token_details = 'None'
            token_type = 'Not yet set'

        token_type_details = TOK_TPL(
            token_type, token_predetails, token_details
        )
        return token_type_details

    @property
    def token_userpass(self):
        """returns a dictionary that has 'auth': SOAP element: auth,
        $username, $password
        """
        token = {
            'auth': {'username': self._username, 'password': self._password}
        }
        return token

    @property
    def token_session_id(self):
        """returns a dictionary that has 'session': '$session_id' """
        token = {'session': self.session_id}
        return token


class FailedPage(requests.Request):
    """simple object to replicate requests-like object for exceptions"""
    def __init__(self, text):
        self.text = text
        self.status_code = -1


class SoapWrap:
    def __init__(self, username, password, host, port="443", protocol='https',
                 soap_path="/soap", loglevel=0, logfile=None,):

        logging_setup(loglevel)

        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__soap_path = soap_path

        self.__username = username
        self.__password = password

        self.last_request = None
        self.last_response = None
        self.all_responses = []

        self.__env_overrides()
        self.__app_ok()
        self.auth = SoapAuth(self.__username, self.__password)

    def __str__(self):
        STR_TPL = (
            "SoapWrap to {}, Healthy: {}"
        ).format
        ret = STR_TPL(self.soap_url, self.app_ok)
        return ret

    def __env_overrides(self):
        """looks for OS environment variables and overrides the corresponding
        attribute if they exist"""
        OR_TPL = ("Overriding {!r} with OS environment variable {!r}").format
        OS_ENV_MAP = {
            'SOAP_USERNAME': 'self.__username',
            'SOAP_PASSWORD': 'self.__password',
            'SOAP_HOSTNAME': 'self.__host',
            'SOAP_PORT': 'self.__port',
            'SOAP_PROTOCOL': 'self.__protocol',
            'SOAP_PATH': 'self.__soap_path',
        }

        for os_env_var, class_var in OS_ENV_MAP.iteritems():
            if not os_env_var in os.environ.keys():
                continue

            if not os.environ[os_env_var]:
                continue

            logger.debug(OR_TPL(os.environ[os_env_var], os_env_var))
            setattr(self, class_var, os.environ[os_env_var])

    def __test_port(self):
        """validates that the SOAP port on the SOAP host can be reached"""
        CHK_TPL = ("Port test to {}:{} {}").format
        if port_check(self.__host, self.__port):
            return True
        else:
            logger.error(CHK_TPL(self.__host, self.__port, "FAILED"))
            return False

    def __test_page(self):
        """validates that the HTTP server is returning a valid response,
        will set self.app_version if so
        """
        CHK_TPL = ("HTTP test to {} {} {}").format
        ER1_TPL = ("Returned Code: {}, Returned Page:\n{}").format
        page = self.http_get(self.app_url)
        page_code = getattr(page, 'status_code', None)
        page_text = getattr(page, 'text', None)
        if not self.__page_ok(page):
            ERROR = ER1_TPL(page_code, page_text)
            logger.error(CHK_TPL(self.app_url, "FAILED", ERROR))
            return False
        self.app_version = self.__extract_version(page)
        if not self.app_version:
            return False
        return True

    def __extract_version(self, page):
        """extracts the serverVersion from the apps home page HTML"""
        ER2_TPL = ("Version info not found in applications home page").format
        version_regex = re.compile(r"flashvars.serverVersion.*'(.*)';")
        version_search = version_regex.search(page.text)
        if not version_search:
            logger.warn(ER2_TPL())
            return None
        if len(version_search.groups()) != 1:
            logger.warn(ER2_TPL())
            return None
        else:
            return version_search.groups()[0]

    def __page_ok(self, page):
        """return True if the page object is not None and has a status code
        of 200
        """
        valid_status = [200]
        if not page:
            return False
        if page.status_code not in valid_status:
            return False
        return True

    def __app_ok(self):
        """runs test_port and test_page"""
        OK_TPL = ("Application at {} is healthy, version: {}").format
        self.app_ok = True
        if not self.__test_port():
            self.app_ok = False
            return self.app_ok

        if not self.__test_page():
            self.app_ok = False
            return self.app_ok
        logger.debug(OK_TPL(self.soap_url, self.app_version))
        return self.app_ok

    def __call_api(self):
        """makes a call to the SOAP API, returns a SoapResponse object,
        expects a SoapRequest object to exist at self.request
        """
        AUTH_TPL = ('Authorization {} for last request: {}').format
        BAD_TPL = ('Bad SOAP request for last request: {}').format
        TIME_TPL = ('Last Request {} took longer than {} seconds!').format

        self.last_response = None

        if not self.app_ok:
            return self.last_response

        if self.last_request.command == "GetResultData":
            self.last_request.command = "GetResultInfo"

        orig_request_start = time.time()
        # get the SOAP response and store it in self.response
        self.__send_request()

        # if bad request, log it and return response
        if not self.last_response.response_ok:
            logger.error(BAD_TPL(self.last_request))
            return self.last_response

        # if auth failed and we are using a session ID, fallback to user/pass
        # and retry the request
        if not self.last_response.auth_ok and self.auth.via_session_id:
            logger.warn(
                "Last request failed due to expired/invalid session ID, "
                "retrying request with username/password"
            )
            self.auth.auth_fallback()
            self.__send_request()

        # if auth is STILL failed, even if request was re-issued,
        # log an auth failure
        if not self.last_response.auth_ok:
            logger.error(AUTH_TPL('FAILED', self.last_request))
            return self.last_response
        else:
            logger.debug(AUTH_TPL('SUCCESS', self.last_request))

        if self.last_request.command == "GetResultInfo":
            full_results = False
            wait = 1
            max_wait = 600
            current_wait = 1
            while full_results is not True:
                result_xml = self.last_response.inner_dict_xml
                result_infos = result_xml['result_infos']
                result_info = result_infos['result_info']
                logger.debug((
                    "GetResultInfo result_infos: {}"
                ).format(result_infos))
                mr_passed = result_info['mr_passed']
                est_total = result_info['estimated_total']
                if mr_passed == est_total:
                    full_results = True
                self.__send_request()
                current_wait += 1
                if current_wait > max_wait:
                    # TODO better message
                    raise Exception(TIME_TPL(self.last_request, max_wait))
                time.sleep(wait)

            self.last_request.command = "GetResultData"
            self.__send_request()
            self.last_request.sent = orig_request_start

        return self.last_response

    def __send_request(self):
        """sends the request to the SOAP API"""
        SEND_TPL = ("Sending {}, SOAP URL: {}").format
        RECV_TPL = ("Received {}, SOAP URL: {}").format

        # set token to user/pass or session ID accordingly
        self.auth.update_token()

        # update last_requests auth_dict with current token
        self.last_request.auth_dict = self.auth.token

        logger.debug(SEND_TPL(self.last_request, self.soap_url))

        # build the xml request for the last request
        request_xml = self.last_request.build_xml()

        # set sent time on last request
        self.last_request.sent = time.time()

        # send the request XML as a SOAP post
        http_response = self.soap_post(request_xml)

        # store the response in a SoapResponse object
        self.last_response = SoapResponse(
            soap_url=self.soap_url,
            request=self.last_request,
            http_response=http_response,
        )

        logger.debug(RECV_TPL(self.last_response, self.soap_url))

        # update auth token with last reponses session_id
        self.auth.session_id = self.last_response.session_id

        # append this response to all responses
        self.all_responses.append(self.last_response)

    @property
    def soap_url(self):
        """returns the SOAP URL"""
        SOAP_TPL = ("{}{}").format
        self._soap_url = SOAP_TPL(self.app_url, self.__soap_path)
        return self._soap_url

    @property
    def app_url(self):
        """returns the application URL"""
        APP_TPL = ("{}://{}:{}").format
        self._app_url = APP_TPL(self.__protocol, self.__host, self.__port)
        return self._app_url

    def ask_saved_question(self, query):
        """sends a saved question Request and returns the response

        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        if not check_single_query(query):
            return None

        request_args = {
            'object_type': 'saved_question',
            'query': query,
            'auth_dict': self.auth.token,
        }

        self.last_request = AskSavedQuestionRequest(**request_args)
        self.__call_api()
        return self.last_response

    def get_saved_question(self, query):
        """sends a get saved question request and returns a SoapResponse
        object
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'saved_question',
            'query': query,
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    def get_all_saved_questions(self):
        """sends a get all saved question request and returns a SoapResponse
        object
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'saved_question',
            'query': '',
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    def ask_question(self, question):
        """sends a question Request and returns the response

        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        # TODO DO ME
        # TODO SUPPORT FILTERS

        request_args = {
            'object_type': 'question',
            'query': query,
            'auth_dict': self.auth.token,
        }

        self.last_request = AskQuestionRequest(**request_args)
        self.__call_api()
        return self.last_response

    def parse_question(self, question):
        """sends a parse question Request and returns the response

        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        ERR1_TPL = ("No inner_dict_xml returned from last response").format
        ERR2_TPL = ("No parse results returned for {!r}").format
        DBUG1_TPL = (
            "No matching questions for {!r}, full list of questions: {}"
        ).format
        DBUG2_TPL = ("Matching parse_result for {!r}: {!r}").format

        request_args = {
            'object_type': 'question',
            'question_request': question,
            'auth_dict': self.auth.token,
        }

        self.last_request = ParseQuestionRequest(**request_args)
        self.__call_api()

        self.last_response.prg_match = None

        result_obj = getattr(self.last_response, 'inner_dict_xml', {})

        if not result_obj:
            logger.error(ERR1_TPL())
            return self.last_response

        prgs_all = result_obj.get('parse_result_groups', {})
        prgs_all = prgs_all.get('parse_result_group', [])
        self.last_response.prgs_all = prgs_all

        if not prgs_all:
            logger.error(ERR2_TPL(question))
            return self.last_response

        prg_match = [
            x for x in prgs_all
            if x['question_text'].lower() == question.lower()
        ]

        if not prg_match:
            logger.debug(DBUG1_TPL(
                question.lower(),
                [x['question_text'] for x in prgs_all],
            ))
            return self.last_response

        prg_match = prg_match[0]
        self.last_response.prg_match = prg_match
        logger.debug(DBUG2_TPL(question.lower(), prg_match))

        return self.last_response

    def ask_parsed_question(self, question, picker=None):
        PICK_TPL = (
            "Re-run this method with picker=$INDEX, where $INDEX is "
            "one of the following:"
        ).format
        PERR_TPL = (
            "Invalid picker index {}, re-run with picker=-1 to see picker "
            "index list"
        ).format

        self.parse_question(question)
        prg_match = getattr(self.last_response, 'prg_match', {})
        prgs_all = getattr(self.last_response, 'prgs_all', [])
        picker_indexes = "\n".join([
            ("INDEX: {}, parsedq: {}").format(xidx, x['question_text'])
            for xidx, x in enumerate(prgs_all)
        ])

        if picker == -1:
            logger.error(PICK_TPL())
            print picker_indexes
            return None

        if not prg_match and picker is None:
            logger.error(PICK_TPL())
            print picker_indexes
            return None

        if picker:
            try:
                prg_match = prgs_all[picker]
            except IndexError:
                logger.error(PERR_TPL(picker))
                return None

        request_args = {
            'object_type': 'question',
            'parse_result_group': prg_match,
            'auth_dict': self.auth.token,
        }

        self.last_request = AskParseQuestionRequest(**request_args)
        self.__call_api()

        result_object = getattr(self.last_response, 'inner_dict_xml', {})
        question_id = result_object.get('question', {}).get('id', '')
        self.last_response.question_id = question_id
        if not question_id:
            logger.error((
                "No question ID returned from AddObject on {}"
            ).format(prg_match))
            return None

        request_args = {
            'object_type': 'question',
            'question_id': question_id,
            'auth_dict': self.auth.token,
        }

        self.last_request = QuestionResults(**request_args)
        self.__call_api()
        return self.last_response

    def get_question_log(self, query):
        """sends a get question request and returns a SoapResponse object
        can only ask for questions by ID
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'question',
            'query': query,
            'auth_dict': self.auth.token,
            'arg_prefixes': ['id'],
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    def get_all_question_logs(self):
        """sends a get all question request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'question',
            'query': '',
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    def get_sensor(self, query):
        """sends a get sensor request and returns a SoapResponse object
        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'sensor',
            'query': query,
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    def get_all_sensors(self):
        """sends a get all sensors request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'sensor',
            'query': '',
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    def get_package(self, query):
        """sends a get package request and returns a SoapResponse object
        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'package_spec',
            'query': query,
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    def get_all_packages(self):
        """sends a get all packages request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'package_spec',
            'objects_dict': {'package_spec': ''},
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    # TODO NOT WORKING (same problem as get_all_groups)
    def get_action(self, query):
        """sends a get action request and returns a SoapResponse object
        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'action',
            'query': query,
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    # TODO NOT WORKING (same problem as get_all_groups)
    def get_all_actions(self):
        """sends a get all actions request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'action',
            'objects_dict': {'action': {'name': ''}},
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    def get_group(self, query):
        """sends a get group request and returns a SoapResponse object
        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'group',
            'query': query,
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    # TODO NOT WORKING
    def get_all_groups(self):
        """sends a get all groups request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        request_args = {
            'object_type': 'group',
            'objects_dict': {'group': {'name': ''}},
            'auth_dict': self.auth.token,
        }

        self.last_request = GetObjectRequest(**request_args)
        self.__call_api()
        return self.last_response

    '''
    """RAW XML FOR REQUEST THAT DOES NOT WORK (also tried <group/>):
<soap:Body xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <tanium_soap_request xmlns="urn:TaniumSOAP">
      <session>...</session>
      <command>GetObject</command>
      <object_list>
        <group>
          <name />
        </group>
      </object_list>
      <ID>0</ID>
      <ContextID>0</ContextID>
    </tanium_soap_request>
  </soap:Body>
    """
    '''

    # TODO
    '''
    def deploy_package(self):
        pass

    def deploy_action(self):
        pass

    def get_system_status(self):
        pass
    '''

    def http_get(self, url, headers={}):
        """perform an HTTP get using the requests module - this is
        so we always bypass SSL verification, and wrap exceptions into a
        requests-like object
        """
        ER1_TPL = ("SSL Error in HTTP GET to {!r}: {}").format
        try:
            ret = requests.get(url, verify=False, headers=headers)
        except requests.exceptions.SSLError as e:
            ret = FailedPage(ER1_TPL(url, e))
        return ret

    def http_post(self, url, data, headers={}):
        """perform an HTTP post using the requests module - this is
        so we always bypass SSL verification, and wrap exceptions into a
        requests-like object
        """
        ER1_TPL = ("SSL Error in HTTP POST to {!r}: {}").format
        try:
            ret = requests.post(url, data=data, verify=False, headers=headers)
        except requests.exceptions.SSLError as e:
            ret = FailedPage(ER1_TPL(url, e))
        return ret

    def soap_post(self, data, url=None):
        """uses http_post to perform a SOAPAction call to url with data"""
        DBG1_TPL = ('Received SOAP Response {}:\n{}').format
        if not url:
            url = self.soap_url
        headers = {'SOAPAction': '""'}
        ret = self.http_post(url=url, data=data, headers=headers)
        self.ret = ret
        httplog(DBG1_TPL(ret.status_code, ret.text.encode(ret.encoding)))
        return ret
