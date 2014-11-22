#!/usr/bin/env python -ttB

import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import unittest

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
root_dir = os.path.join(my_dir, os.pardir, os.pardir)
root_dir = os.path.abspath(root_dir)
path_adds = [my_dir, root_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

from pytan import utils

# control the amount of output from unittests
TESTVERBOSITY = 2

# have unittest exit immediately on unexpected error
FAILFAST = True

# catch control-C to allow current test suite to finish (press 2x to force)
CATCHBREAK = True


class TestPytanUtils(unittest.TestCase):

    def test_is_list(self):
        self.assertTrue(utils.is_list([]))

    def test_is_not_list(self):
        self.assertFalse(utils.is_list(''))

    def test_is_str(self):
        self.assertTrue(utils.is_str(''))

    def test_is_not_str(self):
        self.assertFalse(utils.is_str([]))

    def test_is_dict(self):
        self.assertTrue(utils.is_dict({}))

    def test_is_not_dict(self):
        self.assertFalse(utils.is_dict([]))

    def test_version_lower(self):
        self.assertTrue(utils.version_check('0.0.0'))

    @unittest.expectedFailure
    def test_version_higher(self):
        self.assertFalse(utils.version_check('100.100.100'))

    def test_get_now(self):
        self.assertTrue(utils.get_now())

    def test_jsonify(self):
        exp = '{\n  "x": "d"\n}'
        self.assertEquals(utils.jsonify({'x': 'd'}), exp)

    def test_invalid_port(self):
        self.assertFalse(utils.port_check('localhost', 1, 0))

    @unittest.expectedFailure
    def test_dehumanize_sensors_empty_args1(self):
        utils.dehumanize_sensors('')

    @unittest.expectedFailure
    def test_dehumanize_sensors_empty_args2(self):
        utils.dehumanize_sensors([])

    @unittest.expectedFailure
    def test_dehumanize_sensors_invalid_simple_str(self):
        utils.dehumanize_sensors({})

    def test_dehumanize_sensors1(self):
        sensors = 'Sensor1'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'name': 'Sensor1'}]
        self.assertEquals(sensor_defs, exp)

    def test_dehumanize_sensors2(self):
        sensors = 'Sensor1, that is .*'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'params': {},
                'name': 'Sensor1',
                'options': {}
            }
        ]
        self.assertEquals(sensor_defs, exp)

    def test_dehumanize_sensors3(self):
        sensors = (
            'Sensor1, that is .*, opt:value_type:string, opt:ignore_case, '
            'opt:max_data_age:3600, opt:match_any_value'
        )
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'params': {},
                'name': 'Sensor1',
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0
                }
            }
        ]
        self.assertEquals(sensor_defs, exp)

    def test_dehumanize_sensors4(self):
        sensors = (
            'Sensor1{k1=v1,k2=v2}, that is .*, opt:value_type:string, '
            'opt:ignore_case, opt:max_data_age:3600, opt:match_any_value'
        )
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [
            {
                'filter': {
                    'not_flag': 0,
                    'operator': 'RegexMatch',
                    'value': '.*'
                },
                'name': 'Sensor1',
                'options': {
                    'all_times_flag': 0,
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string'
                },
                'params': {'k1': 'v1', 'k2': 'v2'}
            }
        ]
        self.assertEquals(sensor_defs, exp)

    def test_dehumanize_sensors5(self):
        sensors = [
            'Computer Name',
            'id:1',
            'Operating System, that contains Windows',
            ('Sensor1{k1=v1,k2=v2}, that is .*, opt:value_type:string, '
             'opt:ignore_case, opt:max_data_age:3600, opt:match_any_value'),
        ]
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [
            {
                'filter': {},
                'params': {},
                'name': 'Computer Name',
                'options': {}
            },
            {
                'filter': {},
                'params': {},
                'id': '1',
                'options': {}
            },
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*Windows.*'
                },
                'params': {},
                'name': 'Operating System',
                'options': {}
            },
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'params': {'k2': 'v2', 'k1': 'v1'},
                'name': 'Sensor1',
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0
                }
            }
        ]
        self.assertEquals(sensor_defs, exp)

    def test_dehumanize_sensors_valid_simple_str_id_selector(self):
        sensors = 'id:1'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'id': '1'}]
        self.assertEquals(sensor_defs, exp)

    def test_dehumanize_sensors_valid_simple_str_hash_selector(self):
        sensors = 'hash:1'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'hash': '1'}]
        self.assertEquals(sensor_defs, exp)

    def test_dehumanize_sensors_valid_simple_str_name_selector(self):
        sensors = 'name:Sensor1'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'name': 'Sensor1'}]
        self.assertEquals(sensor_defs, exp)

    def test_dehumanize_sensors_simple_valid_list(self):
        sensors = ['Sensor1']
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'name': 'Sensor1'}]
        self.assertEquals(sensor_defs, exp)

    def test_extract_selector(self):
        s = 'id:1 more:stuff,here'
        exp = ('1 more:stuff,here', 'id')
        self.assertEquals(utils.extract_selector(s), exp)

    def test_extract_selector_use_name_if_noselector(self):
        s = 'Sensor1 more:stuff,here'
        exp = ('Sensor1 more:stuff,here', 'name')
        r = utils.extract_selector(s)
        self.assertEquals(r, exp)

    def test_extract_params(self):
        s = 'Sensor1{k1=v1,k2=v2}, more:stuff,here'
        exp = ('Sensor1, more:stuff,here', {'k2': 'v2', 'k1': 'v1'})
        r = utils.extract_params(s)
        self.assertEquals(r, exp)

    def test_extract_params_noparams(self):
        s = 'Sensor1, more:stuff,here'
        exp = ('Sensor1, more:stuff,here', {})
        r = utils.extract_params(s)
        self.assertEquals(r, exp)

    @unittest.expectedFailure
    def test_extract_params_multiparams(self):
        s = 'Sensor1{k1=v1,k2=v2}{}, more:stuff,here'
        exp = ('Sensor1, more:stuff,here', {'k2': 'v2', 'k1': 'v1'})
        r = utils.extract_params(s)
        self.assertEquals(r, exp)

    @unittest.expectedFailure
    def test_extract_params_missing_seperator(self):
        s = 'Sensor1{v1,v2}, more:stuff,here'
        exp = ('Sensor1, more:stuff,here', {'k2': 'v2', 'k1': 'v1'})
        r = utils.extract_params(s)
        self.assertEquals(r, exp)

    def test_extract_options_single(self):
        s = 'Sensor1, more:stuff,here, opt:ignore_case'
        exp = ('Sensor1, more:stuff,here', {'ignore_case_flag': 1})
        r = utils.extract_options(s)
        self.assertEquals(r, exp)

    def test_extract_options_many(self):
        s = (
            'Sensor1, more:stuff,here, opt:ignore_case, opt:max_data_age:3600'
            ', opt:match_any_value, opt:value_type:string'
        )
        exp = (
            'Sensor1, more:stuff,here',
            {
                'value_type': 'string',
                'ignore_case_flag': 1,
                'max_age_seconds': '3600',
                'all_values_flag': 0,
                'all_times_flag': 0
            }
        )
        r = utils.extract_options(s)
        self.assertEquals(r, exp)

    @unittest.expectedFailure
    def test_extract_options_missing_value_max_data_age(self):
        s = 'Sensor1, more:stuff,here, opt:max_data_age'
        exp = ('Sensor1, more:stuff,here', {'max_age_seconds': ''})
        r = utils.extract_options(s)
        self.assertEquals(r, exp)

    @unittest.expectedFailure
    def test_extract_options_missing_value_value_type(self):
        s = 'Sensor1, more:stuff,here, opt:value_type'
        exp = ('Sensor1, more:stuff,here', {'max_age_seconds': ''})
        r = utils.extract_options(s)
        self.assertEquals(r, exp)

    @unittest.expectedFailure
    def test_extract_options_invalid_option(self):
        s = 'Sensor1, more:stuff,here, opt:invalid_option'
        exp = ('Sensor1, more:stuff,here', {})
        r = utils.extract_options(s)
        self.assertEquals(r, exp)

    def test_extract_options_nooptions(self):
        s = 'Sensor1, more:stuff,here'
        exp = ('Sensor1, more:stuff,here', {})
        r = utils.extract_options(s)
        self.assertEquals(r, exp)

    def test_extract_filter_valid(self):
        s = 'Sensor1, that is .*'
        exp = (
            'Sensor1',
            {'operator': 'RegexMatch', 'not_flag': 0, 'value': '.*'}
        )
        r = utils.extract_filter(s)
        self.assertEquals(r, exp)

    @unittest.expectedFailure
    def test_extract_filter_invalid(self):
        s = 'Sensor1, that meets .*'
        exp = (
            'Sensor1',
            {'operator': 'RegexMatch', 'not_flag': 0, 'value': '.*'}
        )
        r = utils.extract_filter(s)
        self.assertEquals(r, exp)

    def test_extract_filter_nofilter(self):
        s = 'Sensor1'
        exp = ('Sensor1', {})
        r = utils.extract_filter(s)
        self.assertEquals(r, exp)


if __name__ == "__main__":
    unittest.main(
        verbosity=TESTVERBOSITY,
        failfast=FAILFAST,
        catchbreak=CATCHBREAK)
