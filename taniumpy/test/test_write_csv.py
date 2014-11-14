import unittest

import api
import io


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