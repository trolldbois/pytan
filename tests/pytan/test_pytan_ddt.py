#!/usr/bin/env python -ttB

import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import glob
import copy
import unittest

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
root_dir = os.path.join(my_dir, os.pardir, os.pardir)
root_dir = os.path.abspath(root_dir)
path_adds = [my_dir, root_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

from testlib import threaded_http
from testlib import ddt
from pytan import Handler

SERVER_INFO = {
    "username": "Tanium User",
    "password": "T@n!um",
    "host": "172.16.31.128",
    "port": "444",
    "loglevel": 0,
    "debugformat": False,
}

# control the amount of output from unittests
TESTVERBOSITY = 2

# have unittest exit immediately on unexpected error
FAILFAST = True

# catch control-C to allow current test suite to finish (press 2x to force)
CATCHBREAK = True

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

    @ddt.file_data('ddt/ddt_invalid_connects.json')
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

    @ddt.file_data('ddt/ddt_valid_questions.json')
    def test_valid_question(self, value):
        handler = self.setup_test()

        method = value['method']
        args = value['args']

        s = (
            "+++ TESTING EXPECTED QUESTION SUCCESS Handler.{}() with kwargs {}"
        ).format
        spew(s(method, args))

        response = getattr(handler, method)(**args)
        self.assertTrue(response)
        spew("RESPONSE TEST: rows >= 1")
        self.assertTrue(len(response.rows) >= 1)
        spew("RESPONSE TEST: columnes >= 1")
        self.assertTrue(len(response.columns) >= 1)

    @ddt.file_data('ddt/ddt_valid_get_object.json')
    def test_valid_get_object(self, value):
        handler = self.setup_test()

        method = value['method']
        args = value['args']
        tests = value['tests']

        s = (
            "+++ TESTING EXPECTED GET SUCCESS Handler.{}() with kwargs {}"
        ).format
        spew(s(method, args))

        response = getattr(handler, method)(**args)

        self.assertTrue(response)
        for x in tests:
            spew("RESPONSE TEST: {}".format(x))
            self.assertTrue(eval(x))

    @ddt.file_data('ddt/ddt_invalid_questions.json')
    @unittest.expectedFailure
    def test_invalid_question(self, value):
        handler = self.setup_test()

        method = value['method']
        args = value['args']

        s = (
            "+++ TESTING EXPECTED QUESTION FAILURE Handler.{}() with kwargs {}"
        ).format
        spew(s(method, args))

        response = getattr(handler, method)(**args)
        self.assertTrue(response)
        spew("RESPONSE TEST: rows >= 1")
        self.assertGreaterEqual(len(response.rows), 1)
        spew("RESPONSE TEST: columns >= 1")
        self.assertGreaterEqual(len(response.columns), 1)

    @ddt.file_data('ddt/ddt_invalid_get_object.json')
    @unittest.expectedFailure
    def test_invalid_get_object(self, value):
        handler = self.setup_test()

        method = value['method']
        args = value['args']
        tests = value['tests']

        s = (
            "+++ TESTING EXPECTED GET FAILURE Handler.{}() with kwargs {}"
        ).format
        spew(s(method, args))

        response = getattr(handler, method)(**args)

        self.assertTrue(response)
        for x in tests:
            spew("RESPONSE TEST: {}".format(x))
            self.assertTrue(eval(x))


if __name__ == "__main__":
    unittest.main(
        verbosity=TESTVERBOSITY,
        failfast=FAILFAST,
        catchbreak=CATCHBREAK)
