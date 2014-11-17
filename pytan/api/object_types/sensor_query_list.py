
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class SensorQueryList(BaseType):

    _soap_tag = 'sensor_query_list'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={},
            complex_properties={},
            list_properties={'query': SensorQuery},
        )
        
        
        self.query = []

from sensor_query import SensorQuery

