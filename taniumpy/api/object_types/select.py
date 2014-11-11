

# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#


from .base import BaseType

class Select(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(self,
            soap_tag='select',
            simple_properties={  },
            complex_properties={ 'sensor': Sensor,
                        'filter': Filter,
                        'group': Group },
            list_properties={  },
        )
        
        self.sensor = None
        self.filter = None
        self.group = None
        

from sensor import Sensor
from filter import Filter
from group import Group

