"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``parse_result_group``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class ParseResultGroup(BaseType):

    _soap_tag = 'parse_result_group'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.score = None
        self.question_text = None
        self.parse_results = None
        self.question = None
        # no list_properties defined


from .question import Question
from .parse_result_list import ParseResultList

SIMPLE_ARGS = {}
SIMPLE_ARGS['score'] = int
SIMPLE_ARGS['question_text'] = str

COMPLEX_ARGS = {}
COMPLEX_ARGS['parse_results'] = ParseResultList
COMPLEX_ARGS['question'] = Question

LIST_ARGS = {}
# no LIST_ARGS defined
