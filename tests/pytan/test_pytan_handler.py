#!/usr/bin/env python -ttB

import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import glob
import copy
import unittest
import json

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
root_dir = os.path.join(my_dir, os.pardir, os.pardir)
root_dir = os.path.abspath(root_dir)
path_adds = [my_dir, root_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

import pytan
from testlib import threaded_http
from testlib import ddt

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


def spew(m):
    if TESTVERBOSITY == 2:
        print (m)


# where the output files from the tests will be stored
TEST_OUT = os.path.join(my_dir, 'TEST_OUT')

if not os.path.isdir(TEST_OUT):
    os.mkdir(TEST_OUT)

test_files = glob.glob(TEST_OUT + '/*.*')
if test_files:
    spew("Cleaning up %s old test files" % len(test_files))
    [os.unlink(x) for x in test_files]


@ddt.ddt
class InvalidServerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__http = threaded_http.threaded_http(
            port=4433, verbosity=TESTVERBOSITY
        )

    @ddt.file_data('ddt/ddt_invalid_connects.json')
    def test_invalid_connect(self, value):

        args = value['args']
        exc = eval(value['exception'])
        e = value['error_str']

        mykwargs = copy.copy(SERVER_INFO)
        mykwargs.update(args)

        spew("")
        spew("+++ TESTING EXPECTED FAILURE Handler() with kwargs %s" % (
            mykwargs))
        with self.assertRaisesRegexp(exc, e):
            pytan.Handler(**mykwargs)


class ExportObjTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handler = pytan.Handler(**SERVER_INFO)
        spew('\n' + str(cls.handler))

    def setup_test(self):
        spew("")
        return self.handler

    def test_export_basetype(self):
        handler = self.setup_test()
        sensors = [
            "Computer Name", "IP Route Details", "IP Address",
            'Folder Name Search with RegEx Match',
        ]
        r1 = handler.get('sensor', name=sensors)
        self.assertTrue(r1)
        self.assertIsInstance(r1, pytan.api.BaseType)
        self.assertEquals(len(r1), 4)

        # CSV
        a1 = {'obj': r1, 'export_format': 'csv'}

        r_def_opts = handler.export_obj(**a1)
        r_explode_false = handler.export_obj(
            explode_json_string_values=False, **a1
        )
        r_sort_empty = handler.export_obj(header_sort=[], **a1)
        r_sort_true = handler.export_obj(header_sort=True, **a1)

        self.assertIn(
            'parameter_definition', r_def_opts.splitlines()[0].split(',')
        )
        self.assertEqual(
            'category', r_def_opts.splitlines()[0].split(',')[0]
        )

        self.assertEqual(r_explode_false, r_def_opts)
        self.assertEqual(r_sort_empty, r_def_opts)
        self.assertEqual(r_sort_true, r_def_opts)

        r_sort_false = handler.export_obj(header_sort=False, **a1)
        self.assertEqual(
            r_sort_false.splitlines()[0].split(',')[0],
            'subcolumns_subcolumn_3_hidden_flag'
        )

        r_sort = handler.export_obj(
            header_sort=['name', 'description'], **a1
        )
        self.assertEqual(
            ['name', 'description'],
            r_sort.splitlines()[0].split(',')[0:2]
        )

        r_explode_true = handler.export_obj(
            explode_json_string_values=True, **a1
        )
        self.assertIn(
            'parameter_definition_parameters_0_defaultValue',
            r_explode_true.splitlines()[0].split(','),
        )

        e = ".*must be one of.*you supplied.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(header_sort='bad', **a1)

        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(explode_json_string_values='bad', **a1)

        e = ".*must be a list of.*you supplied.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(header_sort=[list()], **a1)

        # JSON TESTS
        a1 = {'obj': r1, 'export_format': 'json'}

        r_def_opts = handler.export_obj(**a1)
        r_type_true = handler.export_obj(include_type=True, **a1)
        r_explode_false = handler.export_obj(
            explode_json_string_values=False, **a1
        )
        r_json = json.loads(r_def_opts)
        self.assertIn('_type', r_json)
        self.assertIn('sensor', r_json)
        self.assertEqual(r_json['sensor'][0]['name'], 'Computer Name')
        self.assertTrue(isinstance(
            r_json['sensor'][3]['parameter_definition'], (unicode, str)
        ))
        self.assertEqual(r_def_opts, r_type_true)
        self.assertEqual(r_def_opts, r_explode_false)

        r_type_false = handler.export_obj(include_type=False, **a1)
        r_json = json.loads(r_type_false)
        self.assertNotIn('_type', r_json)

        e = ".*must be one of.*you supplied.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(explode_json_string_values='bad', **a1)

        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(include_type='bad', **a1)

        # XML TESTS
        a1 = {'obj': r1, 'export_format': 'xml'}

        r_def_opts = handler.export_obj(**a1)
        r_min_false = handler.export_obj(minimal=False, **a1)
        self.assertTrue(r_def_opts.startswith('<sensors><cache_info />'))
        self.assertEqual(r_def_opts, r_min_false)

        r_min_true = handler.export_obj(minimal=True, **a1)
        self.assertTrue(r_min_true.startswith('<sensors><sensor><category>'))

    def test_export_resultset(self):
        handler = self.setup_test()
        r1_sensors = ["Computer Name", "IP Route Details", "IP Address"]
        r1 = handler.ask(qtype="manual_human", sensors=r1_sensors)
        r2_sensors = [
            'Folder Name Search with RegEx Match{dirname=Program Files,'
            'regex=.*}'
        ]
        r2 = handler.ask(qtype="manual_human", sensors=r2_sensors)
        self.assertTrue(r1)
        self.assertIsInstance(r1, pytan.api.ResultSet)
        self.assertGreaterEqual(len(r1.rows), 1)
        self.assertGreaterEqual(len(r1.columns), 1)
        self.assertTrue(r2)
        self.assertIsInstance(r2, pytan.api.ResultSet)
        self.assertGreaterEqual(len(r2.rows), 1)
        self.assertGreaterEqual(len(r2.columns), 1)

        # CSV TESTS
        a1 = {'obj': r1, 'export_format': 'csv'}
        a2 = {'obj': r2, 'export_format': 'csv'}

        r_def_opts = handler.export_obj(**a1)
        r_sort_empty = handler.export_obj(header_sort=[], **a1)
        r_sort_true = handler.export_obj(header_sort=True, **a1)
        r_type_false = handler.export_obj(header_add_type=False, **a1)
        r_sensor_false = handler.export_obj(header_add_sensor=False, **a1)
        r_expand_false = handler.export_obj(expand_grouped_columns=False, **a1)
        r_nonopt = handler.export_obj(invalid_option='', **a1)

        def_exp = (
            'Computer Name,Destination,Flags,Gateway,IP Address,Interface,'
            'Mask,Metric'
        )
        self.assertEqual(r_def_opts.splitlines()[0], def_exp)
        self.assertEqual(r_sort_empty, r_def_opts)
        self.assertEqual(r_sort_true, r_def_opts)
        self.assertEqual(r_type_false, r_def_opts)
        self.assertEqual(r_sensor_false, r_def_opts)
        self.assertEqual(r_expand_false, r_def_opts)
        self.assertEqual(r_nonopt, r_def_opts)

        r_expand_true = handler.export_obj(expand_grouped_columns=True, **a1)
        self.assertIn('UNRELATED TO IP Address', r_expand_true)

        r_sort_false = handler.export_obj(header_sort=False, **a1)
        sort_false_exp = (
            'Computer Name,Destination,Gateway,Mask,Flags,Metric,Interface,'
            'IP Address'
        )
        self.assertEqual(r_sort_false.splitlines()[0], sort_false_exp)

        r_sort = handler.export_obj(
            header_sort=['Computer Name', 'IP Address'], **a1
        )
        self.assertEqual(
            ['Computer Name', 'IP Address'],
            r_sort.splitlines()[0].split(',')[0:2]
        )

        r_type_true = handler.export_obj(header_add_type=True, **a1)
        self.assertIn(
            'Computer Name (String)',
            r_type_true.splitlines()[0].split(',')
        )

        r1_sensor_true = handler.export_obj(header_add_sensor=True, **a1)
        r2_sensor_true = handler.export_obj(
            header_add_sensor=True, sensors=[], **a1
        )
        self.assertIn(
            'Computer Name: Computer Name',
            r1_sensor_true.splitlines()[0].split(',')
        )
        self.assertEqual(r2_sensor_true, r1_sensor_true)

        # test that sensor with params gets handled properly
        r2_sensor_true = handler.export_obj(header_add_sensor=True, **a2)
        exp = (
            '"Folder Name Search with RegEx Match[No, Program Files, No, ]: '
            'Folder Name Search with RegEx Match[No, Program Files, No, ]"'
        )
        self.assertEquals(
            exp, r2_sensor_true.splitlines()[0]
        )

        r1_all_opts = handler.export_obj(
            header_add_sensor=True,
            header_add_type=True,
            expand_grouped_columns=True,
            header_sort=['Computer Name', 'IP Address'],
            **a1
        )
        exp = (
            'Computer Name: Computer Name (String),IP Address: IP Address'
            ' (IPAddress),IP Route Details: Destination (IPAddress),IP'
            ' Route Details: Flags (String),IP Route Details: Gateway '
            '(IPAddress),IP Route Details: Interface (String),IP Route '
            'Details: Mask (String),IP Route Details: Metric (NumericInteger)'
        )
        self.assertEqual(exp, r1_all_opts.splitlines()[0])

        e = '.*not a supported object to export, must be one of.*'
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(obj=list(), export_format='csv')

        e = '.*not a supported export format for ResultSet, must be one of.*'
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(obj=r1, export_format='test')

        e = ".*must be one of.*you supplied.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(header_sort='bad', **a1)

        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(expand_grouped_columns='bad', **a1)

        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(header_add_type='bad', **a1)

        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(header_add_sensor='bad', **a1)

        e = ".*must be a list of.*you supplied.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(
                header_add_sensor=True, sensors=[list()], **a1
            )

        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.export_obj(header_sort=[list()], **a1)

        # JSON TESTS
        a1 = {'obj': r1, 'export_format': 'json'}

        r_def_opts = handler.export_obj(**a1)
        r_json = json.loads(r_def_opts)
        self.assertEquals(
            r_json[0]['row0'][0]['column.display_name'], 'Computer Name'
        )


@ddt.ddt
class ValidServerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.handler = pytan.Handler(**SERVER_INFO)
        spew('\n' + str(cls.handler))

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
        self.assertIsInstance(response, pytan.api.ResultSet)
        self.assertGreaterEqual(len(response.rows), 1)
        self.assertGreaterEqual(len(response.columns), 1)
        for ft in pytan.constants.EXPORT_MAPS['ResultSet'].keys():
            report_file, result = handler.export_to_report_file(
                obj=response, export_format=ft, report_dir=TEST_OUT,
            )
            self.assertTrue(report_file)
            self.assertTrue(result)
            self.assertTrue(os.path.isfile(report_file))
            self.assertGreaterEqual(len(result), 10)

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
        self.assertIsInstance(response, pytan.api.BaseType)
        for x in tests:
            self.assertTrue(eval(x))

        for ft in pytan.constants.EXPORT_MAPS['BaseType'].keys():
            report_file, result = handler.export_to_report_file(
                obj=response, export_format=ft, report_dir=TEST_OUT,
            )
            self.assertTrue(report_file)
            self.assertTrue(result)
            self.assertTrue(os.path.isfile(report_file))
            self.assertGreaterEqual(len(result), 10)

    @ddt.file_data('ddt/ddt_invalid_questions.json')
    def test_invalid_question(self, value):
        handler = self.setup_test()

        method = value['method']
        args = value['args']
        exc = eval(value['exception'])
        e = value['error_str']

        s = (
            "+++ TESTING EXPECTED QUESTION FAILURE Handler.{}() with kwargs {}"
        ).format
        spew(s(method, args))

        with self.assertRaisesRegexp(exc, e):
            getattr(handler, method)(**args)

    @ddt.file_data('ddt/ddt_invalid_get_object.json')
    def test_invalid_get_object(self, value):
        handler = self.setup_test()

        method = value['method']
        args = value['args']
        exc = eval(value['exception'])
        e = value['error_str']

        s = (
            "+++ TESTING EXPECTED GET FAILURE Handler.{}() with kwargs {}"
        ).format
        spew(s(method, args))

        with self.assertRaisesRegexp(exc, e):
            getattr(handler, method)(**args)


if __name__ == "__main__":
    unittest.main(
        verbosity=TESTVERBOSITY,
        failfast=FAILFAST,
        catchbreak=CATCHBREAK)
