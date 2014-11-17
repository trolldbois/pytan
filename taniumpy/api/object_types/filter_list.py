
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class FilterList(BaseType):

    _soap_tag = 'filter_list'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={},
            complex_properties={},
            list_properties={'filter': Filter},
        )
        
        
        self.filter = []

from filter import Filter

