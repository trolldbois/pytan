#!/usr/bin/env python

import os
import sys
import glob
# import itertools
import copy
# import json
import unittest

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
par_dir = os.path.join(my_dir, os.pardir)
lib_dir = os.path.join(par_dir, 'lib')
path_adds = [my_dir, par_dir, lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

import SoapWrap
import threaded_http
import ddt

SERVER_INFO = {
    "username": "Tanium User",
    "password": "T@n!um",
    "host": "172.16.31.128",
    "protocol": "https",
    "soap_path": "/soap",
    "port": "443",
    "loglevel": 0,
    "debugformat": False,
}

# control the amount of output from unittests
TESTVERBOSITY = 2

# control whether the transform tests will be done
DEFAULT_TRANSFORM_TESTS = True

# control whether the combinator transform tests will be done
COMBO_TRANSFORM_TESTS = True

# where the output files from the tests will be stored
TEST_OUT = os.path.join(my_dir, 'TEST_OUT')


def spew(m):
    if TESTVERBOSITY == 2:
        print (m)


@ddt.ddt
class InvalidServerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        spew("### BasicTests setup START")
        cls.__http = threaded_http.threaded_http(
            port=4433, verbosity=TESTVERBOSITY
        )
        spew("### BasicTests setup END")

    @ddt.file_data('test_invalid_connects.json')
    @unittest.expectedFailure
    def test_invalid_connect(self, value):
        mykwargs = copy.copy(SERVER_INFO)
        mykwargs.update(value)
        spew("")
        spew("+++ TESTING EXPECTED FAILURE SoapWrap() with kwargs %s" % (
            mykwargs))
        sw = SoapWrap.SoapWrap(**mykwargs)
        spew(str(sw))


@ddt.ddt
class ValidServerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        spew("### TestsAgainstServer setup START")
        cls.sw = SoapWrap.SoapWrap(**SERVER_INFO)

        if not os.path.isdir(TEST_OUT):
            os.mkdir(TEST_OUT)

        test_files = glob.glob(TEST_OUT + '/*.*')
        if test_files:
            spew("Cleaning up %s old test files" % len(test_files))
            [os.unlink(x) for x in test_files]

        spew('\n' + str(cls.sw))
        spew("### TestsAgainstServer setup END")

    def setup_test(self):
        spew("")
        return self.sw

    def response_tests(self, response):
        '''standard tests for any response object'''

        spew("+++ TESTING REQUEST: %s" % response.request)
        self.assertIsNotNone(response.request)
        self.assertTrue(response.request.xml_raw)
        self.assertIn('<command>', response.request.xml_raw)
        self.assertIn('<object_list>', response.request.xml_raw)
        auth = '<auth>' in response.request.xml_raw
        session = '<session>' in response.request.xml_raw
        self.assertTrue(auth or session)

        spew("+++ TESTING RESPONSE: %s" % response)
        self.assertIsNotNone(response)
        self.assertTrue(response.outer_xml)
        self.assertTrue(response.outer_return)
        self.assertTrue(response.command)
        self.assertTrue(response.session_id)
        self.assertTrue(response.inner_return)
        # self.combo_transform_tests(response)
        # self.transform_tests(response)

    @ddt.file_data('test_valid_data.json')
    def test_valid(self, value):
        sw = self.setup_test()
        method = value.pop('method')
        spew("+++ TESTING EXPECTED SUCCESS SoapWrap.%s() with kwargs %s" % (
            method, value))
        response = getattr(sw, method)(**value)
        self.response_tests(response)

    @ddt.file_data('test_invalid_data.json')
    @unittest.expectedFailure
    def test_invalid(self, value):
        sw = self.setup_test()
        method = value.pop('method')
        spew("+++ TESTING EXPECTED FAILURE SoapWrap.%s() with kwargs %s" % (
            method, value))
        response = getattr(sw, method)(**value)
        self.response_tests(response)


if __name__ == "__main__":
    unittest.main(verbosity=TESTVERBOSITY, failfast=True, catchbreak=True)
