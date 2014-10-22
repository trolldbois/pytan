#!/usr/bin/env python

import os
import sys
import glob
import unittest

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
par_dir = os.path.join(my_dir, os.pardir)
lib_dir = os.path.join(par_dir, 'lib')
path_adds = [my_dir, par_dir, lib_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.insert(0, x)

import tanwrap
import threaded_http

LOGLEVEL = 1
CSV_OUT = os.path.join(my_dir, 'CSV_OUT')


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
        '''tests HTTP port using HTTPS on host with no tanium'''
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
        '''tests HTTP port using HTTP on host with no tanium'''
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
        '''tests accessing a server and port that does not exist at all'''
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

    # TODO ADD INVALID LOGIN TEST
    # TODO ADD INVALID SOAP PATH TEST
    # jims server info
    USERNAME = 'Jim Olsen'
    PASSWORD = 'Evinc3d!'
    HOST = '172.16.31.128'

    sw = None
    sw = tanwrap.SoapWrap(
        USERNAME,
        PASSWORD,
        HOST,
        port=443,
        protocol='https',
        loglevel=LOGLEVEL,
    )

    if not os.path.isdir(CSV_OUT):
        os.mkdir(CSV_OUT)

    csv_files = glob.glob(CSV_OUT + '/*.csv')
    if csv_files:
        print "Cleaning up %s old CSV files" % len(csv_files)
        [os.unlink(x) for x in csv_files]

    print '\n' + str(sw)

    def setUp(self):
        self.assertTrue(self.sw.app_ok)

    def response_tests(self, response):
        '''standard tests for any response object'''
        print "\nRESPONSE: %s\n" % response
        self.assertIsNotNone(response)
        self.assertTrue(response.request.xml_raw)
        self.assertIn('<command>', response.request.xml_raw)
        self.assertIn('<object_list>', response.request.xml_raw)
        auth = '<auth>' in response.request.xml_raw
        session = '<session>' in response.request.xml_raw
        self.assertTrue(auth or session)

        self.assertTrue(response.response_ok)

        self.assertTrue(response.outer_dict_xml)
        self.assertTrue(response.outer_return)

        self.assertTrue(response.command)

        self.assertTrue(response.auth_ok)
        self.assertTrue(response.command_ok)
        self.assertTrue(response.everything_ok)

        self.assertTrue(response.session_id)
        self.assertTrue(response.inner_dict_xml)
        self.assertTrue(response.pre_csv)
        self.assertTrue(response.csv)
        response.write_csv_file(dir=CSV_OUT)
        self.assertIsNotNone(response.csv_path)
        self.assertTrue(os.path.isfile(response.csv_path))

    def test_ask_saved_question_single_str(self):
        q = 'Installed Applications'
        response = self.sw.ask_saved_question(q)
        self.response_tests(response)

    def test_ask_saved_question_single_list(self):
        q = 'Installed Applications'
        response = self.sw.ask_saved_question([q])
        self.response_tests(response)

    def test_ask_parsed_question(self):
        q = 'Get Installed Applications from All Machines'
        response = self.sw.ask_parsed_question(q)
        self.response_tests(response)

    def test_get_single_sensor(self):
        q = 'Computer Name'
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_single_sensor_by_name(self):
        q = 'name:Computer Name'
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_single_sensor_by_id(self):
        q = 'id:1'
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_single_sensor_by_hash(self):
        q = 'hash:322086833'
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_multiple_sensors(self):
        q = ['Computer Name', 'Action Statuses']
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_multiple_sensors_selectors(self):
        q = ['name:Computer Name', 'id:1', 'hash:322086833']
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_all_sensors(self):
        response = self.sw.get_all_sensors()
        self.response_tests(response)

    def test_get_all_saved_questions(self):
        response = self.sw.get_all_saved_questions()
        self.response_tests(response)

    def test_get_saved_question_single(self):
        q = 'Installed Applications'
        response = self.sw.get_saved_question(q)
        self.response_tests(response)

    def test_get_saved_question_multiple(self):
        q = ['Installed Applications', 'Computer Name']
        response = self.sw.get_saved_question(q)
        self.response_tests(response)

    def test_get_all_question_logs(self):
        response = self.sw.get_all_question_logs()
        self.response_tests(response)

    def test_get_question_log(self):
        response = self.sw.get_question_log('1')
        self.response_tests(response)

    def test_get_package_single(self):
        q = 'Distribute Patch Tools'
        response = self.sw.get_package(q)
        self.response_tests(response)

    def test_get_all_packages(self):
        response = self.sw.get_all_packages()
        self.response_tests(response)

    def test_get_all_groups(self):
        response = self.sw.get_all_groups()
        self.response_tests(response)

    # TODO FAILS
    def test_get_group_single(self):
        q = 'All Computers'
        response = self.sw.get_group(q)
        self.response_tests(response)

    # TODO FAILS
    def test_get_all_actions(self):
        response = self.sw.get_all_actions()
        self.response_tests(response)

    # TODO FAILS
    def test_get_action_single(self):
        q = 'Distribute Tanium Standard Utilities'
        response = self.sw.get_action(q)
        self.response_tests(response)

    @unittest.expectedFailure
    def test_get_question_log_fail_invalid_id(self):
        response = self.sw.get_question_log('n')
        self.response_tests(response)

    @unittest.expectedFailure
    def test_get_question_log_fail_by_name(self):
        response = self.sw.get_question_log('name:fail')
        self.response_tests(response)

    @unittest.expectedFailure
    def test_bad_ask_saved_question(self):
        q = ['Installed Applications', 'id:0']
        response = self.sw.ask_saved_question(q)
        self.response_tests(response)

if __name__ == "__main__":
    unittest.main(verbosity=2)
