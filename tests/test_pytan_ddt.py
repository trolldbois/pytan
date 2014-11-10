#!/usr/bin/env python

import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import glob
import copy
import json
import unittest

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
par_dir = os.path.join(my_dir, os.pardir)
path_adds = [my_dir, par_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

import threaded_http
import ddt
from pytan import utils
from pytan import Handler
from pytan import Reporter

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

# have unittest exit immediately on unexpected error
FAILFAST = True

# catch control-C to allow current test suite to finish (press 2x to force)
CATCHBREAK = True

# control whether the transform tests will be done
DEFAULT_TRANSFORM_TESTS = True

# control whether the combinator transform tests will be done
COMBO_TRANSFORM_TESTS = False

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
        spew("+++ TESTING EXPECTED FAILURE Handler() with kwargs %s" % (
            mykwargs))
        handler = Handler(**mykwargs)
        spew(str(handler))


@ddt.ddt
class ValidServerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        spew("### ValidServerTests setup START")
        cls.handler = Handler(**SERVER_INFO)
        cls.reporter = Reporter()

        if not os.path.isdir(TEST_OUT):
            os.mkdir(TEST_OUT)

        test_files = glob.glob(TEST_OUT + '/*.*')
        if test_files:
            spew("Cleaning up %s old test files" % len(test_files))
            [os.unlink(x) for x in test_files]

        spew('\n' + str(cls.handler))
        spew("### ValidServerTests setup END")

    def setup_test(self):
        spew("")
        return self.handler

    def combo_transform_tests(self, response, method, value):
        # derive all the permutations of every option we have for
        # bool args and header sort priority
        # this is complicated and involves combinatorics, but basically
        # we write a response file for every supported format, with every
        # possible combination of options (and embed those options into
        # the filename)
        reporter = self.reporter
        if response.command == 'GetResultData':
            bool_args = reporter.BOOL_KWARGS.keys()
            bool_opts = [True, False]
            bool_combos = utils.combinator1(bool_args, bool_opts)
        else:
            bool_combos = []

        sort_args = ['HEADER_SORT_PRIORITY']
        sort_opts = [reporter.HEADER_SORT_PRIORITY, [], ["name"], False]
        sort_combos = utils.combinator1(sort_args, sort_opts)

        format_tests = [x for x in reporter.FORMATS if 'raw.' not in x]

        all_combos = bool_combos + sort_combos
        all_combos = utils.combinator2(all_combos, format_tests, 'ftype')
        all_combos = [utils.build_fn_from_dict(x) for x in all_combos]

        for combo in all_combos:
            spew("+++ TESTING Reporter.write_response() with {}".format(
                json.dumps(combo)))
            combo['fdir'] = TEST_OUT
            combo['response'] = response
            combo['fname'] = '_'.join([method, utils.stringify_obj(value)])
            f = reporter.write_response(**combo)
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

    def transform_tests(self, response, method, value):
        '''standard transform tests for any response object'''
        reporter = self.reporter
        format_tests = reporter.FORMATS.keys()

        for ft in format_tests:
            spew(
                "+++ TESTING Reporter.write_response() "
                "with default opts for ftype {}".format(ft))
            f = reporter.write_response(
                response, fdir=TEST_OUT, ftype=ft, fpostfix='defaults')
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

    def response_tests(self, response, method, value):
        '''standard tests for any response object'''

        spew("+++ TESTING REQUEST: %s" % response.request)
        self.assertIsNotNone(response.request)

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
        handler = self.setup_test()
        method = value.pop('method')
        spew("+++ TESTING EXPECTED SUCCESS Handler.%s() with kwargs %s" % (
            method, value))
        response = getattr(handler, method)(**value)
        self.assertTrue(response)

    @ddt.file_data('ddt_valid_queries.json')
    def test_valid(self, value):
        handler = self.setup_test()
        method = value.pop('method')
        spew("+++ TESTING EXPECTED SUCCESS Handler.%s() with kwargs %s" % (
            method, value))
        response = getattr(handler, method)(**value)
        self.response_tests(response, method, value)

    @ddt.file_data('ddt_invalid_queries.json')
    @unittest.expectedFailure
    def test_invalid(self, value):
        handler = self.setup_test()
        method = value.pop('method')
        spew("+++ TESTING EXPECTED FAILURE Handler.%s() with kwargs %s" % (
            method, value))
        response = getattr(handler, method)(**value)
        self.response_tests(response, method, value)


if __name__ == "__main__":
    unittest.main(
        verbosity=TESTVERBOSITY,
        failfast=FAILFAST,
        catchbreak=CATCHBREAK)
