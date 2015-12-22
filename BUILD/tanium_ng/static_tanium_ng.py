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
        from . import OBJECT_TYPES
        if el.tag not in OBJECT_TYPES:
            err = 'Unknown type {}'
            err = err.format(el.tag)
            raise TaniumNextGenException(err)
        result = eval(OBJECT_TYPES[el.tag])
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
