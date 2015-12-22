"""Tanium NG: A Python object representation layer for the XML used by the Tanium SOAP API.

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T15-43-08Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
BASE_TYPES = {}
"""Maps Tanium XML soap tags to the Tanium NG Python BaseType object"""
BASE_TYPES['action'] = 'Action'
BASE_TYPES['actions'] = 'ActionList'
BASE_TYPES['info'] = 'ActionListInfo'
BASE_TYPES['action_stop'] = 'ActionStop'
BASE_TYPES['action_stops'] = 'ActionStopList'
BASE_TYPES['archived_question'] = 'ArchivedQuestion'
BASE_TYPES['archived_questions'] = 'ArchivedQuestionList'
BASE_TYPES['audit_data'] = 'AuditData'
BASE_TYPES['filter'] = 'CacheFilter'
BASE_TYPES['cache_filters'] = 'CacheFilterList'
BASE_TYPES['cache_info'] = 'CacheInfo'
BASE_TYPES['client_count'] = 'ClientCount'
BASE_TYPES['client_status'] = 'ClientStatus'
BASE_TYPES['computer_group'] = 'ComputerGroup'
BASE_TYPES['computer_groups'] = 'ComputerGroupList'
BASE_TYPES['computer_spec'] = 'ComputerGroupSpec'
BASE_TYPES['computer_specs'] = 'ComputerSpecList'
BASE_TYPES['errors'] = 'ErrorList'
BASE_TYPES['filter'] = 'Filter'
BASE_TYPES['filters'] = 'FilterList'
BASE_TYPES['group'] = 'Group'
BASE_TYPES['groups'] = 'GroupList'
BASE_TYPES['item'] = 'MetadataItem'
BASE_TYPES['metadata'] = 'MetadataList'
BASE_TYPES['object_list'] = 'ObjectList'
BASE_TYPES['options'] = 'Options'
BASE_TYPES['file'] = 'PackageFile'
BASE_TYPES['package_files'] = 'PackageFileList'
BASE_TYPES['status'] = 'PackageFileStatus'
BASE_TYPES['file_status'] = 'PackageFileStatusList'
BASE_TYPES['file_template'] = 'PackageFileTemplate'
BASE_TYPES['file_templates'] = 'PackageFileTemplateList'
BASE_TYPES['package_spec'] = 'PackageSpec'
BASE_TYPES['package_specs'] = 'PackageSpecList'
BASE_TYPES['parameter'] = 'Parameter'
BASE_TYPES['parameters'] = 'ParameterList'
BASE_TYPES['parse_job'] = 'ParseJob'
BASE_TYPES['parse_jobs'] = 'ParseJobList'
BASE_TYPES['parse_result'] = 'ParseResult'
BASE_TYPES['parse_result_group'] = 'ParseResultGroup'
BASE_TYPES['parse_result_groups'] = 'ParseResultGroupList'
BASE_TYPES['parse_results'] = 'ParseResultList'
BASE_TYPES['permissions'] = 'PermissionList'
BASE_TYPES['plugin'] = 'Plugin'
BASE_TYPES['argument'] = 'PluginArgument'
BASE_TYPES['arguments'] = 'PluginArgumentList'
BASE_TYPES['commands'] = 'PluginCommandList'
BASE_TYPES['plugins'] = 'PluginList'
BASE_TYPES['plugin_schedule'] = 'PluginSchedule'
BASE_TYPES['plugin_schedules'] = 'PluginScheduleList'
BASE_TYPES['sql_response'] = 'PluginSql'
BASE_TYPES['columns'] = 'PluginSqlColumn'
BASE_TYPES['result_row'] = 'PluginSqlResult'
BASE_TYPES['question'] = 'Question'
BASE_TYPES['questions'] = 'QuestionList'
BASE_TYPES['info'] = 'QuestionListInfo'
BASE_TYPES['saved_action'] = 'SavedAction'
BASE_TYPES['saved_action_approval'] = 'SavedActionApproval'
BASE_TYPES['saved_actions'] = 'SavedActionList'
BASE_TYPES['policy'] = 'SavedActionPolicy'
BASE_TYPES['row_ids'] = 'SavedActionRowIdList'
BASE_TYPES['saved_question'] = 'SavedQuestion'
BASE_TYPES['saved_questions'] = 'SavedQuestionList'
BASE_TYPES['select'] = 'Select'
BASE_TYPES['selects'] = 'SelectList'
BASE_TYPES['sensor'] = 'Sensor'
BASE_TYPES['sensors'] = 'SensorList'
BASE_TYPES['query'] = 'SensorQuery'
BASE_TYPES['queries'] = 'SensorQueryList'
BASE_TYPES['subcolumn'] = 'SensorSubcolumn'
BASE_TYPES['subcolumns'] = 'SensorSubcolumnList'
BASE_TYPES['soap_error'] = 'SoapError'
BASE_TYPES['string_hints'] = 'StringHintList'
BASE_TYPES['system_setting'] = 'SystemSetting'
BASE_TYPES['system_settings'] = 'SystemSettingList'
BASE_TYPES['aggregate'] = 'SystemStatusAggregate'
BASE_TYPES['system_status'] = 'SystemStatusList'
BASE_TYPES['upload_file'] = 'UploadFile'
BASE_TYPES['file_parts'] = 'UploadFileList'
BASE_TYPES['upload_file_status'] = 'UploadFileStatus'
BASE_TYPES['user'] = 'User'
BASE_TYPES['users'] = 'UserList'
BASE_TYPES['role'] = 'UserRole'
BASE_TYPES['roles'] = 'UserRoleList'
BASE_TYPES['version'] = 'VersionAggregate'
BASE_TYPES['versions'] = 'VersionAggregateList'
BASE_TYPES['white_listed_url'] = 'WhiteListedUrl'
BASE_TYPES['white_listed_urls'] = 'WhiteListedUrlList'
BASE_TYPES['error'] = 'XmlError'

SENSOR_TYPE_MAP = {
    0: 'Hash',
    # SENSOR_RESULT_TYPE_STRING
    1: 'String',
    # SENSOR_RESULT_TYPE_VERSION
    2: 'Version',
    # SENSOR_RESULT_TYPE_NUMERIC
    3: 'NumericDecimal',
    # SENSOR_RESULT_TYPE_DATE_BES
    4: 'BESDate',
    # SENSOR_RESULT_TYPE_IPADDRESS
    5: 'IPAddress',
    # SENSOR_RESULT_TYPE_DATE_WMI
    6: 'WMIDate',
    #  e.g. "2 years, 3 months, 18 days, 4 hours, 22 minutes:
    # 'TimeDiff', and 3.67 seconds" or "4.2 hours"
    # (numeric + "Y|MO|W|D|H|M|S" units)
    7: 'TimeDiff',
    #  e.g. 125MB or 23K or 34.2Gig (numeric + B|K|M|G|T units)
    8: 'DataSize',
    9: 'NumericInteger',
    10: 'VariousDate',
    11: 'RegexMatch',
    12: 'LastOperatorType',
}
"""Maps Column types in ResultSets from an int to a string."""

import sys
from collections import OrderedDict

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
    encoding = "unicode"
else:
    text_type = unicode  # noqa
    encoding = "us-ascii"


class TaniumNextGenException(Exception):
    pass


class IncorrectTypeException(TaniumNextGenException):
    """Raised when a property is not of the expected type"""
    def __init__(self, name, value, expected):
        self.name = name
        self.expected = expected
        self.value = value
        err = "Attribute '{}' expected type '{}', got '{}' (value: '{}')"
        err = err.format(name, expected.__name__, type(value).__name__, value)
        TaniumNextGenException.__init__(self, err)


class BaseType(object):

    _soap_tag = None

    def __init__(self, simple_properties, complex_properties, list_properties, **kwargs):
        self._initialized = False
        self._simple_properties = simple_properties
        self._complex_properties = complex_properties
        self._list_properties = list_properties
        self._initialized = True

    def __getitem__(self, idx):
        """Allow automatic indexing into lists."""
        if not self._is_list():
            err = 'Not a list type, __getitem__ not supported'
            raise TaniumNextGenException(err)
        result = getattr(self, self._get_list_attr())[idx]
        return result

    def __len__(self):
        """Allow len() for lists and str"""
        result = 0
        if self._is_list():
            result = len(getattr(self, self._get_list_attr()))
        elif getattr(self, 'name', ''):
            result = len(str(self.name))
        elif getattr(self, 'id', ''):
            result = len(str(self.id))
        return result

    def __str__(self):
        class_name = self.__class__.__name__
        vals = OrderedDict()
        if self._is_list():
            vals['length'] = len(self)
        else:
            for k in ['id', 'name']:
                if not hasattr(self, k):
                    continue
                vals[k] = getattr(self, k, None)

            for k in ['query_text', 'hidden_flag', 'package_spec', 'url_regex']:
                if not getattr(self, k, None):
                    continue
                vals[k] = getattr(self, k, None)

        if not vals:
            for k in sorted(self._simple_properties):
                val = getattr(self, k, None)
                if val is not None:
                    vals[k] = val

        if vals:
            vals = ', '.join(["'{}'='{}'".format(*p) for p in vals.items()])
        else:
            vals = "No attributes assigned yet!"

        result = '{}: {}'.format(class_name, vals)
        return result

    def __setattr__(self, name, value):
        """Enforce type of attribute assignments"""
        val_not_none = value is not None
        name_not_init = name != '_initialized'
        self_is_init = getattr(self, '_initialized', False)
        check_type = all([val_not_none, name_not_init, self_is_init])

        if check_type:
            if name in getattr(self, '_complex_properties', {}):
                value = self._check_complex(name, value)
            elif name in getattr(self, '_simple_properties', {}):
                value = self._check_simple(name, value)
            elif name in getattr(self, '_list_properties', {}):
                value = self._check_list(name, value)
        super(BaseType, self).__setattr__(name, value)

    def _set_values(self, values):
        for k, v in values.items():
            setattr(self, k, v)

    def _is_list(self):
        result = len(self._list_properties) == 1
        return result

    def _get_list_attr(self):
        result = None
        if self._is_list:
            result = list(self._list_properties.keys())[0]
        return result

    def _check_complex(self, name, value):
        if not isinstance(value, self._complex_properties[name]):
            raise IncorrectTypeException(name, value, self._complex_properties[name])
        return value

    def _check_simple(self, name, value):
        if not isinstance(value, self._simple_properties[name]):
            try:
                value = self._simple_properties[name](value)
            except:
                raise IncorrectTypeException(name, value, self._simple_properties[name])
        return value

    def _check_list(self, name, value):
        if value != [] and not isinstance(value, self._list_properties[name]):
            raise IncorrectTypeException(name, value, self._list_properties[name])
        return value

    def append(self, n):
        """Allow adding to list."""
        if not self._is_list():
            err = 'Not a list type, append not supported'
            raise TaniumNextGenException(err)
        getattr(self, self._get_list_attr()).append(n)

    def to_soap_element(self, minimal=False):  # noqa
        # print(minimal)
        root = ET.Element(self._soap_tag)
        for p in self._simple_properties:
            el = ET.Element(p)
            val = getattr(self, p)
            # print(p, val)
            if val is not None:
                el.text = str(val)
            if val is not None or not minimal:
                root.append(el)
        for p, t in self._complex_properties.items():
            val = getattr(self, p)
            # print(p, t, val)
            if val is not None or not minimal:
                if val is not None and not isinstance(val, t):
                    raise IncorrectTypeException(p, t, type(val))
                if isinstance(val, BaseType):
                    child = val.to_soap_element(minimal=minimal)
                    # the tag name is the property name,
                    # not the property type's soap tag
                    el = ET.Element(p)
                    if child.getchildren() is not None:
                        for child_prop in child.getchildren():
                            el.append(child_prop)
                    root.append(el)
                else:
                    el = ET.Element(p)
                    root.append(el)
                    if val is not None:
                        el.append(str(val))
        for p, t in self._list_properties.items():
            vals = getattr(self, p)
            # print(p, t, vals)
            if not vals:
                continue
            # fix for str types in list props
            if issubclass(t, BaseType):
                for val in vals:
                    # print(val, type(val))
                    root.append(val.to_soap_element(minimal=minimal))
            else:
                for val in vals:
                    el = ET.Element(p)
                    root.append(el)
                    if val is not None:
                        el.text = str(val)
                    if vals is not None or not minimal:
                        root.append(el)
        return root

    def to_soap_body(self, minimal=False):
        """Deserialize self into an XML body"""
        el = self.to_soap_element(minimal=minimal)
        result = ET.tostring(el, encoding=encoding)
        # print(result)
        return result

    @classmethod
    def from_soap_element(cls, el):
        result = cls()
        for p, t in result._simple_properties.items():
            pel = el.find("./{}".format(p))
            if pel is not None and pel.text:
                setattr(result, p, t(pel.text))
            else:
                setattr(result, p, None)
        for p, t in result._complex_properties.items():
            elems = el.findall('./{}'.format(p))
            if len(elems) > 1:
                raise TaniumNextGenException(
                    'Unexpected: {} elements for property'.format(p)
                )
            elif len(elems) == 1:
                setattr(
                    result,
                    p,
                    result._complex_properties[p].from_soap_element(elems[0]),
                )
            else:
                setattr(result, p, None)
        for p, t in result._list_properties.items():
            setattr(result, p, [])
            elems = el.findall('./{}'.format(p))
            for elem in elems:
                if issubclass(t, BaseType):
                    getattr(result, p).append(t.from_soap_element(elem))
                else:
                    getattr(result, p).append(elem.text)

        return result

    @classmethod
    def _get_obj_type(cls, el):
        """Based on the tag of ``el``, find the appropriate tanium_type."""
        if el.tag not in BASE_TYPES:
            err = 'Unknown type {}'
            err = err.format(el.tag)
            raise TaniumNextGenException(err)
        result = eval(BASE_TYPES[el.tag])
        return result

    @classmethod
    def from_soap_body(cls, body):
        """Parse text ``body`` as XML and produce Python tanium objects.

        This method assumes a single <result_object>, which may be a list or a single object.
        """
        tree = ET.fromstring(body)
        el = tree.find(".//result_object/*")
        if el is None:
            result = el
        if el is not None:
            obj = cls._get_obj_type(el)
            result = obj.from_soap_element(el)
            result._ORIGINAL_OBJECT = el
        return result


class Row(object):
    """A row in a result set.

    Values are stored in column order, also accessible
    by key using []
    """

    def __init__(self, columns):
        self.id = None
        self.cid = None
        self.vals = []
        self.columns = columns

    def __str__(self):
        class_name = self.__class__.__name__
        val = ', '.join([
            "{}:{}".format(
                self.columns[i].display_name,
                len(self.vals[i]),
            )
            for i, _ in enumerate(self.columns)
        ])
        ret = '{}: {}'.format(class_name, val)
        return ret

    @classmethod
    def from_soap_element(cls, el, columns):
        row = Row(columns)
        val = el.find("id")
        if val is not None:
            row.id = val.text
        val = el.find("cid")
        if val is not None:
            row.cid = val.text
        row_cols = el.findall("c")
        for rc in row_cols:
            row_vals = rc.findall("v")
            vals_text = [v.text for v in row_vals]
            row.vals.append(vals_text)
        return row

    def __len__(self):
        return len(self.vals)

    def __getitem__(self, column_name):
        for i in range(len(self.columns)):
            if self.columns[i].display_name == column_name:
                return self.vals[i]
        raise Exception('Column {} not found'.format(column_name))


class Column(object):

    def __init__(self):
        self.what_hash = None
        self.display_name = None
        self.result_type = None

    def __str__(self):
        class_name = self.__class__.__name__
        val = self.display_name
        ret = '{}: {}'.format(class_name, val)
        return ret

    @classmethod
    def from_soap_element(cls, el):
        result = Column()
        val = el.find('wh')
        if val is not None:
            result.what_hash = int(val.text)
        val = el.find('dn')
        if val is not None:
            result.display_name = val.text
        val = el.find('rt')
        if val is not None:
            val = int(val.text)
            if val in SENSOR_TYPE_MAP:
                result.result_type = SENSOR_TYPE_MAP[val]
            else:
                result.result_type = int(val)

        return result


class ColumnSet(object):

    def __init__(self):
        self.columns = []

    def __str__(self):
        class_name = self.__class__.__name__
        val = ', '.join([str(x.display_name) for x in self.columns])
        ret = '{}: {}'.format(class_name, val)
        return ret

    @classmethod
    def from_soap_elment(cls, el):
        result = ColumnSet()
        columns = el.findall('./c')
        for column in columns:
            result.columns.append(Column.from_soap_element(column))
        return result

    def __len__(self):
        return len(self.columns)

    def __getitem__(self, ndx):
        return self.columns[ndx]


class ResultInfo(object):
    """Wrap the result of GetResultInfo"""

    def __init__(self):
        self.age = None
        self.id = None
        self.report_count = None
        self.question_id = None
        self.archived_question_id = None
        self.seconds_since_issued = None
        self.issue_seconds = None
        self.expire_seconds = None
        self.tested = None
        self.passed = None
        self.mr_tested = None
        self.mr_passed = None
        self.estimated_total = None
        self.select_count = None
        self.row_count = None
        self.error_count = None
        self.no_result_count = None
        self.row_count_machines = None
        self.row_count_flag = None

    def __str__(self):
        class_name = self.__class__.__name__
        q_id = getattr(self, 'question_id', -1)
        total_rows = getattr(self, 'row_count', -1)
        est_total = getattr(self, 'estimated_total', -1)
        passed = getattr(self, 'passed', -1)
        mr_passed = getattr(self, 'mr_passed', -1)
        tested = getattr(self, 'tested', -1)
        mr_tested = getattr(self, 'mr_tested', -1)
        ret_str = (
            '{} for ID {!r}, Total Rows: {}, EstTotal: {}, '
            'Passed: {}, MrPassed: {}, Tested: {}, MrTested: {}'
        ).format

        ret = ret_str(class_name, q_id, total_rows, est_total, passed,
                      mr_passed, tested, mr_tested)
        return ret

    @classmethod
    def from_soap_element(cls, el):
        """Deserialize a ResultInfo from a result_info SOAPElement

        Assumes all properties are integer values (true today)

        """
        result = ResultInfo()
        for property in vars(result):
            val = el.find('.//{}'.format(property))
            if val is not None and val.text:
                setattr(result, property, int(val.text))
        return result


class ResultSet(object):
    """Wrap the result of GetResultData"""

    def __init__(self):
        self.age = None
        self.id = None
        self.report_count = None
        self.question_id = None
        self.archived_question_id = None
        self.seconds_since_issued = None
        self.issue_seconds = None
        self.expire_seconds = None
        self.tested = None
        self.passed = None
        self.mr_tested = None
        self.mr_passed = None
        self.estimated_total = None
        self.select_count = None
        self.row_count = None
        self.error_count = None
        self.no_result_count = None
        self.row_count_machines = None
        self.row_count_flag = None
        self.columns = None
        self.rows = None
        self.cache_id = None
        self.expiration = None
        self.filtered_row_count = None
        self.filtered_row_count_machines = None
        self.item_count = None

    def __str__(self):
        class_name = self.__class__.__name__
        q_id = getattr(self, 'question_id', -1)
        r_cols = len(getattr(self, 'columns', []) or [])
        total_rows = getattr(self, 'row_count', -1)
        current_rows = len(getattr(self, 'rows', []))
        est_total = getattr(self, 'estimated_total', -1)
        passed = getattr(self, 'passed', -1)
        mr_passed = getattr(self, 'mr_passed', -1)
        tested = getattr(self, 'tested', -1)
        mr_tested = getattr(self, 'mr_tested', -1)
        ret_str = (
            '{} for ID {!r}, Columns: {}, Total Rows: {}, Current Rows: {}, EstTotal: {}, '
            'Passed: {}, MrPassed: {}, Tested: {}, MrTested: {}'
        ).format

        ret = ret_str(class_name, q_id, r_cols, total_rows, current_rows, est_total, passed,
                      mr_passed, tested, mr_tested)
        return ret

    def __len__(self):
        """Allow len() for rows"""
        rows = getattr(self, 'rows', []) or []
        return len(rows)

    @classmethod
    def from_soap_element(cls, el):  # noqa
        """Deserialize a ResultSet from a result_set SOAPElement"""
        result = ResultSet()
        for property in vars(result):
            if property in ['column_set', 'row_set']:
                continue
            val = el.find('.//{}'.format(property))
            if val is not None and val.text:
                setattr(result, property, int(val.text))
        val = el.find('.//cs')
        if val is not None:
            result.columns = ColumnSet.from_soap_element(val)
        result.rows = []
        # TODO: Make sure that each "r" is a row, with one value
        # per column in "c/v". This was tested with just one client.
        rows = el.findall('.//rs/r')
        for row in rows:
            result.rows.append(Row.from_soap_element(row, result.columns))
        return result


class Action(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``action``."""

    _soap_tag = 'action'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'comment': text_type,
                'start_time': text_type,
                'expiration_time': text_type,
                'status': text_type,
                'skip_lock_flag': int,
                'expire_seconds': int,
                'distribute_seconds': int,
                'creation_time': text_type,
                'stopped_flag': int,
                'cache_row_id': int,
            },
            complex_properties={
                'target_group': Group,
                'action_group': Group,
                'package_spec': PackageSpec,
                'user': User,
                'approver': User,
                'history_saved_question': SavedQuestion,
                'saved_action': SavedAction,
                'metadata': MetadataList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
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
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ActionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``actions``."""

    _soap_tag = 'actions'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'info': ActionListInfo,
                'cache_info': CacheInfo,
            },
            list_properties={
                'action': Action,
            },
        )
        # no simple_properties defined in console.wsdl
        self.info = None
        self.cache_info = None
        self.action = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ActionListInfo(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``info``."""

    _soap_tag = 'info'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'highest_id': int,
                'total_count': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.highest_id = None
        self.total_count = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ActionStop(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``action_stop``."""

    _soap_tag = 'action_stop'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
            },
            complex_properties={
                'action': Action,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.action = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ActionStopList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``action_stops``."""

    _soap_tag = 'action_stops'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'action_stop': ActionStop,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.action_stop = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ArchivedQuestion(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``archived_question``."""

    _soap_tag = 'archived_question'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ArchivedQuestionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``archived_questions``."""

    _soap_tag = 'archived_questions'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'archived_question': ArchivedQuestion,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.archived_question = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class AuditData(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``audit_data``."""

    _soap_tag = 'audit_data'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'creation_time': text_type,
                'modification_time': text_type,
                'last_modified_by': text_type,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.creation_time = None
        self.modification_time = None
        self.last_modified_by = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class CacheFilter(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``filter``."""

    _soap_tag = 'filter'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'field': text_type,
                'value': text_type,
                'type': text_type,
                'operator': text_type,
                'not_flag': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.field = None
        self.value = None
        self.type = None
        self.operator = None
        self.not_flag = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class CacheFilterList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``cache_filters``."""

    _soap_tag = 'cache_filters'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'filter': CacheFilter,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.filter = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class CacheInfo(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``cache_info``."""

    _soap_tag = 'cache_info'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'cache_id': int,
                'page_row_count': int,
                'filtered_row_count': int,
                'cache_row_count': int,
                'expiration': text_type,
            },
            complex_properties={
                'errors': ErrorList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.cache_id = None
        self.page_row_count = None
        self.filtered_row_count = None
        self.cache_row_count = None
        self.expiration = None
        self.errors = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ClientCount(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``client_count``."""

    _soap_tag = 'client_count'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ClientStatus(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``client_status``."""

    _soap_tag = 'client_status'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'host_name': text_type,
                'computer_id': text_type,
                'ipaddress_client': text_type,
                'ipaddress_server': text_type,
                'protocol_version': int,
                'full_version': text_type,
                'last_registration': text_type,
                'send_state': text_type,
                'receive_state': text_type,
                'status': text_type,
                'port_number': int,
                'public_key_valid': int,
                'cache_row_id': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.host_name = None
        self.computer_id = None
        self.ipaddress_client = None
        self.ipaddress_server = None
        self.protocol_version = None
        self.full_version = None
        self.last_registration = None
        self.send_state = None
        self.receive_state = None
        self.status = None
        self.port_number = None
        self.public_key_valid = None
        self.cache_row_id = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ComputerGroup(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``computer_group``."""

    _soap_tag = 'computer_group'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'deleted_flag': int,
            },
            complex_properties={
                'computer_specs': ComputerSpecList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.deleted_flag = None
        self.computer_specs = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ComputerGroupList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``computer_groups``."""

    _soap_tag = 'computer_groups'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'computer_group': ComputerGroup,
            },
        )
        # no simple_properties defined in console.wsdl
        self.cache_info = None
        self.computer_group = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ComputerGroupSpec(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``computer_spec``."""

    _soap_tag = 'computer_spec'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'computer_name': text_type,
                'ip_address': text_type,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.computer_name = None
        self.ip_address = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ComputerSpecList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``computer_specs``."""

    _soap_tag = 'computer_specs'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'computer_spec': ComputerGroupSpec,
            },
        )
        # no simple_properties defined in console.wsdl
        self.cache_info = None
        self.computer_spec = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ErrorList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``errors``."""

    _soap_tag = 'errors'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'error': XmlError,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.error = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class Filter(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``filter``."""

    _soap_tag = 'filter'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'operator': text_type,
                'value_type': text_type,
                'value': text_type,
                'not_flag': int,
                'max_age_seconds': int,
                'ignore_case_flag': int,
                'all_values_flag': int,
                'substring_flag': int,
                'substring_start': int,
                'substring_length': int,
                'delimiter': text_type,
                'delimiter_index': int,
                'utf8_flag': int,
                'aggregation': text_type,
                'all_times_flag': int,
                'start_time': text_type,
                'end_time': text_type,
            },
            complex_properties={
                'sensor': Sensor,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.operator = None
        self.value_type = None
        self.value = None
        self.not_flag = None
        self.max_age_seconds = None
        self.ignore_case_flag = None
        self.all_values_flag = None
        self.substring_flag = None
        self.substring_start = None
        self.substring_length = None
        self.delimiter = None
        self.delimiter_index = None
        self.utf8_flag = None
        self.aggregation = None
        self.all_times_flag = None
        self.start_time = None
        self.end_time = None
        self.sensor = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class FilterList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``filters``."""

    _soap_tag = 'filters'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'filter': Filter,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.filter = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class Group(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``group``."""

    _soap_tag = 'group'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'text': text_type,
                'and_flag': int,
                'not_flag': int,
                'type': int,
                'source_id': int,
                'deleted_flag': int,
            },
            complex_properties={
                'sub_groups': GroupList,
                'filters': FilterList,
                'parameters': ParameterList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.text = None
        self.and_flag = None
        self.not_flag = None
        self.type = None
        self.source_id = None
        self.deleted_flag = None
        self.sub_groups = None
        self.filters = None
        self.parameters = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class GroupList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``groups``."""

    _soap_tag = 'groups'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'group': Group,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.group = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class MetadataItem(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``item``."""

    _soap_tag = 'item'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'name': text_type,
                'value': text_type,
                'admin_flag': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.name = None
        self.value = None
        self.admin_flag = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class MetadataList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``metadata``."""

    _soap_tag = 'metadata'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'item': MetadataItem,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.item = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ObjectList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``object_list``."""

    _soap_tag = 'object_list'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'export_id': text_type,
            },
            complex_properties={
                'questions': QuestionList,
                'actions': ActionList,
                'saved_actions': SavedActionList,
                'roles': UserRoleList,
                'system_status': SystemStatusList,
                'system_settings': SystemSettingList,
                'client_count': ClientCount,
                'white_listed_urls': WhiteListedUrlList,
                'computer_groups': ComputerGroupList,
            },
            list_properties={
                'question': Question,
                'group': Group,
                'groups': GroupList,
                'saved_question': SavedQuestion,
                'saved_questions': SavedQuestionList,
                'archived_question': ArchivedQuestion,
                'archived_questions': ArchivedQuestionList,
                'parse_job': ParseJob,
                'parse_jobs': ParseJobList,
                'parse_result_group': ParseResultGroup,
                'parse_result_groups': ParseResultGroupList,
                'action': Action,
                'saved_action': SavedAction,
                'action_stop': ActionStop,
                'action_stops': ActionStopList,
                'package_spec': PackageSpec,
                'package_specs': PackageSpecList,
                'package_file': PackageFile,
                'package_files': PackageFileList,
                'sensor': Sensor,
                'sensors': SensorList,
                'user': User,
                'users': UserList,
                'client_status': ClientStatus,
                'system_setting': SystemSetting,
                'saved_action_approval': SavedActionApproval,
                'plugin': Plugin,
                'plugins': PluginList,
                'plugin_schedule': PluginSchedule,
                'plugin_schedules': PluginScheduleList,
                'white_listed_url': WhiteListedUrl,
                'upload_file': UploadFile,
                'upload_file_status': UploadFileStatus,
                'soap_error': SoapError,
                'computer_group': ComputerGroup,
            },
        )
        self.export_id = None
        self.questions = None
        self.actions = None
        self.saved_actions = None
        self.roles = None
        self.system_status = None
        self.system_settings = None
        self.client_count = None
        self.white_listed_urls = None
        self.computer_groups = None
        self.question = []
        self.group = []
        self.groups = []
        self.saved_question = []
        self.saved_questions = []
        self.archived_question = []
        self.archived_questions = []
        self.parse_job = []
        self.parse_jobs = []
        self.parse_result_group = []
        self.parse_result_groups = []
        self.action = []
        self.saved_action = []
        self.action_stop = []
        self.action_stops = []
        self.package_spec = []
        self.package_specs = []
        self.package_file = []
        self.package_files = []
        self.sensor = []
        self.sensors = []
        self.user = []
        self.users = []
        self.client_status = []
        self.system_setting = []
        self.saved_action_approval = []
        self.plugin = []
        self.plugins = []
        self.plugin_schedule = []
        self.plugin_schedules = []
        self.white_listed_url = []
        self.upload_file = []
        self.upload_file_status = []
        self.soap_error = []
        self.computer_group = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class Options(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``options``."""

    _soap_tag = 'options'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'export_flag': int,
                'export_format': int,
                'export_leading_text': text_type,
                'export_trailing_text': text_type,
                'flags': int,
                'hide_errors_flag': int,
                'include_answer_times_flag': int,
                'row_counts_only_flag': int,
                'aggregate_over_time_flag': int,
                'most_recent_flag': int,
                'include_hashes_flag': int,
                'hide_no_results_flag': int,
                'use_user_context_flag': int,
                'script_data': text_type,
                'return_lists_flag': int,
                'return_cdata_flag': int,
                'pct_done_limit': int,
                'context_id': int,
                'sample_frequency': int,
                'sample_start': int,
                'sample_count': int,
                'suppress_scripts': int,
                'suppress_object_list': int,
                'row_start': int,
                'row_count': int,
                'sort_order': text_type,
                'filter_string': text_type,
                'filter_not_flag': int,
                'recent_result_buckets': text_type,
                'cache_id': int,
                'cache_expiration': int,
                'cache_sort_fields': text_type,
                'include_user_details': int,
                'include_hidden_flag': int,
                'use_error_objects': int,
                'use_json': int,
                'json_pretty_print': int,
            },
            complex_properties={
                'cache_filters': CacheFilterList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.export_flag = None
        self.export_format = None
        self.export_leading_text = None
        self.export_trailing_text = None
        self.flags = None
        self.hide_errors_flag = None
        self.include_answer_times_flag = None
        self.row_counts_only_flag = None
        self.aggregate_over_time_flag = None
        self.most_recent_flag = None
        self.include_hashes_flag = None
        self.hide_no_results_flag = None
        self.use_user_context_flag = None
        self.script_data = None
        self.return_lists_flag = None
        self.return_cdata_flag = None
        self.pct_done_limit = None
        self.context_id = None
        self.sample_frequency = None
        self.sample_start = None
        self.sample_count = None
        self.suppress_scripts = None
        self.suppress_object_list = None
        self.row_start = None
        self.row_count = None
        self.sort_order = None
        self.filter_string = None
        self.filter_not_flag = None
        self.recent_result_buckets = None
        self.cache_id = None
        self.cache_expiration = None
        self.cache_sort_fields = None
        self.include_user_details = None
        self.include_hidden_flag = None
        self.use_error_objects = None
        self.use_json = None
        self.json_pretty_print = None
        self.cache_filters = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PackageFile(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file``."""

    _soap_tag = 'file'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'hash': text_type,
                'name': text_type,
                'size': int,
                'source': text_type,
                'download_seconds': int,
                'trigger_download': int,
                'cache_status': text_type,
                'status': int,
                'bytes_downloaded': int,
                'bytes_total': int,
                'download_start_time': text_type,
                'last_download_progress_time': text_type,
                'deleted_flag': int,
            },
            complex_properties={
                'file_status': PackageFileStatusList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.hash = None
        self.name = None
        self.size = None
        self.source = None
        self.download_seconds = None
        self.trigger_download = None
        self.cache_status = None
        self.status = None
        self.bytes_downloaded = None
        self.bytes_total = None
        self.download_start_time = None
        self.last_download_progress_time = None
        self.deleted_flag = None
        self.file_status = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PackageFileList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``package_files``."""

    _soap_tag = 'package_files'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'file': PackageFile,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.file = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PackageFileStatus(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``status``."""

    _soap_tag = 'status'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'server_id': int,
                'server_name': text_type,
                'status': int,
                'cache_status': text_type,
                'cache_message': text_type,
                'bytes_downloaded': int,
                'bytes_total': int,
                'download_start_time': text_type,
                'last_download_progress_time': text_type,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.server_id = None
        self.server_name = None
        self.status = None
        self.cache_status = None
        self.cache_message = None
        self.bytes_downloaded = None
        self.bytes_total = None
        self.download_start_time = None
        self.last_download_progress_time = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PackageFileStatusList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file_status``."""

    _soap_tag = 'file_status'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'status': PackageFileStatus,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.status = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PackageFileTemplate(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file_template``."""

    _soap_tag = 'file_template'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'hash': text_type,
                'name': text_type,
                'source': text_type,
                'download_seconds': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.hash = None
        self.name = None
        self.source = None
        self.download_seconds = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PackageFileTemplateList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file_templates``."""

    _soap_tag = 'file_templates'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'file_template': PackageFileTemplate,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.file_template = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PackageSpec(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``package_spec``."""

    _soap_tag = 'package_spec'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'display_name': text_type,
                'command': text_type,
                'command_timeout': int,
                'expire_seconds': int,
                'hidden_flag': int,
                'signature': text_type,
                'source_id': int,
                'verify_group_id': int,
                'verify_expire_seconds': int,
                'skip_lock_flag': int,
                'parameter_definition': text_type,
                'creation_time': text_type,
                'modification_time': text_type,
                'last_modified_by': text_type,
                'available_time': text_type,
                'deleted_flag': int,
                'last_update': text_type,
                'cache_row_id': int,
            },
            complex_properties={
                'files': PackageFileList,
                'file_templates': PackageFileTemplateList,
                'verify_group': Group,
                'parameters': ParameterList,
                'sensors': SensorList,
                'metadata': MetadataList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
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
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PackageSpecList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``package_specs``."""

    _soap_tag = 'package_specs'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'package_spec': PackageSpec,
            },
        )
        # no simple_properties defined in console.wsdl
        self.cache_info = None
        self.package_spec = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class Parameter(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parameter``."""

    _soap_tag = 'parameter'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'key': text_type,
                'value': text_type,
                'type': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.key = None
        self.value = None
        self.type = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ParameterList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parameters``."""

    _soap_tag = 'parameters'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'parameter': Parameter,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.parameter = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ParseJob(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_job``."""

    _soap_tag = 'parse_job'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'question_text': text_type,
                'parser_version': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.question_text = None
        self.parser_version = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ParseJobList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_jobs``."""

    _soap_tag = 'parse_jobs'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'parse_job': ParseJob,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.parse_job = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ParseResult(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_result``."""

    _soap_tag = 'parse_result'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'parameter_definition': text_type,
            },
            complex_properties={
                'parameters': ParameterList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.parameter_definition = None
        self.parameters = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ParseResultGroup(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_result_group``."""

    _soap_tag = 'parse_result_group'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'score': int,
                'question_text': text_type,
            },
            complex_properties={
                'parse_results': ParseResultList,
                'question': Question,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.score = None
        self.question_text = None
        self.parse_results = None
        self.question = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ParseResultGroupList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_result_groups``."""

    _soap_tag = 'parse_result_groups'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'parse_result_group': ParseResultGroup,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.parse_result_group = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class ParseResultList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_results``."""

    _soap_tag = 'parse_results'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'parse_result': ParseResult,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.parse_result = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PermissionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``permissions``."""

    _soap_tag = 'permissions'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'permission': text_type,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.permission = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class Plugin(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``plugin``."""

    _soap_tag = 'plugin'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'name': text_type,
                'bundle': text_type,
                'plugin_server': text_type,
                'input': text_type,
                'script_response': text_type,
                'exit_code': int,
                'type': text_type,
                'path': text_type,
                'filename': text_type,
                'plugin_url': text_type,
                'run_detached_flag': int,
                'execution_id': int,
                'timeout_seconds': int,
                'cache_row_id': int,
                'local_admin_flag': int,
                'allow_rest': int,
                'raw_http_response': int,
                'raw_http_request': int,
                'use_json_flag': int,
                'status': text_type,
                'status_file_content': text_type,
            },
            complex_properties={
                'arguments': PluginArgumentList,
                'sql_response': PluginSql,
                'metadata': MetadataList,
                'commands': PluginCommandList,
                'permissions': PermissionList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.name = None
        self.bundle = None
        self.plugin_server = None
        self.input = None
        self.script_response = None
        self.exit_code = None
        self.type = None
        self.path = None
        self.filename = None
        self.plugin_url = None
        self.run_detached_flag = None
        self.execution_id = None
        self.timeout_seconds = None
        self.cache_row_id = None
        self.local_admin_flag = None
        self.allow_rest = None
        self.raw_http_response = None
        self.raw_http_request = None
        self.use_json_flag = None
        self.status = None
        self.status_file_content = None
        self.arguments = None
        self.sql_response = None
        self.metadata = None
        self.commands = None
        self.permissions = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PluginArgument(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``argument``."""

    _soap_tag = 'argument'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'name': text_type,
                'type': text_type,
                'value': text_type,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.name = None
        self.type = None
        self.value = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PluginArgumentList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``arguments``."""

    _soap_tag = 'arguments'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'argument': PluginArgument,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.argument = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PluginCommandList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``commands``."""

    _soap_tag = 'commands'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'command': text_type,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.command = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PluginList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``plugins``."""

    _soap_tag = 'plugins'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'plugin': Plugin,
            },
        )
        # no simple_properties defined in console.wsdl
        self.cache_info = None
        self.plugin = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PluginSchedule(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``plugin_schedule``."""

    _soap_tag = 'plugin_schedule'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'plugin_name': text_type,
                'plugin_bundle': text_type,
                'plugin_server': text_type,
                'start_hour': int,
                'end_hour': int,
                'start_date': int,
                'end_date': int,
                'run_on_days': text_type,
                'run_interval_seconds': int,
                'enabled': int,
                'deleted_flag': int,
                'input': text_type,
                'last_run_time': text_type,
                'last_exit_code': int,
                'last_run_text': text_type,
            },
            complex_properties={
                'arguments': PluginArgumentList,
                'user': User,
                'last_run_sql': PluginSql,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.plugin_name = None
        self.plugin_bundle = None
        self.plugin_server = None
        self.start_hour = None
        self.end_hour = None
        self.start_date = None
        self.end_date = None
        self.run_on_days = None
        self.run_interval_seconds = None
        self.enabled = None
        self.deleted_flag = None
        self.input = None
        self.last_run_time = None
        self.last_exit_code = None
        self.last_run_text = None
        self.arguments = None
        self.user = None
        self.last_run_sql = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PluginScheduleList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``plugin_schedules``."""

    _soap_tag = 'plugin_schedules'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'plugin_schedule': PluginSchedule,
            },
        )
        # no simple_properties defined in console.wsdl
        self.cache_info = None
        self.plugin_schedule = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PluginSql(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``sql_response``."""

    _soap_tag = 'sql_response'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'rows_affected': int,
                'result_count': int,
            },
            complex_properties={
                'columns': PluginSqlColumn,
            },
            list_properties={
                'result_row': PluginSqlResult,
            },
        )
        self.rows_affected = None
        self.result_count = None
        self.columns = None
        self.result_row = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PluginSqlColumn(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``columns``."""

    _soap_tag = 'columns'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'name': text_type,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.name = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class PluginSqlResult(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``result_row``."""

    _soap_tag = 'result_row'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'value': text_type,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.value = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class Question(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``question``."""

    _soap_tag = 'question'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'expire_seconds': int,
                'skip_lock_flag': int,
                'expiration': text_type,
                'name': text_type,
                'query_text': text_type,
                'hidden_flag': int,
                'action_tracking_flag': int,
                'force_computer_id_flag': int,
                'cache_row_id': int,
                'index': int,
            },
            complex_properties={
                'selects': SelectList,
                'context_group': Group,
                'group': Group,
                'user': User,
                'management_rights_group': Group,
                'saved_question': SavedQuestion,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
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
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class QuestionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``questions``."""

    _soap_tag = 'questions'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'info': QuestionListInfo,
                'cache_info': CacheInfo,
            },
            list_properties={
                'question': Question,
            },
        )
        # no simple_properties defined in console.wsdl
        self.info = None
        self.cache_info = None
        self.question = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class QuestionListInfo(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``info``."""

    _soap_tag = 'info'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'highest_id': int,
                'total_count': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.highest_id = None
        self.total_count = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SavedAction(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_action``."""

    _soap_tag = 'saved_action'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'comment': text_type,
                'status': int,
                'issue_seconds': int,
                'distribute_seconds': int,
                'start_time': text_type,
                'end_time': text_type,
                'action_group_id': int,
                'public_flag': int,
                'policy_flag': int,
                'expire_seconds': int,
                'approved_flag': int,
                'issue_count': int,
                'creation_time': text_type,
                'next_start_time': text_type,
                'last_start_time': text_type,
                'user_start_time': text_type,
                'cache_row_id': int,
            },
            complex_properties={
                'package_spec': PackageSpec,
                'action_group': Group,
                'target_group': Group,
                'policy': SavedActionPolicy,
                'metadata': MetadataList,
                'row_ids': SavedActionRowIdList,
                'user': User,
                'approver': User,
                'last_action': Action,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
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
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SavedActionApproval(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_action_approval``."""

    _soap_tag = 'saved_action_approval'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'approved_flag': int,
            },
            complex_properties={
                'metadata': MetadataList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.approved_flag = None
        self.metadata = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SavedActionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_actions``."""

    _soap_tag = 'saved_actions'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'saved_action': SavedAction,
            },
        )
        # no simple_properties defined in console.wsdl
        self.cache_info = None
        self.saved_action = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SavedActionPolicy(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``policy``."""

    _soap_tag = 'policy'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'saved_question_id': int,
                'saved_question_group_id': int,
                'row_filter_group_id': int,
                'max_age': int,
                'min_count': int,
            },
            complex_properties={
                'saved_question_group': Group,
                'row_filter_group': Group,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.saved_question_id = None
        self.saved_question_group_id = None
        self.row_filter_group_id = None
        self.max_age = None
        self.min_count = None
        self.saved_question_group = None
        self.row_filter_group = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SavedActionRowIdList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``row_ids``."""

    _soap_tag = 'row_ids'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'row_id': int,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.row_id = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SavedQuestion(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_question``."""

    _soap_tag = 'saved_question'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'public_flag': int,
                'hidden_flag': int,
                'issue_seconds': int,
                'issue_seconds_never_flag': int,
                'expire_seconds': int,
                'sort_column': int,
                'query_text': text_type,
                'row_count_flag': int,
                'keep_seconds': int,
                'archive_enabled_flag': int,
                'most_recent_question_id': int,
                'action_tracking_flag': int,
                'mod_time': text_type,
                'index': int,
                'cache_row_id': int,
            },
            complex_properties={
                'question': Question,
                'packages': PackageSpecList,
                'user': User,
                'archive_owner': User,
                'mod_user': User,
                'metadata': MetadataList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
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
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SavedQuestionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_questions``."""

    _soap_tag = 'saved_questions'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'saved_question': SavedQuestion,
            },
        )
        # no simple_properties defined in console.wsdl
        self.cache_info = None
        self.saved_question = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class Select(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``select``."""

    _soap_tag = 'select'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'sensor': Sensor,
                'filter': Filter,
                'group': Group,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        # no simple_properties defined in console.wsdl
        self.sensor = None
        self.filter = None
        self.group = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SelectList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``selects``."""

    _soap_tag = 'selects'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'select': Select,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.select = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class Sensor(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``sensor``."""

    _soap_tag = 'sensor'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'hash': int,
                'string_count': int,
                'category': text_type,
                'description': text_type,
                'source_id': int,
                'source_hash': int,
                'parameter_definition': text_type,
                'value_type': text_type,
                'max_age_seconds': int,
                'ignore_case_flag': int,
                'exclude_from_parse_flag': int,
                'delimiter': text_type,
                'creation_time': text_type,
                'modification_time': text_type,
                'last_modified_by': text_type,
                'preview_sensor_flag': int,
                'hidden_flag': int,
                'deleted_flag': int,
                'cache_row_id': int,
            },
            complex_properties={
                'queries': SensorQueryList,
                'parameters': ParameterList,
                'subcolumns': SensorSubcolumnList,
                'string_hints': StringHintList,
                'metadata': MetadataList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.hash = None
        self.string_count = None
        self.category = None
        self.description = None
        self.source_id = None
        self.source_hash = None
        self.parameter_definition = None
        self.value_type = None
        self.max_age_seconds = None
        self.ignore_case_flag = None
        self.exclude_from_parse_flag = None
        self.delimiter = None
        self.creation_time = None
        self.modification_time = None
        self.last_modified_by = None
        self.preview_sensor_flag = None
        self.hidden_flag = None
        self.deleted_flag = None
        self.cache_row_id = None
        self.queries = None
        self.parameters = None
        self.subcolumns = None
        self.string_hints = None
        self.metadata = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SensorList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``sensors``."""

    _soap_tag = 'sensors'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'sensor': Sensor,
            },
        )
        # no simple_properties defined in console.wsdl
        self.cache_info = None
        self.sensor = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SensorQuery(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``query``."""

    _soap_tag = 'query'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'platform': text_type,
                'script': text_type,
                'script_type': text_type,
                'signature': text_type,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.platform = None
        self.script = None
        self.script_type = None
        self.signature = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SensorQueryList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``queries``."""

    _soap_tag = 'queries'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'query': SensorQuery,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.query = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SensorSubcolumn(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``subcolumn``."""

    _soap_tag = 'subcolumn'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'name': text_type,
                'index': int,
                'value_type': text_type,
                'ignore_case_flag': int,
                'hidden_flag': int,
                'exclude_from_parse_flag': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.name = None
        self.index = None
        self.value_type = None
        self.ignore_case_flag = None
        self.hidden_flag = None
        self.exclude_from_parse_flag = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SensorSubcolumnList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``subcolumns``."""

    _soap_tag = 'subcolumns'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'subcolumn': SensorSubcolumn,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.subcolumn = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SoapError(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``soap_error``."""

    _soap_tag = 'soap_error'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'object_name': text_type,
                'exception_name': text_type,
                'context': text_type,
                'object_request': text_type,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.object_name = None
        self.exception_name = None
        self.context = None
        self.object_request = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class StringHintList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``string_hints``."""

    _soap_tag = 'string_hints'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'string_hint': text_type,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.string_hint = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SystemSetting(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``system_setting``."""

    _soap_tag = 'system_setting'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'value': text_type,
                'default_value': text_type,
                'value_type': text_type,
                'setting_type': text_type,
                'hidden_flag': int,
                'read_only_flag': int,
                'cache_row_id': int,
            },
            complex_properties={
                'audit_data': AuditData,
                'metadata': MetadataList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.value = None
        self.default_value = None
        self.value_type = None
        self.setting_type = None
        self.hidden_flag = None
        self.read_only_flag = None
        self.cache_row_id = None
        self.audit_data = None
        self.metadata = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SystemSettingList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``system_settings``."""

    _soap_tag = 'system_settings'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'system_setting': SystemSetting,
            },
        )
        # no simple_properties defined in console.wsdl
        self.cache_info = None
        self.system_setting = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SystemStatusAggregate(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``aggregate``."""

    _soap_tag = 'aggregate'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'send_forward_count': int,
                'send_backward_count': int,
                'send_none_count': int,
                'send_ok_count': int,
                'receive_forward_count': int,
                'receive_backward_count': int,
                'receive_none_count': int,
                'receive_ok_count': int,
                'slowlink_count': int,
                'blocked_count': int,
                'leader_count': int,
                'normal_count': int,
            },
            complex_properties={
                'versions': VersionAggregateList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.send_forward_count = None
        self.send_backward_count = None
        self.send_none_count = None
        self.send_ok_count = None
        self.receive_forward_count = None
        self.receive_backward_count = None
        self.receive_none_count = None
        self.receive_ok_count = None
        self.slowlink_count = None
        self.blocked_count = None
        self.leader_count = None
        self.normal_count = None
        self.versions = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class SystemStatusList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``system_status``."""

    _soap_tag = 'system_status'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                'aggregate': SystemStatusAggregate,
                'cache_info': CacheInfo,
            },
            list_properties={
                'client_status': ClientStatus,
            },
        )
        # no simple_properties defined in console.wsdl
        self.aggregate = None
        self.cache_info = None
        self.client_status = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class UploadFile(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``upload_file``."""

    _soap_tag = 'upload_file'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'key': text_type,
                'destination_file': text_type,
                'hash': text_type,
                'force_overwrite': int,
                'file_size': int,
                'start_pos': int,
                'bytes': text_type,
                'file_cached': int,
                'part_size': int,
                'percent_complete': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.key = None
        self.destination_file = None
        self.hash = None
        self.force_overwrite = None
        self.file_size = None
        self.start_pos = None
        self.bytes = None
        self.file_cached = None
        self.part_size = None
        self.percent_complete = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class UploadFileList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file_parts``."""

    _soap_tag = 'file_parts'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'upload_file': UploadFile,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.upload_file = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class UploadFileStatus(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``upload_file_status``."""

    _soap_tag = 'upload_file_status'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'hash': text_type,
                'percent_complete': int,
                'file_cached': int,
            },
            complex_properties={
                'file_parts': UploadFileList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.hash = None
        self.percent_complete = None
        self.file_cached = None
        self.file_parts = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class User(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``user``."""

    _soap_tag = 'user'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'domain': text_type,
                'group_id': int,
                'deleted_flag': int,
                'last_login': text_type,
                'active_session_count': int,
                'local_admin_flag': int,
            },
            complex_properties={
                'permissions': PermissionList,
                'roles': UserRoleList,
                'metadata': MetadataList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.domain = None
        self.group_id = None
        self.deleted_flag = None
        self.last_login = None
        self.active_session_count = None
        self.local_admin_flag = None
        self.permissions = None
        self.roles = None
        self.metadata = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class UserList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``users``."""

    _soap_tag = 'users'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'user': User,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.user = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class UserRole(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``role``."""

    _soap_tag = 'role'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'description': text_type,
            },
            complex_properties={
                'permissions': PermissionList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.description = None
        self.permissions = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class UserRoleList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``roles``."""

    _soap_tag = 'roles'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'role': UserRole,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.role = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class VersionAggregate(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``version``."""

    _soap_tag = 'version'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'version_string': text_type,
                'count': int,
                'filtered': int,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.version_string = None
        self.count = None
        self.filtered = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class VersionAggregateList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``versions``."""

    _soap_tag = 'versions'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'version': VersionAggregate,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.version = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class WhiteListedUrl(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``white_listed_url``."""

    _soap_tag = 'white_listed_url'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'chunk_id': text_type,
                'download_seconds': int,
                'url_regex': text_type,
            },
            complex_properties={
                'metadata': MetadataList,
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.id = None
        self.chunk_id = None
        self.download_seconds = None
        self.url_regex = None
        self.metadata = None
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class WhiteListedUrlList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``white_listed_urls``."""

    _soap_tag = 'white_listed_urls'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no SIMPLE_ARGS defined in console.wsdl
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                'white_listed_url': WhiteListedUrl,
            },
        )
        # no simple_properties defined in console.wsdl
        # no complex_properties defined in console.wsdl
        self.white_listed_url = []
        self._values = kwargs.get('values', {})
        self._set_values(self._values)


class XmlError(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``error``."""

    _soap_tag = 'error'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'type': text_type,
                'exception': text_type,
                'error_context': text_type,
            },
            complex_properties={
                # no COMPLEX_ARGS defined in console.wsdl
            },
            list_properties={
                # no LIST_ARGS defined in console.wsdl
            },
        )
        self.type = None
        self.exception = None
        self.error_context = None
        # no complex_properties defined in console.wsdl
        # no list_properties defined in console.wsdl
        self._values = kwargs.get('values', {})
        self._set_values(self._values)
