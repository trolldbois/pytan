"""Tanium NG: A Python object representation layer for the XML used by the Tanium SOAP API.

This module is meant to be a completely standalone module.

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-24T23-33-06Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
# BEGIN STATIC CODE
# TODO ADD TO BUILDER HEADER
# TODO MAKE TICKLE DYNAMICALLY LOAD

import sys
import json
import logging


# try to use PytanError as the base class for all exceptions
try:
    from pytan import PytanError
    PytanError = PytanError
except:
    PytanError = Exception

mylog = logging.getLogger(__name__)

# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
    string_types = str,  # noqa
    integer_types = int,  # noqa
else:
    text_type = unicode  # noqa
    string_types = basestring,  # noqa
    integer_types = (int, long)  # noqa


class TaniumNGError(PytanError):

    """For errors in Tanium NG."""

    pass


class BadTypeError(TaniumNGError):

    """Raised when a property is not of the expected type."""

    def __init__(self, obj, name, value, expected, original=None):
        """pass."""
        self.name = name
        self.expected = expected
        self.value = value
        self.original = original
        err = "Object {!r} attribute '{}' expected type '{}', got '{}' (value: '{}') (orig: {})"
        err = err.format(obj, name, expected.__name__, type(value).__name__, value, original)
        TaniumNGError.__init__(self, err)


def get_obj_type(tag):
    """Map Tanium XML soap tags to the Tanium NG Python BaseType object."""
    if tag not in BASE_TYPES:  # noqa
        err = 'Unknown type {}'
        err = err.format(tag)
        raise TaniumNGError(err)
    result = BASE_TYPES[tag]  # noqa
    return result


class BaseType(object):

    """Base Python Type used for all Tanium XML SOAP Objects."""

    _SOAP_TAG = None
    """str of XML tag that Tanium SOAP API Uses to define this object"""

    _INIT_VALUES = {}
    """dict that stores optional argument values={} for setting values after initialization"""

    _INITIALIZED = False
    """bool to check if the BaseType has finished initiailizing or not"""

    _SIMPLE_PROPS = {}
    """dict that stores the simple properties for this object (str, int)"""

    _COMPLEX_PROPS = {}
    """dict that stores the complex properties for this object (other BaseTypes)"""

    _LIST_PROPS = {}
    """dict that stores the complex properties for this object (other BaseTypes, str, int)"""

    _ALL_PROPS = {}
    """dict that stores all properties for this object"""

    _IS_LIST = False
    """bool indicating if this is a single list object or not"""

    _LIST_ATTR = ''
    """str that stores the name of the list attribute for this object if it is a single list"""

    _LIST_TYPE = None
    """stores the type of the list objects for this object if it is a single list"""

    _ITEM_ATTRS = []
    """list that stores a preferentially sorted list of non-list attributes for this object"""

    _TICKLE = None
    """Holds the tickle module which provides serialization/deserialization of objects"""

    def __init__(self, simple_properties, complex_properties, list_properties, **kwargs):
        """pass."""
        self._INITIALIZED = False

        self._INIT_VALUES = kwargs.get('values', {}) or {}

        self._SIMPLE_PROPS = simple_properties
        self._COMPLEX_PROPS = complex_properties
        self._LIST_PROPS = list_properties
        self._ALL_PROPS = {}
        self._ALL_PROPS.update(self._SIMPLE_PROPS)
        self._ALL_PROPS.update(self._COMPLEX_PROPS)
        self._ALL_PROPS.update(self._LIST_PROPS)

        self._IS_LIST = len(list_properties) == 1
        if self._IS_LIST:
            self._LIST_ATTR, self._LIST_TYPE = list(list_properties.items())[0]

        self._ITEM_ATTRS = list(self._SIMPLE_PROPS.keys()) + list(self._COMPLEX_PROPS.keys())
        self._ITEM_ATTRS = sorted(self._ITEM_ATTRS)
        for f in ['name', 'id']:
            if f in self._ITEM_ATTRS:
                self._ITEM_ATTRS.remove(f)
                self._ITEM_ATTRS.insert(0, f)

        self._INITIALIZED = True

    def _list_only_method(self):
        """Exception to throw on methods that are only supported for single list types."""
        if not self._IS_LIST:
            err = 'Not a list type with a single list property!'
            raise TaniumNGError(err)

    def __getitem__(self, idx):
        """Support a[n] for single list types."""
        self._list_only_method()
        result = getattr(self, self._LIST_ATTR).__getitem__(idx)
        return result

    def append(self, value):
        """Support self.append for single list types."""
        self._list_only_method()
        if not isinstance(value, self._LIST_TYPE):
            raise BadTypeError(self, self._LIST_ATTR, value, self._LIST_TYPE)
        getattr(self, self._LIST_ATTR).append(value)

    def __add__(self, value):
        """Support + operand for single list types.

        >>> a = SensorList()
        >>> b = SensorList()
        >>> c = Sensor()
        >>> b.append(c)
        >>> d = a + b
        """
        self._list_only_method()
        mylist = getattr(self, self._LIST_ATTR)
        valuelist = getattr(value, value._LIST_ATTR)
        newlist = mylist + valuelist
        newobj = self.__class__()
        setattr(newobj, newobj._LIST_ATTR, newlist)
        return newobj

    def __iadd__(self, value):
        """Support += operand for list types.

        >>> a = SensorList()
        >>> b = SensorList()
        >>> c = Sensor()
        >>> b.append(c)
        >>> a += b
        """
        self._list_only_method()
        mylist = getattr(self, self._LIST_ATTR)
        mylist += getattr(value, value._LIST_ATTR)
        return self

    def __len__(self):
        """Return length of list, elsewise return the number of attributes that are not None."""
        if self._IS_LIST:
            result = len(getattr(self, self._LIST_ATTR))
        else:
            result = sum([1 for k in self._ITEM_ATTRS if getattr(self, k, None) is not None])
        return result

    def __repr__(self):
        """Return class name, list length (if a list), and all attributes."""
        return self.__str__()

    def __str__(self):
        """Return class name, list length (if a list), and all attributes."""
        class_name = self.__class__.__name__
        vals = []
        if self._IS_LIST:
            name = 'length'
            val = len(self)
            vals.append([name, val])

        for k in self._ITEM_ATTRS:
            if getattr(self, k, None) in [None, []]:
                continue
            name = k
            val = getattr(self, k, None)
            if isinstance(val, list):
                val = "{} items".format(len(val))
            else:
                val = str(val).replace('\n', '')
            vals.append([name, val])

        if vals:
            result = ', '.join(["{}.{}={}".format(class_name, *p) for p in vals])
        else:
            result = "No attributes assigned yet!"
        return result

    def __setattr__(self, name, value):
        """Enforce type of attribute assignments."""
        val_not_none = value is not None
        is_init = name != '_INITIALIZED' and getattr(self, '_INITIALIZED', False)
        if all([val_not_none, is_init]):
            if name in getattr(self, '_LIST_PROPS', {}):
                value = self._check_list(name, value)
            elif name in getattr(self, '_COMPLEX_PROPS', {}):
                value = self._check_complex(name, value)
            elif name in getattr(self, '_SIMPLE_PROPS', {}):
                value = self._check_simple(name, value)
        super(BaseType, self).__setattr__(name, value)

    def _set_init_values(self):
        for k, v in self._INIT_VALUES.items():
            setattr(self, k, v)

    def _check_complex(self, name, value):
        if not isinstance(value, self._COMPLEX_PROPS[name]):
            raise BadTypeError(self, name, value, self._COMPLEX_PROPS[name])
        return value

    def _check_simple(self, name, value):
        if self._SIMPLE_PROPS[name] == int:
            try:
                value = int(self._SIMPLE_PROPS[name](value))
            except Exception as e:
                raise BadTypeError(self, name, value, self._SIMPLE_PROPS[name], e)
        elif self._SIMPLE_PROPS[name] == text_type:
            if not isinstance(value, string_types):
                raise BadTypeError(self, name, value, self._SIMPLE_PROPS[name])
        return value

    def _check_list(self, name, value):
        if not isinstance(value, list):
            raise BadTypeError(self, name, value, self._LIST_PROPS[name])
        '''
        # too strict / not performant
        for i in value:
            if not isinstance(i, self._LIST_PROPS[name]):
                raise BadTypeError(self, name, i, self._LIST_PROPS[name])
        '''
        return value

    def to_xml(self, **kwargs):
        """Deserialize self ``obj`` into an XML body, relies on tickle."""
        result = self._TICKLE.tools.to_xml(self, **kwargs)
        return result

    def to_dict(self, **kwargs):
        """Deserialize self ``obj`` into a dict, relies on tickle."""
        result = self._TICKLE.tools.to_dict(self, **kwargs)
        return result

    def to_json(self, **kwargs):
        """Deserialize self ``obj`` into a JSON string, relies on tickle."""
        result = self._TICKLE.tools.to_json(self, **kwargs)
        return result

    def to_csv(self, **kwargs):
        """Deserialize self ``obj`` into a CSV string, relies on tickle."""
        result = self._TICKLE.tools.to_csv(self, **kwargs)
        return result


class ColumnList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``cs``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'cs'
    _OVERRIDE_XPATH = {
        'columns': './c',
    }

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
            },
            complex_properties={
            },
            list_properties={
                'columns': Column,
            },
            **kwargs
        )
        self.columns = []
        self._set_init_values()

    def __getitem__(self, idx):
        """Support getitem via [0] or [display_name]."""
        if isinstance(idx, int):
            result = super(ColumnList, self).__getitem__(idx)
        else:
            result = None
            for c in self.columns:
                if c.display_name == idx:
                    result = c

            if result is None:
                err = "No column named {!r} found! Column names: {!r}"
                err = err.format(idx, ', '.join([c.display_name for c in self.columns]))
                raise TaniumNGError(err)

        return result


class Column(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``c``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'c'
    _OVERRIDE_XPATH = {
        'what_hash': './wh',
        'display_name': './dn',
        'result_type_int': './rt',
        'values': './v',
    }

    _RESULT_TYPE_MAP = {
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
    """
    Maps a Result type from the Tanium SOAP API from an int to a string
    """

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'what_hash': int,
                'display_name': text_type,
                'result_type_int': int,
            },
            complex_properties={},
            list_properties={
                'values': text_type,
            },
            **kwargs
        )
        self.what_hash = None
        self.display_name = None
        self.result_type_int = None
        self.values = []
        self._set_init_values()
        self._ITEM_ATTRS.append('result_type')

    @property
    def result_type(self):
        """Map a Result type self.result_type_int int to a string using self._RESULT_TYPE_MAP."""
        result = getattr(self, 'result_type_int', None)
        if result in self._RESULT_TYPE_MAP:
            result = self._RESULT_TYPE_MAP[result]
        return result


class RowList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``rs``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'rs'
    _OVERRIDE_XPATH = {
        'rows': './r',
    }

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={},
            complex_properties={},
            list_properties={'rows': Row},
            **kwargs
        )
        self.rows = []
        self._set_init_values()


class Row(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``r``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'r'
    _OVERRIDE_XPATH = {
        'columns': './c',
    }
    """Override the xpath used to find these elements"""

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={'id': int, 'cid': int},
            complex_properties={},
            list_properties={'columns': Column},
            **kwargs
        )
        self.id = None
        self.cid = None
        self.columns = []
        self._set_init_values()

    def __getitem__(self, idx):
        """Support getitem via [0] or [display_name]."""
        if isinstance(idx, int):
            result = super(Row, self).__getitem__(idx)
        else:
            result = None
            for c in self.columns:
                if c.display_name == idx:
                    result = c

            if result is None:
                err = "No column named {!r} found! Column names: {!r}"
                err = err.format(idx, ', '.join([c.display_name for c in self.columns]))
                raise TaniumNGError(err)

        return result


class ResultSet(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``result_set``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'result_set'
    _OVERRIDE_XPATH = {
        'rows': './rs',
        'columns': './cs',
    }
    """Override the xpath used to find these elements"""

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'age': int,
                'report_count': int,
                'saved_question_id': int,
                'question_id': int,
                'archived_question_id': int,
                'seconds_since_issued': int,
                'issue_seconds': int,
                'expire_seconds': int,
                'tested': int,
                'passed': int,
                'mr_tested': int,
                'mr_passed': int,
                'estimated_total': int,
                'select_count': int,
                'row_count': int,
                'row_count_machines': int,
                'filtered_row_count': int,
                'filtered_row_count_machines': int,
                'item_count': int,
            },
            complex_properties={
                'rows': RowList,
                'columns': ColumnList
            },
            list_properties={},
            **kwargs
        )

        self.now = None
        self.age = None
        self.report_count = None
        self.saved_question_id = None
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
        self.row_count_machines = None
        self.filtered_row_count = None
        self.filtered_row_count_machines = None
        self.item_count = None
        self.rows = None
        self.columns = None
        self._set_init_values()

    def _post_xml_hook(self, **kwargs):
        run_hooks = kwargs.get('run_hooks', True)

        # if there are no rows or run_hooks is False, don't do anything
        if not self.rows or not run_hooks:
            return False

        # set each rows columns attr to the index correlated column attr
        for row in self.rows:
            for idx, row_col in enumerate(row):
                # for each of the simple properties in this row's column
                for attr in row_col._SIMPLE_PROPS:
                    # get the value for this attr from the index correlated column
                    col_val = getattr(self.columns[idx], attr)
                    # set the value to this row's column attr
                    setattr(row_col, attr, col_val)
        return True

    def get_column(self, idx):
        """passthrough to ColumnList [idx]."""
        result = self.columns[idx]
        return result

    def get_row_column(self, n, idx):
        """passthrough to Row[n] ColumnList [idx]."""
        result = self.rows[n][idx]
        return result


class ResultSetList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``result_sets``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.

    result_set could technically be a list, but the Tanium SOAP API only ever returns one, so
    we have it defined as a complex property instead of a list property.
    """

    _SOAP_TAG = 'result_sets'

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={'now': text_type},
            complex_properties={'result_set': ResultSet},
            list_properties={},
            **kwargs
        )
        self.now = None
        self.result_set = None
        self._set_init_values()


class ResultInfo(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``result_info``.

    This is the return from GetResultInfo, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'result_info'

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'age': int,
                'report_count': int,
                'saved_question_id': int,
                'question_id': int,
                'archived_question_id': int,
                'seconds_since_issued': int,
                'issue_seconds': int,
                'expire_seconds': int,
                'tested': int,
                'passed': int,
                'mr_tested': int,
                'mr_passed': int,
                'estimated_total': int,
                'select_count': int,
                'row_count': int,
                'error_count': int,
                'no_results_count': int,
                'row_count_machines': int,
                'row_count_flag': int,
            },
            complex_properties={},
            list_properties={},
            **kwargs
        )
        self.id = None
        self.age = None
        self.report_count = None
        self.saved_question_id = None
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
        self.no_results_count = None
        self.row_count_machines = None
        self.row_count_flag = None
        self._set_init_values()


class ResultInfoList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``result_infos``.

    This is the return from GetResultInfo, and it is not defined in console.wsdl,
    so it is statically defined.

    result_info could technically be a list, but the Tanium SOAP API only ever returns one, so
    we have it defined as a complex property instead of a list property.
    """

    _SOAP_TAG = 'result_infos'

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={'now': text_type},
            complex_properties={'result_info': ResultInfo},
            list_properties={},
            **kwargs
        )
        self.now = None
        self.result_info = None
        self._set_init_values()


# END STATIC CODE
# BEGIN DYNAMIC CODE


class Action(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``action``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'action'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'comment': text_type,
                'distribute_seconds': int,
                'status': text_type,
                'name': text_type,
                'expire_seconds': int,
                'cache_row_id': int,
                'expiration_time': text_type,
                'creation_time': text_type,
                'stopped_flag': int,
                'skip_lock_flag': int,
                'start_time': text_type,
            },
            complex_properties={
                'saved_action': SavedAction,
                'metadata': MetadataList,
                'user': User,
                'history_saved_question': SavedQuestion,
                'action_group': Group,
                'approver': User,
                'package_spec': PackageSpec,
                'target_group': Group,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.comment = None
        self.distribute_seconds = None
        self.status = None
        self.name = None
        self.expire_seconds = None
        self.cache_row_id = None
        self.expiration_time = None
        self.creation_time = None
        self.stopped_flag = None
        self.skip_lock_flag = None
        self.start_time = None
        self.saved_action = None
        self.metadata = None
        self.user = None
        self.history_saved_question = None
        self.action_group = None
        self.approver = None
        self.package_spec = None
        self.target_group = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ActionList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``actions``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'actions'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'info': ActionListInfo,
                'cache_info': CacheInfo,
            },
            list_properties={
                'action': Action,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.info = None
        self.cache_info = None
        self.action = []
        self._set_init_values()


class ActionListInfo(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``info``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'info'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'highest_id': int,
                'total_count': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.highest_id = None
        self.total_count = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ActionStop(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``action_stop``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'action_stop'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
            },
            complex_properties={
                'action': Action,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.action = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ActionStopList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``action_stops``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'action_stops'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'action_stop': ActionStop,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.action_stop = []
        self._set_init_values()


class ArchivedQuestion(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``archived_question``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'archived_question'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ArchivedQuestionList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``archived_questions``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'archived_questions'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'archived_question': ArchivedQuestion,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.archived_question = []
        self._set_init_values()


class AuditData(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``audit_data``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'audit_data'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'modification_time': text_type,
                'creation_time': text_type,
                'last_modified_by': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.modification_time = None
        self.creation_time = None
        self.last_modified_by = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class CacheFilter(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``filter``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'filter'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'not_flag': int,
                'value': text_type,
                'field': text_type,
                'operator': text_type,
                'type': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.not_flag = None
        self.value = None
        self.field = None
        self.operator = None
        self.type = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class CacheFilterList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``cache_filters``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'cache_filters'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'filter': CacheFilter,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.filter = []
        self._set_init_values()


class CacheInfo(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``cache_info``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'cache_info'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'page_row_count': int,
                'cache_id': int,
                'filtered_row_count': int,
                'expiration': text_type,
                'cache_row_count': int,
            },
            complex_properties={
                'errors': ErrorList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.page_row_count = None
        self.cache_id = None
        self.filtered_row_count = None
        self.expiration = None
        self.cache_row_count = None
        self.errors = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ClientCount(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``client_count``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'client_count'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ClientStatus(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``client_status``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'client_status'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'ipaddress_server': text_type,
                'full_version': text_type,
                'ipaddress_client': text_type,
                'status': text_type,
                'send_state': text_type,
                'cache_row_id': int,
                'host_name': text_type,
                'receive_state': text_type,
                'last_registration': text_type,
                'public_key_valid': int,
                'computer_id': text_type,
                'port_number': int,
                'protocol_version': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.ipaddress_server = None
        self.full_version = None
        self.ipaddress_client = None
        self.status = None
        self.send_state = None
        self.cache_row_id = None
        self.host_name = None
        self.receive_state = None
        self.last_registration = None
        self.public_key_valid = None
        self.computer_id = None
        self.port_number = None
        self.protocol_version = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ComputerGroup(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``computer_group``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'computer_group'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
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
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.name = None
        self.deleted_flag = None
        self.computer_specs = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ComputerGroupList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``computer_groups``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'computer_groups'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'computer_group': ComputerGroup,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.computer_group = []
        self._set_init_values()


class ComputerGroupSpec(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``computer_spec``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'computer_spec'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'computer_name': text_type,
                'ip_address': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.computer_name = None
        self.ip_address = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ComputerSpecList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``computer_specs``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'computer_specs'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'computer_spec': ComputerGroupSpec,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.computer_spec = []
        self._set_init_values()


class ErrorList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``errors``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'errors'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'error': XmlError,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.error = []
        self._set_init_values()


class Filter(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``filter``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'filter'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'value': text_type,
                'substring_length': int,
                'delimiter_index': int,
                'end_time': text_type,
                'substring_start': int,
                'delimiter': text_type,
                'operator': text_type,
                'aggregation': text_type,
                'utf8_flag': int,
                'start_time': text_type,
                'not_flag': int,
                'all_values_flag': int,
                'value_type': text_type,
                'ignore_case_flag': int,
                'substring_flag': int,
                'max_age_seconds': int,
                'all_times_flag': int,
            },
            complex_properties={
                'sensor': Sensor,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.value = None
        self.substring_length = None
        self.delimiter_index = None
        self.end_time = None
        self.substring_start = None
        self.delimiter = None
        self.operator = None
        self.aggregation = None
        self.utf8_flag = None
        self.start_time = None
        self.not_flag = None
        self.all_values_flag = None
        self.value_type = None
        self.ignore_case_flag = None
        self.substring_flag = None
        self.max_age_seconds = None
        self.all_times_flag = None
        self.sensor = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class FilterList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``filters``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'filters'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'filter': Filter,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.filter = []
        self._set_init_values()


class Group(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``group``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'group'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'text': text_type,
                'type': int,
                'not_flag': int,
                'name': text_type,
                'deleted_flag': int,
                'and_flag': int,
                'source_id': int,
            },
            complex_properties={
                'parameters': ParameterList,
                'sub_groups': GroupList,
                'filters': FilterList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.text = None
        self.type = None
        self.not_flag = None
        self.name = None
        self.deleted_flag = None
        self.and_flag = None
        self.source_id = None
        self.parameters = None
        self.sub_groups = None
        self.filters = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class GroupList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``groups``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'groups'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'group': Group,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.group = []
        self._set_init_values()


class MetadataItem(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``item``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'item'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'admin_flag': int,
                'name': text_type,
                'value': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.admin_flag = None
        self.name = None
        self.value = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class MetadataList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``metadata``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'metadata'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'item': MetadataItem,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.item = []
        self._set_init_values()


class ObjectList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``object_list``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'object_list'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'export_id': text_type,
            },
            complex_properties={
                'questions': QuestionList,
                'computer_groups': ComputerGroupList,
                'actions': ActionList,
                'system_settings': SystemSettingList,
                'roles': UserRoleList,
                'white_listed_urls': WhiteListedUrlList,
                'saved_actions': SavedActionList,
                'client_count': ClientCount,
                'system_status': SystemStatusList,
            },
            list_properties={
                'plugin': Plugin,
                'package_specs': PackageSpecList,
                'parse_result_group': ParseResultGroup,
                'plugins': PluginList,
                'plugin_schedule': PluginSchedule,
                'user': User,
                'groups': GroupList,
                'group': Group,
                'white_listed_url': WhiteListedUrl,
                'action': Action,
                'package_files': PackageFileList,
                'action_stops': ActionStopList,
                'plugin_schedules': PluginScheduleList,
                'package_spec': PackageSpec,
                'users': UserList,
                'soap_error': SoapError,
                'upload_file_status': UploadFileStatus,
                'sensors': SensorList,
                'parse_jobs': ParseJobList,
                'parse_result_groups': ParseResultGroupList,
                'package_file': PackageFile,
                'saved_action_approval': SavedActionApproval,
                'saved_questions': SavedQuestionList,
                'saved_question': SavedQuestion,
                'sensor': Sensor,
                'saved_action': SavedAction,
                'computer_group': ComputerGroup,
                'upload_file': UploadFile,
                'client_status': ClientStatus,
                'parse_job': ParseJob,
                'action_stop': ActionStop,
                'system_setting': SystemSetting,
                'archived_question': ArchivedQuestion,
                'archived_questions': ArchivedQuestionList,
                'question': Question,
            },
            **kwargs
        )
        self.export_id = None
        self.questions = None
        self.computer_groups = None
        self.actions = None
        self.system_settings = None
        self.roles = None
        self.white_listed_urls = None
        self.saved_actions = None
        self.client_count = None
        self.system_status = None
        self.plugin = []
        self.package_specs = []
        self.parse_result_group = []
        self.plugins = []
        self.plugin_schedule = []
        self.user = []
        self.groups = []
        self.group = []
        self.white_listed_url = []
        self.action = []
        self.package_files = []
        self.action_stops = []
        self.plugin_schedules = []
        self.package_spec = []
        self.users = []
        self.soap_error = []
        self.upload_file_status = []
        self.sensors = []
        self.parse_jobs = []
        self.parse_result_groups = []
        self.package_file = []
        self.saved_action_approval = []
        self.saved_questions = []
        self.saved_question = []
        self.sensor = []
        self.saved_action = []
        self.computer_group = []
        self.upload_file = []
        self.client_status = []
        self.parse_job = []
        self.action_stop = []
        self.system_setting = []
        self.archived_question = []
        self.archived_questions = []
        self.question = []
        self._set_init_values()


class Options(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``options``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'options'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'json_pretty_print': int,
                'use_error_objects': int,
                'include_hashes_flag': int,
                'return_cdata_flag': int,
                'most_recent_flag': int,
                'use_user_context_flag': int,
                'suppress_object_list': int,
                'use_json': int,
                'aggregate_over_time_flag': int,
                'hide_no_results_flag': int,
                'cache_sort_fields': text_type,
                'script_data': text_type,
                'filter_not_flag': int,
                'include_hidden_flag': int,
                'export_flag': int,
                'flags': int,
                'include_user_details': int,
                'cache_expiration': int,
                'recent_result_buckets': text_type,
                'export_leading_text': text_type,
                'sort_order': text_type,
                'hide_errors_flag': int,
                'filter_string': text_type,
                'sample_start': int,
                'export_trailing_text': text_type,
                'row_counts_only_flag': int,
                'pct_done_limit': int,
                'suppress_scripts': int,
                'cache_id': int,
                'context_id': int,
                'include_answer_times_flag': int,
                'export_format': int,
                'sample_frequency': int,
                'row_count': int,
                'row_start': int,
                'sample_count': int,
                'return_lists_flag': int,
            },
            complex_properties={
                'cache_filters': CacheFilterList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.json_pretty_print = None
        self.use_error_objects = None
        self.include_hashes_flag = None
        self.return_cdata_flag = None
        self.most_recent_flag = None
        self.use_user_context_flag = None
        self.suppress_object_list = None
        self.use_json = None
        self.aggregate_over_time_flag = None
        self.hide_no_results_flag = None
        self.cache_sort_fields = None
        self.script_data = None
        self.filter_not_flag = None
        self.include_hidden_flag = None
        self.export_flag = None
        self.flags = None
        self.include_user_details = None
        self.cache_expiration = None
        self.recent_result_buckets = None
        self.export_leading_text = None
        self.sort_order = None
        self.hide_errors_flag = None
        self.filter_string = None
        self.sample_start = None
        self.export_trailing_text = None
        self.row_counts_only_flag = None
        self.pct_done_limit = None
        self.suppress_scripts = None
        self.cache_id = None
        self.context_id = None
        self.include_answer_times_flag = None
        self.export_format = None
        self.sample_frequency = None
        self.row_count = None
        self.row_start = None
        self.sample_count = None
        self.return_lists_flag = None
        self.cache_filters = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageFile(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``file``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'file'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'source': text_type,
                'bytes_downloaded': int,
                'last_download_progress_time': text_type,
                'status': int,
                'name': text_type,
                'deleted_flag': int,
                'cache_status': text_type,
                'size': int,
                'trigger_download': int,
                'bytes_total': int,
                'download_start_time': text_type,
                'hash': text_type,
                'download_seconds': int,
            },
            complex_properties={
                'file_status': PackageFileStatusList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.source = None
        self.bytes_downloaded = None
        self.last_download_progress_time = None
        self.status = None
        self.name = None
        self.deleted_flag = None
        self.cache_status = None
        self.size = None
        self.trigger_download = None
        self.bytes_total = None
        self.download_start_time = None
        self.hash = None
        self.download_seconds = None
        self.file_status = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageFileList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``package_files``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'package_files'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'file': PackageFile,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.file = []
        self._set_init_values()


class PackageFileStatus(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``status``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'status'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'bytes_total': int,
                'last_download_progress_time': text_type,
                'server_id': int,
                'bytes_downloaded': int,
                'cache_message': text_type,
                'status': int,
                'download_start_time': text_type,
                'cache_status': text_type,
                'server_name': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.bytes_total = None
        self.last_download_progress_time = None
        self.server_id = None
        self.bytes_downloaded = None
        self.cache_message = None
        self.status = None
        self.download_start_time = None
        self.cache_status = None
        self.server_name = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageFileStatusList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``file_status``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'file_status'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'status': PackageFileStatus,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.status = []
        self._set_init_values()


class PackageFileTemplate(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``file_template``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'file_template'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'name': text_type,
                'source': text_type,
                'hash': text_type,
                'download_seconds': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.name = None
        self.source = None
        self.hash = None
        self.download_seconds = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageFileTemplateList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``file_templates``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'file_templates'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'file_template': PackageFileTemplate,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.file_template = []
        self._set_init_values()


class PackageSpec(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``package_spec``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'package_spec'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'modification_time': text_type,
                'last_update': text_type,
                'verify_expire_seconds': int,
                'command_timeout': int,
                'name': text_type,
                'expire_seconds': int,
                'deleted_flag': int,
                'parameter_definition': text_type,
                'signature': text_type,
                'cache_row_id': int,
                'creation_time': text_type,
                'hidden_flag': int,
                'last_modified_by': text_type,
                'command': text_type,
                'verify_group_id': int,
                'available_time': text_type,
                'skip_lock_flag': int,
                'display_name': text_type,
                'source_id': int,
            },
            complex_properties={
                'sensors': SensorList,
                'metadata': MetadataList,
                'parameters': ParameterList,
                'file_templates': PackageFileTemplateList,
                'files': PackageFileList,
                'verify_group': Group,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.modification_time = None
        self.last_update = None
        self.verify_expire_seconds = None
        self.command_timeout = None
        self.name = None
        self.expire_seconds = None
        self.deleted_flag = None
        self.parameter_definition = None
        self.signature = None
        self.cache_row_id = None
        self.creation_time = None
        self.hidden_flag = None
        self.last_modified_by = None
        self.command = None
        self.verify_group_id = None
        self.available_time = None
        self.skip_lock_flag = None
        self.display_name = None
        self.source_id = None
        self.sensors = None
        self.metadata = None
        self.parameters = None
        self.file_templates = None
        self.files = None
        self.verify_group = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageSpecList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``package_specs``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'package_specs'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'package_spec': PackageSpec,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.package_spec = []
        self._set_init_values()


class Parameter(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``parameter``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'parameter'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'value': text_type,
                'key': text_type,
                'type': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.value = None
        self.key = None
        self.type = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ParameterList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``parameters``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'parameters'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'parameter': Parameter,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.parameter = []
        self._set_init_values()


class ParseJob(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``parse_job``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'parse_job'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'parser_version': int,
                'question_text': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.parser_version = None
        self.question_text = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ParseJobList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``parse_jobs``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'parse_jobs'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'parse_job': ParseJob,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.parse_job = []
        self._set_init_values()


class ParseResult(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``parse_result``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'parse_result'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
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
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.parameter_definition = None
        self.parameters = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ParseResultGroup(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``parse_result_group``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'parse_result_group'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
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
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.score = None
        self.question_text = None
        self.parse_results = None
        self.question = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ParseResultGroupList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``parse_result_groups``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'parse_result_groups'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'parse_result_group': ParseResultGroup,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.parse_result_group = []
        self._set_init_values()


class ParseResultList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``parse_results``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'parse_results'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'parse_result': ParseResult,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.parse_result = []
        self._set_init_values()


class PermissionList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``permissions``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'permissions'

    CONSTANTS = [
        {'name': 'ADMIN', 'value': 'admin', 'type': text_type},
        {'name': 'QUESTION_READ', 'value': 'question_read', 'type': text_type},
        {'name': 'QUESTION_WRITE', 'value': 'question_write', 'type': text_type},
        {'name': 'SENSOR_READ', 'value': 'sensor_read', 'type': text_type},
        {'name': 'SENSOR_WRITE', 'value': 'sensor_write', 'type': text_type},
        {'name': 'ACTION_READ', 'value': 'action_read', 'type': text_type},
        {'name': 'ACTION_WRITE', 'value': 'action_write', 'type': text_type},
        {'name': 'ACTION_APPROVE', 'value': 'action_approval', 'type': text_type},
        {'name': 'NOTIFICATION_WRITE', 'value': 'notification_write', 'type': text_type},
        {'name': 'CLIENTS_READ', 'value': 'clients_read', 'type': text_type},
        {'name': 'QUESTION_LOG_READ', 'value': 'question_log_read', 'type': text_type},
        {'name': 'CONTENT_ADMIN', 'value': 'content_admin', 'type': text_type},
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'permission': text_type,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.permission = []
        self._set_init_values()


class Plugin(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``plugin``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'plugin'

    CONSTANTS = [
        {'name': 'SQL', 'value': 'SQL', 'type': text_type},
        {'name': 'SCRIPT', 'value': 'Script', 'type': text_type},
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'allow_rest': int,
                'bundle': text_type,
                'local_admin_flag': int,
                'type': text_type,
                'name': text_type,
                'filename': text_type,
                'execution_id': int,
                'timeout_seconds': int,
                'path': text_type,
                'raw_http_response': int,
                'cache_row_id': int,
                'status_file_content': text_type,
                'status': text_type,
                'use_json_flag': int,
                'exit_code': int,
                'plugin_url': text_type,
                'plugin_server': text_type,
                'input': text_type,
                'raw_http_request': int,
                'script_response': text_type,
                'run_detached_flag': int,
            },
            complex_properties={
                'permissions': PermissionList,
                'metadata': MetadataList,
                'arguments': PluginArgumentList,
                'sql_response': PluginSql,
                'commands': PluginCommandList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.allow_rest = None
        self.bundle = None
        self.local_admin_flag = None
        self.type = None
        self.name = None
        self.filename = None
        self.execution_id = None
        self.timeout_seconds = None
        self.path = None
        self.raw_http_response = None
        self.cache_row_id = None
        self.status_file_content = None
        self.status = None
        self.use_json_flag = None
        self.exit_code = None
        self.plugin_url = None
        self.plugin_server = None
        self.input = None
        self.raw_http_request = None
        self.script_response = None
        self.run_detached_flag = None
        self.permissions = None
        self.metadata = None
        self.arguments = None
        self.sql_response = None
        self.commands = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PluginArgument(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``argument``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'argument'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'value': text_type,
                'name': text_type,
                'type': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.value = None
        self.name = None
        self.type = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class PluginArgumentList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``arguments``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'arguments'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'argument': PluginArgument,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.argument = []
        self._set_init_values()


class PluginCommandList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``commands``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'commands'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'command': text_type,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.command = []
        self._set_init_values()


class PluginList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``plugins``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'plugins'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'plugin': Plugin,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.plugin = []
        self._set_init_values()


class PluginSchedule(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``plugin_schedule``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'plugin_schedule'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'run_interval_seconds': int,
                'plugin_bundle': text_type,
                'run_on_days': text_type,
                'end_hour': int,
                'end_date': int,
                'last_run_text': text_type,
                'name': text_type,
                'deleted_flag': int,
                'last_run_time': text_type,
                'start_hour': int,
                'last_exit_code': int,
                'enabled': int,
                'plugin_server': text_type,
                'input': text_type,
                'start_date': int,
                'plugin_name': text_type,
            },
            complex_properties={
                'last_run_sql': PluginSql,
                'arguments': PluginArgumentList,
                'user': User,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.run_interval_seconds = None
        self.plugin_bundle = None
        self.run_on_days = None
        self.end_hour = None
        self.end_date = None
        self.last_run_text = None
        self.name = None
        self.deleted_flag = None
        self.last_run_time = None
        self.start_hour = None
        self.last_exit_code = None
        self.enabled = None
        self.plugin_server = None
        self.input = None
        self.start_date = None
        self.plugin_name = None
        self.last_run_sql = None
        self.arguments = None
        self.user = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PluginScheduleList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``plugin_schedules``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'plugin_schedules'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'plugin_schedule': PluginSchedule,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.plugin_schedule = []
        self._set_init_values()


class PluginSql(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``sql_response``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'sql_response'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
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
            **kwargs
        )
        self.rows_affected = None
        self.result_count = None
        self.columns = None
        self.result_row = []
        self._set_init_values()


class PluginSqlColumn(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``columns``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'columns'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'name': text_type,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.name = []
        self._set_init_values()


class PluginSqlResult(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``result_row``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'result_row'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'value': text_type,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.value = []
        self._set_init_values()


class Question(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``question``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'question'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'query_text': text_type,
                'hidden_flag': int,
                'expiration': text_type,
                'index': int,
                'force_computer_id_flag': int,
                'name': text_type,
                'expire_seconds': int,
                'cache_row_id': int,
                'skip_lock_flag': int,
                'action_tracking_flag': int,
            },
            complex_properties={
                'context_group': Group,
                'user': User,
                'saved_question': SavedQuestion,
                'management_rights_group': Group,
                'group': Group,
                'selects': SelectList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.query_text = None
        self.hidden_flag = None
        self.expiration = None
        self.index = None
        self.force_computer_id_flag = None
        self.name = None
        self.expire_seconds = None
        self.cache_row_id = None
        self.skip_lock_flag = None
        self.action_tracking_flag = None
        self.context_group = None
        self.user = None
        self.saved_question = None
        self.management_rights_group = None
        self.group = None
        self.selects = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class QuestionList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``questions``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'questions'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'info': QuestionListInfo,
                'cache_info': CacheInfo,
            },
            list_properties={
                'question': Question,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.info = None
        self.cache_info = None
        self.question = []
        self._set_init_values()


class QuestionListInfo(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``info``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'info'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'highest_id': int,
                'total_count': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.highest_id = None
        self.total_count = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedAction(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``saved_action``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'saved_action'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'comment': text_type,
                'last_start_time': text_type,
                'approved_flag': int,
                'issue_seconds': int,
                'distribute_seconds': int,
                'status': int,
                'next_start_time': text_type,
                'name': text_type,
                'expire_seconds': int,
                'policy_flag': int,
                'end_time': text_type,
                'issue_count': int,
                'cache_row_id': int,
                'creation_time': text_type,
                'public_flag': int,
                'action_group_id': int,
                'user_start_time': text_type,
                'start_time': text_type,
            },
            complex_properties={
                'policy': SavedActionPolicy,
                'last_action': Action,
                'user': User,
                'metadata': MetadataList,
                'row_ids': SavedActionRowIdList,
                'action_group': Group,
                'approver': User,
                'package_spec': PackageSpec,
                'target_group': Group,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.comment = None
        self.last_start_time = None
        self.approved_flag = None
        self.issue_seconds = None
        self.distribute_seconds = None
        self.status = None
        self.next_start_time = None
        self.name = None
        self.expire_seconds = None
        self.policy_flag = None
        self.end_time = None
        self.issue_count = None
        self.cache_row_id = None
        self.creation_time = None
        self.public_flag = None
        self.action_group_id = None
        self.user_start_time = None
        self.start_time = None
        self.policy = None
        self.last_action = None
        self.user = None
        self.metadata = None
        self.row_ids = None
        self.action_group = None
        self.approver = None
        self.package_spec = None
        self.target_group = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedActionApproval(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``saved_action_approval``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'saved_action_approval'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
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
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.name = None
        self.approved_flag = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedActionList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``saved_actions``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'saved_actions'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'saved_action': SavedAction,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.saved_action = []
        self._set_init_values()


class SavedActionPolicy(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``policy``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'policy'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'saved_question_group_id': int,
                'row_filter_group_id': int,
                'max_age': int,
                'saved_question_id': int,
                'min_count': int,
            },
            complex_properties={
                'row_filter_group': Group,
                'saved_question_group': Group,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.saved_question_group_id = None
        self.row_filter_group_id = None
        self.max_age = None
        self.saved_question_id = None
        self.min_count = None
        self.row_filter_group = None
        self.saved_question_group = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedActionRowIdList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``row_ids``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'row_ids'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'row_id': int,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.row_id = []
        self._set_init_values()


class SavedQuestion(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``saved_question``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'saved_question'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'query_text': text_type,
                'archive_enabled_flag': int,
                'issue_seconds': int,
                'most_recent_question_id': int,
                'name': text_type,
                'expire_seconds': int,
                'public_flag': int,
                'sort_column': int,
                'cache_row_id': int,
                'keep_seconds': int,
                'hidden_flag': int,
                'action_tracking_flag': int,
                'index': int,
                'row_count_flag': int,
                'issue_seconds_never_flag': int,
                'mod_time': text_type,
            },
            complex_properties={
                'packages': PackageSpecList,
                'metadata': MetadataList,
                'user': User,
                'mod_user': User,
                'archive_owner': User,
                'question': Question,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.query_text = None
        self.archive_enabled_flag = None
        self.issue_seconds = None
        self.most_recent_question_id = None
        self.name = None
        self.expire_seconds = None
        self.public_flag = None
        self.sort_column = None
        self.cache_row_id = None
        self.keep_seconds = None
        self.hidden_flag = None
        self.action_tracking_flag = None
        self.index = None
        self.row_count_flag = None
        self.issue_seconds_never_flag = None
        self.mod_time = None
        self.packages = None
        self.metadata = None
        self.user = None
        self.mod_user = None
        self.archive_owner = None
        self.question = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedQuestionList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``saved_questions``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'saved_questions'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'saved_question': SavedQuestion,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.saved_question = []
        self._set_init_values()


class Select(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``select``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'select'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'group': Group,
                'filter': Filter,
                'sensor': Sensor,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.group = None
        self.filter = None
        self.sensor = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SelectList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``selects``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'selects'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'select': Select,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.select = []
        self._set_init_values()


class Sensor(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``sensor``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'sensor'

    CONSTANTS = [
        {'name': 'WMI_SENSOR', 'value': '1', 'type': int},
        {'name': 'BES_SENSOR', 'value': '2', 'type': int},
        {'name': 'VBS_SENSOR', 'value': '4', 'type': int},
        {'name': 'PSHELL_SENSOR', 'value': '5', 'type': int},
        {'name': 'MULTITYPE_SENSOR', 'value': '6', 'type': int},
        {'name': 'HASH_RESULT', 'value': '0', 'type': int},
        {'name': 'TEXT_RESULT', 'value': '1', 'type': int},
        {'name': 'VERSION_RESULT', 'value': '2', 'type': int},
        {'name': 'NUMERIC_RESULT', 'value': '3', 'type': int},
        {'name': 'BES_DATETIME_RESULT', 'value': '4', 'type': int},
        {'name': 'IP_RESULT', 'value': '5', 'type': int},
        {'name': 'WMI_DATETIME_RESULT', 'value': '6', 'type': int},
        {'name': 'TIMEDIFF_REUSLT', 'value': '7', 'type': int},
        {'name': 'DATASIZE_RESULT', 'value': '8', 'type': int},
        {'name': 'NUMERIC_INTEGER_RESULT', 'value': '9', 'type': int},
        {'name': 'REGEX_RESULT', 'value': '11', 'type': int},
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'modification_time': text_type,
                'string_count': int,
                'description': text_type,
                'source_hash': int,
                'name': text_type,
                'exclude_from_parse_flag': int,
                'deleted_flag': int,
                'parameter_definition': text_type,
                'delimiter': text_type,
                'cache_row_id': int,
                'category': text_type,
                'creation_time': text_type,
                'hidden_flag': int,
                'last_modified_by': text_type,
                'value_type': text_type,
                'ignore_case_flag': int,
                'preview_sensor_flag': int,
                'hash': int,
                'max_age_seconds': int,
                'source_id': int,
            },
            complex_properties={
                'parameters': ParameterList,
                'string_hints': StringHintList,
                'subcolumns': SensorSubcolumnList,
                'queries': SensorQueryList,
                'metadata': MetadataList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.modification_time = None
        self.string_count = None
        self.description = None
        self.source_hash = None
        self.name = None
        self.exclude_from_parse_flag = None
        self.deleted_flag = None
        self.parameter_definition = None
        self.delimiter = None
        self.cache_row_id = None
        self.category = None
        self.creation_time = None
        self.hidden_flag = None
        self.last_modified_by = None
        self.value_type = None
        self.ignore_case_flag = None
        self.preview_sensor_flag = None
        self.hash = None
        self.max_age_seconds = None
        self.source_id = None
        self.parameters = None
        self.string_hints = None
        self.subcolumns = None
        self.queries = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()

    @property
    def parameter_definition_dict(self):
        """Wrapper around parameter_definition to get the JSON string loaded."""
        # TODO: ADD parameter_definition_dict TO BUILDER, and add for all other objs that have pd
        try:
            result = json.loads(self.parameter_definition)
        except Exception as e:
            result = {
                "msg": "Unable to parse parameter_definition as JSON!",
                "parameter_definition": self.parameter_definition,
                "exception": e,
            }
        return result


class SensorList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``sensors``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'sensors'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'sensor': Sensor,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.sensor = []
        self._set_init_values()


class SensorQuery(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``query``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'query'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'script': text_type,
                'script_type': text_type,
                'platform': text_type,
                'signature': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.script = None
        self.script_type = None
        self.platform = None
        self.signature = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class SensorQueryList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``queries``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'queries'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'query': SensorQuery,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.query = []
        self._set_init_values()


class SensorSubcolumn(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``subcolumn``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'subcolumn'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'hidden_flag': int,
                'index': int,
                'ignore_case_flag': int,
                'name': text_type,
                'exclude_from_parse_flag': int,
                'value_type': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.hidden_flag = None
        self.index = None
        self.ignore_case_flag = None
        self.name = None
        self.exclude_from_parse_flag = None
        self.value_type = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class SensorSubcolumnList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``subcolumns``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'subcolumns'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'subcolumn': SensorSubcolumn,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.subcolumn = []
        self._set_init_values()


class SoapError(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``soap_error``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'soap_error'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'object_name': text_type,
                'object_request': text_type,
                'exception_name': text_type,
                'context': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.object_name = None
        self.object_request = None
        self.exception_name = None
        self.context = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class StringHintList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``string_hints``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'string_hints'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'string_hint': text_type,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.string_hint = []
        self._set_init_values()


class SystemSetting(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``system_setting``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'system_setting'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'value': text_type,
                'hidden_flag': int,
                'cache_row_id': int,
                'value_type': text_type,
                'default_value': text_type,
                'name': text_type,
                'setting_type': text_type,
                'read_only_flag': int,
            },
            complex_properties={
                'metadata': MetadataList,
                'audit_data': AuditData,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.value = None
        self.hidden_flag = None
        self.cache_row_id = None
        self.value_type = None
        self.default_value = None
        self.name = None
        self.setting_type = None
        self.read_only_flag = None
        self.metadata = None
        self.audit_data = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SystemSettingList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``system_settings``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'system_settings'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
            },
            list_properties={
                'system_setting': SystemSetting,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.system_setting = []
        self._set_init_values()


class SystemStatusAggregate(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``aggregate``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'aggregate'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'slowlink_count': int,
                'receive_ok_count': int,
                'send_ok_count': int,
                'leader_count': int,
                'normal_count': int,
                'send_none_count': int,
                'blocked_count': int,
                'send_forward_count': int,
                'receive_backward_count': int,
                'receive_forward_count': int,
                'receive_none_count': int,
                'send_backward_count': int,
            },
            complex_properties={
                'versions': VersionAggregateList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.slowlink_count = None
        self.receive_ok_count = None
        self.send_ok_count = None
        self.leader_count = None
        self.normal_count = None
        self.send_none_count = None
        self.blocked_count = None
        self.send_forward_count = None
        self.receive_backward_count = None
        self.receive_forward_count = None
        self.receive_none_count = None
        self.send_backward_count = None
        self.versions = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SystemStatusList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``system_status``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'system_status'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'aggregate': SystemStatusAggregate,
                'cache_info': CacheInfo,
            },
            list_properties={
                'client_status': ClientStatus,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        self.aggregate = None
        self.cache_info = None
        self.client_status = []
        self._set_init_values()


class UploadFile(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``upload_file``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'upload_file'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'key': text_type,
                'force_overwrite': int,
                'percent_complete': int,
                'start_pos': int,
                'file_size': int,
                'part_size': int,
                'file_cached': int,
                'destination_file': text_type,
                'bytes': text_type,
                'hash': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.key = None
        self.force_overwrite = None
        self.percent_complete = None
        self.start_pos = None
        self.file_size = None
        self.part_size = None
        self.file_cached = None
        self.destination_file = None
        self.bytes = None
        self.hash = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class UploadFileList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``file_parts``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'file_parts'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'upload_file': UploadFile,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.upload_file = []
        self._set_init_values()


class UploadFileStatus(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``upload_file_status``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'upload_file_status'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'file_cached': int,
                'hash': text_type,
                'percent_complete': int,
            },
            complex_properties={
                'file_parts': UploadFileList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.file_cached = None
        self.hash = None
        self.percent_complete = None
        self.file_parts = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class User(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``user``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'user'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'group_id': int,
                'last_login': text_type,
                'local_admin_flag': int,
                'domain': text_type,
                'name': text_type,
                'active_session_count': int,
                'deleted_flag': int,
            },
            complex_properties={
                'permissions': PermissionList,
                'roles': UserRoleList,
                'metadata': MetadataList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.group_id = None
        self.last_login = None
        self.local_admin_flag = None
        self.domain = None
        self.name = None
        self.active_session_count = None
        self.deleted_flag = None
        self.permissions = None
        self.roles = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class UserList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``users``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'users'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'user': User,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.user = []
        self._set_init_values()


class UserRole(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``role``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'role'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
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
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.name = None
        self.description = None
        self.permissions = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class UserRoleList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``roles``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'roles'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'role': UserRole,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.role = []
        self._set_init_values()


class VersionAggregate(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``version``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'version'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'version_string': text_type,
                'filtered': int,
                'count': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.version_string = None
        self.filtered = None
        self.count = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class VersionAggregateList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``versions``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'versions'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'version': VersionAggregate,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.version = []
        self._set_init_values()


class WhiteListedUrl(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``white_listed_url``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'white_listed_url'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'chunk_id': text_type,
                'url_regex': text_type,
                'download_seconds': int,
            },
            complex_properties={
                'metadata': MetadataList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.id = None
        self.chunk_id = None
        self.url_regex = None
        self.download_seconds = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class WhiteListedUrlList(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``white_listed_urls``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'white_listed_urls'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                'white_listed_url': WhiteListedUrl,
            },
            **kwargs
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.white_listed_url = []
        self._set_init_values()


class XmlError(BaseType):

    """Python Object representation for Tanium SOAP XML tag: ``error``.

    This class is dynamically generated from the console.wsdl for the Tanium Server SOAP API.
    """

    _SOAP_TAG = 'error'

    CONSTANTS = [
        # no constants defined in console.wsdl
    ]

    def __init__(self, **kwargs):
        """pass."""
        BaseType.__init__(
            self,
            simple_properties={
                'error_context': text_type,
                'exception': text_type,
                'type': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
            **kwargs
        )
        self.error_context = None
        self.exception = None
        self.type = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


BASE_TYPES = {}
"""Maps Tanium XML soap tags to the Tanium NG Python BaseType object"""
BASE_TYPES['result_infos'] = ResultInfoList  # static
BASE_TYPES['result_info'] = ResultInfo  # static
BASE_TYPES['result_sets'] = ResultSetList  # static
BASE_TYPES['result_set'] = ResultSet  # static
BASE_TYPES['cs'] = ColumnList  # static
BASE_TYPES['c'] = Column  # static
BASE_TYPES['rs'] = RowList  # static
BASE_TYPES['r'] = Row  # static

BASE_TYPES['action'] = Action
BASE_TYPES['actions'] = ActionList
BASE_TYPES['info'] = ActionListInfo
BASE_TYPES['action_stop'] = ActionStop
BASE_TYPES['action_stops'] = ActionStopList
BASE_TYPES['archived_question'] = ArchivedQuestion
BASE_TYPES['archived_questions'] = ArchivedQuestionList
BASE_TYPES['audit_data'] = AuditData
BASE_TYPES['filter'] = CacheFilter
BASE_TYPES['cache_filters'] = CacheFilterList
BASE_TYPES['cache_info'] = CacheInfo
BASE_TYPES['client_count'] = ClientCount
BASE_TYPES['client_status'] = ClientStatus
BASE_TYPES['computer_group'] = ComputerGroup
BASE_TYPES['computer_groups'] = ComputerGroupList
BASE_TYPES['computer_spec'] = ComputerGroupSpec
BASE_TYPES['computer_specs'] = ComputerSpecList
BASE_TYPES['errors'] = ErrorList
BASE_TYPES['filter'] = Filter
BASE_TYPES['filters'] = FilterList
BASE_TYPES['group'] = Group
BASE_TYPES['groups'] = GroupList
BASE_TYPES['item'] = MetadataItem
BASE_TYPES['metadata'] = MetadataList
BASE_TYPES['object_list'] = ObjectList
BASE_TYPES['options'] = Options
BASE_TYPES['file'] = PackageFile
BASE_TYPES['package_files'] = PackageFileList
BASE_TYPES['status'] = PackageFileStatus
BASE_TYPES['file_status'] = PackageFileStatusList
BASE_TYPES['file_template'] = PackageFileTemplate
BASE_TYPES['file_templates'] = PackageFileTemplateList
BASE_TYPES['package_spec'] = PackageSpec
BASE_TYPES['package_specs'] = PackageSpecList
BASE_TYPES['parameter'] = Parameter
BASE_TYPES['parameters'] = ParameterList
BASE_TYPES['parse_job'] = ParseJob
BASE_TYPES['parse_jobs'] = ParseJobList
BASE_TYPES['parse_result'] = ParseResult
BASE_TYPES['parse_result_group'] = ParseResultGroup
BASE_TYPES['parse_result_groups'] = ParseResultGroupList
BASE_TYPES['parse_results'] = ParseResultList
BASE_TYPES['permissions'] = PermissionList
BASE_TYPES['plugin'] = Plugin
BASE_TYPES['argument'] = PluginArgument
BASE_TYPES['arguments'] = PluginArgumentList
BASE_TYPES['commands'] = PluginCommandList
BASE_TYPES['plugins'] = PluginList
BASE_TYPES['plugin_schedule'] = PluginSchedule
BASE_TYPES['plugin_schedules'] = PluginScheduleList
BASE_TYPES['sql_response'] = PluginSql
BASE_TYPES['columns'] = PluginSqlColumn
BASE_TYPES['result_row'] = PluginSqlResult
BASE_TYPES['question'] = Question
BASE_TYPES['questions'] = QuestionList
BASE_TYPES['info'] = QuestionListInfo
BASE_TYPES['saved_action'] = SavedAction
BASE_TYPES['saved_action_approval'] = SavedActionApproval
BASE_TYPES['saved_actions'] = SavedActionList
BASE_TYPES['policy'] = SavedActionPolicy
BASE_TYPES['row_ids'] = SavedActionRowIdList
BASE_TYPES['saved_question'] = SavedQuestion
BASE_TYPES['saved_questions'] = SavedQuestionList
BASE_TYPES['select'] = Select
BASE_TYPES['selects'] = SelectList
BASE_TYPES['sensor'] = Sensor
BASE_TYPES['sensors'] = SensorList
BASE_TYPES['query'] = SensorQuery
BASE_TYPES['queries'] = SensorQueryList
BASE_TYPES['subcolumn'] = SensorSubcolumn
BASE_TYPES['subcolumns'] = SensorSubcolumnList
BASE_TYPES['soap_error'] = SoapError
BASE_TYPES['string_hints'] = StringHintList
BASE_TYPES['system_setting'] = SystemSetting
BASE_TYPES['system_settings'] = SystemSettingList
BASE_TYPES['aggregate'] = SystemStatusAggregate
BASE_TYPES['system_status'] = SystemStatusList
BASE_TYPES['upload_file'] = UploadFile
BASE_TYPES['file_parts'] = UploadFileList
BASE_TYPES['upload_file_status'] = UploadFileStatus
BASE_TYPES['user'] = User
BASE_TYPES['users'] = UserList
BASE_TYPES['role'] = UserRole
BASE_TYPES['roles'] = UserRoleList
BASE_TYPES['version'] = VersionAggregate
BASE_TYPES['versions'] = VersionAggregateList
BASE_TYPES['white_listed_url'] = WhiteListedUrl
BASE_TYPES['white_listed_urls'] = WhiteListedUrlList
BASE_TYPES['error'] = XmlError

# END DYNAMIC CODE
