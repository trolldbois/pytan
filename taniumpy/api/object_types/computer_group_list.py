

# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#


from .base import BaseType

class ComputerGroupList(BaseType):

    OBJECT_LIST_TAG = 'computer_groups'

    def __init__(self):
        BaseType.__init__(self,
            soap_tag='computer_groups',
            simple_properties={  },
            complex_properties={ 'cache_info': CacheInfo },
            list_properties={ 'computer_group': ComputerGroup },
        )
        
        self.cache_info = None
        self.computer_group = []

from computer_group import ComputerGroup
from cache_info import CacheInfo

