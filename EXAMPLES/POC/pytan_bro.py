#!/usr/bin/env python
"""TODO."""
from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import json
import logging
import logging.handlers
import os
import sys
import threading
import time
from io import StringIO, open

__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.9'

STATIC_PYTAN_LIB_PATH = "/github/pytan/lib"
"""Manually defined PyTan library directory, for scripts that do not live in bin/."""

ALLOWED_ROLES = ["Question Author"]
"""List of User Roles that are allowed to be attached to Tanium users running this script."""

DEFAULT_REPEAT_SECONDS = 300
"""If a section does not have a 'repeat_seconds' defined, we will default to this."""

THIS_FILE = os.path.abspath(sys.argv[0])
THIS_NAME = os.path.basename(THIS_FILE)
THIS_BASENAME = os.path.splitext(THIS_NAME)[0]
THIS_PATH = os.path.dirname(THIS_FILE)
PARENT_PATH = os.path.dirname(THIS_PATH)

AUTO_PYTAN_LIB_PATH = os.path.join(PARENT_PATH, "lib")
"""Automagic reference to pytan library dir, if this script lives in bin/."""

PATH_ADDS = [STATIC_PYTAN_LIB_PATH, AUTO_PYTAN_LIB_PATH]
"""Paths to add to sys.path/PYTHONPATH."""

[sys.path.append(aa) for aa in PATH_ADDS if aa not in sys.path]

THIS_LOG = logging.getLogger(THIS_BASENAME)
THIS_LOG.setLevel(logging.DEBUG)
THIS_LOG.propagate = False

try:
    import pytan
    import pytan.binsupport
    import taniumpy
except Exception as e:
    m = (
        "!!! Unable to import PyTan !!!\n"
        "*** Original error: {}\n"
        "*** Paths added to PYTHONPATH: {}\n"
        "*** Full PYTHONPATH: {}\n\n"
        "*** Move this script to the bin/ directory\n"
        "*** Or update 'STATIC_PYTAN_LIB_PATH' in this script with '/path/to/pytan/lib'.\n"
        "*** Or manually add '/path/to/pytan/lib' to the environment variable 'PYTHONPATH'\n"
    ).format(e, ", ".join(PATH_ADDS), ", ".join(sys.path))
    raise Exception(m)

PYTAN_PKG_INIT_PATH = pytan.__file__
PYTAN_PKG_PATH = os.path.dirname(PYTAN_PKG_INIT_PATH)
PYTAN_LIB_PATH = os.path.dirname(PYTAN_PKG_PATH)
PYTAN_BASE_PATH = os.path.dirname(PYTAN_LIB_PATH)

WRITE_PUC_FILENAME = "write_pytan_user_config.py"
WRITE_PUC_PATH = os.path.join(PYTAN_BASE_PATH, "bin", WRITE_PUC_FILENAME)

PUC_HELP = "\nUse '{}' to create a PyTan Config file in JSON format!".format(WRITE_PUC_PATH)

LOG_CON_OUTPUT = sys.stdout
"""Send console output to stdout."""

LOG_CON_FORMAT = "%(asctime)s [%(name)s] [%(funcName)s] PID=%(process)d THREAD=%(threadName)s %(levelname)-8s %(message)s"
"""Format for the console output."""
pytan.constants.INFO_FORMAT = LOG_CON_FORMAT

LOG_CON_LEVEL = "DEBUG"
"""Set the console handler to DEBUG, let the logger control the actual level."""

LOG_CON_HANDLER_NAME = "console_handler"
"""Name to label console handler with."""

LOG_FILE_DIR = THIS_PATH
"""Directory to store log files, if not absolute will be joined with cwd."""

LOG_FILE_NAME = "{}.log".format(THIS_BASENAME)
"""File name to use for file log, if not supplied the basename of LOGGER_NAME will be used."""

LOG_FILE_MB = 10
"""MB of file log size before rollover."""

LOG_FILE_COUNT = 10
"""Number of rolled over file logs to keep."""

LOG_FILE_FORMAT = "%(asctime)s [%(name)s] [%(funcName)s] PID=%(process)d THREAD=%(threadName)s %(levelname)-8s %(message)s"
"""Format for the file log output"""

LOG_FILE_LEVEL = "DEBUG"
"""Set the file handler to DEBUG, let the logger control the actual level."""

LOG_FILE_HANDLER_NAME = "log_file_handler"
"""Name to label tanium handler with."""


class QuestionThread(threading.Thread):
    """Thread for running a question section."""

    def __init__(self, handler, section_name, section_dict):
        """Constructor."""
        threading.Thread.__init__(self)
        self.setName(section_name)

        self.handler = handler

        self.last_result = {}
        self.last_fetched = None

        if "question" not in section_dict:
            m = "'question' not supplied for section '{}' (full section: {})"
            raise Exception(m.format(section_name, section_dict))

        self.question = section_dict["question"]

        if "repeat_seconds" not in section_dict:
            m = "'repeat_seconds' not supplied for section '{}', using default of '{}'"
            THIS_LOG.info(m.format(section_name, DEFAULT_REPEAT_SECONDS))
            self.repeat_seconds = DEFAULT_REPEAT_SECONDS
        else:
            self.repeat_seconds = section_dict["repeat_seconds"]

        self.daemon = True
        self.start()

    def run(self):
        """Run the thread."""
        while True:
            m = "Thread Name: {}, asking parsed question '{}'"
            THIS_LOG.debug(m.format(self.getName(), self.question))
            self.last_result = self.handler.ask_parsed(question_text=self.question, picker=1)
            self.last_fetched = datetime.datetime.now()

            m = "Thread Name: {}, received results for question '{}': {}"
            THIS_LOG.debug(m.format(self.getName(), self.question, self.last_result["question_results"]))

            m = "Thread Name: {}, sleeping for {} seconds"
            THIS_LOG.debug(m.format(self.getName(), self.repeat_seconds))
            time.sleep(self.repeat_seconds)


class IniReaderError(Exception):
    """Reader exceptions."""


class IniReader(object):
    """Reads an INI file into a python dict structure."""

    TEXT_PRE = "__TEXT::"

    BOOL_OPTS = ["true", "false", "yes", "no", "on", "off"]

    BOOL_TRUE = ["true", "yes", "on"]

    _VERSION = sys.version_info
    IS_PY2 = _VERSION[0] == 2
    IS_PY3 = _VERSION[0] == 3

    if IS_PY2:
        integer_types = (int, long)  # noqa
        text_type = unicode  # noqa
        import ConfigParser as configparser
    elif IS_PY3:
        integer_types = int,
        text_type = str
        import configparser as configparser

    _value_cache = {}
    _parser_type = configparser.RawConfigParser

    def read(self, ini_path=None, ini_text=None, ini_handle=None, **kwargs):
        """Die."""
        if ini_text:
            fh = StringIO(ini_text)
            path = "<ini_text stream>"
        elif ini_path:
            if os.path.isfile(ini_path):
                fh = open(ini_path, encoding="utf-8")
                path = ini_path
            else:
                m = "Unable to find 'ini_path': '{}'"
                raise IniReaderError(m.format(ini_path))
        elif ini_handle:
            fh = ini_handle
            path = "<ini_handle stream>"
        else:
            m = "Must provide ini_text, ini_path, or ini_handle as an argument"
            raise IniReaderError(m)

        cp = self.configparser.RawConfigParser()
        try:
            cp.readfp(fh)
        except Exception as e:
            m = "Unable to parse INI file '{}', error: {}"
            raise IniReaderError(m.format(path, e))

        ret = {s: {i[0]: self._tv(i[1]) for i in cp.items(s)} for s in cp.sections()}
        return path, ret

    def _tv(self, value):
        """Cache to avoid transforming value too many times."""
        if value not in self._value_cache:
            new_value = value
            if self.is_txt(value):
                new_value = self.to_txt(value)
            elif self.is_int(value):
                new_value = int(value)
            elif self.is_float(value):
                new_value = float(value)
            elif self.is_bool(value):
                new_value = self.to_bool(value)
            elif self.is_none(value):
                new_value = None
            self._value_cache[value] = new_value
        return self._value_cache[value]

    def is_float(self, value):
        """Check if the value is a float."""
        return self._is_type(value, float)

    def is_int(self, value):
        """Check if the value is an int."""
        return any([self._is_type(value, t) for t in self.integer_types])

    def is_txt(self, value):
        """Check if the value begins with TEXT_PRE."""
        return self.text_type(value).startswith(self.TEXT_PRE)

    def is_bool(self, value):
        """Check if the value is a bool."""
        return value.lower() in self.BOOL_OPTS

    def is_none(self, value):
        """Check if the value is a None."""
        return value.lower() == self.text_type(None).lower()

    def to_txt(self, value):
        """Convert a value to text, removing FORCE_TEXT::."""
        return "".join(self.text_type(value).split(self.TEXT_PRE, 1)[1:])

    def to_bool(self, value):
        """Convert value to a bool."""
        return value.lower() in self.BOOL_TRUE

    def _is_type(self, value, ptype):
        """Try to set value to python type ptype."""
        try:
            ptype(value)
            ret = True
        except Exception:
            ret = False
        return ret


def get_handler(logger, handler_name):
    """Retrieve a handler object from a logger by name.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object
    handler_name : str
        * str of python logging handler name to remove from `logger`

    Returns
    -------
    ret : obj or None
        * obj if handler named handler_name is found, None otherwise
    """
    ret = None
    for h in list(logger.handlers):
        if h.name == handler_name:
            ret = h
            break
    return ret


def make_handler_con(**kwargs):
    """Create a console output handler object.

    Parameters
    ----------
    log_con_format : str, optional
        * python logging formatter str to use for logging
        * default : :data:`Logging.LOG_CON_FORMAT`
    log_con_level : str, optional
        * python logging level to use for logging
        * default : :data:`Logging.LOG_CON_LEVEL`
    log_con_handler_name : str, optional
        * name to use for identifying handler
        * default : :data:`Logging.LOG_CON_HANDLER_NAME`
    log_con_output : stream, optional
        * stream to use for output (sys.stdout, sys.stderr)
        * default : :data:`Logging.LOG_CON_OUTPUT`

    Returns
    -------
    handler : python logging handler object
        * handler created by this method
    """
    log_format = kwargs.get("log_con_format", LOG_CON_FORMAT)
    log_level = kwargs.get("log_con_level", LOG_CON_LEVEL)
    log_handler_name = kwargs.get("log_con_handler_name", LOG_CON_HANDLER_NAME)
    log_output = kwargs.get("log_con_output", LOG_CON_OUTPUT)

    handler = logging.StreamHandler(stream=log_output)
    handler.setFormatter(logging.Formatter(log_format))
    handler.setLevel(getattr(logging, log_level.upper()))
    handler.name = log_handler_name
    return handler


def make_handler_file(**kwargs):
    """Create and a file output handler object.

    Parameters
    ----------
    log_file_format : str, optional
        * python logging formatter str to use for logging
        * default : :data:`Logging.LOG_FILE_FORMAT`
    log_file_level : str, optional
        * python logging level to use for logging
        * default : :data:`Logging.LOG_FILE_LEVEL`
    log_file_handler_name : str, optional
        * name to use for identifying handler
        * default : :data:`Logging.LOG_FILE_HANDLER_NAME`
    log_file_name : str, optional
        * filename to use for logging
        * uses basename of logger name if not supplied
        * default : :data:`Logging.LOG_FILE_NAME`
    log_file_dir : str, optional
        * dir to use for logging
        * uses absolute path of cwd if empty/not supplied
        * turns all paths into absolute paths from cwd if relative
        * default : :data:`Logging.LOG_FILE_DIR`
    log_file_count : int, optional
        * number of logs to keep when rolling logs over
        * default : :data:`Logging.LOG_FILE_COUNT`
    log_file_mb : int, optional
        * MB of file log size before rollover
        * default : :data:`Logging.LOG_FILE_MB`

    Returns
    -------
    handler : python logging handler object
        * handler created by this method
    """
    log_format = kwargs.get("log_file_format", LOG_FILE_FORMAT)
    log_level = kwargs.get("log_file_level", LOG_FILE_LEVEL)
    log_handler_name = kwargs.get("log_file_handler_name", LOG_FILE_HANDLER_NAME)
    log_name = kwargs.get("log_file_name", LOG_FILE_NAME)
    log_dir = kwargs.get("log_file_dir", LOG_FILE_DIR)
    log_count = kwargs.get("log_file_count", LOG_FILE_COUNT)
    log_mb = kwargs.get("log_file_mb", LOG_FILE_MB)

    log_max_bytes = log_mb * 1024 * 1024

    log_dir = os.path.expanduser(log_dir)

    if not os.path.isabs(log_dir):
        log_dir = os.path.abspath(log_dir)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, log_name)

    handler = logging.handlers.RotatingFileHandler(
        filename=log_path,
        maxBytes=log_max_bytes,
        backupCount=log_count,
    )
    handler.setFormatter(logging.Formatter(log_format))
    handler.setLevel(getattr(logging, log_level.upper()))
    handler.name = log_handler_name
    return handler


def setup_parser():
    """Configure the argument parser."""
    parser = pytan.binsupport.CustomArgParse(
        description=__doc__,
        add_help=True,
        formatter_class=pytan.binsupport.CustomArgFormat,
    )
    helpstr = "PyTan Config file in JSON format to use for connecting to Tanium instance -- {}"
    helpstr = helpstr.format(PUC_HELP)
    parser.add_argument(
        "-p",
        "--pytan_config",
        required=False,
        action="store",
        default=pytan.constants.PYTAN_USER_CONFIG,
        dest="pytan_config",
        help=helpstr,
    )
    parser.add_argument(
        "-b",
        "--bro_config",
        required=False,
        action="store",
        default=os.path.join(THIS_PATH, "pytan_bro.ini"),
        dest="bro_config",
        help="Bro Config file in INI format to use for determining questions to ask",
    )
    parser.add_argument(
        "--log_file_dir",
        required=False,
        action="store",
        default=THIS_PATH,
        dest="log_file_dir",
        help="Path to store log_file",
    )
    parser.add_argument(
        "--log_file_name",
        required=False,
        action="store",
        default=LOG_FILE_NAME,
        dest="log_file_name",
        help="Filename to store logs to",
    )
    return parser


def validate_args(args, parser):
    """Validate the arguments after the parser has processed them."""
    args.pytan_config = os.path.abspath(os.path.expanduser(args.pytan_config))
    if not os.path.isfile(args.pytan_config):
        m = "Unable to find Pytan Config file in JSON format at '{}'{}"
        parser.error(m.format(args.pytan_config, PUC_HELP))

    try:
        with open(args.pytan_config) as fh:
            config = json.load(fh)
    except Exception as e:
        m = "Unable to read Pytan Config file in JSON format at '{}', error: {}{}"
        parser.error(m.format(args.pytan_config, e, PUC_HELP))

    fields = ["username", "password", "host"]
    for k in fields:
        if k not in config:
            m = "Setting '{}' not defined in Pytan Config file in JSON format at '{}'{}"
            parser.error(m.format(k, args.pytan_config, PUC_HELP))

    args.bro_config = os.path.abspath(os.path.expanduser(args.bro_config))
    if not os.path.isfile(args.bro_config):
        m = "Unable to find Bro Config file in INI format at '{}'"
        parser.error(m.format(args.bro_config))

    args.log_file_dir = os.path.abspath(os.path.expanduser(args.log_file_dir))
    if not os.path.isdir(args.log_file_dir):
        try:
            os.makedirs(args.log_file_dir)
        except Exception as e:
            m = "Unable to create the logs directory '{}', error: {}"
            raise Exception(m.format(args.log_file_dir, e))
    return args


def parse_args(parser):
    """Parse and validate the arguments."""
    args = parser.parse_args()
    args = validate_args(args, parser)
    return args


def setup_logging(args):
    """Create our own console and file handlers."""
    logcon_handler = make_handler_con(**args.__dict__)
    THIS_LOG.addHandler(logcon_handler)

    logfile_handler = make_handler_file(**args.__dict__)
    all_loggers = pytan.utils.get_all_pytan_loggers()
    all_loggers["pytan_bro"] = THIS_LOG

    for k, v in all_loggers.items():
        if not get_handler(v, LOG_FILE_HANDLER_NAME):
            v.addHandler(logfile_handler)

    THIS_LOG.info("Now logging to file: {}".format(logfile_handler.stream.name))


def validate_roles(user_obj):
    """Validate that the roles for user are in ALLOWED_ROLES."""
    has_allowed = False
    for role in user_obj.roles:
        if role.name not in ALLOWED_ROLES:
            m = "Role '{}' attached to user name '{}', id '{}' is not allowed! Allowed roles: {}"
            m = m.format(role.name, user_obj.name, user_obj.id, ", ".join(ALLOWED_ROLES))
            raise Exception(m)
        else:
            has_allowed = True

    if not has_allowed:
        m = "User name '{}', id '{}' has none of the allowed roles: {}"
        m = m.format(user_obj.name, user_obj.id, ", ".join(ALLOWED_ROLES))
        raise Exception(m)
    else:
        m = "User name '{}', id '{}' has at least one of the allowed roles: {}"
        m = m.format(user_obj.name, user_obj.id, ", ".join(ALLOWED_ROLES))
        THIS_LOG.debug(m)


def connect_tanium(args):
    """Connect to tanium and get a handler."""
    try:
        handler = pytan.handler.Handler(pytan_user_config=args.pytan_config)
    except:
        m = "Failed to connect to the Tanium Instance!"
        THIS_LOG.exception(m)
        raise

    handler.session.USER_OBJ = get_userinfo(handler)
    validate_roles(handler.session.USER_OBJ)

    THIS_LOG.info(handler)
    return handler


def read_bro_config(args):
    """Read the bro config ini file."""
    ini_reader = IniReader()
    try:
        bro_path, bro_config = ini_reader.read(ini_path=args.bro_config)
    except:
        m = "Failed to read the Bro Config File!"
        THIS_LOG.exception(m)
        raise

    THIS_LOG.debug("Successfully read Bro Config File '{}':\n{}".format(bro_path, pytan.utils.jsonify(bro_config)))
    return bro_path, bro_config


def session_user_id(handler):
    """Get the user ID from handler.session.session_id."""
    try:
        result = int(handler.session.session_id.split('-')[0])
    except:
        m = "Unable to parse user ID from session {!r}"
        raise Exception(m.format(handler.session.session_id))
    return result


def get_userinfo(handler):
    """Fetch the user info for user ID."""
    user_id = session_user_id(handler)
    user_obj = taniumpy.User()
    user_obj.id = user_id
    try:
        result = handler.session.find(user_obj)
    except:
        m = "Failed to fetch user info for user ID: {}"
        raise Exception(m.format(user_id))

    m = "Successfully retrieved user id {} info: {}"
    THIS_LOG.info(m.format(user_id, result))
    return result


def print_tracker_results(thread_tracker):
    """Example of getting results from each thread."""
    for section_name, section_thread in thread_tracker.items():
        result_data = section_thread.last_result.get("question_results", None)
        fetched = section_thread.last_fetched
        m = "Question '{}' last ResultData {} last fetched on {}"
        m = m.format(section_name, result_data, fetched)
        THIS_LOG.info(m)


if __name__ == "__main__":
    pytan.binsupport.HistoryConsole()

    parser = setup_parser()
    args = parse_args(parser)
    setup_logging(args)
    handler = connect_tanium(args)
    bro_path, bro_config = read_bro_config(args)

    thread_tracker = {}

    for section_name, section_dict in bro_config.items():
        if "question" not in section_dict:
            m = "Skipping section '{}', no 'question' setting provided!"
            THIS_LOG.info(m.format(section_name))
            continue

        thread_tracker[section_name] = QuestionThread(handler, section_name, section_dict)

    while True:
        print_tracker_results(thread_tracker)
        time.sleep(5)
