#!/usr/bin/env python

import os
import sys
import glob
import unittest

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
par_dir = os.path.join(my_dir, os.pardir)
lib_dir = os.path.join(par_dir, 'lib')
path_adds = [my_dir, par_dir, lib_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.insert(0, x)

from SoapWrap import SoapWrap
import threaded_http


# TODO: let these be more dynamic
# (like when ryan's test framework is awesome)

# ryans server info
# USERNAME = 'Administrator'
# PASSWORD = 'Tanium!'
# HOST = '192.168.42.130'

# jims server info
USERNAME = 'Jim Olsen'
PASSWORD = 'Evinc3d!'
HOST = '172.16.31.128'
PORT = 443

# other options for SoapWrap
LOGLEVEL = 0
DEBUGFORMAT = False

# control the amount of output from unittests
TESTVERBOSITY = 2

# where the output files from the tests will be stored
TEST_OUT = os.path.join(my_dir, 'TEST_OUT')


def spew(m):
    if TESTVERBOSITY == 2:
        print (m)


class BasicTests(unittest.TestCase):
    spew("### BasicTests setup START")
    __http = threaded_http.threaded_http(port=4433, verbosity=TESTVERBOSITY)
    spew("### BasicTests setup END")

    @unittest.expectedFailure
    def test_soap_path(self):
        '''tests HTTP port using HTTPS on host with no tanium'''
        spew("")
        sw = SoapWrap(
            USERNAME,
            PASSWORD,
            HOST,
            PORT,
            soap_path='/invalid_path',
            loglevel=LOGLEVEL,
            debugformat=DEBUGFORMAT,
        )
        spew(str(sw))

    @unittest.expectedFailure
    def test_badpassword(self):
        '''tests tanium host with bad password'''
        spew("")
        sw = SoapWrap(
            USERNAME,
            'INVALID_PASSWORD',
            HOST,
            PORT,
            loglevel=LOGLEVEL,
            debugformat=DEBUGFORMAT,
        )
        spew(str(sw))

    @unittest.expectedFailure
    def test_badusername(self):
        '''tests tanium host with bad username'''
        spew("")
        sw = SoapWrap(
            'INVALID_USER',
            PASSWORD,
            HOST,
            PORT,
            loglevel=LOGLEVEL,
            debugformat=DEBUGFORMAT,
        )
        spew(str(sw))

    @unittest.expectedFailure
    def test_nossl(self):
        '''tests HTTP port using HTTPS on host with no tanium'''
        spew("")
        sw = SoapWrap(
            'user',
            'password',
            '127.0.0.1',
            port=4433,
            protocol='https',
            loglevel=LOGLEVEL,
            debugformat=DEBUGFORMAT,
        )
        spew(str(sw))

    @unittest.expectedFailure
    def test_badhost(self):
        '''tests HTTP port using HTTP on host with no tanium'''
        spew("")
        sw = SoapWrap(
            'user',
            'password',
            '127.0.0.1',
            port=4433,
            protocol='http',
            loglevel=LOGLEVEL,
            debugformat=DEBUGFORMAT,
        )
        spew(sw)

    @unittest.expectedFailure
    def test_nonhost(self):
        '''tests accessing a server and port that does not exist at all'''
        spew("")
        sw = SoapWrap(
            'user',
            'password',
            '1.1.1.1',
            port=4433,
            protocol='https',
            loglevel=LOGLEVEL,
            debugformat=DEBUGFORMAT,
        )
        spew(sw)


class TestsAgainstServer(unittest.TestCase):
    spew("### TestsAgainstServer setup START")
    sw = SoapWrap(
        USERNAME,
        PASSWORD,
        HOST,
        PORT,
        protocol='https',
        loglevel=LOGLEVEL,
        debugformat=DEBUGFORMAT,
    )

    if not os.path.isdir(TEST_OUT):
        os.mkdir(TEST_OUT)

    csv_files = glob.glob(TEST_OUT + '/*.csv')
    if csv_files:
        spew("Cleaning up %s old CSV files" % len(csv_files))
        [os.unlink(x) for x in csv_files]

    spew('\n' + str(sw))
    spew("### TestsAgainstServer setup END")

    def setup_test(self):
        spew("")
        return self.sw

    def response_tests(self, response):
        '''standard tests for any response object'''
        spew("RESPONSE: %s\n" % response)
        self.assertIsNotNone(response)
        self.assertTrue(response.request.xml_raw)
        self.assertIn('<command>', response.request.xml_raw)
        self.assertIn('<object_list>', response.request.xml_raw)
        auth = '<auth>' in response.request.xml_raw
        session = '<session>' in response.request.xml_raw
        self.assertTrue(auth or session)
        self.assertTrue(response.outer_xml)
        self.assertTrue(response.outer_return)
        self.assertTrue(response.command)
        self.assertTrue(response.session_id)
        self.assertTrue(response.inner_return)
        if response.command == 'GetObject':
            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                fprefix="defaults",
                format='csv',
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="nosort",
                HEADER_SORT_PRIORITY=None,
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="manualsort",
                HEADER_SORT_PRIORITY=['name'],
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

        else:
            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="defaults",
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="addtypetrue",
                ADD_TYPE_TO_HEADERS=True,
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="addtypefalse",
                ADD_TYPE_TO_HEADERS=False,
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="addsensortrue",
                ADD_SENSOR_TO_HEADERS=True,
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="addsensorfalse",
                ADD_SENSOR_TO_HEADERS=False,
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="expandcoltrue",
                EXPAND_GROUPED_COLUMNS=True,
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="expandcolfalse",
                EXPAND_GROUPED_COLUMNS=False,
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="hidecnttrue",
                HIDE_COUNT_COLUMN=True,
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

            f = self.sw.transform.write_response(
                response,
                fdir=TEST_OUT,
                format='csv',
                fprefix="hidecntfalse",
                HIDE_COUNT_COLUMN=False,
            )
            spew("wrote response to: %s" % f)
            self.assertTrue(os.path.isfile(f))

    def test_ask_saved_question_single_str(self):
        sw = self.setup_test()
        q = 'Installed Applications'
        response = sw.ask_saved_question(q)
        self.response_tests(response)

    def test_ask_saved_question_single_list(self):
        sw = self.setup_test()
        q = 'Installed Applications'
        response = sw.ask_saved_question([q])
        self.response_tests(response)

    def test_ask_parsed_question_simple(self):
        sw = self.setup_test()
        q = 'Get Installed Applications from All Machines'
        response = sw.ask_parsed_question(q)
        self.response_tests(response)

    def test_ask_parsed_question_complex(self):
        sw = self.setup_test()
        q = (
            'Get Computer Name and Operating System and IP Address and '
            'IP Route Details and Installed Applications from all machines'
        )
        response = sw.ask_parsed_question(q)
        self.response_tests(response)

    @unittest.expectedFailure
    def test_ask_parsed_question_invalid_picker(self):
        sw = self.setup_test()
        q = 'Get Installed Applications from All Machines'
        picker = 99999
        response = sw.ask_parsed_question(q, picker)
        self.response_tests(response)

    def test_ask_parsed_question_forced_picker0(self):
        sw = self.setup_test()
        q = 'Get Installed Applications from All Machines'
        picker = 0
        response = sw.ask_parsed_question(q, picker)
        self.response_tests(response)

    def test_ask_parsed_question_forced_picker1(self):
        sw = self.setup_test()
        q = 'Get Installed Applications from All Machines'
        picker = 1
        response = sw.ask_parsed_question(q, picker)
        self.response_tests(response)

    @unittest.expectedFailure
    def test_ask_parsed_question_picker_list(self):
        sw = self.setup_test()
        q = 'Get Installed Applications from All Machines'
        picker = -1
        response = sw.ask_parsed_question(q, picker)
        self.assertIsNotNone(response)
        self.assertTrue(response.prgs_all)

    def test_get_single_sensor_object(self):
        sw = self.setup_test()
        q = 'Computer Name'
        response = sw.get_sensor_object(q)
        self.response_tests(response)

    def test_get_single_sensor_object_by_name(self):
        sw = self.setup_test()
        q = 'name:Computer Name'
        response = sw.get_sensor_object(q)
        self.response_tests(response)

    def test_get_single_sensor_object_by_id(self):
        sw = self.setup_test()
        q = 'id:1'
        response = sw.get_sensor_object(q)
        self.response_tests(response)

    def test_get_single_sensor_object_by_hash(self):
        sw = self.setup_test()
        q = 'hash:322086833'
        response = sw.get_sensor_object(q)
        self.response_tests(response)

    def test_get_multiple_sensor_objects(self):
        sw = self.setup_test()
        q = ['Computer Name', 'Action Statuses']
        response = sw.get_sensor_object(q)
        self.response_tests(response)

    def test_get_multiple_sensor_objects_selectors(self):
        sw = self.setup_test()
        q = ['name:Computer Name', 'id:1', 'hash:322086833']
        response = sw.get_sensor_object(q)
        self.response_tests(response)

    def test_get_all_sensor_objects(self):
        sw = self.setup_test()
        response = sw.get_all_sensor_objects()
        self.response_tests(response)

    def test_get_all_saved_question_objects(self):
        sw = self.sw
        response = sw.get_all_saved_question_objects()
        self.response_tests(response)

    def test_get_saved_question_object_single(self):
        sw = self.setup_test()
        q = 'Installed Applications'
        response = sw.get_saved_question_object(q)
        self.response_tests(response)

    def test_get_saved_question_object_multiple(self):
        sw = self.setup_test()
        q = ['Installed Applications', 'Computer Name']
        response = sw.get_saved_question_object(q)
        self.response_tests(response)

    def test_get_all_question_objects(self):
        sw = self.setup_test()
        response = sw.get_all_question_objects()
        self.response_tests(response)

    def test_get_question_object(self):
        sw = self.setup_test()
        response = sw.get_question_object('1')
        self.response_tests(response)

    def test_get_package_object_single(self):
        sw = self.setup_test()
        q = 'Distribute Patch Tools'
        response = sw.get_package_object(q)
        self.response_tests(response)

    def test_get_all_packages(self):
        sw = self.setup_test()
        response = sw.get_all_package_objects()
        self.response_tests(response)

    def test_get_all_group_objects(self):
        sw = self.setup_test()
        response = sw.get_all_group_objects()
        self.response_tests(response)

    def test_get_group_object_single(self):
        sw = self.setup_test()
        q = 'All Computers'
        response = sw.get_group_object(q)
        self.response_tests(response)

    def test_get_all_action_objects(self):
        sw = self.setup_test()
        response = sw.get_all_action_objects()
        self.response_tests(response)

    def test_get_action_object_single_by_id(self):
        sw = self.setup_test()
        q = '1'
        response = sw.get_action_object(q)
        self.response_tests(response)

    @unittest.expectedFailure
    def test_get_action_object_single_by_name(self):
        sw = self.setup_test()
        q = 'Distribute Tanium Standard Utilities'
        response = sw.get_action_object(q)
        self.response_tests(response)

    @unittest.expectedFailure
    def test_get_question_object_fail_invalid_id(self):
        sw = self.setup_test()
        response = sw.get_question_object('n')
        self.response_tests(response)

    @unittest.expectedFailure
    def test_get_question_object_fail_by_name(self):
        sw = self.setup_test()
        response = sw.get_question_object('name:fail')
        self.response_tests(response)

    @unittest.expectedFailure
    def test_bad_ask_saved_question(self):
        sw = self.setup_test()
        q = ['Installed Applications', 'id:0']
        response = sw.ask_saved_question(q)
        self.response_tests(response)

if __name__ == "__main__":
    unittest.main(verbosity=TESTVERBOSITY)
