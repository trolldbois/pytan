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


class TestToFlatDict(unittest.TestCase):

    def test_user_to_flat_dict(self):
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
        permissions.permission = 'Question Asker'

        self.assertEquals(user.to_flat_dict(), {
            'id': 1,
            'name': 'Tanium',
            'roles_role_0_id': 3,
            'roles_role_0_name': 'Administrator',
            'roles_role_0_permissions_permission': 'Administrator',
            'roles_role_1_id': 5,
            'roles_role_1_name': 'Question Asker',
            'roles_role_1_permissions_permission': 'Question Asker'
        })
