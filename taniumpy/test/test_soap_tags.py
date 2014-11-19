import xml.etree.ElementTree as ET
import unittest

import api


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
        # find the "selects" node, which is the SOAP tag for select_list in question
        self.assertIsNotNone(et.find(".//selects/select"))