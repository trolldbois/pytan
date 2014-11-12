#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
import os
import sys

sys.dont_write_bytecode = True
my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import api

host = '172.16.31.128'
username = 'Tanium User'
password = 'T@n!um'

session = api.Session(host)
session.authenticate(username, password)

for object_type_class in dir(api):
    if object_type_class.startswith('__'):
        continue

    try:
        type_class = getattr(api, object_type_class)()
    except:
        print "UNABLE TO INSTANTIATE api.{}()".format(
            object_type_class,
        )
        continue

    # print type_class
    # print list_props
    # continue
    try:
        response = session.find(type_class)
        print (
            "findall on {} == {} obj len:{} req len: {} resp len:{}"
        ).format(
            object_type_class,
            response,
            len(str(response)),
            len(str(session.request_body)),
            len(str(session.response_body)),
        )
    except Exception as e:
        print "EXCEPTION FROM 'findall' on {!r}: {}".format(
            object_type_class,
            e,
        )

    list_props = getattr(type_class, 'list_properties', {})
    if list_props:
        for k, v in list_props.iteritems():
            list_item = v()
            list_item.id = 1
            getattr(type_class, k).append(list_item)
    else:
        type_class.id = 1

    try:
        response = session.find(type_class)
        print (
            "find id 1 on {} == {} obj len:{} req len: {} resp len:{}"
        ).format(
            object_type_class,
            response,
            len(str(response)),
            len(str(session.request_body)),
            len(str(session.response_body)),
        )
    except Exception as e:
        print "EXCEPTION FROM 'find id 1' on {!r}: {}".format(
            object_type_class,
            e,
        )
