
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ParseResultGroup(BaseType):

    _OBJECT_LIST_TAG = 'parse_result_group'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='parse_result_group',
            simple_properties={'score': int,
                        'question_text': str},
            complex_properties={'parse_results': ParseResultList,
                        'question': Question},
            list_properties={},
        )
        self.score = None
        self.question_text = None
        self.parse_results = None
        self.question = None
        

from parse_result_list import ParseResultList
from question import Question

