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

CSV_OUT = os.path.join(my_dir, 'CSV_OUT')
LOGLEVEL = 0


def setUp():
    print 'yo'


class BasicTests(unittest.TestCase):
    print "### BasicTests setup START"
    __http = threaded_http.threaded_http(port=4433)
    print "### BasicTests setup END"

    @unittest.expectedFailure
    def test_soap_path(self):
        '''tests HTTP port using HTTPS on host with no tanium'''
        print ""
        sw = tanwrap.SoapWrap(
            USERNAME,
            PASSWORD,
            HOST,
            soap_path='/invalid_path',
            loglevel=LOGLEVEL,
        )
        print str(sw)
        self.assertTrue(sw.app_ok)

    @unittest.expectedFailure
    def test_badpassword(self):
        '''tests HTTP port using HTTPS on host with no tanium'''
        print ""
        sw = tanwrap.SoapWrap(
            USERNAME,
            'INVALID_PASSWORD',
            HOST,
            loglevel=LOGLEVEL,
        )
        print str(sw)
        self.assertTrue(sw.app_ok)

    @unittest.expectedFailure
    def test_badusername(self):
        '''tests HTTP port using HTTPS on host with no tanium'''
        print ""
        sw = tanwrap.SoapWrap(
            'INVALID_USER',
            PASSWORD,
            HOST,
            loglevel=LOGLEVEL,
        )
        print str(sw)
        self.assertTrue(sw.app_ok)

    @unittest.expectedFailure
    def test_nossl(self):
        '''tests HTTP port using HTTPS on host with no tanium'''
        print ""
        sw = tanwrap.SoapWrap(
            'user',
            'password',
            '127.0.0.1',
            port=4433,
            protocol='https',
            loglevel=LOGLEVEL,
        )
        print str(sw)
        self.assertTrue(sw.app_ok)

    @unittest.expectedFailure
    def test_badhost(self):
        '''tests HTTP port using HTTP on host with no tanium'''
        print ""
        sw = tanwrap.SoapWrap(
            'user',
            'password',
            '127.0.0.1',
            port=4433,
            protocol='http',
            loglevel=LOGLEVEL,
        )
        print sw
        self.assertTrue(sw.app_ok)

    @unittest.expectedFailure
    def test_nonhost(self):
        '''tests accessing a server and port that does not exist at all'''
        print ""
        sw = tanwrap.SoapWrap(
            'user',
            'password',
            '1.1.1.1',
            port=4433,
            protocol='https',
            loglevel=LOGLEVEL,
        )
        print sw
        self.assertTrue(sw.app_ok)


class TestsAgainstServer(unittest.TestCase):
    print "### TestsAgainstServer setup START"
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
    print "### TestsAgainstServer setup END"

    def setUp(self):
        self.assertTrue(self.sw.app_ok)

    def response_tests(self, response):
        '''standard tests for any response object'''
        print "RESPONSE: %s\n" % response
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

        self.assertTrue(response.session_id)
        self.assertTrue(response.inner_dict_xml)
        self.assertTrue(response.csv)
        self.assertTrue(response.check_everything_ok())

        response.write_csv_file(dir=CSV_OUT)
        self.assertIsNotNone(response.csv_path)
        self.assertTrue(os.path.isfile(response.csv_path))

    def test_ask_saved_question_single_str(self):
        print ""
        sw = self.sw
        q = 'Installed Applications'
        response = sw.ask_saved_question(q)
        self.response_tests(response)

    def test_ask_saved_question_single_list(self):
        print ""
        sw = self.sw
        q = 'Installed Applications'
        response = sw.ask_saved_question([q])
        self.response_tests(response)

    def test_ask_parsed_question(self):
        print ""
        sw = self.sw
        q = 'Get Installed Applications from All Machines'
        response = sw.ask_parsed_question(q)
        self.response_tests(response)

    @unittest.expectedFailure
    def test_ask_parsed_question_invalid_picker(self):
        print ""
        sw = self.sw
        q = 'Get Installed Applications from All Machines'
        picker = 99999
        response = sw.ask_parsed_question(q, picker)
        self.response_tests(response)

    def test_ask_parsed_question_forced_picker0(self):
        print ""
        sw = self.sw
        q = 'Get Installed Applications from All Machines'
        picker = 0
        response = sw.ask_parsed_question(q, picker)
        self.response_tests(response)

    def test_ask_parsed_question_forced_picker1(self):
        print ""
        sw = self.sw
        q = 'Get Installed Applications from All Machines'
        picker = 1
        response = sw.ask_parsed_question(q, picker)
        self.response_tests(response)

    def test_ask_parsed_question_picker_list(self):
        print ""
        sw = self.sw
        q = 'Get Installed Applications from All Machines'
        picker = -1
        response = sw.ask_parsed_question(q, picker)
        self.assertIsNotNone(response)
        self.assertTrue(response.prgs_all)

    def test_get_single_sensor(self):
        print ""
        sw = self.sw
        q = 'Computer Name'
        response = sw.get_sensor(q)
        self.response_tests(response)

    def test_get_single_sensor_by_name(self):
        print ""
        sw = self.sw
        q = 'name:Computer Name'
        response = sw.get_sensor(q)
        self.response_tests(response)

    def test_get_single_sensor_by_id(self):
        print ""
        sw = self.sw
        q = 'id:1'
        response = sw.get_sensor(q)
        self.response_tests(response)

    def test_get_single_sensor_by_hash(self):
        print ""
        sw = self.sw
        q = 'hash:322086833'
        response = sw.get_sensor(q)
        self.response_tests(response)

    def test_get_multiple_sensors(self):
        print ""
        sw = self.sw
        q = ['Computer Name', 'Action Statuses']
        response = sw.get_sensor(q)
        self.response_tests(response)

    def test_get_multiple_sensors_selectors(self):
        print ""
        sw = self.sw
        q = ['name:Computer Name', 'id:1', 'hash:322086833']
        response = sw.get_sensor(q)
        self.response_tests(response)

    def test_get_all_sensors(self):
        print ""
        sw = self.sw
        response = sw.get_all_sensors()
        self.response_tests(response)

    def test_get_all_saved_questions(self):
        sw = self.sw
        response = sw.get_all_saved_questions()
        self.response_tests(response)

    def test_get_saved_question_single(self):
        print ""
        sw = self.sw
        q = 'Installed Applications'
        response = sw.get_saved_question(q)
        self.response_tests(response)

    def test_get_saved_question_multiple(self):
        print ""
        sw = self.sw
        q = ['Installed Applications', 'Computer Name']
        response = sw.get_saved_question(q)
        self.response_tests(response)

    def test_get_all_question_logs(self):
        print ""
        sw = self.sw
        response = sw.get_all_question_logs()
        self.response_tests(response)

    def test_get_question_log(self):
        print ""
        sw = self.sw
        response = sw.get_question_log('1')
        self.response_tests(response)

    def test_get_package_single(self):
        print ""
        sw = self.sw
        q = 'Distribute Patch Tools'
        response = sw.get_package(q)
        self.response_tests(response)

    def test_get_all_packages(self):
        print ""
        sw = self.sw
        response = sw.get_all_packages()
        self.response_tests(response)

    def test_get_all_groups(self):
        print ""
        sw = self.sw
        response = sw.get_all_groups()
        self.response_tests(response)

    def test_get_group_single(self):
        print ""
        sw = self.sw
        q = 'All Computers'
        response = sw.get_group(q)
        self.response_tests(response)

    def test_get_all_actions(self):
        print ""
        sw = self.sw
        response = sw.get_all_actions()
        self.response_tests(response)

    def test_get_action_single_by_id(self):
        print ""
        sw = self.sw
        q = '1'
        response = sw.get_action(q)
        self.response_tests(response)

    @unittest.expectedFailure
    def test_get_action_single_by_name(self):
        print ""
        sw = self.sw
        q = 'Distribute Tanium Standard Utilities'
        response = sw.get_action(q)
        self.response_tests(response)

    @unittest.expectedFailure
    def test_get_question_log_fail_invalid_id(self):
        print ""
        sw = self.sw
        response = sw.get_question_log('n')
        self.response_tests(response)

    @unittest.expectedFailure
    def test_get_question_log_fail_by_name(self):
        print ""
        sw = self.sw
        response = sw.get_question_log('name:fail')
        self.response_tests(response)

    @unittest.expectedFailure
    def test_bad_ask_saved_question(self):
        print ""
        sw = self.sw
        q = ['Installed Applications', 'id:0']
        response = sw.ask_saved_question(q)
        self.response_tests(response)

if __name__ == "__main__":
    unittest.main(verbosity=2)
