
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class CacheFilterList(BaseType):

    _OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='cache_filter_list',
            simple_properties={},
            complex_properties={},
            list_properties={'filter': CacheFilter},
        )
        
        
        self.filter = []

from cache_filter import CacheFilter

