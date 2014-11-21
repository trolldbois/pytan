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
import io
import json


class TestWriteCSV(unittest.TestCase):

    def test_user_to_csv(self):
        user = api.User()
        user.id = 1
        user.name = 'Tanium'
        user_role_list = api.UserRoleList()
        user.roles = user_role_list
        user_role = api.UserRole()
        user_role_list.append(user_role)
        user_role.id = 3
        user_role.name = 'Administrator'
        permissions = api.UserPermissions()
        user_role.permissions = permissions
        permissions.permission = 'Administrator'
        user_role = api.UserRole()
        user_role_list.append(user_role)
        user_role.id = 5
        user_role.name = 'Question Asker'
        permissions = api.UserPermissions()
        user_role.permissions = permissions
        # This is to test that the csv writer turns \n into \r\n
        # and does not turn \r\n into \r\r\n
        permissions.permission = 'Question\nAsker\r\n'

        out = io.BytesIO()
        api.BaseType.write_csv(out, user)
        self.assertEquals(out.getvalue(),
"""id,name,roles_role_0_id,roles_role_0_name,roles_role_0_permissions_permission,roles_role_1_id,roles_role_1_name,roles_role_1_permissions_permission\r
1,Tanium,3,Administrator,Administrator,5,Question Asker,"Question\r\nAsker\r\n"\r
""")

    def test_with_jsonable_property(self):
        sensor = api.Sensor()
        sensor.parameter_definition = json.dumps([{"name": "param1"}, {"name": "param2"}])
        out = io.BytesIO()
        api.BaseType.write_csv(out, sensor, explode_json_string_values=True)
        self.assertEquals(out.getvalue(),
"""parameter_definition_0_name,parameter_definition_1_name\r
param1,param2\r
""")
