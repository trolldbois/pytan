"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``saved_question``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class SavedQuestion(BaseType):

    _soap_tag = 'saved_question'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.name = None
        self.public_flag = None
        self.hidden_flag = None
        self.issue_seconds = None
        self.issue_seconds_never_flag = None
        self.expire_seconds = None
        self.sort_column = None
        self.query_text = None
        self.row_count_flag = None
        self.keep_seconds = None
        self.archive_enabled_flag = None
        self.most_recent_question_id = None
        self.action_tracking_flag = None
        self.mod_time = None
        self.index = None
        self.cache_row_id = None
        self.question = None
        self.packages = None
        self.user = None
        self.archive_owner = None
        self.mod_user = None
        self.metadata = None
        # no list_properties defined


from .question import Question
from .metadata_list import MetadataList
from .user import User
from .package_spec_list import PackageSpecList

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['public_flag'] = int
SIMPLE_ARGS['hidden_flag'] = int
SIMPLE_ARGS['issue_seconds'] = int
SIMPLE_ARGS['issue_seconds_never_flag'] = int
SIMPLE_ARGS['expire_seconds'] = int
SIMPLE_ARGS['sort_column'] = int
SIMPLE_ARGS['query_text'] = str
SIMPLE_ARGS['row_count_flag'] = int
SIMPLE_ARGS['keep_seconds'] = int
SIMPLE_ARGS['archive_enabled_flag'] = int
SIMPLE_ARGS['most_recent_question_id'] = int
SIMPLE_ARGS['action_tracking_flag'] = int
SIMPLE_ARGS['mod_time'] = str
SIMPLE_ARGS['index'] = int
SIMPLE_ARGS['cache_row_id'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['question'] = Question
COMPLEX_ARGS['packages'] = PackageSpecList
COMPLEX_ARGS['user'] = User
COMPLEX_ARGS['archive_owner'] = User
COMPLEX_ARGS['mod_user'] = User
COMPLEX_ARGS['metadata'] = MetadataList

LIST_ARGS = {}
# no LIST_ARGS defined
