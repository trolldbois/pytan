"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``action``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class Action(BaseType):

    _soap_tag = 'action'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.name = None
        self.comment = None
        self.start_time = None
        self.expiration_time = None
        self.status = None
        self.skip_lock_flag = None
        self.expire_seconds = None
        self.distribute_seconds = None
        self.creation_time = None
        self.stopped_flag = None
        self.cache_row_id = None
        self.target_group = None
        self.action_group = None
        self.package_spec = None
        self.user = None
        self.approver = None
        self.history_saved_question = None
        self.saved_action = None
        self.metadata = None
        # no list_properties defined


from .saved_action import SavedAction
from .saved_question import SavedQuestion
from .metadata_list import MetadataList
from .package_spec import PackageSpec
from .user import User
from .group import Group

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['comment'] = str
SIMPLE_ARGS['start_time'] = str
SIMPLE_ARGS['expiration_time'] = str
SIMPLE_ARGS['status'] = str
SIMPLE_ARGS['skip_lock_flag'] = int
SIMPLE_ARGS['expire_seconds'] = int
SIMPLE_ARGS['distribute_seconds'] = int
SIMPLE_ARGS['creation_time'] = str
SIMPLE_ARGS['stopped_flag'] = int
SIMPLE_ARGS['cache_row_id'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['target_group'] = Group
COMPLEX_ARGS['action_group'] = Group
COMPLEX_ARGS['package_spec'] = PackageSpec
COMPLEX_ARGS['user'] = User
COMPLEX_ARGS['approver'] = User
COMPLEX_ARGS['history_saved_question'] = SavedQuestion
COMPLEX_ARGS['saved_action'] = SavedAction
COMPLEX_ARGS['metadata'] = MetadataList

LIST_ARGS = {}
# no LIST_ARGS defined
