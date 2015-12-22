"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``question``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class Question(BaseType):

    _soap_tag = 'question'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.expire_seconds = None
        self.skip_lock_flag = None
        self.expiration = None
        self.name = None
        self.query_text = None
        self.hidden_flag = None
        self.action_tracking_flag = None
        self.force_computer_id_flag = None
        self.cache_row_id = None
        self.index = None
        self.selects = None
        self.context_group = None
        self.group = None
        self.user = None
        self.management_rights_group = None
        self.saved_question = None
        # no list_properties defined


from .select_list import SelectList
from .user import User
from .group import Group
from .saved_question import SavedQuestion

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['expire_seconds'] = int
SIMPLE_ARGS['skip_lock_flag'] = int
SIMPLE_ARGS['expiration'] = str
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['query_text'] = str
SIMPLE_ARGS['hidden_flag'] = int
SIMPLE_ARGS['action_tracking_flag'] = int
SIMPLE_ARGS['force_computer_id_flag'] = int
SIMPLE_ARGS['cache_row_id'] = int
SIMPLE_ARGS['index'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['selects'] = SelectList
COMPLEX_ARGS['context_group'] = Group
COMPLEX_ARGS['group'] = Group
COMPLEX_ARGS['user'] = User
COMPLEX_ARGS['management_rights_group'] = Group
COMPLEX_ARGS['saved_question'] = SavedQuestion

LIST_ARGS = {}
# no LIST_ARGS defined
