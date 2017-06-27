"""Parse METADATA from a given source against a metadata structure."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import os
import pprint
import sys

THIS_FILE = os.path.abspath(__file__)
THIS_SCRIPT = os.path.basename(THIS_FILE)
THIS_PATH = os.path.dirname(THIS_FILE)
TOOL_PATH = os.path.dirname(THIS_PATH)

if THIS_PATH not in sys.path:
    sys.path.append(THIS_PATH)

IS_PY2 = sys.version_info[0] == 2
UNI_TYPE = unicode if IS_PY2 else str # noqa
STR_TYPES = (str, UNI_TYPE) if IS_PY2 else (str,)
DICT_TYPES = (dict,)
LIST_TYPES = (list, tuple)
BOOL_TYPES = (bool,)
INT_TYPES = (int)


def check_type(o, t):
    """Validate object o is of type t."""
    if not isinstance(o, t):
        m = "Object type is '{}', must be of type {}, full object: {}".format
        raise Exception(m(type(o).__name__, t, pprint.pformat(o)))


def check_key(o, k, t=None):
    """Validate o is a dict and has key k and value of k is of type t."""
    check_type(o, DICT_TYPES)

    if k not in o:
        m = "No key '{}' defined in full object: {}".format
        raise Exception(m(k, pprint.pformat(o)))

    if t is not None and not isinstance(o[k], t):
        m = "Has key '{}' of type '{}', must be of type {}, full object: {}".format
        raise Exception(m(k, type(o[k]).__name__, t, pprint.pformat(o)))


def check_eval_type(o, k):
    """Validate dict o key k can be evaluated as a python type."""
    type_map = {
        "str": STR_TYPES,
        "dict": DICT_TYPES,
        "bool": BOOL_TYPES,
        "list": LIST_TYPES,
        "int": INT_TYPES,
    }
    if o[k] in type_map:
        ret = type_map[o[k]]
    else:
        m = "Unable to evalute key {} value '{}' must be one of: {}, full object: {}".format
        raise Exception(m(k, o[k], type_map.keys(), pprint.pformat(o)))
    return ret


class MetaDataParser(object):
    """Parse METADATA from a given source against a metadata structure."""

    def __init__(self, structure):
        """Constructor."""
        self.LOG = logging.getLogger("MDParser")
        self.check_structure(structure)
        self.structure = structure

    def check_structure(self, structure):
        """Validate structure definition."""
        check_type(structure, LIST_TYPES)
        for item in structure:
            self.check_structure_item(item)

    def check_structure_item(self, item):
        """Validate structure item definition."""
        check_key(item, "KEY", STR_TYPES)
        check_key(item, "TYPE", STR_TYPES)
        check_key(item, "HELP", STR_TYPES)
        check_key(item, "REQUIRED", BOOL_TYPES)
        item["TYPE_EVAL"] = check_eval_type(item, "TYPE")
        if item["TYPE"] == "list":
            check_key(item, "ITEM_TYPE", STR_TYPES)
            item["ITEM_TYPE_EVAL"] = check_eval_type(item, "ITEM_TYPE")
            if item["ITEM_TYPE"] == "dict":
                check_key(item, "ITEM_STRUCTURE", LIST_TYPES)
                self.check_structure(structure=item["ITEM_STRUCTURE"])

    def from_json_file(self, json_path):
        """Load metadata from json_path and parse."""
        json_str = self.load_json_path(json_path=json_path)
        ret = self.load_json_str(json_str=json_str)

        m = "Loaded Metadata JSON path: '{}'".format
        self.LOG.info(m(json_path))

        self.parse_md(md=ret, structure=self.structure)

        ret["JSON_PATH"] = json_path
        ret["JSON_NAME"] = os.path.basename(json_path)
        ret["JSON_DIR"] = os.path.dirname(json_path)
        return ret

    def load_json_path(self, json_path):
        """Load a json file."""
        if not os.path.isfile(json_path):
            m = "Metadata JSON path '{}' not found!".format
            raise Exception(m(json_path))

        with open(json_path) as fh:
            ret = fh.read()
        return ret

    def load_json_str(self, json_str):
        """Parse json_str into a python object."""
        try:
            ret = json.loads(json_str)
        except Exception as e:
            m = "Unable to load Metadata JSON: '{}', error: {}".format
            raise Exception(m(json_str, e))
        return ret

    def parse_md(self, md, structure, parent="root"):
        """Validate metadata is a dict and parse using structure."""
        check_type(md, DICT_TYPES)
        for item in structure:
            self.parse_md_item(md=md, item=item, parent=parent)

    def parse_md_item(self, md, item, parent):
        """Validate md against structure item."""
        key = item["KEY"]
        item_type = item["TYPE"]
        type_eval = item["TYPE_EVAL"]
        default = item.get("DEFAULT", None)
        required = item["REQUIRED"]
        values = item.get("VALUES", [])
        deps = item.get("DEPS", {})
        value = default

        dep_match = [md.get(k, None) in v for k, v in deps.items()]
        if not all(dep_match):
            return

        if key in md:
            value = md[key]
            m = "Metadata key '{}' under '{}' has value '{}'".format
            self.LOG.debug(m(key, parent, value))
            if not isinstance(value, type_eval):
                m = "Metadata key '{}' value {!r} under '{}' is type '{}', must be one of types: {}".format
                raise Exception(m(key, value, parent, type(value).__name__, type_eval))
            if values and value not in values:
                m = "Metadata key '{}' value {!r} under '{}' is invalid, must be one : {}".format
                raise Exception(m(key, value, parent, values))
        elif required:
            m = "Metadata missing required key '{}' under '{}', structure:\n{}".format
            raise Exception(m(key, parent, pprint.pformat(item)))
        elif default is not None:
            md[key] = default
            m = "Metadata key '{}' under '{}' not supplied, using default value '{}'".format
            self.LOG.debug(m(key, parent, value))

        if item_type == "list" and value:
            sub_type = item["ITEM_TYPE"]
            sub_type_eval = item["ITEM_TYPE_EVAL"]
            sub_structure = item.get("ITEM_STRUCTURE", {})
            for idx, sub_md in enumerate(value):
                sub_parent = "{} #{}".format(key, idx + 1)
                if not isinstance(sub_md, sub_type_eval):
                    m = "Metadata subitem in key '{}' under '{}' is type '{}', must be one of types: {}".format
                    raise Exception(m(key, sub_parent, type(sub_md).__name__, sub_type_eval))
                if sub_type == "dict":
                    self.parse_md(md=sub_md, structure=sub_structure, parent=sub_parent)


if __name__ == "__main__":
    import log_help
    import md_structure
    log = log_help.setup_logging()
    z = MetaDataParser(structure=md_structure.md_structure)
    f = "/Users/jim.olsen/Desktop/projects/tdc/client/METADATA_NIX.json"
    md = z.from_json_file(f)
    pprint.pprint(md)
