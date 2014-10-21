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

    # jims server info
    USERNAME = 'Jim Olsen'
    PASSWORD = 'Evinc3d!'
    HOST = '172.16.31.128'

    def setUp(self):
        if not os.path.isdir(CSV_OUT):
            os.mkdir(CSV_OUT)

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
    def test_bad_ask_saved_question(self):
        '''response from asking a saved question with multiple sensors'''
        q = ['Installed Applications', 'id:0']
        response = self.sw.ask_saved_question(q)
        self.assertNotEqual(None, response)

    def response_tests(self, response):
        '''standard tests for any response object

        - response.request.build_xml() returns something that has:
          * auth or session in it
          * command in it
          * object-list in it
        - response.request.command is not empty
        - response.status_code is 200
        - response.text is not empty
        - response.csv is not empty
        - response.write_csv_file() produces a non-empty file and
            does not return False
        '''
        self.assertIsNotNone(response)
        self.assertTrue(response.request.xml_raw)
        self.assertIn('<command>', response.request.xml_raw)
        self.assertIn('<object_list>', response.request.xml_raw)
        auth = '<auth>' in response.request.xml_raw
        session = '<session>' in response.request.xml_raw
        self.assertTrue(auth or session)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text)
        self.assertTrue(response.xml_raw)
        self.assertTrue(response.csv)
        response.write_csv_file(dir=CSV_OUT)
        self.assertIsNotNone(response.csv_path)
        self.assertTrue(os.path.isfile(response.csv_path))

    def test_ask_saved_question_single_str(self):
        '''response from asking a saved question with single sensor as str'''
        q = 'Installed Applications'
        response = self.sw.ask_saved_question(q)
        self.response_tests(response)

    def test_ask_saved_question_single_list(self):
        '''response from asking a saved question with single sensor as list'''
        q = 'Installed Applications'
        response = self.sw.ask_saved_question([q])
        self.response_tests(response)

    def test_get_single_sensor(self):
        '''response from getobject for single sensor'''
        q = 'Computer Name'
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_single_sensor_by_name(self):
        '''response from getobject for single sensor by name:'''
        q = 'name:Computer Name'
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_single_sensor_by_id(self):
        '''response from getobject for single sensor by id:'''
        q = 'id:1'
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_single_sensor_by_hash(self):
        '''response from getobject for single sensor by hash:'''
        q = 'hash:322086833'
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_multiple_sensors(self):
        '''response from getobject for multiple sensors'''
        q = ['Computer Name', 'Action Statuses']
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_multiple_sensors_selectors(self):
        '''response from getobject for multiple sensors with selectors'''
        q = ['name:Computer Name', 'id:1', 'hash:322086833']
        response = self.sw.get_sensor(q)
        self.response_tests(response)

    def test_get_all_sensors(self):
        '''response from getobject for all sensors'''
        response = self.sw.get_all_sensors()
        self.response_tests(response)

    def test_get_all_saved_questions(self):
        '''response from getobject for all saved questions'''
        response = self.sw.get_all_saved_questions()
        self.response_tests(response)

    def test_get_saved_question_single(self):
        '''response from getobject for single saved question'''
        q = 'Installed Applications'
        response = self.sw.get_saved_question(q)
        self.response_tests(response)

    def test_get_saved_question_multiple(self):
        '''response from getobject for multiple saved questions'''
        q = ['Installed Applications', 'Computer Name']
        response = self.sw.get_saved_question(q)
        self.response_tests(response)

    def test_get_all_questions_log(self):
        '''response from getobject for all questions that have been asked'''
        response = self.sw.get_all_questions_log()
        self.response_tests(response)

    def test_get_question_log(self):
        '''response from getobject for all questions that have been asked'''
        response = self.sw.get_question_log('1')
        self.response_tests(response)

    def test_get_question_log1(self):
        '''response from getobject for all questions that have been asked'''
        response = self.sw.get_question_log('n')
        self.response_tests(response)

if __name__ == "__main__":
    unittest.main(verbosity=2)
