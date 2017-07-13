from __future__ import absolute_import, division, print_function, unicode_literals

import getpass
import logging
import sys

from . import text_type

LOG = logging.getLogger(__name__.split(".")[-1])

YES_LIST = ['yes', 'y', 'ye', 'true', '1', 1, True]
"""List of possible "True" strings."""

NO_LIST = ['no', 'n', 'false', '0', 0, False]
"""List of possible "No" strings."""

PROMPTER_LINE = "Provide input: "
SECURE_VALUES = ["password"]


def ask(**kwargs):
    # empty_ok=False
    # default=""
    # is_int=False
    # is_bool=False
    # prompter=None
    # choices=[]
    # is_password=False
    # prompt=""
    # TODO add list_separator support to get muliple values

    prompter = get_prompter(**kwargs)
    prompt = build_prompt(**kwargs)

    while True:
        LOG.info(prompt)
        kwargs["ret"] = get_response(prompter, **kwargs)

        show_ret = "**HIDDEN**" if secure_value(**kwargs) else kwargs["ret"]
        m = "received console response {!r} from asking {!r}"
        m = m.format(show_ret, prompt)

        val_info = process_response(**kwargs)

        is_valid = val_info.get("is_valid", False)
        ret = val_info.get("ret", kwargs["ret"])

        if is_valid:
            break

    show_ret = "**HIDDEN**" if secure_value(**kwargs) else ret
    m = "parsed console response {!r} from asking {!r}"
    m = m.format(show_ret, prompt)
    LOG.debug(m)
    return ret


def secure_value(**kwargs):
    prompt = kwargs.get("prompt", "")
    secure_values = kwargs.get("secure_values", SECURE_VALUES)
    is_password = kwargs.get("is_password", False)

    ret = False
    if is_password:
        ret = True

    for x in secure_values:
        if x in prompt.lower():
            ret = True
    return ret


def process_response(**kwargs):
    if kwargs["ret"]:
        kwargs["is_valid"] = True

        if kwargs.get("is_int", False) and kwargs["is_valid"]:
            kwargs = val_int(**kwargs)

        if kwargs.get("is_bool", False) and kwargs["is_valid"]:
            kwargs = val_bool(**kwargs)

        if kwargs["is_valid"]:
            kwargs = val_choices(**kwargs)

    else:
        kwargs["is_valid"] = False

        if kwargs.get("default", ""):
            kwargs["ret"] = kwargs.get("default", "")
            kwargs["is_valid"] = True
        else:
            if kwargs.get("empty_ok", False):
                kwargs["is_valid"] = True
            else:
                print("")
                m = "Must supply a value!!"
                LOG.error(m)
    return kwargs


def val_bool(**kwargs):
    choices = kwargs.get("choices", ["yes", "no"]) or ["yes", "no"]
    ret = kwargs.get("ret", "")

    ret_bool = coerce_bool(ret)
    if ret_bool is None:
        print("")
        m = "{} is an invalid choice, please respond with one of: {}"
        m = m.format(ret, ', '.join(choices))
        LOG.error(m)
        kwargs["is_valid"] = False
    else:
        kwargs["ret"] = ret_bool
    return kwargs


def val_int(**kwargs):
    ret = kwargs.get("ret", "")

    try:
        kwargs["ret"] = int(ret)
    except:
        print("")
        m = "'{}' is not a number, please supply a number value"
        LOG.error(ret, m)
        kwargs["is_valid"] = False
    return kwargs


def val_choices(**kwargs):
    choices = kwargs.get("choices", [])
    is_bool = kwargs.get("is_bool", False)
    ret = kwargs.get("ret", "")

    if choices and not is_bool:
        if text_type(ret).lower() not in choices:
            print("")
            m = "{} is an invalid choice, please respond with one of: {}"
            m = m.format(ret, ', '.join(choices))
            LOG.error(m)
            kwargs["is_valid"] = False
    return kwargs


def get_response(prompter, **kwargs):
    try:
        ret = prompter(str(PROMPTER_LINE))  # hack for windows
        ret = ret.replace("\\n", "\n")
    except EOFError:
        print("\n")
        m = "EOF entered, exiting!"
        LOG.error(m)
        sys.exit(99)
    return ret


def try_int(response):
    try:
        response = int(response)
    except:
        print("")
        m = "Must supply a number value!!"
        LOG.error(m)
        response = None
    return response


def coerce_bool(m):
    if isinstance(m, text_type):
        m = m.lower()

    if m in YES_LIST:
        ret = True
    elif m in NO_LIST:
        ret = False
    else:
        ret = None
    return ret


def get_prompter(**kwargs):
    prompter = kwargs.get("prompter", None)

    if prompter:
        ret = prompter
    else:
        if secure_value(**kwargs):
            ret = getpass.getpass
        else:
            ret = getpass._raw_input
    return ret


def build_prompt(**kwargs):
    prompt = kwargs.get("prompt", "No prompt provided!")
    default = kwargs.get("default", "")
    choices = kwargs.get("choices", [])
    is_bool = kwargs.get("is_bool", False)

    if is_bool and not choices:
        choices = ["yes", "no"]

    if default:
        prompt = "{}\n\t[<ENTER> for default: {}]".format(prompt, default)

    if choices:
        prompt = "{}\n\t[choices: {}]".format(prompt, ", ".join(choices))

    return prompt
