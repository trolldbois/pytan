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


class TestUserSerialize(unittest.TestCase):

    def test_serialize(self):
        user = api.User()
        user.name = 'Testing'
        role = api.UserRole()
        role.id = 3
        role.description = 'Description'
        user_roles = api.UserRoleList()
        user_roles.role.append(role)
        user.roles = user_roles
        body = user.toSOAPBody()
        self.assertEquals(body, """<user><domain /><deleted_flag /><name>Testing</name><active_session_count /><last_login /><local_admin_flag /><group_id /><id /><metadata /><roles><role><description>Description</description><id>3</id><name /><permissions /></role></roles><permissions /></user>""")
