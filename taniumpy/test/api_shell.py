#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
import os
import sys
import logging
sys.dont_write_bytecode = True
my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import api

# logging.basicConfig(level=logging.DEBUG)

host = '172.16.31.128'
username = 'Tanium User'
password = 'T@n!um'

session = api.Session(host)
print session
session.authenticate(username, password)
print session


# v='''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
# <SOAP-ENV:Body>
#   <typens:tanium_soap_request xmlns:typens="urn:TaniumSOAP">
#     <session>3-4813-ef4056a1daec52fa8d438edaa993c617e87ef09f2e62c1b3bb3a70ff833f73c6c436513abbb5e581969226a1cb9edf80206b5f822e8bd82654feeedf625cee27</session>
#     <command>GetObject</command>
#     <object_list>
#       <action><id>1</id></action><action><id>2</id></action>
#     </object_list>
#   </typens:tanium_soap_request>
# </SOAP-ENV:Body>
# </SOAP-ENV:Envelope>
# '''

# b = session._getResponse(v)
# print len(b)

# all_sensors = session.find(api.SensorList())
