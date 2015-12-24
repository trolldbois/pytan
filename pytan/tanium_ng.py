"""Tanium NG: A Python object representation layer for the XML used by the Tanium SOAP API.

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-23T16-04-31Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""

# BEGIN STATIC CODE
from . import text_type  # noqa
from . import utils

TaniumNextGenException = utils.exceptions.TaniumNextGenException
IncorrectTypeException = utils.exceptions.IncorrectTypeException


def get_obj_type(tag):
    """Maps Tanium XML soap tags to the Tanium NG Python BaseType object"""
    if tag not in BASE_TYPES:  # noqa
        err = 'Unknown type {}'
        err = err.format(tag)
        raise TaniumNextGenException(err)
    result = BASE_TYPES[tag]  # noqa
    return result


# XML CODE FOR BASE TYPE ONLY FOR NOW
# TODO TRY LXML
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

from . import encoding
from . import utils
xml_pretty = utils.tools.xml_pretty


class ObjectToXML(object):
    """Convert a tanium_ng BaseType object into an ElementTree object and then an XML string.

    x = ObjectToXML(obj)

    Get ROOT:
    x.ROOT

    Get XML:
    x.XML
    """

    EMPTY_ATTRS = True
    """bool that controls if empty attributes will be included in the Element Tree Object"""

    OBJ = None
    """tanium_ng object to convert to ElementTree object ROOT"""

    ROOT = None
    """ElementTree object created from OBJ"""

    XML = ''
    """XML string created from ROOT"""

    def __init__(self, obj, **kwargs):
        # print("New ObjectToXML for obj: {}".format(obj))
        self.EMPTY_ATTRS = kwargs.get('empty_attrs', self.EMPTY_ATTRS)
        self.PARENT = kwargs.get('parent', True)
        self.OBJ = obj

        # basetype methods
        self.ROOT = ET.Element(obj._SOAP_TAG)
        self.base_simple()
        self.base_complex()
        self.base_list()

        if self.PARENT:
            self.XML = ET.tostring(self.ROOT, encoding=encoding)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for p in self.OBJ._SIMPLE_PROPS:
            val = getattr(self.OBJ, p)
            if val is None and not self.EMPTY_ATTRS:
                continue
            self.add_simple_el(p, val)

    def add_simple_el(self, p, val):
        val = text_type(val) if val is not None else None
        el = ET.Element(p)
        el.text = val
        self.ROOT.append(el)

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for p in self.OBJ._COMPLEX_PROPS:
            val = getattr(self.OBJ, p)
            if val is None and not self.EMPTY_ATTRS:
                continue

            if isinstance(val, BaseType):
                val_btr = ObjectToXML(val, empty_attrs=self.EMPTY_ATTRS, parent=False)
                children = val_btr.ROOT.getchildren() or []

                el = ET.Element(p)
                for c in children:
                    el.append(c)
                self.ROOT.append(el)
            else:
                # TODO TEST MORE
                self.add_simple_el(p, val)
                # el = ET.Element(p)
                # val = text_type(val) if val is not None else None
                # el.append(val)
                # self.ROOT.append(el)

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for p, t in self.OBJ._LIST_PROPS.items():
            vals = getattr(self.OBJ, p)
            if not vals:
                continue

            if issubclass(t, BaseType):
                for val in vals:
                    val_btr = ObjectToXML(val, empty_attrs=self.EMPTY_ATTRS, parent=False)
                    self.ROOT.append(val_btr.ROOT)
            else:
                '''
                fix for non tanium_ng types in list props, only happens in:
                PermissionList
                PluginCommandList
                PluginSqlColumn
                PluginSqlResult
                StringHintList
                SavedActionRowIdList
                '''
                for val in vals:
                    if val is None and not self.EMPTY_ATTRS:
                        continue
                    self.add_simple_el(p, val)


class XMLToObject(object):
    """Convert an XML String or an ElementTree object into a tanium_ng BaseType object.

    x = XMLToObject(xml=xml)
        ..or..
    x = XMLToObject(objclass=tanium_ng.Sensor, root=root)

    Get OBJ:
    x.OBJ
    """

    OBJ = None
    """tanium_ng object that gets created from ROOT"""

    ROOT = None
    """ElementTree object to convert into a tanium_ng object"""

    XML = ''
    """XML string to convert into a tanium_ng object"""

    XMLTREE = None
    """If XML string supplied, full elementtree used to search for ROOT"""

    def __init__(self, **kwargs):
        # print("New XMLToObject for root: {}".format(root))
        self.XML = kwargs.get('xml', '')
        self.ROOT = kwargs.get('root', '')
        self.OBJCLASS = kwargs.get('objclass')

        if self.OBJCLASS and self.ROOT:
            self.OBJ = self.OBJCLASS()
        elif self.XML:
            # basetype search
            self.XMLTREE = ET.fromstring(self.XML)
            xpath = ".//result_object/*"
            self.ROOT = self.XMLTREE.find(xpath)

            # add if not ROOT, check for ResultXML xpath
            # throw error if neither ResultXML nor result_object found? may need to change xpath
            # for result_object

            if self.ROOT:
                self.OBJCLASS = get_obj_type(self.ROOT.tag)
                self.OBJ = self.OBJCLASS()
            # m = "xpath: {} root: {}"
            # m = m.format(xpath, self.ROOT)
            # print(m)
        else:
            err = "Must supply either xml or both objclass and root!"
            raise TaniumNextGenException(err)

        if self.ROOT:
            # basetype methods
            self.base_simple()
            self.base_complex()
            self.base_list()
            self.OBJ._XMLTREE = self.XMLTREE
            self.OBJ._XML = self.XML
            self.OBJ._ROOT = self.ROOT

    def base_simple(self):
        """Process the simple properties for the tanium_ng object"""
        for prop, prop_type in self.OBJ._SIMPLE_PROPS.items():
            xpath = "./{}".format(prop)
            prop_el = self.ROOT.find(xpath)
            if prop_el is not None and prop_el.text:
                setattr(self.OBJ, prop, prop_type(prop_el.text))
            else:
                setattr(self.OBJ, prop, None)

    def base_complex(self):
        """Process the complex properties for the tanium_ng object"""
        for prop, prop_type in self.OBJ._COMPLEX_PROPS.items():
            xpath = './{}'.format(prop)
            prop_elems = self.ROOT.findall(xpath)
            if len(prop_elems) > 1:
                err = 'Found {} elements for property {}, should only be 1 (xpath: {})'
                err = err.format(len(prop_elems), prop, xpath)
                raise TaniumNextGenException(err)
            elif len(prop_elems) == 1:
                val_btr = XMLToObject(objclass=prop_type, root=prop_elems[0])
                setattr(self.OBJ, prop, val_btr.OBJ)
            else:
                setattr(self.OBJ, prop, None)

    def base_list(self):
        """Process the list properties for the tanium_ng object"""
        for prop, prop_type in self.OBJ._LIST_PROPS.items():
            setattr(self.OBJ, prop, [])
            prop_list = getattr(self.OBJ, prop)
            xpath = './{}'.format(prop)
            prop_elems = self.ROOT.findall(xpath)
            for prop_elem in prop_elems:
                if issubclass(prop_type, BaseType):
                    val_btr = XMLToObject(objclass=prop_type, root=prop_elem)
                    prop_list.append(val_btr.OBJ)
                else:
                    prop_list.append(prop_elem.text)


def to_xml(obj, **kwargs):
    """Deserialize tanium_ng object ``obj`` into an XML body"""
    tickle_val = ObjectToXML(obj, **kwargs)
    result = tickle_val.XML
    # print(xml_pretty(result))
    return result


def from_xml(xml, **kwargs):
    """Serialize ``xml`` from XML into a tanium_ng object."""
    tickle_val = XMLToObject(xml=xml, **kwargs)
    result = tickle_val.OBJ
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
    """Wrap the result of GetResultInfo

    Not defined in console.wsdl, so statically defined here
    """

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


class Action(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``action``."""

    _SOAP_TAG = 'action'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'cache_row_id': int,
                'id': int,
                'name': text_type,
                'status': text_type,
                'stopped_flag': int,
                'comment': text_type,
                'skip_lock_flag': int,
                'expire_seconds': int,
                'creation_time': text_type,
                'start_time': text_type,
                'expiration_time': text_type,
                'distribute_seconds': int,
            },
            complex_properties={
                'action_group': Group,
                'package_spec': PackageSpec,
                'saved_action': SavedAction,
                'history_saved_question': SavedQuestion,
                'target_group': Group,
                'user': User,
                'metadata': MetadataList,
                'approver': User,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.cache_row_id = None
        self.id = None
        self.name = None
        self.status = None
        self.stopped_flag = None
        self.comment = None
        self.skip_lock_flag = None
        self.expire_seconds = None
        self.creation_time = None
        self.start_time = None
        self.expiration_time = None
        self.distribute_seconds = None
        self.action_group = None
        self.package_spec = None
        self.saved_action = None
        self.history_saved_question = None
        self.target_group = None
        self.user = None
        self.metadata = None
        self.approver = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ActionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``actions``."""

    _SOAP_TAG = 'actions'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
                'info': ActionListInfo,
            },
            list_properties={
                'action': Action,
            },
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.info = None
        self.action = []
        self._set_init_values()


class ActionListInfo(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``info``."""

    _SOAP_TAG = 'info'

    def __init__(self, **kwargs):
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
        )
        self.highest_id = None
        self.total_count = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ActionStop(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``action_stop``."""

    _SOAP_TAG = 'action_stop'

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
                # no list properties defined in console.wsdl
            },
        )
        self.id = None
        self.action = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ActionStopList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``action_stops``."""

    _SOAP_TAG = 'action_stops'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.action_stop = []
        self._set_init_values()


class ArchivedQuestion(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``archived_question``."""

    _SOAP_TAG = 'archived_question'

    def __init__(self, **kwargs):
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
        )
        self.id = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ArchivedQuestionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``archived_questions``."""

    _SOAP_TAG = 'archived_questions'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.archived_question = []
        self._set_init_values()


class AuditData(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``audit_data``."""

    _SOAP_TAG = 'audit_data'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'last_modified_by': text_type,
                'creation_time': text_type,
                'modification_time': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.last_modified_by = None
        self.creation_time = None
        self.modification_time = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class CacheFilter(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``filter``."""

    _SOAP_TAG = 'filter'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'operator': text_type,
                'field': text_type,
                'value': text_type,
                'type': text_type,
                'not_flag': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.operator = None
        self.field = None
        self.value = None
        self.type = None
        self.not_flag = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class CacheFilterList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``cache_filters``."""

    _SOAP_TAG = 'cache_filters'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.filter = []
        self._set_init_values()


class CacheInfo(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``cache_info``."""

    _SOAP_TAG = 'cache_info'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'page_row_count': int,
                'cache_id': int,
                'cache_row_count': int,
                'filtered_row_count': int,
                'expiration': text_type,
            },
            complex_properties={
                'errors': ErrorList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.page_row_count = None
        self.cache_id = None
        self.cache_row_count = None
        self.filtered_row_count = None
        self.expiration = None
        self.errors = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ClientCount(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``client_count``."""

    _SOAP_TAG = 'client_count'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ClientStatus(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``client_status``."""

    _SOAP_TAG = 'client_status'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'computer_id': text_type,
                'host_name': text_type,
                'last_registration': text_type,
                'status': text_type,
                'full_version': text_type,
                'send_state': text_type,
                'protocol_version': int,
                'public_key_valid': int,
                'cache_row_id': int,
                'port_number': int,
                'ipaddress_client': text_type,
                'ipaddress_server': text_type,
                'receive_state': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.computer_id = None
        self.host_name = None
        self.last_registration = None
        self.status = None
        self.full_version = None
        self.send_state = None
        self.protocol_version = None
        self.public_key_valid = None
        self.cache_row_id = None
        self.port_number = None
        self.ipaddress_client = None
        self.ipaddress_server = None
        self.receive_state = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ComputerGroup(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``computer_group``."""

    _SOAP_TAG = 'computer_group'

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
                # no list properties defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.deleted_flag = None
        self.computer_specs = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ComputerGroupList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``computer_groups``."""

    _SOAP_TAG = 'computer_groups'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.computer_group = []
        self._set_init_values()


class ComputerGroupSpec(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``computer_spec``."""

    _SOAP_TAG = 'computer_spec'

    def __init__(self, **kwargs):
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
        )
        self.id = None
        self.computer_name = None
        self.ip_address = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ComputerSpecList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``computer_specs``."""

    _SOAP_TAG = 'computer_specs'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.computer_spec = []
        self._set_init_values()


class ErrorList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``errors``."""

    _SOAP_TAG = 'errors'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.error = []
        self._set_init_values()


class Filter(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``filter``."""

    _SOAP_TAG = 'filter'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'substring_start': int,
                'aggregation': text_type,
                'value_type': text_type,
                'substring_flag': int,
                'delimiter_index': int,
                'value': text_type,
                'end_time': text_type,
                'not_flag': int,
                'max_age_seconds': int,
                'utf8_flag': int,
                'operator': text_type,
                'substring_length': int,
                'all_times_flag': int,
                'start_time': text_type,
                'all_values_flag': int,
                'ignore_case_flag': int,
                'delimiter': text_type,
            },
            complex_properties={
                'sensor': Sensor,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.id = None
        self.substring_start = None
        self.aggregation = None
        self.value_type = None
        self.substring_flag = None
        self.delimiter_index = None
        self.value = None
        self.end_time = None
        self.not_flag = None
        self.max_age_seconds = None
        self.utf8_flag = None
        self.operator = None
        self.substring_length = None
        self.all_times_flag = None
        self.start_time = None
        self.all_values_flag = None
        self.ignore_case_flag = None
        self.delimiter = None
        self.sensor = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class FilterList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``filters``."""

    _SOAP_TAG = 'filters'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.filter = []
        self._set_init_values()


class Group(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``group``."""

    _SOAP_TAG = 'group'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'name': text_type,
                'deleted_flag': int,
                'text': text_type,
                'not_flag': int,
                'source_id': int,
                'and_flag': int,
                'type': int,
            },
            complex_properties={
                'parameters': ParameterList,
                'filters': FilterList,
                'sub_groups': GroupList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.id = None
        self.name = None
        self.deleted_flag = None
        self.text = None
        self.not_flag = None
        self.source_id = None
        self.and_flag = None
        self.type = None
        self.parameters = None
        self.filters = None
        self.sub_groups = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class GroupList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``groups``."""

    _SOAP_TAG = 'groups'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.group = []
        self._set_init_values()


class MetadataItem(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``item``."""

    _SOAP_TAG = 'item'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'admin_flag': int,
                'value': text_type,
                'name': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.admin_flag = None
        self.value = None
        self.name = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class MetadataList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``metadata``."""

    _SOAP_TAG = 'metadata'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.item = []
        self._set_init_values()


class ObjectList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``object_list``."""

    _SOAP_TAG = 'object_list'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'export_id': text_type,
            },
            complex_properties={
                'white_listed_urls': WhiteListedUrlList,
                'roles': UserRoleList,
                'client_count': ClientCount,
                'questions': QuestionList,
                'computer_groups': ComputerGroupList,
                'saved_actions': SavedActionList,
                'actions': ActionList,
                'system_status': SystemStatusList,
                'system_settings': SystemSettingList,
            },
            list_properties={
                'plugin_schedule': PluginSchedule,
                'sensor': Sensor,
                'users': UserList,
                'package_spec': PackageSpec,
                'saved_action_approval': SavedActionApproval,
                'sensors': SensorList,
                'package_file': PackageFile,
                'parse_job': ParseJob,
                'plugin_schedules': PluginScheduleList,
                'client_status': ClientStatus,
                'parse_jobs': ParseJobList,
                'white_listed_url': WhiteListedUrl,
                'action': Action,
                'question': Question,
                'package_files': PackageFileList,
                'user': User,
                'parse_result_groups': ParseResultGroupList,
                'archived_question': ArchivedQuestion,
                'groups': GroupList,
                'package_specs': PackageSpecList,
                'computer_group': ComputerGroup,
                'system_setting': SystemSetting,
                'parse_result_group': ParseResultGroup,
                'action_stop': ActionStop,
                'soap_error': SoapError,
                'group': Group,
                'saved_question': SavedQuestion,
                'saved_questions': SavedQuestionList,
                'plugin': Plugin,
                'saved_action': SavedAction,
                'action_stops': ActionStopList,
                'upload_file_status': UploadFileStatus,
                'archived_questions': ArchivedQuestionList,
                'upload_file': UploadFile,
                'plugins': PluginList,
            },
        )
        self.export_id = None
        self.white_listed_urls = None
        self.roles = None
        self.client_count = None
        self.questions = None
        self.computer_groups = None
        self.saved_actions = None
        self.actions = None
        self.system_status = None
        self.system_settings = None
        self.plugin_schedule = []
        self.sensor = []
        self.users = []
        self.package_spec = []
        self.saved_action_approval = []
        self.sensors = []
        self.package_file = []
        self.parse_job = []
        self.plugin_schedules = []
        self.client_status = []
        self.parse_jobs = []
        self.white_listed_url = []
        self.action = []
        self.question = []
        self.package_files = []
        self.user = []
        self.parse_result_groups = []
        self.archived_question = []
        self.groups = []
        self.package_specs = []
        self.computer_group = []
        self.system_setting = []
        self.parse_result_group = []
        self.action_stop = []
        self.soap_error = []
        self.group = []
        self.saved_question = []
        self.saved_questions = []
        self.plugin = []
        self.saved_action = []
        self.action_stops = []
        self.upload_file_status = []
        self.archived_questions = []
        self.upload_file = []
        self.plugins = []
        self._set_init_values()


class Options(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``options``."""

    _SOAP_TAG = 'options'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'json_pretty_print': int,
                'context_id': int,
                'most_recent_flag': int,
                'return_lists_flag': int,
                'use_json': int,
                'include_hashes_flag': int,
                'cache_sort_fields': text_type,
                'export_format': int,
                'export_leading_text': text_type,
                'use_user_context_flag': int,
                'pct_done_limit': int,
                'row_start': int,
                'flags': int,
                'cache_id': int,
                'sort_order': text_type,
                'filter_string': text_type,
                'hide_no_results_flag': int,
                'row_count': int,
                'suppress_scripts': int,
                'return_cdata_flag': int,
                'hide_errors_flag': int,
                'aggregate_over_time_flag': int,
                'sample_frequency': int,
                'script_data': text_type,
                'sample_count': int,
                'include_hidden_flag': int,
                'export_flag': int,
                'suppress_object_list': int,
                'sample_start': int,
                'cache_expiration': int,
                'export_trailing_text': text_type,
                'recent_result_buckets': text_type,
                'filter_not_flag': int,
                'row_counts_only_flag': int,
                'include_user_details': int,
                'include_answer_times_flag': int,
                'use_error_objects': int,
            },
            complex_properties={
                'cache_filters': CacheFilterList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.json_pretty_print = None
        self.context_id = None
        self.most_recent_flag = None
        self.return_lists_flag = None
        self.use_json = None
        self.include_hashes_flag = None
        self.cache_sort_fields = None
        self.export_format = None
        self.export_leading_text = None
        self.use_user_context_flag = None
        self.pct_done_limit = None
        self.row_start = None
        self.flags = None
        self.cache_id = None
        self.sort_order = None
        self.filter_string = None
        self.hide_no_results_flag = None
        self.row_count = None
        self.suppress_scripts = None
        self.return_cdata_flag = None
        self.hide_errors_flag = None
        self.aggregate_over_time_flag = None
        self.sample_frequency = None
        self.script_data = None
        self.sample_count = None
        self.include_hidden_flag = None
        self.export_flag = None
        self.suppress_object_list = None
        self.sample_start = None
        self.cache_expiration = None
        self.export_trailing_text = None
        self.recent_result_buckets = None
        self.filter_not_flag = None
        self.row_counts_only_flag = None
        self.include_user_details = None
        self.include_answer_times_flag = None
        self.use_error_objects = None
        self.cache_filters = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageFile(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file``."""

    _SOAP_TAG = 'file'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'size': int,
                'id': int,
                'download_seconds': int,
                'bytes_downloaded': int,
                'name': text_type,
                'status': int,
                'last_download_progress_time': text_type,
                'hash': text_type,
                'deleted_flag': int,
                'download_start_time': text_type,
                'cache_status': text_type,
                'trigger_download': int,
                'bytes_total': int,
                'source': text_type,
            },
            complex_properties={
                'file_status': PackageFileStatusList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.size = None
        self.id = None
        self.download_seconds = None
        self.bytes_downloaded = None
        self.name = None
        self.status = None
        self.last_download_progress_time = None
        self.hash = None
        self.deleted_flag = None
        self.download_start_time = None
        self.cache_status = None
        self.trigger_download = None
        self.bytes_total = None
        self.source = None
        self.file_status = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageFileList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``package_files``."""

    _SOAP_TAG = 'package_files'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.file = []
        self._set_init_values()


class PackageFileStatus(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``status``."""

    _SOAP_TAG = 'status'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'cache_message': text_type,
                'status': int,
                'cache_status': text_type,
                'last_download_progress_time': text_type,
                'bytes_downloaded': int,
                'server_name': text_type,
                'server_id': int,
                'download_start_time': text_type,
                'bytes_total': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.cache_message = None
        self.status = None
        self.cache_status = None
        self.last_download_progress_time = None
        self.bytes_downloaded = None
        self.server_name = None
        self.server_id = None
        self.download_start_time = None
        self.bytes_total = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageFileStatusList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file_status``."""

    _SOAP_TAG = 'file_status'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.status = []
        self._set_init_values()


class PackageFileTemplate(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file_template``."""

    _SOAP_TAG = 'file_template'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'download_seconds': int,
                'hash': text_type,
                'source': text_type,
                'name': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.download_seconds = None
        self.hash = None
        self.source = None
        self.name = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageFileTemplateList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file_templates``."""

    _SOAP_TAG = 'file_templates'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.file_template = []
        self._set_init_values()


class PackageSpec(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``package_spec``."""

    _SOAP_TAG = 'package_spec'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'available_time': text_type,
                'id': int,
                'name': text_type,
                'signature': text_type,
                'command': text_type,
                'parameter_definition': text_type,
                'cache_row_id': int,
                'source_id': int,
                'skip_lock_flag': int,
                'command_timeout': int,
                'hidden_flag': int,
                'display_name': text_type,
                'expire_seconds': int,
                'creation_time': text_type,
                'modification_time': text_type,
                'last_modified_by': text_type,
                'deleted_flag': int,
                'verify_expire_seconds': int,
                'verify_group_id': int,
                'last_update': text_type,
            },
            complex_properties={
                'parameters': ParameterList,
                'files': PackageFileList,
                'sensors': SensorList,
                'file_templates': PackageFileTemplateList,
                'verify_group': Group,
                'metadata': MetadataList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.available_time = None
        self.id = None
        self.name = None
        self.signature = None
        self.command = None
        self.parameter_definition = None
        self.cache_row_id = None
        self.source_id = None
        self.skip_lock_flag = None
        self.command_timeout = None
        self.hidden_flag = None
        self.display_name = None
        self.expire_seconds = None
        self.creation_time = None
        self.modification_time = None
        self.last_modified_by = None
        self.deleted_flag = None
        self.verify_expire_seconds = None
        self.verify_group_id = None
        self.last_update = None
        self.parameters = None
        self.files = None
        self.sensors = None
        self.file_templates = None
        self.verify_group = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PackageSpecList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``package_specs``."""

    _SOAP_TAG = 'package_specs'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.package_spec = []
        self._set_init_values()


class Parameter(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parameter``."""

    _SOAP_TAG = 'parameter'

    def __init__(self, **kwargs):
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
        )
        self.value = None
        self.key = None
        self.type = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ParameterList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parameters``."""

    _SOAP_TAG = 'parameters'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.parameter = []
        self._set_init_values()


class ParseJob(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_job``."""

    _SOAP_TAG = 'parse_job'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'question_text': text_type,
                'parser_version': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.question_text = None
        self.parser_version = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class ParseJobList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_jobs``."""

    _SOAP_TAG = 'parse_jobs'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.parse_job = []
        self._set_init_values()


class ParseResult(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_result``."""

    _SOAP_TAG = 'parse_result'

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
                # no list properties defined in console.wsdl
            },
        )
        self.id = None
        self.parameter_definition = None
        self.parameters = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ParseResultGroup(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_result_group``."""

    _SOAP_TAG = 'parse_result_group'

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
                # no list properties defined in console.wsdl
            },
        )
        self.score = None
        self.question_text = None
        self.parse_results = None
        self.question = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class ParseResultGroupList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_result_groups``."""

    _SOAP_TAG = 'parse_result_groups'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.parse_result_group = []
        self._set_init_values()


class ParseResultList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``parse_results``."""

    _SOAP_TAG = 'parse_results'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.parse_result = []
        self._set_init_values()


class PermissionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``permissions``."""

    _SOAP_TAG = 'permissions'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.permission = []
        self._set_init_values()


class Plugin(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``plugin``."""

    _SOAP_TAG = 'plugin'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'timeout_seconds': int,
                'run_detached_flag': int,
                'name': text_type,
                'status': text_type,
                'input': text_type,
                'local_admin_flag': int,
                'use_json_flag': int,
                'execution_id': int,
                'status_file_content': text_type,
                'allow_rest': int,
                'cache_row_id': int,
                'path': text_type,
                'plugin_server': text_type,
                'raw_http_request': int,
                'exit_code': int,
                'filename': text_type,
                'raw_http_response': int,
                'bundle': text_type,
                'script_response': text_type,
                'plugin_url': text_type,
                'type': text_type,
            },
            complex_properties={
                'arguments': PluginArgumentList,
                'commands': PluginCommandList,
                'sql_response': PluginSql,
                'metadata': MetadataList,
                'permissions': PermissionList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.timeout_seconds = None
        self.run_detached_flag = None
        self.name = None
        self.status = None
        self.input = None
        self.local_admin_flag = None
        self.use_json_flag = None
        self.execution_id = None
        self.status_file_content = None
        self.allow_rest = None
        self.cache_row_id = None
        self.path = None
        self.plugin_server = None
        self.raw_http_request = None
        self.exit_code = None
        self.filename = None
        self.raw_http_response = None
        self.bundle = None
        self.script_response = None
        self.plugin_url = None
        self.type = None
        self.arguments = None
        self.commands = None
        self.sql_response = None
        self.metadata = None
        self.permissions = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PluginArgument(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``argument``."""

    _SOAP_TAG = 'argument'

    def __init__(self, **kwargs):
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
        )
        self.value = None
        self.name = None
        self.type = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class PluginArgumentList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``arguments``."""

    _SOAP_TAG = 'arguments'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.argument = []
        self._set_init_values()


class PluginCommandList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``commands``."""

    _SOAP_TAG = 'commands'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.command = []
        self._set_init_values()


class PluginList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``plugins``."""

    _SOAP_TAG = 'plugins'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.plugin = []
        self._set_init_values()


class PluginSchedule(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``plugin_schedule``."""

    _SOAP_TAG = 'plugin_schedule'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'end_hour': int,
                'id': int,
                'enabled': int,
                'name': text_type,
                'last_exit_code': int,
                'input': text_type,
                'start_date': int,
                'run_on_days': text_type,
                'end_date': int,
                'last_run_text': text_type,
                'last_run_time': text_type,
                'plugin_bundle': text_type,
                'deleted_flag': int,
                'plugin_name': text_type,
                'run_interval_seconds': int,
                'start_hour': int,
                'plugin_server': text_type,
            },
            complex_properties={
                'arguments': PluginArgumentList,
                'user': User,
                'last_run_sql': PluginSql,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.end_hour = None
        self.id = None
        self.enabled = None
        self.name = None
        self.last_exit_code = None
        self.input = None
        self.start_date = None
        self.run_on_days = None
        self.end_date = None
        self.last_run_text = None
        self.last_run_time = None
        self.plugin_bundle = None
        self.deleted_flag = None
        self.plugin_name = None
        self.run_interval_seconds = None
        self.start_hour = None
        self.plugin_server = None
        self.arguments = None
        self.user = None
        self.last_run_sql = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class PluginScheduleList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``plugin_schedules``."""

    _SOAP_TAG = 'plugin_schedules'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.plugin_schedule = []
        self._set_init_values()


class PluginSql(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``sql_response``."""

    _SOAP_TAG = 'sql_response'

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
        self._set_init_values()


class PluginSqlColumn(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``columns``."""

    _SOAP_TAG = 'columns'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.name = []
        self._set_init_values()


class PluginSqlResult(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``result_row``."""

    _SOAP_TAG = 'result_row'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.value = []
        self._set_init_values()


class Question(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``question``."""

    _SOAP_TAG = 'question'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'hidden_flag': int,
                'cache_row_id': int,
                'id': int,
                'index': int,
                'name': text_type,
                'query_text': text_type,
                'action_tracking_flag': int,
                'force_computer_id_flag': int,
                'expire_seconds': int,
                'skip_lock_flag': int,
                'expiration': text_type,
            },
            complex_properties={
                'saved_question': SavedQuestion,
                'selects': SelectList,
                'context_group': Group,
                'management_rights_group': Group,
                'user': User,
                'group': Group,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.hidden_flag = None
        self.cache_row_id = None
        self.id = None
        self.index = None
        self.name = None
        self.query_text = None
        self.action_tracking_flag = None
        self.force_computer_id_flag = None
        self.expire_seconds = None
        self.skip_lock_flag = None
        self.expiration = None
        self.saved_question = None
        self.selects = None
        self.context_group = None
        self.management_rights_group = None
        self.user = None
        self.group = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class QuestionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``questions``."""

    _SOAP_TAG = 'questions'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'cache_info': CacheInfo,
                'info': QuestionListInfo,
            },
            list_properties={
                'question': Question,
            },
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.info = None
        self.question = []
        self._set_init_values()


class QuestionListInfo(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``info``."""

    _SOAP_TAG = 'info'

    def __init__(self, **kwargs):
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
        )
        self.highest_id = None
        self.total_count = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedAction(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_action``."""

    _SOAP_TAG = 'saved_action'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'cache_row_id': int,
                'id': int,
                'name': text_type,
                'status': int,
                'comment': text_type,
                'public_flag': int,
                'last_start_time': text_type,
                'policy_flag': int,
                'user_start_time': text_type,
                'action_group_id': int,
                'creation_time': text_type,
                'issue_seconds': int,
                'issue_count': int,
                'start_time': text_type,
                'next_start_time': text_type,
                'approved_flag': int,
                'end_time': text_type,
                'expire_seconds': int,
                'distribute_seconds': int,
            },
            complex_properties={
                'last_action': Action,
                'action_group': Group,
                'package_spec': PackageSpec,
                'target_group': Group,
                'row_ids': SavedActionRowIdList,
                'user': User,
                'policy': SavedActionPolicy,
                'metadata': MetadataList,
                'approver': User,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.cache_row_id = None
        self.id = None
        self.name = None
        self.status = None
        self.comment = None
        self.public_flag = None
        self.last_start_time = None
        self.policy_flag = None
        self.user_start_time = None
        self.action_group_id = None
        self.creation_time = None
        self.issue_seconds = None
        self.issue_count = None
        self.start_time = None
        self.next_start_time = None
        self.approved_flag = None
        self.end_time = None
        self.expire_seconds = None
        self.distribute_seconds = None
        self.last_action = None
        self.action_group = None
        self.package_spec = None
        self.target_group = None
        self.row_ids = None
        self.user = None
        self.policy = None
        self.metadata = None
        self.approver = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedActionApproval(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_action_approval``."""

    _SOAP_TAG = 'saved_action_approval'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'approved_flag': int,
                'name': text_type,
            },
            complex_properties={
                'metadata': MetadataList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.id = None
        self.approved_flag = None
        self.name = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedActionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_actions``."""

    _SOAP_TAG = 'saved_actions'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.saved_action = []
        self._set_init_values()


class SavedActionPolicy(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``policy``."""

    _SOAP_TAG = 'policy'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'max_age': int,
                'min_count': int,
                'row_filter_group_id': int,
                'saved_question_group_id': int,
                'saved_question_id': int,
            },
            complex_properties={
                'row_filter_group': Group,
                'saved_question_group': Group,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.max_age = None
        self.min_count = None
        self.row_filter_group_id = None
        self.saved_question_group_id = None
        self.saved_question_id = None
        self.row_filter_group = None
        self.saved_question_group = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedActionRowIdList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``row_ids``."""

    _SOAP_TAG = 'row_ids'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.row_id = []
        self._set_init_values()


class SavedQuestion(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_question``."""

    _SOAP_TAG = 'saved_question'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'cache_row_id': int,
                'id': int,
                'keep_seconds': int,
                'name': text_type,
                'query_text': text_type,
                'index': int,
                'most_recent_question_id': int,
                'action_tracking_flag': int,
                'public_flag': int,
                'hidden_flag': int,
                'expire_seconds': int,
                'sort_column': int,
                'issue_seconds': int,
                'issue_seconds_never_flag': int,
                'row_count_flag': int,
                'mod_time': text_type,
                'archive_enabled_flag': int,
            },
            complex_properties={
                'mod_user': User,
                'archive_owner': User,
                'question': Question,
                'user': User,
                'packages': PackageSpecList,
                'metadata': MetadataList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.cache_row_id = None
        self.id = None
        self.keep_seconds = None
        self.name = None
        self.query_text = None
        self.index = None
        self.most_recent_question_id = None
        self.action_tracking_flag = None
        self.public_flag = None
        self.hidden_flag = None
        self.expire_seconds = None
        self.sort_column = None
        self.issue_seconds = None
        self.issue_seconds_never_flag = None
        self.row_count_flag = None
        self.mod_time = None
        self.archive_enabled_flag = None
        self.mod_user = None
        self.archive_owner = None
        self.question = None
        self.user = None
        self.packages = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SavedQuestionList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``saved_questions``."""

    _SOAP_TAG = 'saved_questions'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.saved_question = []
        self._set_init_values()


class Select(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``select``."""

    _SOAP_TAG = 'select'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                # no simple properties defined in console.wsdl
            },
            complex_properties={
                'filter': Filter,
                'sensor': Sensor,
                'group': Group,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        # no simple properties defined in console.wsdl
        self.filter = None
        self.sensor = None
        self.group = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SelectList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``selects``."""

    _SOAP_TAG = 'selects'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.select = []
        self._set_init_values()


class Sensor(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``sensor``."""

    _SOAP_TAG = 'sensor'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'hidden_flag': int,
                'id': int,
                'source_hash': int,
                'name': text_type,
                'value_type': text_type,
                'description': text_type,
                'parameter_definition': text_type,
                'source_id': int,
                'max_age_seconds': int,
                'hash': int,
                'preview_sensor_flag': int,
                'cache_row_id': int,
                'category': text_type,
                'creation_time': text_type,
                'modification_time': text_type,
                'string_count': int,
                'exclude_from_parse_flag': int,
                'deleted_flag': int,
                'ignore_case_flag': int,
                'last_modified_by': text_type,
                'delimiter': text_type,
            },
            complex_properties={
                'parameters': ParameterList,
                'string_hints': StringHintList,
                'queries': SensorQueryList,
                'subcolumns': SensorSubcolumnList,
                'metadata': MetadataList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.hidden_flag = None
        self.id = None
        self.source_hash = None
        self.name = None
        self.value_type = None
        self.description = None
        self.parameter_definition = None
        self.source_id = None
        self.max_age_seconds = None
        self.hash = None
        self.preview_sensor_flag = None
        self.cache_row_id = None
        self.category = None
        self.creation_time = None
        self.modification_time = None
        self.string_count = None
        self.exclude_from_parse_flag = None
        self.deleted_flag = None
        self.ignore_case_flag = None
        self.last_modified_by = None
        self.delimiter = None
        self.parameters = None
        self.string_hints = None
        self.queries = None
        self.subcolumns = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SensorList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``sensors``."""

    _SOAP_TAG = 'sensors'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.sensor = []
        self._set_init_values()


class SensorQuery(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``query``."""

    _SOAP_TAG = 'query'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'signature': text_type,
                'platform': text_type,
                'script_type': text_type,
                'script': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.signature = None
        self.platform = None
        self.script_type = None
        self.script = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class SensorQueryList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``queries``."""

    _SOAP_TAG = 'queries'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.query = []
        self._set_init_values()


class SensorSubcolumn(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``subcolumn``."""

    _SOAP_TAG = 'subcolumn'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'hidden_flag': int,
                'name': text_type,
                'value_type': text_type,
                'exclude_from_parse_flag': int,
                'index': int,
                'ignore_case_flag': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.hidden_flag = None
        self.name = None
        self.value_type = None
        self.exclude_from_parse_flag = None
        self.index = None
        self.ignore_case_flag = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class SensorSubcolumnList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``subcolumns``."""

    _SOAP_TAG = 'subcolumns'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.subcolumn = []
        self._set_init_values()


class SoapError(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``soap_error``."""

    _SOAP_TAG = 'soap_error'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'exception_name': text_type,
                'context': text_type,
                'object_request': text_type,
                'object_name': text_type,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.exception_name = None
        self.context = None
        self.object_request = None
        self.object_name = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class StringHintList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``string_hints``."""

    _SOAP_TAG = 'string_hints'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.string_hint = []
        self._set_init_values()


class SystemSetting(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``system_setting``."""

    _SOAP_TAG = 'system_setting'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'hidden_flag': int,
                'read_only_flag': int,
                'id': int,
                'name': text_type,
                'value_type': text_type,
                'default_value': text_type,
                'setting_type': text_type,
                'value': text_type,
                'cache_row_id': int,
            },
            complex_properties={
                'metadata': MetadataList,
                'audit_data': AuditData,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.hidden_flag = None
        self.read_only_flag = None
        self.id = None
        self.name = None
        self.value_type = None
        self.default_value = None
        self.setting_type = None
        self.value = None
        self.cache_row_id = None
        self.metadata = None
        self.audit_data = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SystemSettingList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``system_settings``."""

    _SOAP_TAG = 'system_settings'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.cache_info = None
        self.system_setting = []
        self._set_init_values()


class SystemStatusAggregate(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``aggregate``."""

    _SOAP_TAG = 'aggregate'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'send_none_count': int,
                'send_ok_count': int,
                'receive_backward_count': int,
                'normal_count': int,
                'slowlink_count': int,
                'receive_none_count': int,
                'receive_ok_count': int,
                'send_backward_count': int,
                'receive_forward_count': int,
                'blocked_count': int,
                'leader_count': int,
                'send_forward_count': int,
            },
            complex_properties={
                'versions': VersionAggregateList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.send_none_count = None
        self.send_ok_count = None
        self.receive_backward_count = None
        self.normal_count = None
        self.slowlink_count = None
        self.receive_none_count = None
        self.receive_ok_count = None
        self.send_backward_count = None
        self.receive_forward_count = None
        self.blocked_count = None
        self.leader_count = None
        self.send_forward_count = None
        self.versions = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class SystemStatusList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``system_status``."""

    _SOAP_TAG = 'system_status'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        self.aggregate = None
        self.cache_info = None
        self.client_status = []
        self._set_init_values()


class UploadFile(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``upload_file``."""

    _SOAP_TAG = 'upload_file'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'bytes': text_type,
                'id': int,
                'destination_file': text_type,
                'key': text_type,
                'file_size': int,
                'force_overwrite': int,
                'part_size': int,
                'start_pos': int,
                'file_cached': int,
                'hash': text_type,
                'percent_complete': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.bytes = None
        self.id = None
        self.destination_file = None
        self.key = None
        self.file_size = None
        self.force_overwrite = None
        self.part_size = None
        self.start_pos = None
        self.file_cached = None
        self.hash = None
        self.percent_complete = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class UploadFileList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``file_parts``."""

    _SOAP_TAG = 'file_parts'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.upload_file = []
        self._set_init_values()


class UploadFileStatus(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``upload_file_status``."""

    _SOAP_TAG = 'upload_file_status'

    def __init__(self, **kwargs):
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
        )
        self.file_cached = None
        self.hash = None
        self.percent_complete = None
        self.file_parts = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class User(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``user``."""

    _SOAP_TAG = 'user'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'domain': text_type,
                'name': text_type,
                'active_session_count': int,
                'last_login': text_type,
                'local_admin_flag': int,
                'group_id': int,
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
        )
        self.id = None
        self.domain = None
        self.name = None
        self.active_session_count = None
        self.last_login = None
        self.local_admin_flag = None
        self.group_id = None
        self.deleted_flag = None
        self.permissions = None
        self.roles = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class UserList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``users``."""

    _SOAP_TAG = 'users'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.user = []
        self._set_init_values()


class UserRole(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``role``."""

    _SOAP_TAG = 'role'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'description': text_type,
                'id': int,
                'name': text_type,
            },
            complex_properties={
                'permissions': PermissionList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.description = None
        self.id = None
        self.name = None
        self.permissions = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class UserRoleList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``roles``."""

    _SOAP_TAG = 'roles'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.role = []
        self._set_init_values()


class VersionAggregate(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``version``."""

    _SOAP_TAG = 'version'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'filtered': int,
                'version_string': text_type,
                'count': int,
            },
            complex_properties={
                # no complex properties defined in console.wsdl
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.filtered = None
        self.version_string = None
        self.count = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()


class VersionAggregateList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``versions``."""

    _SOAP_TAG = 'versions'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.version = []
        self._set_init_values()


class WhiteListedUrl(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``white_listed_url``."""

    _SOAP_TAG = 'white_listed_url'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'chunk_id': text_type,
                'id': int,
                'download_seconds': int,
                'url_regex': text_type,
            },
            complex_properties={
                'metadata': MetadataList,
            },
            list_properties={
                # no list properties defined in console.wsdl
            },
        )
        self.chunk_id = None
        self.id = None
        self.download_seconds = None
        self.url_regex = None
        self.metadata = None
        # no list properties defined in console.wsdl
        self._set_init_values()


class WhiteListedUrlList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``white_listed_urls``."""

    _SOAP_TAG = 'white_listed_urls'

    def __init__(self, **kwargs):
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
        )
        # no simple properties defined in console.wsdl
        # no complex properties defined in console.wsdl
        self.white_listed_url = []
        self._set_init_values()


class XmlError(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``error``."""

    _SOAP_TAG = 'error'

    def __init__(self, **kwargs):
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
        )
        self.error_context = None
        self.exception = None
        self.type = None
        # no complex properties defined in console.wsdl
        # no list properties defined in console.wsdl
        self._set_init_values()

BASE_TYPES = {}
"""Maps Tanium XML soap tags to the Tanium NG Python BaseType object"""
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
