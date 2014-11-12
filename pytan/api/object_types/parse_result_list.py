
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ParseResultList(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='parse_result_list',
            simple_properties={},
            complex_properties={},
            list_properties={'parse_result': ParseResult},
        )
        
        
        self.parse_result = []

from parse_result import ParseResult

