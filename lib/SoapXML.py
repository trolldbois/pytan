#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""XML handling"""
import os
import sys
import logging
import re
import json
import xml.etree.cElementTree as ET
from collections import defaultdict

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
path_adds = [my_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.insert(0, x)

import SoapUtil
import SoapConstants

XMLCLOG = logging.getLogger("SoapWrap.xmlcreate").debug
XMLPLOG = logging.getLogger("SoapWrap.xmlparse").debug

# make it so ElementTree produces Elements with soap: prefix instead of ns0:
ET.register_namespace('soap', SoapConstants.NS_SOAP_ENV)
for attr, uri in SoapConstants.NS_DICT.items():
    ET.register_namespace(attr.split(":")[1], uri)


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
        XMLCLOG(CREATE1_TPL(name, attribs))
        elem = ET.Element(name, **attribs)
    else:
        XMLCLOG(CREATE2_TPL(name, parent.tag, attribs))
        elem = ET.SubElement(parent, name, **attribs)
    if value:
        XMLCLOG(VALUE_TPL(name, value))
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
        if SoapUtil.is_dict(objvalue):
            XMLCLOG(DICT_TPL(objname, parentelem.tag, objvalue))
            objelem = new_elem(objname, parent=parentelem)
            objelem = build_xml_from_dict(objelem, objvalue)
        elif SoapUtil.is_list(objvalue):
            for x in objvalue:
                XMLCLOG(LIST_TPL(objname, parentelem.tag, x))
                objelem = new_elem(objname, parent=parentelem)
                objelem = build_xml_from_dict(objelem, x)
        else:
            XMLCLOG(STR_TPL(objname, parentelem.tag, objvalue))
            objelem = new_elem(objname, objvalue, parent=parentelem)
    return parentelem


def build_request_xml(request):
    """builds the xml envelope needed for a SOAP request

    request.command should be a valid SOAP command, i.e. the following:
      GetObject
      GetResultData

    request.auth_dict should be one of the following:
      # session id based auth
      {'session': '$SESSION_ID'}
      # username/password based auth
      {'auth': {'username': '$USERNAME', 'password': '$PASSWORD'}}

    request.objects_dict should be something like one of the following:
      # get a single sensor
      {'sensor': {'name': 'Computer Name'}}
      {'sensor': {'id': '65'}}
      {'sensor': {'hash': '2940242'}}

      # get all sensors
      {'sensor': {'name': ''}}
    """
    DBG_TPL = ('Created XML:\n{}').format
    xmltree = new_elem(
        'Envelope',
        ns=SoapConstants.NS_SOAP_ENV,
        attribs=SoapConstants.NS_DICT,
    )
    body_elem = new_elem('Body', ns=SoapConstants.NS_SOAP_ENV, parent=xmltree)
    soap_req_elem = new_elem(
        'tanium_soap_request',
        parent=body_elem,
        attribs=SoapConstants.APP_NS,
    )
    build_xml_from_dict(soap_req_elem, request.auth_dict)
    new_elem('command', request.command, parent=soap_req_elem)
    objlist_elem = new_elem('object_list', parent=soap_req_elem)
    build_xml_from_dict(objlist_elem, request.objects_dict)
    new_elem('ID', '0', parent=soap_req_elem)
    new_elem('ContextID', '0', parent=soap_req_elem)
    request.xmltree = xmltree
    request.xml_raw = xml_pretty(xmltree)
    XMLCLOG(DBG_TPL(request.xml_raw))
    return request


def get_outer_xml(text):
    OUTER_XML = ('Parsed XML:\n{}').format
    outer_elem_xml = xml_tree(text)
    outer_elem_xml = xml_clean_ns(outer_elem_xml)
    outer_raw_xml = xml_pretty(outer_elem_xml)
    outer_dict_xml = build_dict_from_xml(outer_elem_xml)
    XMLPLOG(OUTER_XML(outer_raw_xml))
    return outer_dict_xml


def get_ResultXML(outer_return):
    XML_TPL = ('ResultXML:\n{}').format
    inner_raw_xml = outer_return['ResultXML']
    inner_raw_xml = inner_raw_xml.encode('utf-8')
    inner_elem_xml = xml_tree(inner_raw_xml)
    inner_elem_xml = xml_clean_ns(inner_elem_xml)
    inner_raw_xml = xml_pretty(inner_elem_xml)
    inner_dict_xml = build_dict_from_xml(inner_elem_xml)
    XMLPLOG(XML_TPL(inner_raw_xml))
    return inner_dict_xml
