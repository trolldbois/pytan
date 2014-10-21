#!/usr/bin/env python

import os
import sys
import unittest

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
par_dir = os.path.join(my_dir, os.pardir)
lib_dir = os.path.join(par_dir, 'lib')
path_adds = [my_dir, par_dir, lib_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.insert(0, x)

#sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, 'lib'))
import tanwrap
import threaded_http

LOGLEVEL = 0


class BasicTests(unittest.TestCase):

    __http = None

    def setUp(self):
        # Only setup the http server once
        # (or make it so that a tearDown can kill it)
        if BasicTests.__http is None:
            BasicTests.__http = threaded_http.threaded_http(port=4433)

    def tearDown(self):
        pass

    @unittest.expectedFailure
    def test_nossl(self):
        # tests accessing a HTTP port using HTTPS against a host that is not
        # running a tanium server
        sw = tanwrap.SoapWrap(
            'user',
            'password',
            '127.0.0.1',
            port=4433,
            protocol='https',
            loglevel=LOGLEVEL,
        )
        self.assertTrue(sw.app_ok)

    @unittest.expectedFailure
    def test_badhost(self):
        # tests accessing a HTTP port using HTTP against a host that is not
        # running a tanium server
        sw = tanwrap.SoapWrap(
            'user',
            'password',
            '127.0.0.1',
            port=4433,
            protocol='http',
            loglevel=LOGLEVEL,
        )
        self.assertTrue(sw.app_ok)

    @unittest.expectedFailure
    def test_nonhost(self):
        # tests accessing a server and port that does not exist at all
        sw = tanwrap.SoapWrap(
            'user',
            'password',
            '1.1.1.1',
            port=4433,
            protocol='https',
            loglevel=LOGLEVEL,
        )
        self.assertTrue(sw.app_ok)


class TestsAgainstServer(unittest.TestCase):
    # todo: let these be more dynamic
    # (like when ryan's test framework is awesome)

    # ryans server info
    # USERNAME = 'Administrator'
    # PASSWORD = 'Tanium!'
    # HOST = '192.168.42.130'

    # jims server info
    USERNAME = 'Jim Olsen'
    PASSWORD = 'Evinc3d!'
    HOST = '172.16.31.128'

    def setUp(self):
        self.sw = tanwrap.SoapWrap(
            self.USERNAME,
            self.PASSWORD,
            self.HOST,
            port=443,
            protocol='https',
            loglevel=LOGLEVEL,
        )
        self.assertTrue(self.sw.app_ok)

    @unittest.expectedFailure
    def test_bad_saved_q(self):
        q = ['Installed Applications', 'id:0']
        result = self.sw.ask_saved_question(q)
        self.assertNotEqual(None, result)

    def test_ask_saved_q(self):
        '''this should test that:
        - result.request.build_xml() returns something that has:
          * auth or session in it
          * command in it
          * object-list in it
        - result.request.command is not empty
        - result.status_code is 200
        - result.text is not empty
        - result.csv is not empty
        - result.write_csv_file() produces a non-empty file and
            does not return False
        '''
        q = 'Installed Applications'
        result = self.sw.ask_saved_question(q)
        result.write_csv_file()
        self.assertNotEqual(None, result)
        #self.assertEqual(result.command,)
        #self.assertNot

if __name__ == "__main__":
    unittest.main(verbosity=2)
