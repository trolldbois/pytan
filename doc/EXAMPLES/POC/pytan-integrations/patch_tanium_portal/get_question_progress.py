#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4 softtabstop=1 shiftwidth=4 expandtab:
# Please do not change the two lines above. See PEP 8, PEP 263.


import os
import sys
sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
sys.path.append(my_dir)

from config import config
import common

sys.path.append(config['pytan_dir'])

import pytan
import cgi
import json


def json_print_end(x):
    common.print_html(pytan.utils.jsonify(x))
    sys.exit()


# get the form submission
form = cgi.FieldStorage()

formdict = common.formtodict(form)

question_id = formdict.get('question_id', "")

ret = {
    'status': None,
    'percent': 0,
    'finished': False,
    'question_obj': None,
    'result_info': None,
    'result_data': None,
    'error': False,
}

if not question_id:
    ret['status'] = "ERROR: Missing question_id!"
    json_print_end(ret)


try:
    # connect to Tanium
    handler = pytan.Handler(
        username=config['tanium_username'],
        password=config['tanium_password'],
        host=config['tanium_host'],
    )
except:
    ret['status'] = "ERROR: Unable to connect to Tanium!"
    ret['error'] = True
    json_print_end(ret)

try:
    question_obj = handler.get('question', id=question_id)[0]
except:
    ret['status'] = "ERROR: Unable to find question ID {}".format(question_id)
    ret['error'] = True
    json_print_end(ret)

ret['question_obj'] = json.loads(question_obj.to_json(question_obj))

result_info = handler.session.getResultInfo(question_obj)
ret['result_info'] = vars(result_info)

tested_pct = result_info.mr_tested * 100
estimated_total_pct = result_info.estimated_total + .01
new_pct = tested_pct / estimated_total_pct
ret['percent'] = new_pct

if new_pct >= config['pct_complete_threshold']:
    result_data = handler.session.getResultData(question_obj)
    rd_dict = common.dictify_resultset(result_data)
    if not rd_dict:
        ret['status'] = "ERROR: No matching servers found!"
        ret['error'] = True
    else:
        ret['status'] = "Found {} servers".format(len(rd_dict))

    ret['finished'] = True
    ret['result_data'] = rd_dict

else:
    ret['status'] = "Waiting for results.. {0:.0f}%  complete".format(new_pct)

json_print_end(ret)
