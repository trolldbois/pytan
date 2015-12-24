# BEGIN STATIC CODE
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

from . import text_type, encoding  # noqa
from . import utils


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


def get_obj_type(tag):
    """Maps Tanium XML soap tags to the Tanium NG Python BaseType object"""
    if tag not in BASE_TYPES:  # noqa
        err = 'Unknown type {}'
        err = err.format(tag)
        raise TaniumNextGenException(err)
    result = BASE_TYPES[tag]  # noqa
    return result


class BaseType(object):
    """Base Python Type used for all Tanium XML SOAP Objects generated from console.wsdl"""

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
    """dict that stores the complex properties for this object (other BaseTypes)"""

    _IS_LIST = False
    """bool indicating if this is a single list object or not"""

    _LIST_ATTR = ''
    """str that stores the name of the list attribute for this object if it is a single list"""

    _LIST_TYPE = None
    """stores the type of the list objects for this object if it is a single list"""

    _ATTRS = []
    """list that stores a preferentially sorted list of non-list attributes for this object"""

    def __init__(self, simple_properties, complex_properties, list_properties, **kwargs):
        self._INITIALIZED = False

        self._INIT_VALUES = kwargs.get('values', {}) or {}

        self._SIMPLE_PROPS = simple_properties
        self._COMPLEX_PROPS = complex_properties
        self._LIST_PROPS = list_properties

        self._IS_LIST = len(list_properties) == 1
        if self._IS_LIST:
            self._LIST_ATTR, self._LIST_TYPE = list(list_properties.items())[0]

        self._ATTRS = list(self._SIMPLE_PROPS.keys()) + list(self._COMPLEX_PROPS.keys())
        self._ATTRS = sorted(self._ATTRS)
        for f in ['name', 'id']:
            if f in self._ATTRS:
                self._ATTRS.remove(f)
                self._ATTRS.insert(0, f)

        self._ALL_PROPS = {}
        self._ALL_PROPS.update(self._SIMPLE_PROPS)
        self._ALL_PROPS.update(self._COMPLEX_PROPS)
        self._ALL_PROPS.update(self._LIST_PROPS)

        self._INITIALIZED = True

    def _list_only_method(self):
        """Exception to throw on methods that are only supported for single list types"""
        if not self._IS_LIST:
            err = 'Not a list type with a single list property!'
            raise TaniumNextGenException(err)

    def __getitem__(self, idx):
        """Support a[n] for single list types."""
        self._list_only_method()
        result = getattr(self, self._LIST_ATTR).__getitem__(idx)
        return result

    def append(self, value):
        """Support .append() for single list types."""
        self._list_only_method()
        if not isinstance(value, self._LIST_TYPE):
            raise IncorrectTypeException(self._LIST_ATTR, value, self._LIST_TYPE)
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
        """Return length of list attribute if this object is a list, elsewise
        return the number of attributes that are not None.
        """
        if self._IS_LIST:
            result = len(getattr(self, self._LIST_ATTR))
        else:
            result = sum([1 for k in self._ATTRS if getattr(self, k, None) is not None])
        return result

    def __repr__(self):
        """If this is a list item, return class name, list, and all attributes.
        If this is not a list item, return class name and all attributes.
        """
        class_name = self.__class__
        vals = []
        if self._IS_LIST:
            val = '{} items'.format(len(self))
            name = 'LIST:{!r}:{!r}'.format(self._LIST_ATTR, self._LIST_TYPE)
            vals.append([name, val])

        for k in self._ATTRS:
            val = getattr(self, k, None)
            name = '{} ({})'.format(k, self._ALL_PROPS[k])
            if isinstance(val, list):
                val = "{}".format(len(val))
            else:
                val = "{!r}".format(val)
            vals.append([name, val])

        vals = ', '.join(["{}={}".format(*p) for p in vals])
        result = '{}: {}'.format(class_name, vals)
        return result

    def __str__(self):
        """If this is a list item, return class name, list length, and all attributes that are set.
        If this is not a list item, return class name and all attributes that are set.
        """
        class_name = self.__class__.__name__
        vals = []
        if self._IS_LIST:
            name = 'length'
            val = len(self)
            vals.append([name, val])

        for k in self._ATTRS:
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
            vals = ', '.join(["'{}'='{}'".format(*p) for p in vals])
        else:
            vals = "No attributes assigned yet!"

        result = '{}: {}'.format(class_name, vals)
        return result

    def __setattr__(self, name, value):
        """Enforce type of attribute assignments"""
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
            raise IncorrectTypeException(name, value, self._COMPLEX_PROPS[name])
        return value

    def _check_simple(self, name, value):
        if not isinstance(value, self._SIMPLE_PROPS[name]):
            if self._SIMPLE_PROPS[name] == int:
                try:
                    value = self._SIMPLE_PROPS[name](value)
                except:
                    raise IncorrectTypeException(name, value, self._SIMPLE_PROPS[name])
            else:
                raise IncorrectTypeException(name, value, self._SIMPLE_PROPS[name])
        return value

    def _check_list(self, name, value):
        if not isinstance(value, list):
            raise IncorrectTypeException(name, value, self._LIST_PROPS[name])
        for i in value:
            if not isinstance(i, self._LIST_PROPS[name]):
                raise IncorrectTypeException(name, i, self._LIST_PROPS[name])
        return value

    def to_soap_element(self, minimal=False):  # noqa
        # print(minimal)
        root = ET.Element(self._SOAP_TAG)
        for p in self._SIMPLE_PROPS:
            el = ET.Element(p)
            val = getattr(self, p)
            # print(p, val)
            if val is not None:
                el.text = str(val)
            if val is not None or not minimal:
                root.append(el)
        for p, t in self._COMPLEX_PROPS.items():
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
        for p, t in self._LIST_PROPS.items():
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
        return result

    @classmethod
    def from_soap_element(cls, el):
        result = cls()
        for p, t in result._SIMPLE_PROPS.items():
            pel = el.find("./{}".format(p))
            if pel is not None and pel.text:
                setattr(result, p, t(pel.text))
            else:
                setattr(result, p, None)
        for p, t in result._COMPLEX_PROPS.items():
            elems = el.findall('./{}'.format(p))
            if len(elems) > 1:
                raise TaniumNextGenException(
                    'Unexpected: {} elements for property'.format(p)
                )
            elif len(elems) == 1:
                setattr(
                    result,
                    p,
                    result._COMPLEX_PROPS[p].from_soap_element(elems[0]),
                )
            else:
                setattr(result, p, None)
        for p, t in result._LIST_PROPS.items():
            setattr(result, p, [])
            elems = el.findall('./{}'.format(p))
            for elem in elems:
                if issubclass(t, BaseType):
                    getattr(result, p).append(t.from_soap_element(elem))
                else:
                    getattr(result, p).append(elem.text)
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
            obj = get_obj_type(el.tag)
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
            if val in utils.constants.SENSOR_TYPE_MAP:
                result.result_type = utils.constants.SENSOR_TYPE_MAP[val]
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


# END STATIC CODE
# BEGIN DYNAMIC CODE
