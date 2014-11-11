

# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#


from .base import BaseType

class VersionAggregateList(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(self,
            soap_tag='versions',
            simple_properties={  },
            complex_properties={  },
            list_properties={ 'version': VersionAggregate },
        )
        
        
        self.version = []

from version_aggregate import VersionAggregate

