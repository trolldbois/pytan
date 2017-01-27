'''A python package that handles the serialization/deserialization of XML SOAP
requests/responses from Tanium to/from python objects.
'''
import base64
import imghdr
import io
import json
import struct

from .object_types.all_objects import *  # noqa
from .object_types.base import BaseType  # noqa
from .object_types.result_set import ResultSet  # noqa
from .object_types.result_info import ResultInfo  # noqa


def test_jpeg(h, f):
    # SOI APP2 + ICC_PROFILE
    if h[0:4] == "\xff\xd8\xff\xe2" and h[6:17] == b"ICC_PROFILE":
        print "A"
        return "jpeg"
    # SOI APP14 + Adobe
    if h[0:4] == "\xff\xd8\xff\xee" and h[6:11] == b"Adobe":
        return "jpeg"
    # SOI DQT
    if h[0:4] == "\xff\xd8\xff\xdb":
        return "jpeg"


imghdr.tests.append(test_jpeg)


def get_image_size(image_stream):
    what = imghdr.what(None, image_stream) or "Unknown"
    width, height = (None, None)

    if what == "png":
        check = struct.unpack(">i", image_stream[4:8])[0]
        if check == 0x0d0a1a0a:
            width, height = struct.unpack(">ii", image_stream[16:24])
    elif what == "gif":
        width, height = struct.unpack("<HH", image_stream[6:10])
    elif what == "jpeg":
        iohandle = io.BytesIO(image_stream)

        try:
            iohandle.seek(0)  # Read 0xff next
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf or ftype in (0xc4, 0xc8, 0xcc):
                iohandle.seek(size, 1)
                byte = iohandle.read(1)
                while ord(byte) == 0xff:
                    byte = iohandle.read(1)
                ftype = ord(byte)
                size = struct.unpack(">H", iohandle.read(2))[0] - 2
            # We are at a SOFn block
            iohandle.seek(1, 1)  # Skip `precision` byte.
            height, width = struct.unpack('>HH', iohandle.read(4))
        except Exception:  # IGNORE:W0703
            pass
    return what, width, height


# TODO
class WrapType(object):

    _GET_METHOD = ""
    _CREATE_METHOD = ""
    _DELETE_METHOD = ""

    def __init__(self, **kwargs):
        self._FIRSTS = ["name", "id"]
        self._CHANGED = False
        self._ADDED = False
        self._LIST_OBJ = []
        self._KWARGS = kwargs
        self.setattrs(**kwargs)

    @property
    def _name(self):
        ret = self.__class__.__name__
        return ret

    def setattrs(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def _attrs(self):
        ret = [k for k in self._FIRSTS if k in self.__dict__]
        ret = ret + [k for k in self.__dict__ if k not in ret and not k.startswith("_")]
        return ret

    def _get(self, o, k):
        return getattr(o, k, None)

    def __eq__(self, other):
        # this is simple and problematic but should work for most base types
        # used for: obj in objlist, obj == obj

        this_json = self.str_obj(obj=self, str_json=True)
        other_json = self.str_obj(obj=other, str_json=True)

        ret = this_json == other_json
        return ret

    def __str__(self):
        attr_vals = ["{k}: '{v}'".format(k=k, v=self._get(self, k)) for k in self._attrs]
        attrs_text = ", ".join(attr_vals)
        ret = "{c}: {a}"
        ret = ret.format(c=self._name, a=attrs_text)
        return ret

    def __repr__(self):
        return self.__str__()

    def is_bt(self, o):
        return isinstance(o, BaseType)

    def is_wt(self, o):
        return isinstance(o, (WrapType, WrapTypeList))

    def str_obj(self, **str_config):
        obj = str_config.get("obj", self)
        str_json = str_config.get("str_json", False)

        if self.is_bt(obj):
            ret = obj.jsonify() if str_json else obj.__str__(**str_config)
        elif self.is_wt(obj):
            ret = obj.jsonify() if str_json else str(obj)
        else:
            try:
                ret = json.dumps(obj, skipkeys=True, sort_keys=True, indent=2) if str_json else str(obj)
            except:
                ret = str(obj)
        return ret

    def jsonify(self, **kwargs):
        obj = kwargs.get("obj", self)
        ret = obj.to_json(obj=obj)
        return ret

    def to_json(self, **kwargs):
        obj = kwargs.get("obj", self)
        jsonable = obj.to_jsonable()
        ret = json.dumps(jsonable, skipkeys=True, sort_keys=True, indent=2)
        return ret

    def to_jsonable(self, **kwargs):
        ret = {k: self._get(self, k) for k in self._attrs}
        for k, v in ret.items():
            if self.is_bt(v) or self.is_wt(v):
                ret[k] = v.to_jsonable()
        ret["_WRAP_TYPE"] = self._name
        return ret

    @property
    def _get_tracker(self):
        if not hasattr(self, "_TRACKER"):
            self._TRACKER = []
        return self._TRACKER

    def _track(self, t_attr="", t_old="", t_new="", t_action="Updated", **kwargs):
        track = {}
        track["action"] = t_action
        track["attr"] = t_attr
        track["obj"] = str(self)

        margs = {}
        margs.update(kwargs)
        margs.update(obj=t_old)
        track["old"] = self.str_obj(**margs)

        margs.update(obj=t_new)
        track["new"] = self.str_obj(**margs)
        self._get_tracker.append(track)
        return self

    def _track_merge(self, other, **kwargs):
        other_first = kwargs.get("other_first", False)

        this_t = self._get_tracker
        other_t = other._get_tracker
        self._TRACKER = other_t + this_t if other_first else this_t + other_t
        return self._get_tracker

    def _track_set(self, t_attr, t_new, t_action="Updated", **kwargs):
        t_old = getattr(self, t_attr, "")
        margs = {}
        margs.update(kwargs)
        margs.update(t_attr=t_attr, t_old=t_old, t_new=t_new, t_action=t_action)
        self._track(**margs)
        setattr(self, t_attr, t_new)
        self._CHANGED = True
        return self

    def _add_list_item(self, item, list_obj):
        if item in list_obj:
            self._track(t_action="Already exists, did not add list item [{o}] to".format(o=item))
        else:
            self._CHANGED = True
            self._track(t_action="Added list item [{o}] to".format(o=item))
            list_obj.append(item)
        return list_obj

    def _remove_list_item(self, item, list_obj):
        if item in list_obj:
            self._CHANGED = True
            self._track(t_action="Removed list item [{o}] from".format(o=item))
            list_obj.remove(item)
        else:
            self._track(t_action="Does not exist, did not remove list item [{o}] from".format(o=item))
        return list_obj

    def _add_list_items(self, items, list_obj):
        for item in items:
            list_obj = self._add_list_item(item=item, list_obj=list_obj)
        return list_obj

    def _remove_list_items(self, items, list_obj):
        for item in list(items):
            list_obj = self._remove_list_item(item=item, list_obj=list_obj)
        return list_obj

    def _remove_all_list_items(self, list_obj):
        list_obj = self._remove_list_items(list_obj, list_obj)
        return list_obj

    def _set_list_items(self, items, list_obj):
        list_obj = self._remove_all_list_items(list_obj=list_obj)
        list_obj = self._add_list_items(items=items, list_obj=list_obj)
        return list_obj

    def _list_to_xml(self, tag, item_attr, list_obj):
        x_tmpl = "<{t}><{a}>{v}</{a}></{t}>".format
        items = sorted([x_tmpl(v=getattr(o, item_attr, None), t=tag, a=item_attr) for o in list_obj])
        items_txt = "\n  {i}\n".format(i="\n  ".join(items)) if items else ""
        ret = "<{t}s>{i}</{t}s>".format(i=items_txt, t=tag)
        return ret

    def _list_to_str(self, list_obj):
        items = sorted([str(x) for x in list_obj])
        ret = "\n  {}".format("\n  ".join(items)) if items else "No items!"
        return ret


class WrapTypeList(WrapType):

    # attribute used to search thru list items when doing obj['x']
    _PRIMARY_ATTR = "name"

    def __str__(self):
        attr_vals = ["{k}: '{v}'".format(k=k, v=self._get(self, k)) for k in self._attrs]
        attrs_text = ", ".join(attr_vals)
        sep = ", " if attr_vals else ""
        ret = "{c} {a}{s}Length: {n}"
        ret = ret.format(c=self._name, n=len(self), a=attrs_text, s=sep)
        return ret

    def __getitem__(self, n):
        if isinstance(n, int):
            ret = getattr(self, "_LIST_OBJ")[n]
        else:
            pri_values = []
            ret = []
            for item in getattr(self, "_LIST_OBJ"):
                if not hasattr(item, self._PRIMARY_ATTR):
                    continue
                pri_value = str(getattr(item, self._PRIMARY_ATTR))
                pri_values.append(pri_value)
                if pri_value == n:
                    ret.append(item)

            if len(ret) == 0:
                m = "No items found in {o} where primary attribute '{p}' == '{n}', valid items: {pv}"
                m = m.format(o=self, p=self._PRIMARY_ATTR, n=n, pv=pri_values)
                raise Exception(m)
            elif len(ret) > 1:
                m = "More than one items found in {o} where primary attribute '{p}' == '{n}', found items: {r}"
                m = m.format(o=self, p=self._PRIMARY_ATTR, n=n, r=ret)
                raise Exception(m)
            else:
                ret = ret[0]
        return ret

    def __len__(self):
        return len(self._LIST_OBJ)

    def append(self, value):
        return self._LIST_OBJ.append(value)

    def remove(self, value):
        return self._LIST_OBJ.remove(value)

    def to_jsonable(self, **kwargs):
        ret = super(WrapTypeList, self).to_jsonable(**kwargs)
        ret["list"] = [x.to_jsonable(**kwargs) for x in self._LIST_OBJ]
        return ret


class UserGroup(WrapType):

    # name (str)
    # id (intt)
    # users (basetype obj) => UserList

    _GET_METHOD = "get_user_groups"
    _CREATE_METHOD = "create_user_group"
    _DELETE_METHOD = "delete_user_group"

    def _ensure_users(self):
        attr = "users"
        val = getattr(self, attr, None)
        setattr(self, attr, UserList() if val is None else val)

    def add_user(self, item):
        self._ensure_users()
        return self._add_list_item(item=item, list_obj=self.users)

    def add_users(self, items):
        self._ensure_users()
        return self._add_list_items(items=items, list_obj=self.users)

    def remove_user(self, item):
        self._ensure_users()
        return self._remove_list_item(item=item, list_obj=self.users)

    def remove_users(self, items):
        self._ensure_users()
        return self._remove_list_items(items=items, list_obj=self.users)

    def remove_all_users(self):
        self._ensure_users()
        return self._remove_all_list_items(list_obj=self.users)

    def set_users(self, items):
        self._ensure_users()
        return self._set_list_items(items=items, list_obj=self.users)

    def users_xml(self):
        self._ensure_users()
        return self._list_to_xml(tag="user", item_attr="id", list_obj=self.users)

    def users_str(self):
        self._ensure_users()
        return self._list_to_str(list_obj=self.users)


class UserGroupList(WrapTypeList):

    # _LIST_OBJ (list of wraptype obj) => [UserGroup]

    _GET_METHOD = "get_user_groups"
    _CREATE_METHOD = "create_user_group"
    _DELETE_METHOD = "delete_user_group"

    def add_user(self, item):
        for obj in self._LIST_OBJ:
            obj.add_user(item)
            self._track_merge(other=obj)
        self._CHANGED = any([x._CHANGED for x in self]) or self._CHANGED

    def add_users(self, items):
        for item in items:
            self.add_user(item)

    def remove_user(self, item):
        for obj in self._LIST_OBJ:
            obj.remove_user(item)
            self._track_merge(other=obj)
        self._CHANGED = any([x._CHANGED for x in self]) or self._CHANGED

    def remove_users(self, items):
        for item in items:
            self.remove_user(item)

    def user_groups_xml(self):
        return self._list_to_xml(tag="user_group", item_attr="id", list_obj=self._LIST_OBJ)


class ActionGroup(WrapType):

    # computer_group (basetype obj) => Group
    # user_groups (list of wraptype obj) => [UserGroupList]
    # name (str)
    # id (int)
    # public_flag (int)
    # and_flag (int)

    _GET_METHOD = "get_action_groups"
    _CREATE_METHOD = "create_action_group"
    _DELETE_METHOD = "delete_action_group"

    def _ensure_computer_group(self):
        attr = "computer_group"
        val = getattr(self, attr, None)
        setattr(self, attr, Group() if val is None else val)
        self.computer_group.name = getattr(self, "name", "Unavailable")
        self.computer_group.id = getattr(self, "id", "Unavailable")
        attr = "sub_groups"
        val = getattr(self.computer_group, attr, None)
        setattr(self.computer_group, attr, GroupList() if val is None else val)

    def _ensure_user_groups(self):
        attr = "user_groups"
        val = getattr(self, attr, None)
        setattr(self, attr, UserGroupList() if val is None else val)

    def add_computer_group(self, item):
        self._ensure_computer_group()
        return self._add_list_item(item=item, list_obj=self.computer_group.sub_groups)

    def add_computer_groups(self, items):
        self._ensure_computer_group()
        return self._add_list_items(items=items, list_obj=self.computer_group.sub_groups)

    def remove_computer_group(self, item):
        self._ensure_computer_group()
        return self._remove_list_item(item=item, list_obj=self.computer_group.sub_groups)

    def remove_computer_groups(self, items):
        self._ensure_computer_group()
        return self._remove_list_items(items=items, list_obj=self.computer_group.sub_groups)

    def remove_all_computer_groups(self):
        self._ensure_computer_group()
        return self._remove_all_list_items(list_obj=self.computer_group.sub_groups)

    def set_computer_groups(self, items):
        self._ensure_computer_group()
        return self._set_list_items(items=items, list_obj=self.computer_group.sub_groups)

    def computer_groups_str(self):
        self._ensure_computer_group()
        return self._list_to_str(list_obj=self.computer_group.sub_groups)

    def add_user_group(self, item):
        self._ensure_user_groups()
        return self._add_list_item(item=item, list_obj=self.user_groups)

    def add_user_groups(self, items):
        self._ensure_user_groups()
        return self._add_list_items(items=items, list_obj=self.user_groups)

    def remove_user_group(self, item):
        self._ensure_user_groups()
        return self._remove_list_item(item=item, list_obj=self.user_groups)

    def remove_user_groups(self, items):
        self._ensure_user_groups()
        return self._remove_list_items(items=items, list_obj=self.user_groups)

    def remove_all_user_groups(self):
        self._ensure_user_groups()
        return self._remove_all_list_items(list_obj=self.user_groups)

    def set_user_groups(self, items):
        self._ensure_user_groups()
        return self._set_list_items(items=items, list_obj=self.user_groups)

    def user_groups_str(self):
        self._ensure_user_groups()
        return self._list_to_str(list_obj=self.user_groups)

    def user_groups_xml(self):
        self._ensure_user_groups()
        return self.user_groups.user_groups_xml()


class ActionGroupList(WrapTypeList):

    # _LIST_OBJ (list of wraptype obj) => [ActionGroup]

    _GET_METHOD = "get_action_groups"
    _CREATE_METHOD = "create_action_group"
    _DELETE_METHOD = "delete_action_group"


class Dashboard(WrapType):

    # id (int)
    # name (str)
    # public_flag (int)
    # text (str)
    # user (basetype obj) => User
    # computer_group (basetype obj) => Group
    # saved_questions (basetype obj) => SavedQuestionList

    _GET_METHOD = "get_dashboards"
    _CREATE_METHOD = "create_dashboard"
    _DELETE_METHOD = "delete_dashboard"

    def _ensure_saved_questions(self):
        attr = "saved_questions"
        val = getattr(self, attr, None)
        setattr(self, attr, SavedQuestionList() if val is None else val)

    def add_saved_question(self, item):
        self._ensure_saved_questions()
        return self._add_list_item(item=item, list_obj=self.saved_questions)

    def add_saved_questions(self, items):
        self._ensure_saved_questions()
        return self._add_list_items(items=items, list_obj=self.saved_questions)

    def remove_saved_question(self, item):
        self._ensure_saved_questions()
        return self._remove_list_item(item=item, list_obj=self.saved_questions)

    def remove_saved_questions(self, items):
        self._ensure_saved_questions()
        return self._remove_list_items(items=items, list_obj=self.saved_questions)

    def remove_all_saved_questions(self):
        self._ensure_saved_questions()
        return self._remove_all_list_items(list_obj=self.saved_questions)

    def set_saved_questions(self, items):
        self._ensure_saved_questions()
        return self._set_list_items(items=items, list_obj=self.saved_questions)

    def saved_questions_str(self):
        self._ensure_saved_questions()
        return self._list_to_str(list_obj=self.saved_questions)

    def saved_questions_xml(self):
        self._ensure_saved_questions()
        x_tmpl = "<sq><id>{v}</id><index>{i}</index></sq>".format
        items = [x_tmpl(v=getattr(o, "id"), i=idx) for idx, o in enumerate(self.saved_questions)]
        items_txt = "\n  {i}\n".format(i="\n  ".join(items)) if items else ""
        ret = "<dash_sqs>{i}</dash_sqs>".format(i=items_txt)
        return ret


class DashboardList(WrapTypeList):

    # _LIST_OBJ (list of wraptype obj) => [Dashboard]

    _GET_METHOD = "get_dashboards"
    _CREATE_METHOD = "create_dashboard"
    _DELETE_METHOD = "delete_dashboard"


class Image(object):

    def __init__(self, image, **kwargs):
        is_file = kwargs.get("is_file", False)

        self.original_image = image
        self.image = image or ""
        self.image = open(self.image, 'rb').read() if is_file else self.image
        self.image = self.decode if self.is_base64(self.image) else self.image

    def __str__(self):
        self.info
        m = "Image Type: {}, Size: {} bytes, Width: {}, Height: {}"
        m = m.format(self.what, len(self.image), self.width, self.height)
        return m

    def __repr__(self):
        return self.__str__()

    def is_base64(self, txt):
        try:
            a = base64.b64decode(txt)
            b = base64.b64encode(a)
        except:
            ret = False
        else:
            ret = b.strip() == txt.strip()
        return ret

    @property
    def info(self):
        if self.image:
            self.what, self.width, self.height = get_image_size(self.image)
        else:
            self.what, self.width, self.height = (None, None, None)
        return self.what, self.width, self.height

    @property
    def encode(self):
        return base64.b64encode(self.image)

    @property
    def decode(self):
        return base64.b64decode(self.image)


class DashboardCategory(WrapType):

    # name (str)
    # public_flag (int)
    # editable_flag (int)
    # text (str)
    # other_flag (int)
    # icon (obj) => Image
    # user (basetype obj) => User
    # user_groups (wraptype obj) => UserGroupList
    # dashboards (wraptype obj) => DashboardList

    _GET_METHOD = "get_dashboard_categories"
    _CREATE_METHOD = "create_dashboard_category"
    _DELETE_METHOD = "delete_dashboard_category"


class DashboardCategoryList(WrapTypeList):

    # _LIST_OBJ (list of wraptype obj) => [DashboardCategory]

    _GET_METHOD = "get_dashboard_categories"
    _CREATE_METHOD = "create_dashboard_category"
    _DELETE_METHOD = "delete_dashboard_category"
