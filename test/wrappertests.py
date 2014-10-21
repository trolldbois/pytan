#!/usr/bin/env python

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, 'lib'))
import tanwrap
import threaded_http

class BasicTests(unittest.TestCase):

    __http = None
    def setUp(self):
        # Only setup the http server once (or make it so that a tearDown can kill it)
        if BasicTests.__http is None:
            BasicTests.__http = threaded_http.threaded_http(port=4433)

    def tearDown(self):
        pass

    def test_nossl(self):
        sw = tanwrap.SoapWrap('user', 'password', '127.0.0.1', port=4433, protocol='https')
        self.assertFalse(sw.app_ok)

    def test_badhost(self):
        sw = tanwrap.SoapWrap('user', 'password', '127.0.0.1', port=4433, protocol='http')
        self.assertFalse(sw.app_ok)

    def test_nonhost(self):
        sw = tanwrap.SoapWrap('user', 'password', '1.1.1.1', port=4433, protocol='https')
        self.assertFalse(sw.app_ok)

class TestsAgainstServer(unittest.TestCase):
    # todo: let these be more dynamic (like when ryan's test framework is awesome)
    USERNAME = 'Administrator'
    PASSWORD = 'Tanium!'
    HOST = '192.168.42.130'

    def setUp(self):
        self.sw = tanwrap.SoapWrap(self.USERNAME, self.PASSWORD, self.HOST, port=443, protocol='https')
        self.assertTrue(self.sw.app_ok)

    def test_bad_saved_q(self):
        result = self.sw.ask_saved_question(['Installed Applications', 'id:0'])
        self.assertEquals(None, result)

if __name__ == "__main__":
    unittest.main()
