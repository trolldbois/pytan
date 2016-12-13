#!/usr/bin/env python
"""TODO."""
from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import datetime
import json
import logging
import logging.handlers
import os
import re
import sys
import threading
import time
from io import open

import modules.ini_reader

__author__ = 'Jim Olsen <jim.olsen@tanium.com>, Rory Prendergast <rory.prendergast@tanium.com>, ' \
             'James Cobey <james.cobey@tanium.com>'
__version__ = '2.1.9'

REQUIRED_BROKER_VERSION_MIN = '0.6'  # for printing out, this isn't actually checked

STATIC_PYTAN_LIB_PATH = "/github/pytan/lib"
"""Manually defined PyTan library directory, for scripts that do not live in bin/."""

ALLOWED_ROLES = ["Question Author"]
"""List of User Roles that are allowed to be attached to Tanium users running this script."""

DEFAULT_REPEAT_SECONDS = 600
"""If a section does not have a 'repeat_seconds' defined, we will default to this."""

THIS_FILE = os.path.abspath(sys.argv[0])
THIS_NAME = os.path.basename(THIS_FILE)
THIS_BASENAME = os.path.splitext(THIS_NAME)[0]
THIS_PATH = os.path.dirname(THIS_FILE)
PARENT_PATH = os.path.dirname(THIS_PATH)

AUTO_PYTAN_LIB_PATH = os.path.join(PARENT_PATH, "lib")
"""Automagic reference to pytan library dir, if this script lives in bin/."""

PYTAN_INTEGRATIONS_LIB_PATH = os.path.join('..', '..', '..', '..', 'lib')
"""Automagic reference to pytan library dir, if this script lives in EXAMPLES/POC/pytan-integrations/bro"""

PATH_ADDS = [STATIC_PYTAN_LIB_PATH, AUTO_PYTAN_LIB_PATH, PYTAN_INTEGRATIONS_LIB_PATH]
"""Paths to add to sys.path/PYTHONPATH."""

[sys.path.append(aa) for aa in PATH_ADDS if aa not in sys.path]

THIS_LOG = logging.getLogger(THIS_BASENAME)
THIS_LOG.setLevel(logging.DEBUG)
THIS_LOG.propagate = False


if sys.version_info > (3, 0):
    PY_VER = 3
else:
    PY_VER = 2


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

try:
    from modules import broker_sender
except ImportError as e:
    m = (
        "!!! Unable to import Broker API Python Bindings !!!\n"
        "*** Original error: {}\n"
        "*** Paths added to PYTHONPATH: {}\n"
        "*** Full PYTHONPATH: {}\n\n"
        "*** Ensure at least broker version {} is compiled, installed, and available in sys.path or PYTHONPATH.\n"
    ).format(e, ", ".join(PATH_ADDS), ", ".join(sys.path), REQUIRED_BROKER_VERSION_MIN)
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

THREAD_EXAMINE_SECONDS = 5


class QuestionThread(threading.Thread):
    """Thread for running a question section. A question section in bro.ini looks like:

        [question1]
        question=Get last logged in user from all machines

        ...

        And, for each question, the question text is modified such that 'get computer name and Tanium Client IP Address
        and Last Logged In User' is inserted at the beginning, after the word 'Get' is removed if necessary.

        Any encountered exceptions are stored in the exception attribute.

        Call .stop_question() to kill thread.

        Parameters
        ----------
        handler : `pytan.Handler`
            * a functional handler instance.
        section_name : str
            * The name of the thread and the logger name.
        section_dict : dict
            * the dictionary which represents the config file section used to drive questions.
        always_add_prefix : str OR unicode, optional
            * The text to append to the select part of any configured question.
            * default : 'Get Computer Name and Tanium Client IP Address and Last Logged In User and '

"""

    def __init__(self, handler, section_name, section_dict,
                 always_add_prefix='Get Computer Name and Tanium Client IP Address and Last Logged In User and '):
        """Constructor."""
        #threading.Thread.__init__(self)
        super(QuestionThread, self).__init__()
        self.setName(section_name)
        self.always_add_prefix = always_add_prefix
        self.handler = handler
        self.last_result = {}
        self.last_fetched = None
        self.exception = None
        self._stopper = threading.Event()
        # a flag indicating whether to log the message that the thread is waiting for completion.
        # this is always the default case, as question won't have expired for 10 minutes after init.
        # after printing, it is set to false, and after send it is reset to true (default state).
        self.waiting_print_flag = True

        if "question" not in section_dict:
            m = "'question' not supplied for section '{}' (full section: {})"
            raise Exception(m.format(section_name, section_dict))

        self.question = self._mod_question(section_dict['question'])

        if "repeat_seconds" not in section_dict:
            m = "'repeat_seconds' not supplied for section '{}', using default of '{}'"
            THIS_LOG.info(m.format(section_name, DEFAULT_REPEAT_SECONDS))
            self.repeat_seconds = DEFAULT_REPEAT_SECONDS
        else:
            self.repeat_seconds = section_dict["repeat_seconds"]

        if self.repeat_seconds < DEFAULT_REPEAT_SECONDS:
            raise ValueError('repeat_seconds of {} for question in section name {} with text \'{}\' '
                             'is less than minimum value of {}'.format(self.repeat_seconds,
                                                                       section_name, section_dict['question'],
                                                                       DEFAULT_REPEAT_SECONDS))
        self.daemon = True
        self.start()

    def run(self):
        """Run the thread."""
        while True:
            if self.is_stopped():
                break
            m = "Thread Name: {}, asking parsed question '{}'"
            THIS_LOG.debug(m.format(self.getName(), self.question))
            try:
                self.last_result = self.handler.ask_parsed(question_text=self.question, picker=1)
            except pytan.exceptions.PollingError as e:
                pe = "Thread Name {} - Polling error: {}"
                THIS_LOG.warn(pe.format(self.getName(), str(e)))
                self.exception = e
            except Exception as e:
                em = "Thread Name {} - Exception: {}"
                THIS_LOG.warn(em.format(self.getName(), str(e)))
                self.exception = e

            self.last_fetched = datetime.datetime.now()
            try:
                m = "Thread Name: {}, received results for question '{}': {}"
                THIS_LOG.debug(m.format(self.getName(), self.question, self.last_result["question_results"]))
            except KeyError:
                m = "Thread Name: {}, cannot retrieve results for question '{}': {}"
                THIS_LOG.debug(m.format(self.getName(), self.question, self.last_result["question_results"]))
            m = "Thread Name: {}, sleeping for {} seconds"
            THIS_LOG.debug(m.format(self.getName(), self.repeat_seconds))
            self._stopper.wait(self.repeat_seconds)

    def stop_question(self):
        THIS_LOG.info("Question thread {} stopped".format(self.getName()))
        self._stopper.set()

    def is_stopped(self):
        return self._stopper.is_set()

    def _mod_question(self, question_text):
        """Modifies a question to remove Get and add self.always_add_prefix, which guarantees a set of data.
        By default, this set is data which is critical to composing a broker message according to the included
        bro example file, but if the message was changed, this could, in theory, be something else.
        """
        return re.compile('^get ', flags=re.IGNORECASE).sub(self.always_add_prefix, question_text)


def get_handler(logger, handler_name):
    """Retrieve a handler object from a logger by name.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object
    handler_name : str OR unicode
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
    ini_reader = modules.ini_reader.IniReader()
    try:
        bro_config_path, bro_config = ini_reader.read(ini_path=args.bro_config)
    except:
        m = "Failed to read the Bro Config File!"
        THIS_LOG.exception(m)
        raise

    THIS_LOG.debug(
        "Successfully read Bro Config File '{}':\n{}".format(bro_config_path, pytan.utils.jsonify(bro_config)))
    return bro_config_path, bro_config


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


def broker_send(broker_sender, question_start_time, question_results, event_suffix):
    THIS_LOG.info('Sending {} Tanium Console rows of data via broker'.format(question_results.row_count))
    try:
        broker_sender.send_answer_rows(question_start_time, question_results,
                                       broker_sender.event_name_prefix + event_suffix, logger=THIS_LOG)
    except Exception as e:
        m = "FAILED to send data to broker listener at {}:{}, {}"
        m = m.format(broker_sender.dst_host, broker_sender.dst_port, str(e))
        THIS_LOG.critical(m)


def handle_tracker_results(thread_tracker, broker_sender, desired_completion_pct):
    """Logging and sending the data to broker for each question thread"""
    # looping through each thread, which is an active question
    for section_name, section_thread in thread_tracker.items():
        # look for any exception messages
        active_exception = copy.copy(section_thread.exception)
        if active_exception is not None:
            section_thread.exception = None
            raise active_exception
        result_data = section_thread.last_result.get('question_results', None)
        if result_data is None:
            m = "No result data for question {}"
            THIS_LOG.warn(m.format(section_name))
            continue

        question_obj = section_thread.last_result.get('question_object', None)
        if question_obj is None:
            m = "Cannot yet get question object for question {}"
            THIS_LOG.warn(m.format(section_name))
            continue

        question_poller = section_thread.last_result.get('poller_object', None)
        if question_obj is None:
            m = "Cannot yet get poller object for question {}"
            THIS_LOG.warn(m.format(section_name))
            continue
        percent_complete = question_poller.complete_pct
        question_start_time = question_poller.start
        # Questions are active for 10 minutes - the expiration time is start + 10 minutes.
        # If the question is about to expire, meaning the question's expiration time is
        # 2 x THREAD_EXAMINE_SECONDS away from now, we have as much data as we're going to get.
        if question_poller.expiration_timeout <= datetime.datetime.utcnow() - \
                datetime.timedelta(seconds=2 * THREAD_EXAMINE_SECONDS):
            THIS_LOG.info("Question {} with qid {} is about to expire, sending to Bro via broker".format(section_name, result_data.question_id))
            if percent_complete >= desired_completion_pct:
                THIS_LOG.info("Question {} has completed".format(section_name))
                m = "Transforming {} data and attempting to send to broker listener at {}:{}"
                m = m.format(section_name, broker_sender.dst_host, broker_sender.dst_port)
                THIS_LOG.info(m)
                try:
                    broker_send(broker_sender, question_start_time, result_data, section_name)
                except Exception as e:
                    raise e
                finally:
                    if not section_thread.is_stopped():
                        print('stopping thread')
                        section_thread.stop_question()
                        section_thread.waiting_print_flag = True
            else:
                fetched = section_thread.last_fetched
                m = "Question '{}', start time {}, {}% completed, last fetched on {}. Waiting for {}% completion"
                m = m.format(section_name, question_start_time, percent_complete, fetched, desired_completion_pct)
                THIS_LOG.info(m)
        else:
            # only print this every so often so logs don't fill up for no reason.
            if section_thread.waiting_print_flag:
                m = "Waiting for expiration. Expiration time for question id {} is {}, {} complete."
                m = m.format(result_data.question_id, question_poller.expiration_timeout, percent_complete)
                THIS_LOG.debug(m)
                section_thread.waiting_print_flag = False


def get_bro_connection_details(bro_config):
    """Performs sanity checks and assigns defaults. Returns a dict with config items and assigned values for the
    destination section"""
    # set some default values here. Only assign items to destination config that we expect.
    r = dict()
    r['broker_enabled_bro_host'] = None
    r['broker_port'] = None
    r['max_log_lines'] = 10000
    r['question_completion_pct_before_send'] = 99
    r['seconds_after_completion_to_send'] = 20

    # loop through items defined in the section. Assign them to dictionary with same name.
    # if the item doesn't exist, use the defaults specified above.
    for section_name, section_dict in bro_config.items():
        if section_name == 'destination':
            for k, v in r.items():
                r[k] = section_dict.get(k, r[k])

    if (r['broker_enabled_bro_host'] is None) or (r['broker_port'] is None):
        m = "Fatal - both broker_enabled_bro_host and bro_port must be specified " \
            "in the [destination] section"
        THIS_LOG.info(m)
        sys.exit(1)

    return r


if __name__ == "__main__":
    pytan.binsupport.HistoryConsole()

    parser = setup_parser()
    args = parse_args(parser)
    setup_logging(args)
    handler = connect_tanium(args)
    bro_config_path, bro_config = read_bro_config(args)
    dest_config = get_bro_connection_details(bro_config)

    try:
        bs = broker_sender.TaniumBrokerSender(dest_config['broker_enabled_bro_host'], dest_config['broker_port'],
                                              max_log_lines_per_send=dest_config['max_log_lines'])
    except RuntimeError as e:
        m = "Fatal - Cannot connect to broker listener at {}:{}, {}"
        THIS_LOG.fatal(m.format(dest_config['broker_enabled_bro_host'], dest_config['broker_port'], str(e)))
        sys.exit(1)

    thread_tracker = {}

    def create_tracker():
        for section_name, section_dict in bro_config.items():
            if "question" not in section_dict:
                m = "Skipping section '{}', no 'question' setting provided!"
                THIS_LOG.info(m.format(section_name))
                continue
            try:
                THIS_LOG.debug('Creating question thread for {}'.format(section_name))
                thread_tracker[section_name] = QuestionThread(handler, section_name, section_dict)
            except ValueError as e:
                m = 'Fatal - Exception creating question runner, {}'
                THIS_LOG.fatal(m.format(str(e)))
                sys.exit(1)

    def check_tracker():
        for section_name, section_thread in thread_tracker.items():
            if not section_thread.is_alive():
                THIS_LOG.debug('Restarting terminated question thread for {}'.format(section_name))
                # completely remove this poller and re-add it to thread_tracker dict
                del section_thread
                section_dict = bro_config[section_name]
                thread_tracker[section_name] = QuestionThread(handler, section_name, section_dict)

    create_tracker()
    slept_seconds = 0
    while True:
        check_tracker()
        try:
            handle_tracker_results(thread_tracker, bs, dest_config['question_completion_pct_before_send'])
        except Exception as e:
            THIS_LOG.warning("Exception in question thread: {}".format(str(e)))

        time.sleep(THREAD_EXAMINE_SECONDS)
