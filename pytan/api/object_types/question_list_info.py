
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class QuestionListInfo(BaseType):

    _OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='info',
            simple_properties={'highest_id': int,
                        'total_count': int},
            complex_properties={},
            list_properties={},
        )
        self.highest_id = None
        self.total_count = None
        
        



