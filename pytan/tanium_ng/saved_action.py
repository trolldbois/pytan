"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``saved_action``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class SavedAction(BaseType):

    _soap_tag = 'saved_action'

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
        self.status = None
        self.issue_seconds = None
        self.distribute_seconds = None
        self.start_time = None
        self.end_time = None
        self.action_group_id = None
        self.public_flag = None
        self.policy_flag = None
        self.expire_seconds = None
        self.approved_flag = None
        self.issue_count = None
        self.creation_time = None
        self.next_start_time = None
        self.last_start_time = None
        self.user_start_time = None
        self.cache_row_id = None
        self.package_spec = None
        self.action_group = None
        self.target_group = None
        self.policy = None
        self.metadata = None
        self.row_ids = None
        self.user = None
        self.approver = None
        self.last_action = None
        # no list_properties defined


from .metadata_list import MetadataList
from .saved_action_row_id_list import SavedActionRowIdList
from .group import Group
from .action import Action
from .user import User
from .package_spec import PackageSpec
from .saved_action_policy import SavedActionPolicy

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = text_type
SIMPLE_ARGS['comment'] = text_type
SIMPLE_ARGS['status'] = int
SIMPLE_ARGS['issue_seconds'] = int
SIMPLE_ARGS['distribute_seconds'] = int
SIMPLE_ARGS['start_time'] = text_type
SIMPLE_ARGS['end_time'] = text_type
SIMPLE_ARGS['action_group_id'] = int
SIMPLE_ARGS['public_flag'] = int
SIMPLE_ARGS['policy_flag'] = int
SIMPLE_ARGS['expire_seconds'] = int
SIMPLE_ARGS['approved_flag'] = int
SIMPLE_ARGS['issue_count'] = int
SIMPLE_ARGS['creation_time'] = text_type
SIMPLE_ARGS['next_start_time'] = text_type
SIMPLE_ARGS['last_start_time'] = text_type
SIMPLE_ARGS['user_start_time'] = text_type
SIMPLE_ARGS['cache_row_id'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['package_spec'] = PackageSpec
COMPLEX_ARGS['action_group'] = Group
COMPLEX_ARGS['target_group'] = Group
COMPLEX_ARGS['policy'] = SavedActionPolicy
COMPLEX_ARGS['metadata'] = MetadataList
COMPLEX_ARGS['row_ids'] = SavedActionRowIdList
COMPLEX_ARGS['user'] = User
COMPLEX_ARGS['approver'] = User
COMPLEX_ARGS['last_action'] = Action

LIST_ARGS = {}
# no LIST_ARGS defined
