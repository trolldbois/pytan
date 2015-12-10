#!/usr/bin/env python -i
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

# get the form submission
form = cgi.FieldStorage()

formdict = common.formtodict(form)

action_id = formdict.get('action_id', None)
computer_id = formdict.get('computer_id', None)

if not action_id or not computer_id:
    status = "ERROR: Missing action_id or computer_id!"
else:
    # connect to Tanium
    handler = pytan.Handler(
        username=config['tanium_username'],
        password=config['tanium_password'],
        host=config['tanium_host'],
    )

    # this logic assumes only one system should be being deployed to,
    # more servers is more complicated
    action_obj = handler.get('action', id=action_id)[0]
    rd = handler.get_result_data(action_obj, True)
    if not rd.rows:
        status = "Waiting to download."
    else:
        status = rd.rows[0]['Action Statuses'][0].split(':')[1]

status = json.dumps({'status': status})

common.print_html(status)
