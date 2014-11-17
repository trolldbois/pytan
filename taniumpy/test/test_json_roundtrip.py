import unittest
import api


class Test_JSONRoundTrip(unittest.TestCase):

    def test_json_round_trip(self):
        """Test that to_jsonable and from_jsonable are reversible

        Do this by comparing the SOAP bodies of
        a complex object and one constructed with
        from_jsonable(obj.to_jsonable())

        """
        user = api.User()
        user.id = 1
        user.name = "dmz\\joe.user"
        roles = api.UserRoleList()
        user.roles = roles
        role = api.UserRole()
        role.id = 1
        user.roles.append(role)
        soap1 = user.toSOAPBody()
        user2 = api.BaseType.from_jsonable(user.to_jsonable())
        soap2 = user2.toSOAPBody()
        self.assertEqual(soap1, soap2)