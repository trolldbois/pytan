import unittest

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