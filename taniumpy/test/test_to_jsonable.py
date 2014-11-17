import unittest

import api
import json


class TestToJsonable(unittest.TestCase):

    def test_user_to_jsonable(self):
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
        self.maxDiff = None
        self.assertEquals(user.to_jsonable(include_type=False), {
            'id': 1,
            'name': 'Tanium',
            'roles': {'role': [
                {'id': 3,
                'name': 'Administrator',
                'permissions': {'permission': 'Administrator'}},
                {'id': 5,
                 'name': 'Question Asker',
                 'permissions': {'permission': 'Question Asker'}}]}
        })

    def test_with_jsonable_property(self):
        sensor = api.Sensor()
        sensor.parameter_definition = json.dumps([{"name": "param1"}, {"name": "param2"}])
        self.assertEquals(sensor.to_jsonable(
            explode_json_string_values=True,
            include_type=False),
            {'parameter_definition': [{'name': 'param1'}, {'name': 'param2'}]})

    def test_to_json(self):
        user = api.User()
        user.name = 'Test'
        self.assertEqual(api.BaseType.to_json(user), """{"_type": "user", "name": "Test"}""")

    def test_to_json_list(self):
        users = [api.User(), api.User()]
        self.assertEqual(api.BaseType.to_json(users), """[{"_type": "user"}, {"_type": "user"}]""")