
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ActionList(BaseType):

    OBJECT_LIST_TAG = 'actions'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'actions',
            simple_properties = {},
            complex_properties = {'info': ActionListInfo,
                        'cache_info': CacheInfo},
            list_properties = {'action': Action},
        )
        
        self.info = None
        self.cache_info = None
        self.action = []

from action_list_info import ActionListInfo
from action import Action
from cache_info import CacheInfo

