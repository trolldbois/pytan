#!/usr/bin/env python
import sys
import os
import unittest

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
par_dir = os.path.join(my_dir, os.pardir)
path_adds = [my_dir, par_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

import api
# from taniumpy.api.session import Session
# from taniumpy.object_types.user_list import UserList


class TestRequest(unittest.TestCase):

    def test_requestUsers(self):
        body = api.Session('', '').createGetObjectBody(
            api.UserList, row_count=1,
        )
        self.assertTrue('<users/>' in body)
        self.assertTrue('<row_count>1</row_count>' in body)

if __name__ == "__main__":
    unittest.main()
