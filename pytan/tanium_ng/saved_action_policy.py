"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``policy``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class SavedActionPolicy(BaseType):

    _soap_tag = 'policy'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.saved_question_id = None
        self.saved_question_group_id = None
        self.row_filter_group_id = None
        self.max_age = None
        self.min_count = None
        self.saved_question_group = None
        self.row_filter_group = None
        # no list_properties defined


from .group import Group

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['saved_question_id'] = int
SIMPLE_ARGS['saved_question_group_id'] = int
SIMPLE_ARGS['row_filter_group_id'] = int
SIMPLE_ARGS['max_age'] = int
SIMPLE_ARGS['min_count'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['saved_question_group'] = Group
COMPLEX_ARGS['row_filter_group'] = Group

LIST_ARGS = {}
# no LIST_ARGS defined
