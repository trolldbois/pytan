import unittest
import api
from   api.object_types.base import IncorrectTypeException

class TestIncorrectTypeSerialize(unittest.TestCase):

    def test_incorrect_type_serialize(self):
        """This tests when a consumer assigns an incorrect type.

        Serialization will catch when types are not properly
        assigned and raise an IncorrectTypeException.

        """
        user = api.User()
        role = api.UserRole()
        role.id = 1
        user.roles = role  # this should be a UserRoleList
        self.assertRaises(IncorrectTypeException, user.toSOAPBody, [])