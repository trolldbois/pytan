
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ParseResultGroupList(BaseType):

    OBJECT_LIST_TAG = 'parse_result_groups'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='parse_result_groups',
            simple_properties={},
            complex_properties={},
            list_properties={'parse_result_group': ParseResultGroup},
        )
        
        
        self.parse_result_group = []

from parse_result_group import ParseResultGroup

