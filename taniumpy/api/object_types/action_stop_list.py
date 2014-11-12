
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ActionStopList(BaseType):

    OBJECT_LIST_TAG = 'action_stops'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'action_stops',
            simple_properties = {},
            complex_properties = {},
            list_properties = {'action_stop': ActionStop},
        )
        
        
        self.action_stop = []

from action_stop import ActionStop

