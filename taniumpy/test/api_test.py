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

    try:
        response = session.find(type_class)
        print (
            "findall on {!r} == {!r} -- req len: {} resp len:{}"
        ).format(
            object_type_class,
            response,
            len(str(session.request_body)),
            len(str(session.response_body)),
        )
    except Exception as e:
        print "EXCEPTION FROM findall on {!r}: {}".format(
            object_type_class,
            str(e).replace('\n', ' '),
        )

    list_props = getattr(type_class, 'list_properties', {})
    if list_props:
        list_item = list_props.items()[0][1]
        if 'id' in vars(list_item):
            list_item.id = 1
        else:
            print 'SKIP list find by id 1, does not have id: {}'.format(
                object_type_class)
            continue
        getattr(type_class, list_props.items()[0][0]).append(list_item)
    else:
        if 'id' in vars(type_class):
            type_class.id = 1
        else:
            print 'SKIP single find by id 1, does not have id: {}'.format(
                object_type_class)
            continue

    try:
        response = session.find(type_class)
        print (
            "find id 1 on {!r} == {!r} -- req len: {} resp len:{}"
        ).format(
            object_type_class,
            response,
            len(str(session.request_body)),
            len(str(session.response_body)),
        )
    except Exception as e:
        print "EXCEPTION FROM find id 1 on {!r}: {}".format(
            object_type_class,
            str(e).replace('\n', ' '),
        )

# for object_type_class in dir(api):
#     if object_type_class.startswith('__'):
#         continue

#     try:
#         type_class = getattr(api, object_type_class)()
#     except:
#         print "UNABLE TO INSTANTIATE api.{}()".format(
#             object_type_class,
#         )
#         continue
#     print type_class
