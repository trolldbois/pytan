"""Tanium Sensor/Package parameter helper."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import pprint

THIS_FILE = os.path.abspath(__file__)
THIS_SCRIPT = os.path.basename(THIS_FILE)
THIS_PATH = os.path.dirname(THIS_FILE)
TOOL_PATH = os.path.dirname(THIS_PATH)


class ParamHelper(object):
    """Tanium Sensor/Package parameter helper."""

    MODEL_PRE = {}
    MODEL_PRE[None] = "com.tanium.components.parameters"
    MODEL_PRE["ValidationExpression"] = "com.tanium.models"

    # map a mode to a model
    MODE_MAP = {}
    MODE_MAP["text"] = "TextInputParameter"
    MODE_MAP["dropdown"] = "DropDownParameter"
    MODE_MAP["number"] = "NumericParameter"
    MODE_MAP["checkbox"] = "CheckBoxParameter"

    # map the arguments for a given model to their respective model key names
    MODEL_MAP = {}
    MODEL_MAP["TextInputParameter"] = {
        "prompt": "promptText",
        "label": "label",
        "help": "helpString",
        "default_text": "defaultValue",
        "validations": "validationExpressions",
    }
    MODEL_MAP["ValidationExpression"] = {
        "help": "helpString",
        "expression": "expression",
    }
    MODEL_MAP["DropDownParameter"] = {
        "label": "label",
        "help": "helpString",
        "values": "values",
    }
    MODEL_MAP["ParametersArray"] = {
        "parameters": "parameters",
    }
    MODEL_MAP["NumericParameter"] = {
        "default_number": "defaultValue",
        "label": "label",
        "help": "helpString",
        "maximum": "maximum",
        "minimum": "minimum",
    }
    MODEL_MAP["CheckBoxParameter"] = {
        "default_number": "defaultValue",
        "label": "label",
        "help": "helpString",
    }

    def __init__(self, params=None):
        """Constructor."""
        self.LOG = logging.getLogger("ParamHelper")
        self.params = params or []

    def build_param_def(self, params):
        """Add a set of parameters to self.params and return a parameter definition."""
        [self.add_param(**x) for x in params]
        ret = self._model(model_name="ParametersArray", kwargs={"parameters": self.params})
        return ret

    def add_param(self, **kwargs):
        """Add a parameter to self.params."""
        mode = kwargs.get("mode", "text").lower()

        if mode not in self.MODE_MAP:
            m = "Parameter mode '{}' is invalid, must be one of {}".format
            raise Exception(m(mode, self.MODE_MAP.keys()))

        model_name = self.MODE_MAP[mode]
        ret = self._model(model_name=model_name, kwargs=kwargs)
        ret["key"] = "${}".format(len(self.params) + 1)

        self.params.append(ret)

        m = "Added '{model}' parameter key '{key}'".format
        self.LOG.debug(m(**ret))

        m = "Argument dump:\n{}".format
        self.LOG.debug(m(pprint.pformat(kwargs)))

        m = "Parameter dump:\n{}".format
        self.LOG.debug(m(pprint.pformat(ret)))
        return ret

    def _model(self, model_name, kwargs):
        model_map = self.MODEL_MAP[model_name]
        model = self._type(name=model_name)

        ret = {}
        ret["model"] = model
        ret["parameterType"] = model

        for kwkey, objkey in model_map.items():
            if kwkey in kwargs and kwargs[kwkey] not in [None]:
                ret.update({objkey: kwargs[kwkey]})

        if "validationExpressions" in ret:
            exprs = ret["validationExpressions"]
            exprs = [self._model(model_name="ValidationExpression", kwargs=x) for x in exprs]
            ret["validationExpressions"] = exprs
        return ret

    def _type(self, name):
        pre = self.MODEL_PRE.get(name, self.MODEL_PRE[None])
        ret = "{}::{}".format(pre, name)
        return ret
