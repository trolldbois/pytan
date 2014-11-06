#!/usr/bin/env python

import os
import sys
import glob
import copy
import json
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
import SoapUtil
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
        spew("### InvalidServerTests setup START")
        cls.__http = threaded_http.threaded_http(
            port=4433, verbosity=TESTVERBOSITY
        )
        spew("### InvalidServerTests setup END")

    @ddt.file_data('ddt_invalid_connects.json')
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
        spew("### ValidServerTests setup START")
        cls.sw = SoapWrap.SoapWrap(**SERVER_INFO)
        cls.st = SoapWrap.SoapTransform()

        if not os.path.isdir(TEST_OUT):
            os.mkdir(TEST_OUT)

        test_files = glob.glob(TEST_OUT + '/*.*')
        if test_files:
            spew("Cleaning up %s old test files" % len(test_files))
            [os.unlink(x) for x in test_files]

        spew('\n' + str(cls.sw))
        spew("### ValidServerTests setup END")

    def setup_test(self):
        spew("")
        return self.sw

    def combo_transform_tests(self, response, method, value):
        # derive all the permutations of every option we have for
        # bool args and header sort priority
        # this is complicated and involves combinatorics, but basically
        # we write a response file for every supported format, with every
        # possible combination of options (and embed those options into
        # the filename)
        st = self.st
        if response.command == 'GetResultData':
            bool_args = st.BOOL_KWARGS.keys()
            bool_opts = [True, False]
            bool_combos = SoapUtil.combinator1(bool_args, bool_opts)
        else:
            bool_combos = []

        sort_args = ['HEADER_SORT_PRIORITY']
        sort_opts = [st.HEADER_SORT_PRIORITY, [], ["name"], False]
        sort_combos = SoapUtil.combinator1(sort_args, sort_opts)

        format_tests = [x for x in st.FORMATS if 'raw.' not in x]

        all_combos = bool_combos + sort_combos
        all_combos = SoapUtil.combinator2(all_combos, format_tests, 'ftype')
        all_combos = [SoapUtil.build_fn_from_dict(x) for x in all_combos]

        for combo in all_combos:
            spew("+++ TESTING SoapTransform.write_response() with {}".format(
                json.dumps(combo)))
            combo['fdir'] = TEST_OUT
            combo['response'] = response
            combo['fname'] = '_'.join([method, SoapUtil.stringify_obj(value)])
            f = st.write_response(**combo)
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

    def transform_tests(self, response, method, value):
        '''standard transform tests for any response object'''
        st = self.st
        format_tests = st.FORMATS.keys()

        for ft in format_tests:
            spew(
                "+++ TESTING SoapTransform.write_response() "
                "with default opts for ftype {}".format(ft))
            f = st.write_response(
                response, fdir=TEST_OUT, ftype=ft, fpostfix='defaults')
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

    def response_tests(self, response, method, value):
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
        if COMBO_TRANSFORM_TESTS:
            self.combo_transform_tests(response, method, value)
        if DEFAULT_TRANSFORM_TESTS:
            self.transform_tests(response, method, value)

    @ddt.file_data('ddt_valid_methodcalls.json')
    def test_valid_methodcalls(self, value):
        sw = self.setup_test()
        method = value.pop('method')
        spew("+++ TESTING EXPECTED SUCCESS SoapWrap.%s() with kwargs %s" % (
            method, value))
        response = getattr(sw, method)(**value)
        self.assertTrue(response)

    @ddt.file_data('ddt_valid_queries.json')
    def test_valid(self, value):
        sw = self.setup_test()
        method = value.pop('method')
        spew("+++ TESTING EXPECTED SUCCESS SoapWrap.%s() with kwargs %s" % (
            method, value))
        response = getattr(sw, method)(**value)
        self.response_tests(response, method, value)

    @ddt.file_data('ddt_invalid_queries.json')
    @unittest.expectedFailure
    def test_invalid(self, value):
        sw = self.setup_test()
        method = value.pop('method')
        spew("+++ TESTING EXPECTED FAILURE SoapWrap.%s() with kwargs %s" % (
            method, value))
        response = getattr(sw, method)(**value)
        self.response_tests(response, method, value)


if __name__ == "__main__":
    unittest.main(verbosity=TESTVERBOSITY, failfast=True, catchbreak=True)
