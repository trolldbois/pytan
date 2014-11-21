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


class TestRequest(unittest.TestCase):

    def test_requestUsers(self):
        body = api.Session('', '')._createGetObjectBody(
            api.UserList, row_count=1,
        )
        el = ET.fromstring(body)
        self.assertTrue(el.find('.//users') is not None)
        self.assertTrue(el.find(".//row_count").text.strip() == '1')

if __name__ == "__main__":
    unittest.main()
