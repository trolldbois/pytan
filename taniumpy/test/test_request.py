import unittest
from taniumpy.api.session import Session
from taniumpy.object_types.user_list import UserList

class TestRequest(unittest.TestCase):

    def test_requestUsers(self):
        body = Session('', '').createGetObjectBody(UserList)
        self.assertTrue('<users/>' in body)