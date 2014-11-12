import unittest

import api as api


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