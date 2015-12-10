#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""This script was built to test doing various large resultdata sets with and without caching and paging
"""

pytan_loc = '~/gh/pytan'

import os
import sys

sys.dont_write_bytecode = True
sys.path.append(os.path.join(os.path.expanduser(pytan_loc), 'lib'))

import pytan
import getpass
import json
import datetime
import threading
import time
import logging

logging.Formatter.converter = time.gmtime
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
console_handler.setLevel(logging.DEBUG)
mylog = logging.getLogger('LOG')
mylog.setLevel(logging.DEBUG)
mylog.addHandler(console_handler)

# connection info for Tanium Server
handler_args = {
    'username': raw_input('Tanium Username: ').strip(),
    'password': getpass.getpass('Tanium Password: ').strip(),
    'host': raw_input('Tanium Host: ').strip(),
    'port': int(raw_input('Tanium Port: ').strip()),
    'loglevel': 0,
}

my_name = 'test_3308_cache_id'
basefilename = '{}-{}'.format(my_name, pytan.utils.seconds_from_now())
logfile = '{}.log'.format(basefilename)
resultsfile = '{}.results.txt'.format(basefilename)

# global settings that we want to change for this run:
GLOBAL_SETTINGS = [
    {'name': "question_hops_per_report", 'new_val': '1'},
    {'name': "question_min_hops_per_report", 'new_val': '1'},
]

# json of sensor to generate random strings
RANDOM_SENSOR = (
    '''{
  "_type": "sensor",
  "category": "Miscellaneous",
  "delimiter": ",",
  "exclude_from_parse_flag": 1,
  "hidden_flag": 0,
  "ignore_case_flag": 1,
  "max_age_seconds": 900,
  "name": "1kRandomStrings",
  "queries": {
    "_type": "queries",
    "query": [
      {
        "_type": "query",
        "platform": "Linux",
        "script": "#!/bin/bash\\nhostname=`hostname`\\nfor i in $(seq 1 1000); do\\necho &quot;$hostname-$RANDOM$RANDOM&quot;\\ndone\\n",
        "script_type": "UnixShell"
      }
    ]
  },
  "value_type": "String"
}
'''
)

# name to add to sensor as part of pytan copy
RANDOM_STR = 'PyTan Test'

TESTS = [
    {'sensors': [], 'paging': False, 'caching': False},
    {'sensors': [], 'paging': True, 'caching': False},
    {'sensors': [], 'paging': True, 'caching': 900},
    # {'sensors': ['Computer Name'], 'paging': False, 'caching': False},
    # {'sensors': ['Computer Name'], 'paging': True, 'caching': False},
    # {'sensors': ['Computer Name'], 'paging': True, 'caching': 900},
]

STATS_TIMER = 30

RESET_GLOBALS = True

PRINT_STATS = True

PAGE_LIMIT = 50000

CACHE_EXPIRATION = 900

WAIT_FOR_LAST_QUESTION = False

# ____________________________ FUNCTIONS


def update_global_settings():
    # update global settings accordingly
    for i in GLOBAL_SETTINGS:
        i['obj'] = handler.get('setting', name=i['name'])[0]
        if not i['obj'].value == i['new_val']:
            i['orig_value'] = i['obj'].value
            i['obj'].value = i['new_val']
            i['obj'] = handler.session.save(i['obj'])
            mylog.info((
                "Updated {name!r} from {orig_value!r} to {new_val!r}"
            ).format(**i))


def restore_global_settings():
    # restore global settings accordingly
    for i in GLOBAL_SETTINGS:
        i['obj'] = handler.get('setting', name=i['name'])[0]
        i['current_value'] = i['obj'].value
        if i.get('orig_value', None):
            i['obj'].value = i['orig_value']
            i['obj'] = handler.session.save(i['obj'])
            mylog.info((
                "Restored {name!r} from {current_value!r} to {orig_value!r}"
            ).format(**i))


def reset_global_settings():
    # reset global settings accordingly
    for i in GLOBAL_SETTINGS:
        i['obj'] = handler.get('setting', name=i['name'])[0]
        i['current_value'] = i['obj'].value
        i['default_value'] = i['obj'].default_value
        if i['current_value'] != i['default_value']:
            i['obj'].value = i['obj'].default_value
            i['obj'] = handler.session.save(i['obj'])
            # mylog.info((
            #     "Reset {name!r} from {current_value!r} to {default_value!r}"
            # ).format(**i))


def make_random_copy(cnt):
    random_obj = json.loads(RANDOM_SENSOR)
    random_obj = pytan.taniumpy.BaseType.from_jsonable(random_obj)
    random_obj.name = '{} {} #{}'.format(random_obj.name, RANDOM_STR, cnt)
    random_obj = handler.session.add(random_obj)
    random_obj = handler.session.find(random_obj)
    mylog.info((
        "Created new random sensor copy: {}"
    ).format(random_obj.name))
    return random_obj


def clean_random_copies():
    random_obj = json.loads(RANDOM_SENSOR)
    random_obj = pytan.taniumpy.BaseType.from_jsonable(random_obj)
    sw = '{} {}'.format(random_obj.name, RANDOM_STR)
    all_sensors = handler.get_all('sensor')
    rand_sensors = [x for x in all_sensors if x.name.startswith(sw)]
    for x in rand_sensors:
        try:
            handler.session.delete(x)
            mylog.info((
                "Removed old random sensor copy: {}"
            ).format(x.name))
        except:
            pass


def get_result_info(x):
    retry_count = 5
    current_try = 0
    while not current_try >= retry_count:
        try:
            ri = handler.session.getResultInfo(x['question'])
            break
        except:
            if current_try > retry_count:
                raise
            else:
                mylog.exception((
                    "GetResultInfo failed on attempt #{} for question {}"
                ).format(current_try, x['question']))
        current_try += 1
    return ri


def poll_result_info(x):
    x['ri_start'] = datetime.datetime.utcnow()

    # pollerll for completion via pytan's questionpoller with getresultinfo
    poller = pytan.pollers.QuestionPoller(handler, x['question'], polling_secs=30)

    retry_count = 5
    current_try = 0
    while not current_try >= retry_count:
        try:
            poller.run()
            break
        except:
            if current_try > retry_count:
                raise
            else:
                mylog.exception((
                    "Poll ResultInfo failed on attempt #{} for question {}"
                ).format(current_try, x['question']))
        current_try += 1

    x['ri'] = get_result_info(x)
    x['ri_end'] = datetime.datetime.utcnow()
    x['ri_elapsed'] = x['ri_end'] - x['ri_start']
    x['ri_reached_pct'] = get_percentage(x['ri'].mr_tested, x['ri'].estimated_total)
    mylog.info((
        "[TEST #{cnt}] Polling for resultinfo = 99% (reached: {ri_reached_pct}) "
        "took: {ri_elapsed}"
    ).format(**x))
    return x


def normal_get_result_data(x):
    x['rd'] = get_rd(x['question'])
    return x


def get_paging(x):
    if x['paging'] is True:
        x['paging'] = calc_percent(10, x['ri'].row_count)

        if PAGE_LIMIT:
            if x['paging'] > PAGE_LIMIT:
                x['paging'] = PAGE_LIMIT

    return x


def get_rd(q, **kwargs):
    retry_count = 5
    current_try = 0
    while not current_try >= retry_count:
        try:
            rd = handler.session.getResultData(q, **kwargs)
            break
        except:
            if current_try > retry_count:
                raise
            else:
                mylog.exception((
                    "GetResultData failed on attempt #{} for question {} with args: {}"
                ).format(current_try, q, kwargs))

        current_try += 1

    rd.body_len = len(handler.session.response_body)
    rd.row_len = len(rd.rows)
    return rd


def paging_get_result_data(x):

    x = get_paging(x)

    current_row = 0
    total_rows = x['ri'].row_count
    all_rows = []
    current_page = 1
    while True:
        get_rd_args = {'row_count': x['paging'], 'row_start': current_row}

        new_data = get_rd(x['question'], **get_rd_args)
        if new_data is None:
            mylog.warning("None returned for result data!")
            break

        data = new_data

        mylog.info((
            "[TEST #{cnt}] Getting result data page {current_page} for {data.row_count} total rows returned {data.row_len} rows (args: {args}) (response len: {data.body_len})"
        ).format(current_page=current_page, data=data, args=get_rd_args, **x))

        all_rows += data.rows

        if not data.rows:
            mylog.warning("No rows returned!")
            break

        if current_row >= total_rows:
            break

        current_row += x['paging']
        current_page += 1

    data.rows = all_rows
    x['rd'] = data
    return x


def paging_caching_get_result_data(x):
    x = get_paging(x)

    current_row = 0
    total_rows = x['ri'].row_count
    all_rows = []
    cache_id = None
    current_page = 1
    while True:
        get_rd_args = {
            'row_count': x['paging'],
            'row_start': current_row,
            'cache_expiration': x['caching'],
        }

        if cache_id:
            get_rd_args['cache_id'] = cache_id

        new_data = get_rd(x['question'], **get_rd_args)
        if new_data is None:
            mylog.warning("None returned for result data!")
            break

        data = new_data

        mylog.info((
            "[TEST #{cnt}] Getting result data page {current_page} for {data.row_count} total rows returned {data.row_len} rows (args: {args}) (response len: {data.body_len})"
        ).format(current_page=current_page, data=data, args=get_rd_args, **x))

        if get_rd_args.get('cache_id', ''):
            if not get_rd_args['cache_id'] == data.cache_id:
                mylog.warning((
                    "cache id changed from {} to {}"
                ).format(get_rd_args['cache_id'], data.cache_id))

        cache_id = data.cache_id
        all_rows += data.rows

        if not data.rows:
            mylog.warning("No rows returned!")
            break

        if current_row >= total_rows:
            break

        current_row += x['paging']
        current_page += 1

    data.rows = all_rows
    x['rd'] = data
    return x


def get_result_data(x):
    x['rd_start'] = datetime.datetime.utcnow()

    if x['paging']:
        if x['caching']:
            x = paging_caching_get_result_data(x)
        else:
            x = paging_get_result_data(x)
    else:
        x = normal_get_result_data(x)

    x['rd_end'] = datetime.datetime.utcnow()
    x['rd_elapsed'] = x['rd_end'] - x['rd_start']

    mylog.info((
        "[TEST #{cnt}] Getting result data for {rd.row_count} total rows returned {rd.row_len}"
        " rows with paging: {paging} and caching: {caching} took: {rd_elapsed} - "
        "(response len: {rd.body_len})"
    ).format(**x))
    return x


def get_percentage(part, whole):
    f = 100 * float(part) / float(whole)
    return "{0:.2f}%".format(f)


def calc_percent(percent, whole):
    return int((percent * whole) / 100.0)


def get_stats(wait=20):
    while True:
        if PRINT_STATS:
            si = handler.session.get_server_info()

            try:
                pydiags = si.get('pydiags', {})
                strcache = pydiags['String Cache']
                sysperf = pydiags['System Performance Info']
                aqc = pydiags['Active Question Cache']

                mem_avail = get_percentage(sysperf['PhysicalAvailable'], sysperf['PhysicalTotal'])
                handles = sysperf['HandleCount']
                processes = sysperf['ProcessCount']
                strings = strcache['Total String Count']
                est_count = aqc['Active Client Estimate']
                active_questions = aqc['Active Question Estimate']

                mylog.info((
                    "         -- STATS: Memory Available: {}, Handles: {}, Processes: {}, Strings: {}"
                    ", Est Total: {}, Active Questions: {}"
                ).format(
                    mem_avail, handles, processes, strings, est_count, active_questions,
                ))
            except:
                mylog.warning("System Info failed to fetch! {}".format(si))

        time.sleep(wait)


def setup_logging():
    console_handler.setLevel(logging.DEBUG)
    mylog.setLevel(logging.DEBUG)
    # my_file = os.path.abspath(sys.argv[0])
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    file_handler.setLevel(logging.DEBUG)
    mylog.addHandler(file_handler)
    mylog.info("Logging to {}".format(logfile))


def start_stats_thread():
    thread = threading.Thread(target=get_stats, args=(STATS_TIMER,))
    thread.daemon = True
    thread.start()
    mylog.info("Started up stats thread every {} seconds...".format(STATS_TIMER))
    return thread


def start_tests(tests, fd):
    # create copies of the random sensor for each test
    for idx, x in enumerate(tests):
        x['random_obj'] = make_random_copy(idx + 1)

    mylog.info("Waiting three minutes for new sensor propagation...")
    time.sleep(180)
    last_question_expiration = None

    for idx, x in enumerate(tests):
        if WAIT_FOR_LAST_QUESTION and last_question_expiration:
            cache_expiry_min = 5
            cache_expiry = last_question_expiration + datetime.timedelta(
                seconds=cache_expiry_min * 60)
            spewage = False
            while True:
                if datetime.datetime.utcnow() >= cache_expiry:
                    mylog.info((
                        "Last question expired ({} + {} minutes), starting up next question..."
                    ).format(last_question_expiration, cache_expiry_min))
                    break

                if not spewage:
                    mylog.info((
                        "Last question not expired yet ({} + {} minutes), waiting..."
                    ).format(last_question_expiration, cache_expiry_min))
                    spewage = True
                time.sleep(60)

        x['cnt'] = idx + 1

        # add the random object to the sensors
        x['sensors'].append(x['random_obj'].name)

        mylog.info((
            "[TEST #{cnt}] Starting new test -- sensors: {sensorstxt}, paging: {paging}, "
            "caching: {caching}"
        ).format(sensorstxt=';'.join(x['sensors']), **x))

        # ask the question without using pytan's get result logic
        x['question'] = handler.ask_manual_human(sensors=x['sensors'], get_results=False)
        x['question'] = x['question']['question_object']
        last_question_expiration = pytan.utils.timestr_to_datetime(x['question'].expiration)

        mylog.info((
            "[TEST #{cnt}] Question asked: ID: {question.id}, Query: {question.query_text!r}, expires: {expires}"
        ).format(expires=last_question_expiration, **x))

        try:
            x = poll_result_info(x)
        except:
            mylog.exception("Exception occurred during poll_result_info")

        try:
            x = get_result_data(x)
        except:
            mylog.exception("Exception occurred during get_result_data")

        try:
            with open(resultsfile, 'a+b') as fd:
                fd.write((
                    "{cnt}, {sensorstxt}, {rd.row_count}, {row_len}, {paging}, {caching}, "
                    "{ri_elapsed}, {rd_elapsed}\n"
                ).format(sensorstxt=';'.join(x['sensors']), row_len=len(x['rd'].rows), **x))
        except:
            mylog.exception("Exception occurred during results file write")

    return tests

# ____________________________ START WORKFLOW

# connect to tanium using handler_args
handler = pytan.handler.Handler(**handler_args)

setup_logging()

stats_thread = start_stats_thread()

with open(resultsfile, 'wb') as fd:
    fd.write((
        'test#, sensors, row_count_total, row_count_returned, paging, caching, '
        'ri_elapsed, rd_elapsed\n'
    ))

if RESET_GLOBALS:
    reset_global_settings()
    clean_random_copies()

update_global_settings()
test_results = start_tests(TESTS, fd)

# ____________________________ CLEANUP WORKFLOW

clean_random_copies()
restore_global_settings()
