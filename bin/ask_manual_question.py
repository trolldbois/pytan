#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Ask a manual question and save the results as a report format'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.1.0'

import os
import sys
import getpass
sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan
from pytan import utils

examples = [
    {
        'name': 'Print the help for sensors',
        'cmd': 'ask_manual_question.py $API_INFO --sensors-help csv',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for filters',
        'cmd': 'ask_manual_question.py $API_INFO --filters-help csv',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for options',
        'cmd': 'ask_manual_question.py $API_INFO --options-help csv',
        'tests': 'notexitcode',
    },
    {
        'name': 'Ask a question example 1',
        'cmd': (
            'ask_manual_question.py $API_INFO --sensor "Computer Name" --file "$TMP/out.csv" csv'
        ),
        'notes': ['Ask a question with a single sensor', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 2',
        'cmd': 'ask_manual_question.py $API_INFO --sensor "id:1" --file "$TMP/out.csv" csv',
        'notes': ['Ask a question with a single sensor by id', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 3',
        'cmd': (
            'ask_manual_question.py $API_INFO '
            '--sensor "Computer Name" --sensor "Installed Applications" '
            ' --file "$TMP/out.csv" csv'
        ),
        'notes': ['Ask a question with two sensors', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 4',
        'cmd': (
            'ask_manual_question.py $API_INFO --sensor "Folder Name Search with RegEx Match'
            '{dirname=Program Files,regex=Microsoft.*}"'
            ' --file "$TMP/out.csv" csv'
        ),
        'notes': [
            'Ask a question with a sensor that requires parameters',
            'Save the results to a CSV file',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 5',
        'cmd': (
            'ask_manual_question.py $API_INFO '
            '--sensor "Operating System, that contains:Windows, opt:ignore_case, '
            'opt:max_data_age:60" --file "$TMP/out.csv" csv'
        ),
        'notes': [
            'Ask a question with a single sensor',
            'Supply a filter in the sensor that limits the column data to .*Windows.* matches',
            'Supply an option in the sensor that ignores case in the filter',
            'Supply an option in the sensor that re-fetches cached data older than 1 minute',
            'Save the results to a CSV file',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 6',
        'cmd': (
            'ask_manual_question.py $API_INFO '
            '-s "Computer Name" '
            '-s "Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*, '
            'invalidparam=test}, that regex match:.*Shared.*, opt:max_data_age:3600" '
            '-f "Operating System, that contains:Windows" '
            '-f "IP Address, that not equals:10.10.10.10" '
            '-o "or" -o "ignore_case" '
            '--file "$TMP/out.csv" csv'
        ),
        'notes': [
            'Ask a question with two sensors',
            'Supply parameters to the 2nd sensor',
            'Supply a filter in the 2nd sensor that limits the column data to .*Shared.*',
            'Supply an option in the 2nd sensor that re-fetches cached data older than 1 minute',
            'Supply a question filter that limits the rows returned to machines whose '
            'Operating System sensor match .*Windows.*',
            'Supply a question filter that limits the rows returned to machines whose '
            'IP Address filter does not equal 10.10.10.10',
            'Supply two question options, one to OR the question filters supplied, and another '
            'to ignore the case while matching the question filters',
            'Save the results to a CSV file',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 7',
        'cmd': (
            'ask_manual_question.py $API_INFO '
            '-s "Computer Name" -s "Last Logged In User" '
            '-s "Installed Applications, that contains:Google Search" '
            '-s "Installed Applications, that contains:Google Chrome" '
            '-f "Installed Applications, that contains:Google Search" '
            '-f "Installed Applications, that contains:Google Chrome" '
            '-o "and" -o "ignore_case" '
            '--file "$TMP/out.csv" csv'
        ),
        'notes': [
            'Ask a question with 4 sensors',
            'Use filters on 3rd and 4th sensor to limit the column data to only show certain apps',
            'Use 2 question filters to limit the row data to only show the same apps used in'
            ' the sensor filters',
            'Supply two question options, one to AND the question filters supplied, and another '
            'to ignore the case while matching the question filters',
            'Save the results to a CSV file',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
]


def process_handler_args(parser, all_args):
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: all_args.pop(k) for k in handler_opts}

    try:
        h = pytan.Handler(**handler_args)
        print str(h)
    except Exception as e:
        print e
        sys.exit(99)
    return h


if __name__ == "__main__":

    utils.version_check(__version__)
    parser = utils.setup_ask_manual_argparser(__doc__)
    parser = utils.add_ask_report_argparser(parser)

    args = parser.parse_args()
    all_args = args.__dict__

    if not args.username:
        username = raw_input('Tanium Username: ')
        all_args['username'] = username.strip()

    if not args.password:
        password = getpass.getpass('Tanium Password: ')
        all_args['password'] = password.strip()

    if not args.host:
        host = raw_input('Tanium Host: ')
        all_args['host'] = host.strip()

    handler = process_handler_args(parser, all_args)

    q_opts = [
        'sensors', 'question_filters', 'question_options', 'get_results', 'sensors_help',
        'filters_help', 'options_help',
    ]
    q_args = {k: all_args.pop(k) for k in q_opts}

    print "++ Asking manual question:\n{}".format(utils.jsonify(q_args))
    try:
        ret = handler.ask(qtype='manual', **q_args)
    except Exception as e:
        print e
        sys.exit(99)

    print "++ Asked Question {!r} ID: {!r}".format(
        ret['question_object'].query_text, ret['question_object'].id
    )

    if ret['question_results']:
        try:
            report_file, result = handler.export_to_report_file(
                obj=ret['question_results'],
                **all_args)
            m = "++ Report file {!r} written with {} bytes".format
            print(m(report_file, len(result)))
        except Exception as e:
            print e
            sys.exit(99)
    else:
        print (
            "++ No action results returned, run get_results.py to get the results"
        )
