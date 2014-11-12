
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ParseResult(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='parse_result',
            simple_properties={'id': int,
                        'parameter_definition': str},
            complex_properties={'parameters': ParameterList},
            list_properties={},
        )
        self.id = None
        self.parameter_definition = None
        self.parameters = None
        

from parameter_list import ParameterList

