
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class SensorQueryList(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='sensor_query_list',
            simple_properties={},
            complex_properties={},
            list_properties={'query': SensorQuery},
        )
        
        
        self.query = []

from sensor_query import SensorQuery

