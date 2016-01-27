import os
import json
import logging
import getpass

from pytan import PytanError, string_types, input
from pytan.store import ArgStore
from pytan.tickle.tools import obfuscate
from pytan.shellparser import str2bool
from pytan.handler_logs import setup_log

from pytan.constants import HANDLER_DEFAULTS, PYTAN_KEY, ARGS_ORDER

MYLOG = logging.getLogger(__name__)


class ArgumentParsingError(PytanError):
    pass


class UserConfigError(PytanError):
    pass


def build_argstore(**kwargs):
    """pass."""
    setup_log(**kwargs)
    pytan_key = kwargs.get('pytan_key', PYTAN_KEY)
    default_args = kwargs.get('default_args', HANDLER_DEFAULTS)
    args_order = kwargs.get('args_order', ARGS_ORDER)

    kwargs['default_args'] = default_args
    config_file = determine_config_file(**kwargs)
    configfile_args = read_config_file(**kwargs)
    osenv_args = get_osenv_args()

    argstore = ArgStore()
    argstore.handler_args_source = ArgStore(_store_name='handler_args_source')
    argstore.handler_args = ArgStore(_store_name='handler_args')
    argstore.default_args = ArgStore(_store_name='default_args', **default_args)
    argstore.cmdline_args = get_src_args(_store_name='cmdline_args', **kwargs)
    argstore.osenvironment_args = get_src_args(_store_name='osenvironment_args', **osenv_args)
    argstore.configfile_args = get_src_args(_store_name=config_file, **configfile_args)

    for arg, def_val in default_args.items():
        arg_source = find_arg_source(arg, argstore, args_order)
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
            val = handle_string_arg(arg, val, arg_source, def_val)

        val = enforce_arg_type(arg, val, arg_source, def_val)

        if arg == 'password':
            val = obfuscate(key=pytan_key, string=val)

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
    argstore = build_argstore(**kwargs)
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


def find_arg_source(arg, argstore, args_order):
    for src in args_order:
        if arg in argstore[src] and argstore[src].get(arg, None) is not None:
            arg_source = src
            break
    return arg_source


def get_osenv_args(**kwargs):
    osenv_args = {
        k.lower().replace('pytan_', ''): v
        for k, v in os.environ.items()
        if k.lower().startswith('pytan_')
    }
    return osenv_args


def handle_string_arg(arg, value, arg_source, def_val):
    """handle string types that actually should be other types."""
    result = value
    def_argtype = type(def_val)
    if def_argtype == bool:
        try:
            result = str2bool(value)
        except Exception as e:
            err = "Failed to evaluate string {!r} into a boolean from source {!r}, exception: {}"
            err = err.format(value, arg_source, e)
            raise ArgumentParsingError(err)
    if def_argtype == dict:
        try:
            result = dict(eval(value))
        except Exception as e:
            err = "Failed to evaluate string {!r} into a dictionary from source {!r}, exception {}"
            err = err.format(value, arg_source, e)
            raise ArgumentParsingError(err)
    return result


def enforce_arg_type(arg, val, source, def_val):
    pa_type = type(val).__name__
    def_argtype = type(def_val)
    try:
        result = def_argtype(val)
    except Exception as e:
        err = "Argument {!r} value {!r} must be type {!r}, supplied type {!r} via {!r}: {}"
        err = err.format(arg, val, def_argtype.__name__, pa_type, source, e)
        raise ArgumentParsingError(err)
    return result


def get_src_args(_store_name, **kwargs):
    """pass."""
    default_args = kwargs.get('default_args', HANDLER_DEFAULTS)
    src_args = ArgStore(_store_name=_store_name)
    [setattr(src_args, k, kwargs[k]) for k in default_args if k in kwargs]
    return src_args


def determine_config_file(**kwargs):
    default_args = kwargs.get('default_args', HANDLER_DEFAULTS)
    osenv_args = get_osenv_args()
    cf_kwarg = kwargs.get('config_file', '')
    cf_env = osenv_args.get('config_file', '')
    cf_def = default_args['config_file']
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
        raise UserConfigError(err)
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
            raise UserConfigError(err)
        else:
            m = "PyTan User config file successfully loaded: {} "
            m = m.format(config_file)
            MYLOG.info(m)
    else:
        m = "Unable to find PyTan User config file at: {}".format
        MYLOG.info(m(config_file))
        return puc_dict
    return puc_dict
