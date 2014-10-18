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
#import inspect
#import tempfile
import socket
import time
import csv
import StringIO
import re
import json
from datetime import datetime
from collections import defaultdict
import xml.etree.cElementTree as ET
#import xml.etree.ElementTree as ET

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
        elem.text = value
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


def xml_excel(TODO):
    """returns the xml for the response as an XML doc in StringIO obj"""
    # TODO
    xml_excel = StringIO.StringIO()
    return xml_excel


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
            self.command,
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

    def csv_pre(self, ResultXML_dict, result_object):
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
    def __init__(self, **kwargs):
        super(AskSavedQuestionRequest, self).__init__(**kwargs)

    def overrides(self, **kwargs):
        self.command = 'GetResultData'
        # for sorting the xml result
        self.header_priority = []

    def csv_pre(self, ResultXML_dict, result_object):
        """returns the ResultXML_dict for the response as a list of lists, one
        for each row, headers in the first row
        """
        result_sets = ResultXML_dict.get('result_sets', {})
        result_set = result_sets.get('result_set', {})

        # get headers from xml response result_set
        cs = result_set.get('cs', {})
        xml_headers = cs.get('c', [])

        # extract the name for the header of each column
        headers = [x.get('dn', None) for x in xml_headers]

        # get rows from xml response result_set
        rs = result_set.get('rs', {})
        r = rs.get('r', [])
        xml_rows = [x.get('c', []) for x in r]

        # extract the row values for each column
        pre_csv = [[y.get('v', None) for y in x] for x in xml_rows]

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

    def csv_pre(self, ResultXML_dict, result_object):
        """returns the result_object for the response as a list of dicts, one
        for each row
        """
        if not result_object:
            # TODO our call failed to return a result object. print error
            return None
        pre_csv = parse_result_object(result_object, self._multi, self._single)
        return pre_csv


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

        # extract some things from the requests object
        self.status_code = self.http_response.status_code
        self.text = self.http_response.text
        self.__parse_text(self.text)

        # call the request parser to generate a CSV consumable object
        pre_csv = self.request.csv_pre(self.ResultXML_dict, self.result_object)

        header_priority = getattr(self.request, 'header_priority', None)

        # the pre_csv into an actual csv and store it in csv
        self.csv = xml_csv(pre_csv, header_priority)

    def __str__(self):
        received = self.received_human or "Not Yet Sent"
        STR_TPL = (
            "SoapResponse from {}, code {} on: {}, Request: {}"
        ).format
        ret = STR_TPL(self.soap_url, self.status_code, received, self.request)
        return ret

    def __parse_text(self, text):
        """chew up the raw text from the http_response into XML"""
        DBG2_TPL = ('Parsed XML:\n{}').format
        CMD_TPL = ("response command: {}").format
        self.xmltree = xml_tree(text)
        xml_clean_ns(self.xmltree)
        self.xmldict = build_dict_from_xml(self.xmltree)
        self.xml_raw = xml_pretty(self.xmltree)
        xmlparselog(DBG2_TPL(self.xml_raw))

        env_elem = self.xmldict.get('Envelope', {})
        body_elem = env_elem.get('Body', {})
        self.returndict = body_elem.get('return', {})
        self.command = self.returndict.get('command')
        self.session_id = self.returndict.get('session')
        self.object_list = self.returndict.get('object_list')

        logger.debug(CMD_TPL(self.command))
        self.authok = True
        if 'Forbidden' in self.command:
            self.authok = False

        self.reqok = True
        if 'Bad Request' in self.command:
            self.reqok = False

        if not self.command:
            self.reqok = False

        if not self.authok or not self.reqok or not self.command:
            return

        # TODO:
        """if bad_request we throw exception:
[845   -           tanwrap.py:__parse_text()] 2014-10-17 23:15:26,719
DEBUG    response command: ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class ActionNotFound
Traceback (most recent call last):
  File "./tanwrap.py", line 1663, in <module>
    all_actions = sw.get_all_actions()
  File "./tanwrap.py", line 1463, in get_all_actions
    self.__call_api()
  File "./tanwrap.py", line 1215, in __call_api
    self.__send_request()
  File "./tanwrap.py", line 1270, in __send_request
    http_response=http_response,
  File "./tanwrap.py", line 813, in __init__
    pre_csv = self.request.csv_pre(self.ResultXML_dict, self.result_object)
AttributeError: 'SoapResponse' object has no attribute 'ResultXML_dict'

        """
        self.__parse_inner_results()

    def __parse_inner_results(self):
        """look for results embedded in the returndict of the XML response"""

        #ResultXML is used for returns from command=[GetResultData,
        #GetResultInfo]
        DBG3_TPL = ('Inner Result XML:\n{}').format
        self.ResultXML_dict = {}
        ResultXML = self.returndict.get('ResultXML', '')
        if ResultXML:
            ResultXML_tree = xml_tree(ResultXML)
            self.ResultXML_dict = build_dict_from_xml(ResultXML_tree)
            ResultXML_raw = xml_pretty(ResultXML_tree)
            xmlparselog(DBG3_TPL(ResultXML_raw))

        #result_object is used for returns from command=[GetObject, AddObject,
        #DeleteObject]
        self.result_object = self.returndict.get('result_object', {})

    def write_csv_file(self, path=None):
        if self.csv is None:
            # TODO more logging
            return False
        WRITE_TPL = ("Writing CSV to file: {}").format
        if path is None:
            path = str(self.request.objects_dict)
            path = path.replace(': ', '.')
            path = path.translate(None, '\'{[]}')
            path = path.replace(' ', '_')
            path = path.replace(',', '+')
            path = path.replace('+_', '+')
            path = path[0:80]
            path += '__'
            path += get_now()
            path += ".csv"
            path = ("{}__{}").format(self.command, path)
        logger.debug(WRITE_TPL(path))
        x = open(path, 'w+')
        x.write(self.csv)
        x.close()
        return True

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


class FailedPage(object):
    """simple object to replicate requests-like object for exceptions"""
    # TODO subclass requests response object??
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
        return True

    def __extract_version(self, page):
        """extracts the serverVersion from the apps home page HTML"""
        ER2_TPL = ("Version info not found in applications home page").format
        version_regex = re.compile(r"flashvars.serverVersion.*'(.*)';")
        version_search = version_regex.search(page.text)
        if not version_search:
            logger.warn(ER2_TPL())
            return "Unknown"
        if len(version_search.groups()) != 1:
            logger.warn(ER2_TPL())
            return "Unknown"
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
        AUTH_TPL = (
            'Authorization {} for last request: {}').format
        BAD_TPL = (
            'Bad SOAP request for last request: {}').format

        self.last_response = None

        if not self.app_ok:
            return self.last_response

        # get the SOAP response and store it in self.response
        self.__send_request()

        # if bad request, log it and return response
        if not self.last_response.reqok:
            logger.error(BAD_TPL(self.last_request))
            return self.last_response

        # if auth failed and we are using a session ID, fallback to user/pass
        # and retry the request
        if not self.last_response.authok and self.auth.via_session_id:
            logger.warn(
                "Last request failed due to expired/invalid session ID, "
                "retrying request with username/password"
            )
            self.auth.auth_fallback()
            self.__send_request()

        # if auth is STILL failed, even if request was re-issued,
        # log an auth failure
        if not self.last_response.authok:
            logger.error(AUTH_TPL('FAILED', self.last_request))
        else:
            logger.debug(AUTH_TPL('SUCCESS', self.last_request))

        return self.last_response

    def __send_request(self):
        """sends the request to the SOAP API"""
        # TODO: Figure out request sent time for multiple requests
        # TODO NEXT PRIORITY
        # TODO: ADD LOGIC FOR WAITING FOR FULL RESULT SET

        SEND_TPL = ("Sending {}, SOAP URL: {}").format
        RECV_TPL = ("Received {}, SOAP URL: {}").format

        # set token to user/pass or session ID accordingly
        self.auth.update_token()

        logger.debug(SEND_TPL(self.last_request, self.soap_url))

        # update last_requests auth_dict with current token
        self.last_request.auth_dict = self.auth.token

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
        """sends a question Request and returns a SoapResponse object"""
        # TODO NEXT PRIORITY
        pass

    def get_question(self, query):
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

    def get_all_questions(self):
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
    '''
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
    '''

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
    '''
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
        # TODO
        pass

    def deploy_action(self):
        # TODO
        pass

    def get_system_status(self):
        # TODO
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
        httplog(DBG1_TPL(ret.status_code, ret.text))
        return ret


if __name__ == '__main__':
    user = 'JTANIUM1\Jim Olsen'
    password = 'Evinc3d!'
    host = '172.16.31.128'
    port = '443'

    badsslhost = '127.0.0.1'
    badsslport = 4443
    non_host = '172.16.31.129'

    loglevel = 1
    """
    from threaded_http import threaded_http
    threaded_http(port=4443)

    print ('### TEST: bad https host: {}:{}').format(badsslhost, badsslport)
    badssl = SoapWrap(
        user,
        password,
        badsslhost,
        port=badsslport,
        protocol='https',
        loglevel=loglevel,
    )

    print ('### TEST: bad http host: {}:{}').format(badsslhost, badsslport)
    badssl = SoapWrap(
        user,
        password,
        badsslhost,
        port=badsslport,
        protocol='http',
        loglevel=loglevel,
    )

    print ('### TEST: non-existant host: {}:{}').format(non_host, port)
    test_non_host = SoapWrap(
        user,
        password,
        non_host,
        port=port,
        protocol='https',
        loglevel=loglevel,
    )
    """
    print ('### TEST: good host: {}:{}').format(host, port)
    sw = SoapWrap(
        user,
        password,
        host,
        port=port,
        protocol='https',
        loglevel=loglevel,
    )

    # wont work, saved_question needs just one entry
    # saved_question_bad = sw.ask_saved_question(
        # ['Installed Applications', 'id:0'])

    # will work, single str
    ask_saved_question_good1 = sw.ask_saved_question('Installed Applications')
    ask_saved_question_good1.write_csv_file()

    # will work, list with single str
    # saved_question_good2 = sw.ask_saved_question(['Installed Applications'])

    sensor = sw.get_sensor('Computer Name')
    sensor.write_csv_file()

    multiple_sensors = sw.get_sensor(['Computer Name', 'Action Statuses'])
    multiple_sensors.write_csv_file()

    all_sensors = sw.get_all_sensors()
    all_sensors.write_csv_file()

    all_saved_questions = sw.get_all_saved_questions()
    all_saved_questions.write_csv_file()

    saved_question = sw.get_saved_question('Installed Applications')
    saved_question.write_csv_file()

    # this is all questions that have been asked
    all_questions = sw.get_all_questions()
    all_questions.write_csv_file()

    # must only pass id: to get_question
    question = sw.get_question('id:9000')
    question.write_csv_file()

    package = sw.get_package('Distribute Patch Tools')
    package.write_csv_file()

    all_packages = sw.get_all_packages()
    all_packages.write_csv_file()

    # TODO NOT WORKING
    # all_groups = sw.get_all_groups()
    # all_groups.write_csv_file()

    group = sw.get_group('All Computers')
    group.write_csv_file()

    # TODO NOT WORKING
    # all_actions = sw.get_all_actions()
    # all_actions.write_csv_file()

    # TODO NOT WORKING
    # action = sw.get_action('Distribute Tanium Standard Utilities')
    # action.write_csv_file()
