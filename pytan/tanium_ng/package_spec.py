"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``package_spec``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class PackageSpec(BaseType):

    _soap_tag = 'package_spec'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.name = None
        self.display_name = None
        self.command = None
        self.command_timeout = None
        self.expire_seconds = None
        self.hidden_flag = None
        self.signature = None
        self.source_id = None
        self.verify_group_id = None
        self.verify_expire_seconds = None
        self.skip_lock_flag = None
        self.parameter_definition = None
        self.creation_time = None
        self.modification_time = None
        self.last_modified_by = None
        self.available_time = None
        self.deleted_flag = None
        self.last_update = None
        self.cache_row_id = None
        self.files = None
        self.file_templates = None
        self.verify_group = None
        self.parameters = None
        self.sensors = None
        self.metadata = None
        # no list_properties defined


from .metadata_list import MetadataList
from .package_file_list import PackageFileList
from .parameter_list import ParameterList
from .group import Group
from .package_file_template_list import PackageFileTemplateList
from .sensor_list import SensorList

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
SIMPLE_ARGS['display_name'] = text_type
SIMPLE_ARGS['command'] = text_type
SIMPLE_ARGS['command_timeout'] = int
SIMPLE_ARGS['expire_seconds'] = int
SIMPLE_ARGS['hidden_flag'] = int
SIMPLE_ARGS['signature'] = text_type
SIMPLE_ARGS['source_id'] = int
SIMPLE_ARGS['verify_group_id'] = int
SIMPLE_ARGS['verify_expire_seconds'] = int
SIMPLE_ARGS['skip_lock_flag'] = int
SIMPLE_ARGS['parameter_definition'] = text_type
SIMPLE_ARGS['creation_time'] = text_type
SIMPLE_ARGS['modification_time'] = text_type
SIMPLE_ARGS['last_modified_by'] = text_type
SIMPLE_ARGS['available_time'] = text_type
SIMPLE_ARGS['deleted_flag'] = int
SIMPLE_ARGS['last_update'] = text_type
SIMPLE_ARGS['cache_row_id'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['files'] = PackageFileList
COMPLEX_ARGS['file_templates'] = PackageFileTemplateList
COMPLEX_ARGS['verify_group'] = Group
COMPLEX_ARGS['parameters'] = ParameterList
COMPLEX_ARGS['sensors'] = SensorList
COMPLEX_ARGS['metadata'] = MetadataList

LIST_ARGS = {}
# no LIST_ARGS defined
