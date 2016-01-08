import os
import json
import logging
import getpass

from pytan import PytanError, string_types, input
from pytan.tickle.tools import obfuscate
from pytan.store import ArgStore
from pytan.handler_logs import add_override_log

from pytan.constants import HANDLER_DEFAULTS, PYTAN_KEY, ARGS_ORDER

MYLOG = logging.getLogger(__name__)


def create_argstore(**kwargs):
    """pass."""
    add_override_log(**kwargs)
    osenv_args = get_osenv_args()
    config_file = determine_config_file(**kwargs)
    configfile_args = read_config_file(**kwargs)
    default_args = HANDLER_DEFAULTS

    argstore = ArgStore()
    argstore.default_args = get_src_args('default_args', **default_args)
    argstore.cmdline_args = get_src_args('cmdline_args', **kwargs)
    argstore.osenvironment_args = get_src_args('osenvironment_args', **osenv_args)
    argstore.configfile_args = get_src_args(config_file, **configfile_args)
    argstore.handler_args_source = ArgStore(_store_name='handler_args_source')
    argstore.handler_args = ArgStore(_store_name='handler_args')

    for arg, def_val in HANDLER_DEFAULTS.items():
        arg_source = find_arg_source(arg, argstore)
        val = argstore[arg_source][arg]

        if arg == 'password':
            print_val = '**PASSWORD**'
        else:
            print_val = val

        m = "arg = {!r}, val = {!r}, type = {!r}, src = {!r}"
        m = m.format(arg, print_val, type(val).__name__, argstore[arg_source]._store_name)
        MYLOG.debug(m)

        val_is_str = isinstance(val, string_types)
        def_val_is_str = isinstance(def_val, string_types)

        if val_is_str and not def_val_is_str:
            val = handle_string_arg(arg, val)

        val = enforce_arg_type(arg, val, arg_source)

        if arg == 'password':
            val = obfuscate(key=PYTAN_KEY, string=val)

        argstore.handler_args[arg] = val
        argstore.handler_args_source[arg] = arg_source

    return argstore


def prompter(name, prompt_txt='Provide Tanium "{name}": '):
    value = ''
    if name == 'password':
        prompt = getpass.getpass
    else:
        prompt = input

    while True:
        value = prompt(prompt_txt.format(name=name))
        if not value:
            print('Must supply a value for "{}"'.format(name))
        else:
            break
    return value


def prompt_for_args(**kwargs):
    """Utility function to prompt for username, `, and host if empty"""
    argstore = create_argstore(**kwargs)
    handler_args = argstore.handler_args

    missing_session_prompts = ['username', 'password']
    for p in missing_session_prompts:
        if handler_args.get('session_id', '') or handler_args.get(p, ''):
            continue

        handler_args[p] = prompter(p)

    other_prompts = ['host']
    for p in other_prompts:
        if handler_args.get(p, ''):
            continue

        handler_args[p] = prompter(p)
    return handler_args


def find_arg_source(arg, argstore):
    for src in ARGS_ORDER:
        if arg in argstore[src] and argstore[src].get(arg, None) is not None:
            arg_source = src
            break
    return arg_source


def get_osenv_args():
    osenv_args = {
        k.lower().replace('pytan_', ''): v
        for k, v in os.environ.items()
        if k.lower().startswith('pytan_')
    }
    return osenv_args


def handle_string_arg(arg, value):
    """handle string types that actually should be other types."""
    result = value
    def_argtype = type(HANDLER_DEFAULTS[arg])
    if def_argtype == bool:
        valid = ["True", "False"]  # TODO bring in other trues/falses
        if value.capitalize() in valid:
            result = eval(value.capitalize())
        else:
            err = "Argument {!r} must be one of {!r}, supplied string containing {!r}"
            err = err.format(arg, ','.join(valid), value)
            raise PytanError(err)
    if def_argtype == dict:
        try:
            result = dict(eval(value))
        except Exception as e:
            err = "Tried to evaluate a dictionary from string {}, exception: {}"
            err = err.format(value, e)
            raise PytanError(err)
    return result


def enforce_arg_type(arg, val, source):
    pa_type = type(val).__name__
    def_argtype = type(HANDLER_DEFAULTS[arg])
    try:
        result = def_argtype(val)
    except Exception as e:
        err = "Argument {!r} value {!r} must be type {!r}, supplied type {!r} via {!r}: {}"
        err = err.format(arg, val, def_argtype.__name__, pa_type, source, e)
        raise PytanError(err)
    return result


def get_src_args(_store_name, **kwargs):
    """pass."""
    src_args = ArgStore(_store_name=_store_name)
    [setattr(src_args, k, kwargs[k]) for k in HANDLER_DEFAULTS if k in kwargs]
    return src_args


def determine_config_file(**kwargs):
    osenv_args = get_osenv_args()
    cf_kwarg = kwargs.get('config_file', '')
    cf_env = osenv_args.get('config_file', '')
    cf_def = HANDLER_DEFAULTS['config_file']
    config_file = cf_kwarg or cf_env or cf_def
    config_file = os.path.expanduser(config_file)
    return config_file


def write_config_file(puc_dict, **kwargs):
    """Write a PyTan User Config with the current class variables for use with
    pytan_user_config in instantiating Handler()

    Parameters
    ----------
    config_file : str, optional
        * default: self.pytan_user_config
        * JSON file to wite with current class variables

    Returns
    -------
    result : str
        * filename of PyTan User Config that was written to
    """
    config_file = determine_config_file(**kwargs)

    # obfuscate the password
    if puc_dict.get('password', ''):
        puc_dict['password'] = obfuscate(key=PYTAN_KEY, string=puc_dict['password'])

    try:
        with open(config_file, 'w+') as fh:
            json.dump(puc_dict, fh, skipkeys=True, indent=2)
    except Exception as e:
        err = "Failed to write PyTan User config: '{}', exception: {}"
        err = err.format(config_file, e)
        raise PytanError(err)
    else:
        m = "PyTan User config file successfully written: {} "
        m = m.format(config_file)
        MYLOG.info(m)
    return config_file


def read_config_file(**kwargs):
    """Read a PyTan User Config and update the current class variables"""
    config_file = determine_config_file(**kwargs)

    puc_dict = {}

    if os.path.isfile(config_file):
        try:
            with open(config_file) as fh:
                puc_dict = json.load(fh)
        except Exception as e:
            err = "PyTan User config file at: {} is invalid, exception: {}"
            err = err.format(config_file, e)
            raise PytanError(err)
        else:
            m = "PyTan User config file successfully loaded: {} "
            m = m.format(config_file)
            MYLOG.info(m)
    else:
        m = "Unable to find PyTan User config file at: {}".format
        MYLOG.info(m(config_file))
        return puc_dict
    return puc_dict
