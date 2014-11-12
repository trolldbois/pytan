
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class SensorSubcolumnList(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='sensor_subcolumn_list',
            simple_properties={},
            complex_properties={},
            list_properties={'subcolumn': SensorSubcolumn},
        )
        
        
        self.subcolumn = []

from sensor_subcolumn import SensorSubcolumn

