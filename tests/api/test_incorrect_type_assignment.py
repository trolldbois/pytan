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

from api.object_types.base import IncorrectTypeException


class TestIncorrectTypeAssignment(unittest.TestCase):
    """Test that assigning incorrect types raises"""

    def _do_assign(self, args):
        user = api.User()
        user.roles = api.UserRole()  # this is incorrect

    def test_incorrect_type_assignment(self):
        self.assertRaises(IncorrectTypeException, self._do_assign, None)
