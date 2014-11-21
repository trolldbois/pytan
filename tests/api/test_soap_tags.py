#!/usr/bin/env python -ttB

import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import unittest

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
root_dir = os.path.join(my_dir, os.pardir, os.pardir, 'pytan')
root_dir = os.path.abspath(root_dir)
path_adds = [my_dir, root_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

import api
import xml.etree.ElementTree as ET


class Test_SOAPTags(unittest.TestCase):

    def test_soap_tags(self):
        """The that SOAP serialization yields correct tags for complex types"""
        question = api.Question()
        select_list = api.SelectList()
        select = api.Select()
        select.sensor = api.Sensor()
        select_list.append(select)
        question.selects = select_list
        et = ET.fromstring(question.toSOAPBody())
        # find the "selects" node, which is the SOAP tag for
        #select_list in question
        self.assertIsNotNone(et.find(".//selects/select"))
