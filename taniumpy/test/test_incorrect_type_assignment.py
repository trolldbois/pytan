import unittest
import api

from api.object_types.base import IncorrectTypeException


class TestIncorrectTypeAssignment(unittest.TestCase):
    """Test that assigning incorrect types raises"""

    def _do_assign(self, args):
        user = api.User()
        user.roles = api.UserRole()  # this is incorrect

    def test_incorrect_type_assignment(self):
        self.assertRaises(IncorrectTypeException, self._do_assign, None)