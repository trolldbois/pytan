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
root_dir = os.path.join(my_dir, os.pardir)
root_dir = os.path.abspath(root_dir)
path_adds = [my_dir, root_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

import pytan
from random import randint
from testlib import threaded_http
from testlib import ddt

# control the amount of output from unittests
TESTVERBOSITY = 2

# have unittest exit immediately on unexpected error
FAILFAST = True

# catch control-C to allow current test suite to finish (press 2x to force)
CATCHBREAK = True

SERVER_INFO = {
    "username": "Tanium User",
    "password": "T@n!um",
    "host": "172.16.31.128",
    "port": "444",
    "loglevel": TESTVERBOSITY,
    "debugformat": False,
}


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


class CreateObjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handler = pytan.Handler(**SERVER_INFO)
        spew('\n' + str(cls.handler))

    def setup_test(self):
        spew("")
        return self.handler

    def test_create_sensor(self):
        handler = self.setup_test()
        e = "Sensor creation not supported via PyTan as of yet, too complex.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.create_sensor()

    def test_create_package(self):
        handler = self.setup_test()
        kwargs = {
            'name': 'die49',
            'command': 'die49 $1 $2 $3 $4 $5 $6 $7 $8',
            'display_name': 'die49 test',
            'command_timeout_seconds': 9999,
            'expire_seconds': 1500,
            'parameters_json_file': os.path.join(
                root_dir,
                'doc/example_of_all_package_parameters.json'
            ),
            'file_urls': [
                '3600::testing.vbs||https://content.tanium.com/files/'
                'initialcontent/bundles/2014-10-01_11-32-15-7844/'
                'custom_tagging_-_remove_tags_[non-windows]/CustomTagRemove.sh'
            ],
            'verify_filters': ['Custom Tags, that contains tag'],
            'verify_filter_options': ['and'],
            'verify_expire_seconds': 3600,
        }

        try:
            handler.delete('package', name=kwargs['name'])
        except:
            pass

        package_obj = handler.create_package(**kwargs)
        self.assertIsInstance(package_obj, pytan.api.PackageSpec)
        self.assertTrue(package_obj.verify_group_id)
        self.assertEquals(package_obj.name, kwargs['name'])
        self.assertEquals(package_obj.command, kwargs['command'])
        self.assertEquals(package_obj.display_name, kwargs['display_name'])
        self.assertEquals(
            package_obj.command_timeout, kwargs['command_timeout_seconds']
        )
        self.assertEquals(package_obj.expire_seconds, kwargs['expire_seconds'])
        pd = json.loads(package_obj.parameter_definition)
        params = pd['parameters']
        self.assertEquals(len(params), 8)
        self.assertIsInstance(package_obj.files, pytan.api.PackageFileList)
        for x in package_obj.files:
            self.assertIsInstance(x, pytan.api.PackageFile)
        self.assertEquals(
            package_obj.files[0].source,
            'https://content.tanium.com/files/'
            'initialcontent/bundles/2014-10-01_11-32-15-7844/'
            'custom_tagging_-_remove_tags_[non-windows]/CustomTagRemove.sh',
        )
        self.assertEquals(package_obj.files[0].download_seconds, 3600)
        self.assertEquals(package_obj.files[0].name, 'testing.vbs')

        delete_obj = handler.delete('package', name=package_obj.name)
        for x in delete_obj:
            self.assertIsInstance(x, pytan.api.PackageSpec)

    def test_create_group(self):
        handler = self.setup_test()
        kwargs = {
            'groupname': 'All Windows Computers API Test',
            'filters': ['Operating System, that contains WIndows'],
            'filter_options': ['and'],
        }

        try:
            handler.delete('group', name=kwargs['groupname'])
        except:
            pass

        group_obj = handler.create_group(**kwargs)
        self.assertIsInstance(group_obj, pytan.api.Group)
        self.assertIsInstance(group_obj.filters, pytan.api.FilterList)
        for x in group_obj.filters:
            self.assertIsInstance(x, pytan.api.Filter)
            self.assertIsInstance(x.sensor, pytan.api.Sensor)
        self.assertTrue(group_obj.text)
        self.assertEquals(group_obj.and_flag, 1)

        delete_obj = handler.delete('group', name=group_obj.name)
        for x in delete_obj:
            self.assertIsInstance(x, pytan.api.Group)

    def test_create_user(self):
        handler = self.setup_test()
        kwargs = {
            'username': 'API Test User',
            'rolename': 'Administrator',
            'properties': [['property1', 'value1']],
        }

        try:
            handler.delete('user', name=kwargs['username'])
        except:
            pass

        user_obj = handler.create_user(**kwargs)
        self.assertIsInstance(user_obj, pytan.api.User)
        self.assertIsInstance(user_obj.roles, pytan.api.UserRoleList)
        for x in user_obj.roles:
            self.assertIsInstance(x, pytan.api.UserRole)
            self.assertEquals(x.name, 'Administrator')

        self.assertIsInstance(user_obj.metadata, pytan.api.MetadataList)
        for x in user_obj.metadata:
            self.assertIsInstance(x, pytan.api.MetadataItem)
        self.assertEquals(
            user_obj.metadata[0].name, 'TConsole.User.Property.property1'
        )
        self.assertEquals(
            user_obj.metadata[0].value, 'value1'
        )

        self.assertEquals(user_obj.name, kwargs['username'])
        delete_obj = handler.delete('user', name=user_obj.name)
        for x in delete_obj:
            self.assertIsInstance(x, pytan.api.User)

    def test_create_whitelisted_url(self):
        handler = self.setup_test()
        kwargs = {
            'url': 'http://test.com/.*API_Test.*URL',
            'regex': True,
            'download_seconds': 3600,
            'properties': [['property1', 'value1']],
        }

        try:
            handler.delete(
                'whitelisted_url',
                url_regex='regex:%s' % kwargs['url'])
        except:
            pass

        whitelisted_url_obj = handler.create_whitelisted_url(**kwargs)
        self.assertIsInstance(whitelisted_url_obj, pytan.api.WhiteListedUrl)
        self.assertIsInstance(
            whitelisted_url_obj.metadata, pytan.api.MetadataList
        )
        for x in whitelisted_url_obj.metadata:
            self.assertIsInstance(x, pytan.api.MetadataItem)
        self.assertEquals(
            whitelisted_url_obj.metadata[0].name,
            'TConsole.WhitelistedURL.property1'
        )
        self.assertEquals(
            whitelisted_url_obj.metadata[0].value, 'value1'
        )

        self.assertEquals(
            whitelisted_url_obj.url_regex,
            'regex:%s' % kwargs['url']
        )
        delete_obj = handler.delete(
            'whitelisted_url',
            url_regex=whitelisted_url_obj.url_regex
        )
        for x in delete_obj:
            self.assertIsInstance(x, pytan.api.WhiteListedUrl)


class CreateObjFromJsonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handler = pytan.Handler(**SERVER_INFO)
        spew('\n' + str(cls.handler))

    def setup_test(self):
        spew("")
        return self.handler

    def test_create_from_json_action(self):
        handler = self.setup_test()
        # adding a new action ("redeploying it")
        orig_objs = handler.get('action', id=1)
        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        new_obj = handler.create_from_json('action', json_file)
        self.assertIsInstance(new_obj, pytan.api.ActionList)
        for x in new_obj:
            self.assertIsInstance(x, pytan.api.Action)

    def test_create_from_json_client(self):
        handler = self.setup_test()
        # client not supported:
        orig_objs = handler.get('client', status='Leader')
        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        e = ".*is not a json createable object! Supported objects.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.create_from_json('client', json_file)

    def test_create_from_json_sensor(self):
        handler = self.setup_test()
        # adding and deleting a new sensor
        orig_objs = handler.get('sensor', name="IP Route Details")
        for x in orig_objs:
            x.name += " API TEST"
            # make sure the test object is gone before we create it
            try:
                handler.delete('sensor', name=x.name)
            except:
                pass
        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        new_obj = handler.create_from_json('sensor', json_file)
        self.assertIsInstance(new_obj, pytan.api.SensorList)
        for x in new_obj:
            self.assertIsInstance(x, pytan.api.Sensor)
            delete_obj = handler.delete('sensor', name=x.name)
            for i in delete_obj:
                self.assertIsInstance(i, pytan.api.Sensor)

    def test_create_from_json_group(self):
        handler = self.setup_test()
        # adding and deleting a new group
        orig_objs = handler.get('group', name="All Computers")
        for x in orig_objs:
            x.name += " API TEST"
            # make sure the test object is gone before we create it
            try:
                handler.delete('group', name=x.name)
            except:
                pass
        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        new_obj = handler.create_from_json('group', json_file)
        self.assertIsInstance(new_obj, pytan.api.GroupList)
        for x in new_obj:
            self.assertIsInstance(x, pytan.api.Group)
            delete_obj = handler.delete('group', name=x.name)
            for i in delete_obj:
                self.assertIsInstance(i, pytan.api.Group)

    def test_create_from_json_package(self):
        handler = self.setup_test()
        # adding and deleting a new package
        orig_objs = handler.get('package', name="Custom Tagging - Add Tags")
        for x in orig_objs:
            x.name += " API TEST"
            # make sure the test object is gone before we create it
            try:
                handler.delete('package', name=x.name)
            except:
                pass

        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        new_obj = handler.create_from_json('package', json_file)
        self.assertIsInstance(new_obj, pytan.api.PackageSpecList)
        for x in new_obj:
            self.assertIsInstance(x, pytan.api.PackageSpec)
            delete_obj = handler.delete('package', name=x.name)
            for i in delete_obj:
                self.assertIsInstance(i, pytan.api.PackageSpec)

    def test_create_from_json_question(self):
        handler = self.setup_test()
        # adding a new question
        orig_objs = handler.get('question', id=1)
        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        new_obj = handler.create_from_json('question', json_file)
        self.assertIsInstance(new_obj, pytan.api.QuestionList)
        for x in new_obj:
            self.assertIsInstance(x, pytan.api.Question)

    def test_create_from_json_saved_action(self):
        handler = self.setup_test()
        # saved_action does not work (AddObject returns nothing, ??)
        orig_objs = handler.get(
            'saved_action', name="Distribute Tanium Standard Utilities"
        )
        for x in orig_objs:
            x.name += " API TEST"
        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        e = ".*is not a json createable object! Supported objects.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.create_from_json('saved_action', json_file)

    def test_create_from_json_saved_question(self):
        handler = self.setup_test()
        # adding and deleting a saved_question
        orig_objs = handler.get(
            'saved_question', name="Computer Name"
        )
        for x in orig_objs:
            x.name += " API TEST"
            # make sure the test object is gone before we create it
            try:
                handler.delete('saved_question', name=x.name)
            except:
                pass
        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        new_obj = handler.create_from_json('saved_question', json_file)
        self.assertIsInstance(new_obj, pytan.api.SavedQuestionList)
        for x in new_obj:
            self.assertIsInstance(x, pytan.api.SavedQuestion)
            delete_obj = handler.delete('saved_question', name=x.name)
            for i in delete_obj:
                self.assertIsInstance(i, pytan.api.SavedQuestion)

    def test_create_from_json_setting(self):
        handler = self.setup_test()
        # setting not supported:
        orig_objs = handler.get('setting', id='1')
        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        e = ".*is not a json createable object! Supported objects.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.create_from_json('setting', json_file)

    def test_create_from_json_user(self):
        handler = self.setup_test()
        # adding and deleting a user
        orig_objs = handler.get('user', id=1)
        for x in orig_objs:
            x.name += " API TEST"
            # make sure the test object is gone before we create it
            try:
                handler.delete('user', name=x.name)
            except:
                pass

        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        new_obj = handler.create_from_json('user', json_file)
        self.assertIsInstance(new_obj, pytan.api.UserList)
        for x in new_obj:
            self.assertIsInstance(x, pytan.api.User)
            delete_obj = handler.delete('user', name=x.name)
            for i in delete_obj:
                self.assertIsInstance(i, pytan.api.User)

    def test_create_from_json_userrole(self):
        handler = self.setup_test()
        # userrole not supported:
        orig_objs = handler.get('userrole', name='Administrator')
        json_file, results = handler.export_to_report_file(
            obj=orig_objs,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        e = ".*is not a json createable object! Supported objects.*"
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.create_from_json('userrole', json_file)

    def test_create_from_json_whitelisted_url(self):
        handler = self.setup_test()
        # adding and deleting a whitelisted_url
        orig_obj = handler.get_all('whitelisted_url')[0]
        orig_obj.url_regex += " API TEST"
        json_file, results = handler.export_to_report_file(
            obj=orig_obj,
            export_format='json',
            report_dir=TEST_OUT,
            prefix=sys._getframe().f_code.co_name + '_',
        )
        # make sure the test object is gone before we create it
        try:
            handler.delete('whitelisted_url', url_regex=orig_obj.url_regex)
        except:
            pass

        new_obj = handler.create_from_json('whitelisted_url', json_file)
        self.assertIsInstance(new_obj, pytan.api.WhiteListedUrlList)
        for x in new_obj:
            self.assertIsInstance(x, pytan.api.WhiteListedUrl)
            delete_obj = handler.delete(
                'whitelisted_url', url_regex=orig_obj.url_regex
            )
            for i in delete_obj:
                self.assertIsInstance(i, pytan.api.WhiteListedUrl)


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
        r1_ret = handler.ask(qtype="manual_human", sensors=r1_sensors)
        r1 = r1_ret['question_results']
        r2_sensors = [
            'Folder Name Search with RegEx Match{dirname=Program Files,'
            'regex=.*}'
        ]
        r2_ret = handler.ask(qtype="manual_human", sensors=r2_sensors)
        r2 = r2_ret['question_results']
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
            '.*"Folder Name Search with RegEx Match\[No, Program Files, No, '
            '\]: Folder Name Search with RegEx Match\[No, Program Files, No, '
            '\]".*'
        )
        self.assertRegexpMatches(
            r2_sensor_true.splitlines()[0], exp
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
        # create whitelisted_url for getobject tests
        try:
            cls.handler.create_whitelisted_url(url='test1')
            cls.handler.create_whitelisted_url(url='test2')
            cls.handler.create_whitelisted_url(url='test3')
        except:
            pass

        spew('\n' + str(cls.handler))

    def setup_test(self):
        spew("")
        return self.handler

    def test_valid_deploy_action(self):
        handler = self.setup_test()
        action_filters = ['Operating System, that contains Windows']
        action_options = ['and']

        tag_num = randint(100, 999)
        package = (
            'Custom Tagging - Add Tags{$1=tag_should_be_added_%s,$2=tag_should'
            'be_ignored}'
        ) % tag_num

        ret = handler.deploy_action_human(
            action_filters=action_filters,
            action_options=action_options,
            package=package,
            run=True,
            report_dir=TEST_OUT,
        )
        self.assertIsInstance(ret['action_object'], pytan.api.Action)
        self.assertTrue(ret['action_progress_human'])
        self.assertTrue(ret['action_progress_map'])
        self.assertTrue(ret['pre_action_question_results'])
        self.assertIsInstance(ret['action_results'], pytan.api.ResultSet)
        self.assertGreaterEqual(len(ret['action_results'].rows), 1)
        self.assertGreaterEqual(len(ret['action_results'].columns), 1)
        for ft in pytan.constants.EXPORT_MAPS['ResultSet'].keys():
            report_file, result = handler.export_to_report_file(
                obj=ret['action_results'],
                export_format=ft,
                report_dir=TEST_OUT,
                prefix=sys._getframe().f_code.co_name + '_',
            )
            self.assertTrue(report_file)
            self.assertTrue(result)
            self.assertTrue(os.path.isfile(report_file))
            self.assertGreaterEqual(len(result), 10)

    def test_valid_deploy_action_no_results(self):
        handler = self.setup_test()
        action_filters = ['Operating System, that contains Windows']
        action_options = ['and']

        tag_num = randint(100, 999)
        package = (
            'Custom Tagging - Add Tags{$1=tag_should_be_added_%s,$2=tag_should'
            'be_ignored}'
        ) % tag_num

        ret = handler.deploy_action_human(
            action_filters=action_filters,
            action_options=action_options,
            package=package,
            run=True,
            get_results=False,
        )
        self.assertIsInstance(ret['action_object'], pytan.api.Action)
        self.assertTrue(ret['pre_action_question_results'])

    def test_deploy_action_no_run(self):
        handler = self.setup_test()
        action_filters = ['Operating System, that contains Windows']
        action_options = ['and']

        tag_num = randint(100, 999)
        package = (
            'Custom Tagging - Add Tags{$1=tag_should_be_added_%s,$2=tag_should'
            'be_ignored}'
        ) % tag_num

        e = ".*'Run' is not True.*"
        with self.assertRaisesRegexp(pytan.utils.RunFalse, e):
            handler.deploy_action_human(
                action_filters=action_filters,
                action_options=action_options,
                package=package,
                report_dir=TEST_OUT,
            )

    def test_deploy_action_missing_params(self):
        handler = self.setup_test()
        action_filters = ['Operating System, that contains Windows']
        action_options = ['and']

        package = 'Custom Tagging - Add Tags'

        e = 'parameter key.*requires a value, parameter definition'
        with self.assertRaisesRegexp(pytan.utils.HandlerError, e):
            handler.deploy_action_human(
                action_filters=action_filters,
                action_options=action_options,
                package=package,
                report_dir=TEST_OUT,
                run=True,
            )

    def test_deploy_action_missing_package(self):
        handler = self.setup_test()
        action_filters = ['Operating System, that contains Windows']
        action_options = ['and']

        package = ''

        e = "'' must be a string supplied as 'package'"
        with self.assertRaisesRegexp(pytan.utils.HumanParserError, e):
            handler.deploy_action_human(
                action_filters=action_filters,
                action_options=action_options,
                package=package,
                report_dir=TEST_OUT,
                run=True,
            )

    @ddt.file_data('ddt/ddt_valid_questions.json')
    def test_valid_question(self, value):
        handler = self.setup_test()

        method = value['method']
        args = value['args']

        s = (
            "+++ TESTING EXPECTED QUESTION SUCCESS Handler.{}() with kwargs {}"
        ).format
        spew(s(method, args))

        ret = getattr(handler, method)(**args)
        self.assertIsInstance(
            ret['question_object'],
            (pytan.api.Question, pytan.api.SavedQuestion)
        )
        self.assertIsInstance(ret['question_results'], pytan.api.ResultSet)
        self.assertGreaterEqual(len(ret['question_results'].rows), 1)
        self.assertGreaterEqual(len(ret['question_results'].columns), 1)
        for ft in pytan.constants.EXPORT_MAPS['ResultSet'].keys():
            report_file, result = handler.export_to_report_file(
                obj=ret['question_results'],
                export_format=ft,
                report_dir=TEST_OUT,
                prefix=sys._getframe().f_code.co_name + '_',
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
            spew("+++ EVAL TEST: %s" % x)
            self.assertTrue(eval(x))

        for ft in pytan.constants.EXPORT_MAPS['BaseType'].keys():
            report_file, result = handler.export_to_report_file(
                obj=response, export_format=ft, report_dir=TEST_OUT,
                prefix=sys._getframe().f_code.co_name + '_',
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
