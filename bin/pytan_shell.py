#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '3.0.0'

import os
import sys
sys.dont_write_bytecode = True
my_filepath = os.path.abspath(sys.argv[0])
my_file = os.path.basename(my_filepath)
my_name = os.path.splitext(my_file)[0]
my_dir = os.path.dirname(my_filepath)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]
[sys.path.insert(0, aa) for aa in path_adds if aa not in sys.path]

import pytan  # noqa
i = "pytan.shell.{}".format(my_name)
__import__(i)
module = eval(i)
worker = module.Worker()

if __name__ == "__main__":
    version_check = worker.version_check(__version__)
    console = worker.interactive_check()
    check = worker.check()
    setup = worker.setup()
    args = worker.parse_args()
    handler = worker.get_handler()
    result = worker.get_result()
    exec(worker.get_exec())

from pytan.utils import taniumpy  # noqa
from pytan.utils import constants  # noqa
from pytan import utils  # noqa
self = handler  # noqa


def ask_manual(**kwargs):
    """pass."""

    """
    sensors = kwargs.get('sensors', [])
    filters = kwargs.get('filters', [])
    options = kwargs.get('options', [])
    sensor_specs = kwargs.get('sensor_specs', [])
    filter_specs = kwargs.get('filter_specs', [])
    option_specs = kwargs.get('option_specs', [])

    sensor_defs = utils.parsers.parse_sensors(sensors=sensors)
    filter_defs = utils.parsers.parse_filters(filters=filters)
    option_defs = utils.parsers.parse_options(options=options)
    """
    utils.helpers.check_for_help(kwargs=kwargs)

    clean_keys = [
        'defs',
        'd',
        'obj',
        'objtype',
        'key',
        'default',
        'defname',
        'deftypes',
        'empty_ok',
        'id',
        'pytan_help',
        'handler',
        'sse',
    ]
    clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

    # get our defs from kwargs and churn them into what we want
    sensor_defs = utils.validate.defs_gen(
        defname='sensor_defs',
        deftypes=['list()', 'str()', 'dict()'],
        strconv='name',
        empty_ok=True,
        **clean_kwargs
    )

    filter_defs = utils.validate.defs_gen(
        defname='filter_defs',
        deftypes=['list()', 'dict()'],
        empty_ok=True,
        **clean_kwargs
    )

    option_defs = utils.validate.defs_gen(
        defname='option_defs',
        deftypes=['dict()'],
        empty_ok=True,
        **clean_kwargs
    )

    sse = kwargs.get('sse', False)
    clean_kwargs['sse_format'] = clean_kwargs.get('sse_format', 'xml_obj')

    max_age_seconds = utils.validate.get_kwargs_int(
        key='max_age_seconds',
        default=600,
        **clean_kwargs
    )

    # do basic validation of our defs
    utils.validate.defs_sensors(sensor_defs=sensor_defs)
    utils.validate.defs_filters(filter_defs=filter_defs)

    # get the sensor objects that are in our defs and add them as d['sensor_obj']
    h = (
        "Issue a GetObject to get the full object of a sensor for inclusion in a "
        "Select for a Question"
    )
    sensor_defs = self._get_sensor_defs(defs=sensor_defs, pytan_help=h, **clean_kwargs)
    h = (
        "Issue a GetObject to get the full object of a sensor for inclusion in a "
        "Group for a Question"
    )
    filter_defs = self._get_sensor_defs(defs=filter_defs, pytan_help=h, **clean_kwargs)

    # build a SelectList object from our sensor_defs
    selectlist_obj = utils.tanium_obj.build_selectlist_obj(sensor_defs=sensor_defs)

    # build a Group object from our question filters/options
    group_obj = utils.tanium_obj.build_group_obj(
        filter_defs=filter_defs, option_defs=option_defs,
    )

    # build a Question object from selectlist_obj and group_obj
    add_obj = utils.tanium_obj.build_manual_q(selectlist_obj=selectlist_obj, group_obj=group_obj)

    add_obj.max_age_seconds = max_age_seconds

    # add our Question and get a Question ID back
    h = "Issue an AddObject to add a Question object"
    added_obj = self._add(obj=add_obj, pytan_help=h, **clean_kwargs)

    m = "Question Added, ID: {}, query text: {!r}, expires: {}".format
    self.mylog.debug(m(added_obj.id, added_obj.query_text, added_obj.expiration))

    poller = self.pollers.QuestionPoller(handler=self, obj=added_obj, **clean_kwargs)

    ret = {
        'question_object': added_obj,
        'poller_object': poller,
        'question_results': None,
        'poller_success': None,
    }

    if kwargs.get('get_results', True):
        # poll the Question ID returned above to wait for results
        ret['poller_success'] = ret['poller_object'].run(**clean_kwargs)

        # get the results
        if sse and self.session.platform_is_6_5(**clean_kwargs):
            rd = self.get_result_data_sse(obj=added_obj, **clean_kwargs)
        else:
            rd = self.get_result_data(obj=added_obj, **clean_kwargs)

        if isinstance(rd, utils.taniumpy.object_types.result_set.ResultSet):
            # add the sensors from this question to the ResultSet object for reporting
            rd.sensors = [x['sensor_obj'] for x in sensor_defs]

        ret['question_results'] = rd
    return ret
