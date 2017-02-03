# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""The main :mod:`pytan` module that provides first level entities for programmatic use."""
import datetime
import io
import json
import logging
import os
import pprint
import re

try:
    import taniumpy
    from . import version
    from . import constants
    from . import exceptions
    from . import utils
    from . import sessions
    from . import pollers
except:
    raise

kwmerge = utils.kwmerge
mklist = utils.mklist
get_obj_info = utils.get_obj_info
joiner = utils.joiner
re_exact = utils.re_exact
join_list_attrs = utils.join_list_attrs
seconds_from_now = utils.seconds_from_now
collapse_lod = utils.collapse_lod
get_bt_obj = utils.get_bt_obj
is_simple_str = utils.is_simple_str
list_objs_attr = utils.list_objs_attr
valvalue = utils.valvalue

PP_NAME = "PyTan Updated"
PP_VALUE = "{d} by v{v}"
SEARCH_RE = re.compile(r"(?<!\\)::")
ESCAPED_COMMAS_RE = re.compile(constants.ESCAPED_COMMAS)
ESCAPED_COLONS_RE = re.compile(constants.ESCAPED_COLONS)
PARSELOG = logging.getLogger("pytan.parser")


class Handler(object):
    """Creates a connection to a Tanium SOAP Server on host:port

    Parameters
    ----------
    username : str
        * default: None
        * `username` to connect to `host` with
    password : str
        * default: None
        * `password` to connect to `host` with
    host : str
        * default: None
        * hostname or ip of Tanium SOAP Server
    port : int, optional
        * default: 443
        * port of Tanium SOAP Server on `host`
    loglevel : int, optional
        * default: 0
        * 0 do not print anything except warnings/errors
        * 1 and higher will print more
    debugformat : bool, optional
        * default: False
        * False: use one line logformat
        * True: use two lines
    gmt_log : bool, optional
        * default: True
        * True: use GMT timezone for log output
        * False: use local time for log output
    session_id : str, optional
        * default: None
        * session_id to use while authenticating instead of username/password
    pytan_user_config : str, optional
        * default: constants.PYTAN_USER_CONFIG
        * JSON file containing key/value pairs to override class variables

    Other Parameters
    ----------------
    http_debug : bool, optional
        * default: False
        * False: do not print requests package debug
        * True: do print requests package debug
        * This is passed through to :class:`sessions.Session`
    http_auth_retry: bool, optional
        * default: True
        * True: retry HTTP GET/POST's
        * False: do not retry HTTP GET/POST's
        * This is passed through to :class:`sessions.Session`
    http_retry_count: int, optional
        * default: 5
        * number of times to retry HTTP GET/POST's if the connection times out/fails
        * This is passed through to :class:`sessions.Session`
    soap_request_headers : dict, optional
        * default: {'Content-Type': 'text/xml; charset=utf-8', 'Accept-Encoding': 'gzip'}
        * dictionary of headers to add to every HTTP GET/POST
        * This is passed through to :class:`sessions.Session`
    auth_connect_timeout_sec : int, optional
        * default: 5
        * number of seconds before timing out for a connection while authenticating
        * This is passed through to :class:`sessions.Session`
    auth_response_timeout_sec : int, optional
        * default: 15
        * number of seconds before timing out for a response while authenticating
        * This is passed through to :class:`sessions.Session`
    info_connect_timeout_sec : int, optional
        * default: 5
        * number of seconds before timing out for a connection while getting /info.json
        * This is passed through to :class:`sessions.Session`
    info_response_timeout_sec : int, optional
        * default: 15
        * number of seconds before timing out for a response while getting /info.json
        * This is passed through to :class:`sessions.Session`
    soap_connect_timeout_sec : int, optional
        * default: 15
        * number of seconds before timing out for a connection for a SOAP request
        * This is passed through to :class:`sessions.Session`
    soap_response_timeout_sec : int, optional
        * default: 540
        * number of seconds before timing out for a response for a SOAP request
        * This is passed through to :class:`sessions.Session`
    stats_loop_enabled : bool, optional
        * default: False
        * False: do not enable the statistics loop thread
        * True: enable the statistics loop thread
        * This is passed through to :class:`sessions.Session`
    stats_loop_sleep_sec : int, optional
        * default: 5
        * number of seconds to sleep in between printing the statistics when stats_loop_enabled is True
        * This is passed through to :class:`sessions.Session`
    record_all_requests: bool, optional
        * default: False
        * False: do not add each requests response object to session.ALL_REQUESTS_RESPONSES
        * True: add each requests response object to session.ALL_REQUESTS_RESPONSES
        * This is passed through to :class:`sessions.Session`
    stats_loop_targets : list of dict, optional
        * default: [{'Version': 'Settings/Version'}, {'Active Questions': 'Active Question Cache/Active Question Estimate'}, {'Clients': 'Active Question Cache/Active Client Estimate'}, {'Strings': 'String Cache/Total String Count'}, {'Handles': 'System Performance Info/HandleCount'}, {'Processes': 'System Performance Info/ProcessCount'}, {'Memory Available': 'percentage(System Performance Info/PhysicalAvailable,System Performance Info/PhysicalTotal)'}]
        * list of dictionaries with the key being the section of info.json to print info from, and the value being the item with in that section to print the value
        * This is passed through to :class:`sessions.Session`
    persistent: bool, optional
        * default: False
        * False: do not request a persistent session
        * True: do request a persistent
        * This is passed through to :func:`sessions.Session.authenticate`
    force_server_version: str, optional
        * default: ''
        * use this to override the server_version detection

    Notes
    -----
      * for 6.2: port 444 is the default SOAP port, port 443 forwards /soap/ URLs to the SOAP port,
        Use port 444 if you have direct access to it. However, port 444 is the only port that
        exposes the /info page in 6.2
      * for 6.5: port 443 is the default SOAP port, there is no port 444

    See Also
    --------
    :data:`constants.LOG_LEVEL_MAPS` : maps a given `loglevel` to respective logger names and their logger levels
    :data:`constants.INFO_FORMAT` : debugformat=False
    :data:`constants.DEBUG_FORMAT` : debugformat=True
    :class:`taniumpy.session.Session` : Session object used by Handler

    Examples
    --------
    Setup a Handler() object::

        >>> import sys
        >>> sys.path.append('/path/to/pytan/')
        >>> import pytan
        >>> handler = pytan.Handler('username', 'password', 'host')
    """

    def __init__(self, username=None, password=None, host=None, port=443,  # noqa
                 loglevel=0, debugformat=False, gmt_log=True, session_id=None, **kwargs):  # noqa
        super(Handler, self).__init__()
        self.mylog = logging.getLogger("pytan.handler")

        # update self with all local variables that are not self/kwargs/k/v
        for k, v in locals().iteritems():
            if k in ['self', 'kwargs', 'k', 'v']:
                continue
            setattr(self, k, v)

        # setup the console logging handler
        utils.setup_console_logging(gmt_tz=self.gmt_log)

        # create all the loggers and set their levels based on loglevel
        utils.set_log_levels(loglevel=int(self.loglevel))

        # change the format of console logging handler if need be
        utils.change_console_format(debug=self.debugformat)

        # get the default pytan user config file
        puc_default = os.path.expanduser(constants.PYTAN_USER_CONFIG)

        # see if the pytan_user_config file location was overridden
        puc_kwarg = kwargs.get('pytan_user_config', '')

        self.puc = puc_kwarg or puc_default
        kwargs = self.read_pytan_user_config(kwargs)

        if gmt_log != self.gmt_log:
            utils.setup_console_logging(gmt_tz=self.gmt_log)

        if loglevel != self.loglevel:
            utils.set_log_levels(loglevel=self.loglevel)

        if debugformat != self.debugformat:
            utils.change_console_format(debug=self.debugformat)

        if not self.session_id:

            if not self.username:
                raise exceptions.HandlerError("Must supply username!")

            if not self.password:
                raise exceptions.HandlerError("Must supply password!")

        if self.password:
            self.password = utils.vig_decode(constants.PYTAN_KEY, self.password)

        if not self.host:
            raise exceptions.HandlerError("Must supply host!")

        if not self.port:
            raise exceptions.HandlerError("Must supply port!")

        try:
            self.port = int(self.port)
        except ValueError:
            raise exceptions.HandlerError("port must be an integer!")

        utils.test_app_port(host=self.host, port=self.port)

        # establish our Session class
        self.session = sessions.Session(host=self.host, port=self.port, **kwargs)

        # authenticate using the Session class
        self.session.authenticate(
            username=self.username, password=self.password, session_id=self.session_id, **kwargs
        )

    def __str__(self):
        str_tpl = "PyTan v{} Handler for {}".format
        ret = str_tpl(version.__version__, self.session)
        return ret

    def read_pytan_user_config(self, kwargs):  # noqa
        """Read a PyTan User Config and update the current class variables

        Returns
        -------
        kwargs : dict
            * kwargs with updated variables from PyTan User Config (if any)
        """
        if not os.path.isfile(self.puc):
            m = "Unable to find PyTan User config file at: {}".format
            self.mylog.debug(m(self.puc))
            return kwargs

        try:
            with open(self.puc) as fh:
                puc_dict = json.load(fh)
        except Exception as e:
            m = "PyTan User config file at: {} is invalid, exception: {}".format
            self.mylog.error(m(self.puc, e))
        else:
            m = "PyTan User config file successfully loaded: {} ".format
            self.mylog.info(m(self.puc))

            # handle class params
            for h_arg, arg_default in constants.HANDLER_ARG_DEFAULTS.iteritems():
                if h_arg not in puc_dict:
                    continue

                if h_arg == 'password':
                    puc_dict['password'] = utils.vig_decode(
                        constants.PYTAN_KEY, puc_dict['password'],
                    )

                class_val = getattr(self, h_arg, None)
                puc_val = puc_dict[h_arg]

                if class_val != arg_default:
                    m = "User supplied argument for {}, ignoring value from: {}".format
                    self.mylog.debug(m(h_arg, self.puc))
                    continue

                if arg_default is None or puc_val != class_val:
                    m = "Setting class variable {} with value from: {}".format
                    self.mylog.debug(m(h_arg, self.puc))
                    setattr(self, h_arg, puc_val)

            # handle kwargs params
            for k, v in puc_dict.iteritems():
                if k in ['self', 'kwargs', 'k', 'v']:
                    m = "Skipping kwargs variable {} from: {}".format
                    self.mylog.debug(m(k, self.puc))
                    continue

                if not hasattr(self, k) and k not in kwargs:
                    m = "Setting kwargs variable {} with value from: {}".format
                    self.mylog.debug(m(k, self.puc))
                    kwargs[k] = v
        return kwargs

    def write_pytan_user_config(self, **kwargs):
        """Write a PyTan User Config with the current class variables for use with pytan_user_config in instantiating Handler()

        Parameters
        ----------
        pytan_user_config : str, optional
            * default: self.puc
            * JSON file to wite with current class variables

        Returns
        -------
        puc : str
            * filename of PyTan User Config that was written to
        """
        puc_kwarg = kwargs.get('pytan_user_config', '')
        puc = puc_kwarg or self.puc
        puc = os.path.expanduser(puc)

        puc_dict = {}

        for k, v in vars(self).iteritems():
            if k in ['mylog', 'methodlog', 'session', 'puc']:
                m = "Skipping class variable {} from inclusion in: {}".format
                self.mylog.debug(m(k, puc))
                continue

            m = "Including class variable {} in: {}".format
            self.mylog.debug(m(k, puc))
            puc_dict[k] = v

        # obfuscate the password
        puc_dict['password'] = utils.vig_encode(constants.PYTAN_KEY, self.password)

        try:
            with open(puc, 'w+') as fh:
                json.dump(puc_dict, fh, skipkeys=True, indent=2)
        except Exception as e:
            m = "Failed to write PyTan User config: '{}', exception: {}".format
            raise exceptions.HandlerError(m(puc, e))
        else:
            m = "PyTan User config file successfully written: {} ".format
            self.mylog.info(m(puc))
        return puc

    def get_server_version(self, **kwargs):
        """Uses :func:`taniumpy.session.Session.get_server_version` to get the version of the Tanium Server

        Returns
        -------
        server_version: str
            * Version of Tanium Server in string format
        """
        server_version = self.session.get_server_version(**kwargs)
        return server_version

    # Questions
    def ask(self, **kwargs):
        """Ask a type of question and get the results back

        Parameters
        ----------
        qtype : str, optional
            * default: 'manual'
            * type of question to ask: {'saved', 'manual', '_manual'}

        Returns
        -------
        result : dict, containing:
            * `question_object` : one of the following depending on `qtype`: :class:`taniumpy.object_types.question.Question` or :class:`taniumpy.object_types.saved_question.SavedQuestion`
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`

        See Also
        --------
        :data:`constants.Q_OBJ_MAP` : maps qtype to a method in Handler()
        :func:`pytan.handler.Handler.ask_saved` : method used when qtype == 'saved'
        :func:`pytan.handler.Handler.ask_manual` : method used when qtype == 'manual'
        :func:`pytan.handler.Handler._ask_manual` : method used when qtype == '_manual'
        """
        qtype = kwargs.get('qtype', 'manual')

        clean_keys = ['qtype']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        q_obj_map = utils.get_q_obj_map(qtype=qtype)

        method = getattr(self, q_obj_map['handler'])
        result = method(**clean_kwargs)
        return result

    def ask_saved(self, refresh_data=False, **kwargs):
        """Ask a saved question and get the results back

        Parameters
        ----------
        id : int, list of int, optional
            * id of saved question to ask
        name : str, list of str
            * name of saved question
        refresh_data: bool, optional
            * default False
            * False: do not perform a getResultInfo before issuing a getResultData
            * True: perform a getResultInfo before issuing a getResultData
        sse : bool, optional
            * default: False
            * True: perform a server side export when getting result data
            * False: perform a normal get result data (default for 6.2)
            * Keeping False by default for now until the columnset's are properly identified in the server export
        sse_format : str, optional
            * default: 'xml_obj'
            * format to have server side export report in, one of: {'csv', 'xml', 'xml_obj', 'cef', 0, 1, 2}
        leading : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to prepend to each row
        trailing : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to append to each row
        polling_secs : int, optional
            * default: 5
            * Number of seconds to wait in between GetResultInfo loops
            * This is passed through to :class:`pollers.QuestionPoller`
        complete_pct : int/float, optional
            * default: 99
            * Percentage of mr_tested out of estimated_total to consider the question "done"
            * This is passed through to :class:`pollers.QuestionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`pollers.QuestionPoller`
        callbacks : dict, optional
            * default: {}
            * can be a dict of functions to be run with the key names being the various state changes: 'ProgressChanged', 'AnswersChanged', 'AnswersComplete'
            * This is passed through to :func:`pollers.QuestionPoller.run`
        override_estimated_total : int, optional
            * instead of getting number of systems that should see this question from result_info.estimated_total, use this number
            * This is passed through to :func:`pollers.QuestionPoller`
        force_passed_done_count : int, optional
            * when this number of systems have passed the right hand side of the question, consider the question complete
            * This is passed through to :func:`pollers.QuestionPoller`

        Returns
        -------
        ret : dict, containing
            * `question_object` : :class:`taniumpy.object_types.saved_question.SavedQuestion`, the saved question object
            * `question_object` : :class:`taniumpy.object_types.question.Question`, the question asked by `saved_question_object`
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`, the results for `question_object`
            * `poller_object` : None if `refresh_data` == False, elsewise :class:`pollers.QuestionPoller`, poller object used to wait until all results are in before getting `question_results`,
            * `poller_success` : None if `refresh_data` == False, elsewise True or False

        Notes
        -----
        id or name must be supplied
        """
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs)
        sse = kwargs.get('sse', False)
        clean_kwargs['sse_format'] = clean_kwargs.get('sse_format', 'xml_obj')

        # get the saved_question object the user passed in
        h = "Issue a GetObject to find saved question objects"
        sq_objs = self.get(objtype='saved_question', pytan_help=h, **clean_kwargs)

        if len(sq_objs) != 1:
            err = (
                "Multiple saved questions returned, can only ask one "
                "saved question!\nArgs: {}\nReturned saved questions:\n\t{}"
            ).format
            sq_objstr = '\n\t'.join([str(x) for x in sq_objs])
            raise exceptions.HandlerError(err(kwargs, sq_objstr))

        sq_obj = sq_objs[0]

        h = (
            "Issue a GetObject to get the full object of the last question asked by a saved "
            "question"
        )
        q_obj = self._find(obj=sq_obj.question, pytan_help=h, **clean_kwargs)

        poller = None
        poller_success = None

        if refresh_data:
            # if GetResultInfo is issued on a saved question, Tanium will issue a new question
            # to fetch new/updated results
            h = (
                "Issue a GetResultInfo for a saved question in order to issue a new question, "
                "which refreshes the data for that saved question"
            )
            self.get_result_info(obj=sq_obj, pytan_help=h, **clean_kwargs)

            # re-fetch the saved question object to get the newly asked question info
            h = (
                "Issue a GetObject for the saved question in order get the ID of the newly "
                "asked question"
            )
            shrunk_obj = utils.shrink_obj(obj=sq_obj)
            sq_obj = self._find(obj=shrunk_obj, pytan_help=h, **clean_kwargs)

            h = (
                "Issue a GetObject to get the full object of the last question asked by a saved "
                "question"
            )
            q_obj = self._find(obj=sq_obj.question, pytan_help=h, **clean_kwargs)

            m = "Question Added, ID: {}, query text: {!r}, expires: {}".format
            self.mylog.debug(m(q_obj.id, q_obj.query_text, q_obj.expiration))

            # poll the new question for this saved question to wait for results
            poller = pollers.QuestionPoller(handler=self, obj=q_obj, **clean_kwargs)
            poller_success = poller.run(**clean_kwargs)

        # get the results
        if sse and self.session.platform_is_6_5(**clean_kwargs):
            h = (
                "Issue a GetResultData for a server side export to get the answers for the last "
                "asked question of this saved question"
            )

            rd = self.get_result_data_sse(obj=q_obj, pytan_help=h, **clean_kwargs)
        else:
            h = (
                "Issue a GetResultData to get the answers for the last asked question of "
                "this saved question"
            )
            rd = self.get_result_data(obj=q_obj, pytan_help=h, **clean_kwargs)

        if isinstance(rd, taniumpy.object_types.result_set.ResultSet):
            # add the sensors from this question to the ResultSet object for reporting
            rd.sensors = [x.sensor for x in q_obj.selects]

        ret = {
            'saved_question_object': sq_obj,
            'poller_object': poller,
            'poller_success': poller_success,
            'question_object': q_obj,
            'question_results': rd,
        }

        return ret

    def ask_manual(self, **kwargs):
        """Ask a manual question using human strings and get the results back

        This method takes a string or list of strings and parses them into
        their corresponding definitions needed by :func:`_ask_manual`

        Parameters
        ----------
        sensors : str, list of str
            * default: []
            * sensors (columns) to include in question
        question_filters : str, list of str, optional
            * default: []
            * filters that apply to the whole question
        question_options : str, list of str, optional
            * default: []
            * options that apply to the whole question
        get_results : bool, optional
            * default: True
            * True: wait for result completion after asking question
            * False: just ask the question and return it in result
        sensors_help : bool, optional
            * default: False
            * False: do not print the help string for sensors
            * True: print the help string for sensors and exit
        filters_help : bool, optional
            * default: False
            * False: do not print the help string for filters
            * True: print the help string for filters and exit
        options_help : bool, optional
            * default: False
            * False: do not print the help string for options
            * True: print the help string for options and exit
        polling_secs : int, optional
            * default: 5
            * Number of seconds to wait in between GetResultInfo loops
            * This is passed through to :class:`pollers.QuestionPoller`
        complete_pct : int/float, optional
            * default: 99
            * Percentage of mr_tested out of estimated_total to consider the question "done"
            * This is passed through to :class:`pollers.QuestionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`pollers.QuestionPoller`
        callbacks : dict, optional
            * default: {}
            * can be a dict of functions to be run with the key names being the various state changes: 'ProgressChanged', 'AnswersChanged', 'AnswersComplete'
            * This is passed through to :func:`pollers.QuestionPoller.run`
        override_estimated_total : int, optional
            * instead of getting number of systems that should see this question from result_info.estimated_total, use this number
            * This is passed through to :func:`pollers.QuestionPoller`
        force_passed_done_count : int, optional
            * when this number of systems have passed the right hand side of the question, consider the question complete
            * This is passed through to :func:`pollers.QuestionPoller`

        Returns
        -------
        result : dict, containing:
            * `question_object` : :class:`taniumpy.object_types.question.Question`, the actual question created and added by PyTan
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`, the Result Set for `question_object` if `get_results` == True
            * `poller_object` : :class:`pollers.QuestionPoller`, poller object used to wait until all results are in before getting `question_results`
            * `poller_success` : None if `get_results` == True, elsewise True or False

        Examples
        --------
        >>> # example of str for `sensors`
        >>> sensors = 'Sensor1'

        >>> # example of str for `sensors` with params
        >>> sensors = 'Sensor1{key:value}'

        >>> # example of str for `sensors` with params and filter
        >>> sensors = 'Sensor1{key:value}, that contains:example text'

        >>> # example of str for `sensors` with params and filter and options
        >>> sensors = (
        ...     'Sensor1{key:value}, that contains:example text,'
        ...     'opt:ignore_case, opt:max_data_age:60'
        ... )

        >>> # example of str for question_filters
        >>> question_filters = 'Sensor2, that contains:example test'

        >>> # example of list of str for question_options
        >>> question_options = ['max_data_age:3600', 'and']

        Notes
        -----

        When asking a question from the Tanium console, you construct a question like:

            Get Computer Name and IP Route Details from all machines with Is Windows containing "True"

        Asking the same question in PyTan has some similarities:

            >>> r = handler.ask_manual(sensors=['Computer Name', 'IP Route Details'], question_filters=['Is Windows, that contains:True'])

        There are two sensors in this question, after the "Get" and before the "from all machines": "Computer Name" and "IP Route Details". The sensors after the "Get" and before the "from all machines" can be referred to as any number of things:

            * sensors
            * left hand side
            * column selects

        The sensors that are defined after the "Get" and before the "from all machines" are best described as a column selection, and control what columns you want to show up in your results. These sensor names are the same ones that would need to be passed into ask_question() for the sensors arguments.

        You can filter your column selections by using a filter in the console like so:

            Get Computer Name starting with "finance" and IP Route Details from all machines with Is Windows containing "True"

        And in PyTan:

             >>> r = handler.ask_manual(sensors=['Computer Name, that starts with:finance', 'IP Route Details'], question_filters=['Is Windows, that contains:True'])

        This will cause the results to have the same number of columns, but for any machine that returns results that do not match the filter specified for a given sensor, the row for that column will contain "[no results]".

        There is also a sensor specified after the "from all machines with": "Is Windows". This sensor can be referred to as any number of things:

            * question filters
            * sensors (also)
            * right hand side
            * row selects

        Any system that does not match the conditions in the question filters will return no results at all.  These question filters are really just sensors all over again, but instead of controlling what columns are output in the results, they control what rows are output in the results.

        See Also
        --------
        :data:`constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`constants.OPTION_MAPS` : valid option dictionaries for options
        :func:`pytan.handler.Handler._ask_manual` : private method with the actual workflow used to create and add the question object
        """
        utils.check_for_help(kwargs=kwargs)

        sensors = kwargs.get('sensors', [])
        q_filters = kwargs.get('question_filters', [])
        q_options = kwargs.get('question_options', [])

        sensor_defs = utils.dehumanize_sensors(sensors=sensors)
        q_filter_defs = utils.dehumanize_question_filters(question_filters=q_filters)
        q_option_defs = utils.dehumanize_question_options(question_options=q_options)

        clean_keys = ['sensor_defs', 'question_filter_defs', 'question_option_defs']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        result = self._ask_manual(
            sensor_defs=sensor_defs,
            question_filter_defs=q_filter_defs,
            question_option_defs=q_option_defs,
            **clean_kwargs
        )
        return result

    def parse_query(self, question_text, **kwargs):
        """Ask a parsed question as `question_text` and get a list of parsed results back

        Parameters
        ----------
        question_text : str
            * The question text you want the server to parse into a list of parsed results

        Returns
        -------
        parse_job_results : :class:`taniumpy.object_types.parse_result_group.ParseResultGroup`
        """
        if not self.session.platform_is_6_5(**kwargs):
            m = "ParseJob not supported in version: {}".format
            m = m(self.session.server_version)
            raise exceptions.UnsupportedVersionError(m)

        parse_job = taniumpy.ParseJob()
        parse_job.question_text = question_text
        parse_job.parser_version = 2

        clean_keys = ['obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        parse_job_results = self.session.add(obj=parse_job, **clean_kwargs)
        return parse_job_results

    def ask_parsed(self, question_text, picker=None, get_results=True, **kwargs):  # noqa
        """Ask a parsed question as `question_text` and use the index of the parsed results from `picker`

        Parameters
        ----------
        question_text : str
            * The question text you want the server to parse into a list of parsed results
        picker : int
            * default: None
            * The index number of the parsed results that correlates to the actual question you wish to run
        get_results : bool, optional
            * default: True
            * True: wait for result completion after asking question
            * False: just ask the question and return it in `ret`
        sse : bool, optional
            * default: False
            * True: perform a server side export when getting result data
            * False: perform a normal get result data (default for 6.2)
            * Keeping False by default for now until the columnset's are properly identified in the server export
        sse_format : str, optional
            * default: 'xml_obj'
            * format to have server side export report in, one of: {'csv', 'xml', 'xml_obj', 'cef', 0, 1, 2}
        leading : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to prepend to each row
        trailing : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to append to each row
        polling_secs : int, optional
            * default: 5
            * Number of seconds to wait in between GetResultInfo loops
            * This is passed through to :class:`pollers.QuestionPoller`
        complete_pct : int/float, optional
            * default: 99
            * Percentage of mr_tested out of estimated_total to consider the question "done"
            * This is passed through to :class:`pollers.QuestionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`pollers.QuestionPoller`
        callbacks : dict, optional
            * default: {}
            * can be a dict of functions to be run with the key names being the various state changes: 'ProgressChanged', 'AnswersChanged', 'AnswersComplete'
            * This is passed through to :func:`pollers.QuestionPoller.run`
        override_estimated_total : int, optional
            * instead of getting number of systems that should see this question from result_info.estimated_total, use this number
            * This is passed through to :func:`pollers.QuestionPoller`
        force_passed_done_count : int, optional
            * when this number of systems have passed the right hand side of the question, consider the question complete
            * This is passed through to :func:`pollers.QuestionPoller`

        Returns
        -------
        ret : dict, containing:
            * `question_object` : :class:`taniumpy.object_types.question.Question`, the actual question added by PyTan
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`, the Result Set for `question_object` if `get_results` == True
            * `poller_object` : :class:`pollers.QuestionPoller`, poller object used to wait until all results are in before getting `question_results`
            * `poller_success` : None if `get_results` == True, elsewise True or False
            * `parse_results` : :class:`taniumpy.object_types.parse_result_group_list.ParseResultGroupList`, the parse result group returned from Tanium after parsing `question_text`

        Examples
        --------

        Ask the server to parse 'computer name', but don't pick a choice (will print out a list of choices at critical logging level and then throw an exception):
            >>> v = handler.ask_parsed('computer name')

        Ask the server to parse 'computer name' and pick index 1 as the question you want to run:
            >>> v = handler.ask_parsed('computer name', picker=1)
        """
        if not self.session.platform_is_6_5(**kwargs):
            m = "ParseJob not supported in version: {}".format
            m = m(self.session.server_version)
            raise exceptions.UnsupportedVersionError(m)

        clean_keys = ['obj', 'question_text', 'handler']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        sse = kwargs.get('sse', False)
        clean_kwargs['sse_format'] = clean_kwargs.get('sse_format', 'xml_obj')

        params = None
        # Stripping param values out of parsed question
        if '[' in question_text:
            params = [k.lower().split("[") for k in question_text.lower().split("]")]
            question_text = ''.join(params[i][0] for i in range(len(params) - 1))
        h = "Issue an AddObject to add a ParseJob for question_text and get back ParseResultGroups"
        parse_job_results = self.parse_query(
            question_text=question_text, pytan_help=h, **clean_kwargs
        )

        if not parse_job_results:
            m = (
                "Question Text '{}' was unable to be parsed into a valid query text by the server"
            ).format
            raise exceptions.ServerParseError(m())

        pi = "Index {0}, Score: {1}, Query: {2}".format
        pw = (
            "You must supply an index as picker=$index to choose one of the parse "
            "responses -- re-run ask_parsed with picker set to one of these indexes!!"
        ).format

        if picker is None:
            self.mylog.critical(pw())
            for idx, x in enumerate(parse_job_results):
                text = x.question_text.lower()
                if params:
                    for i in range(len(params) - 1):
                        text = text.replace(params[i][0], params[i][0] + '[' + params[i][1] + ']')
                self.mylog.critical(pi(idx + 1, x.score, text))
            raise exceptions.PickerError(pw())

        try:
            picked_parse_job = parse_job_results[picker - 1]
        except:
            invalid_pw = (
                "You supplied an invalid picker index {} - {}"
            ).format
            self.mylog.critical(invalid_pw(picker, pw))

            pi = "Index {0}, Score: {1}, Query: {2}"
            for idx, x in enumerate(parse_job_results):
                text = x.question_text.lower()
                if params:
                    for i in range(len(params) - 1):
                        text = text.replace(params[i][0], params[i][0] + '[' + params[i][1] + ']')
                self.mylog.critical(pi(idx + 1, x.score, text))
            raise exceptions.PickerError(pw())

        add_obj = picked_parse_job.question
        # TODO: BUILD PARAMETER KEY AND VALUE.  BELOW CONDITIONAL SERVES AS A REMINDER
        # if params:
        #    text = picked_parse_job.question_text.lower()
        #    for i in range(len(params) - 1):
        #        text = text.replace(params[i][0], params[i][0] + '[' + params[i][1] + ']')
        #    picked_parse_job.question.query_text = text

        # add our Question and get a Question ID back
        h = "Issue an AddObject to add the Question object from the chosen ParseResultGroup"
        added_obj = self._add(obj=add_obj, pytan_help=h, **clean_kwargs)

        m = "Question Added, ID: {}, query text: {!r}, expires: {}".format
        self.mylog.debug(m(added_obj.id, added_obj.query_text, added_obj.expiration))

        poller = pollers.QuestionPoller(handler=self, obj=added_obj, **clean_kwargs)

        ret = {
            'question_object': added_obj,
            'poller_object': poller,
            'question_results': None,
            'poller_success': None,
            'parse_results': parse_job_results,
        }

        if get_results:
            # poll the Question ID returned above to wait for results
            ret['poller_success'] = ret['poller_object'].run(**clean_kwargs)

            # get the results
            if sse:
                rd = self.get_result_data_sse(obj=added_obj, **clean_kwargs)
            else:
                rd = self.get_result_data(obj=added_obj, **clean_kwargs)

            if isinstance(rd, taniumpy.object_types.result_set.ResultSet):
                # add the sensors from this question to the ResultSet object for reporting
                rd.sensors = rd.sensors = [x.sensor for x in added_obj.selects]

            ret['question_results'] = rd
        return ret

    # Actions
    def deploy_action(self, **kwargs):
        """Deploy an action and get the results back

        This method takes a string or list of strings and parses them into
        their corresponding definitions needed by :func:`_deploy_action`

        Parameters
        ----------
        package : str
            * package to deploy with this action
        action_filters : str, list of str, optional
            * default: []
            * each string must describe a sensor and a filter which limits which computers the action will deploy `package` to
        action_options : str, list of str, optional
            * default: []
            * options to apply to `action_filters`
        start_seconds_from_now : int, optional
            * default: 0
            * start action N seconds from now
        distribute_seconds : int, optional
            * default: 0
            * distribute action evenly over clients over N seconds
        issue_seconds : int, optional
            * default: 0
            * have the server re-ask the action status question if performing a GetResultData over N seconds ago
        expire_seconds : int, optional
            * default: package.expire_seconds
            * expire action N seconds from now, will be derived from package if not supplied
        run : bool, optional
            * default: False
            * False: just ask the question that pertains to verify action, export the results to CSV, and raise exceptions.RunFalse -- does not deploy the action
            * True: actually deploy the action
        get_results : bool, optional
            * default: True
            * True: wait for result completion after deploying action
            * False: just deploy the action and return the object in `ret`
        action_name : str, optional
            * default: prepend package name with "API Deploy "
            * custom name for action
        action_comment : str, optional
            * default:
            * custom comment for action
        polling_secs : int, optional
            * default: 5
            * Number of seconds to wait in between GetResultInfo loops
            * This is passed through to :class:`pollers.ActionPoller`
        complete_pct : int/float, optional
            * default: 100
            * Percentage of passed_count out of successfully run actions to consider the action "done"
            * This is passed through to :class:`pollers.ActionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`pollers.ActionPoller`
        override_passed_count : int, optional
            * instead of getting number of systems that should run this action by asking a question, use this number
            * This is passed through to :class:`pollers.ActionPoller`

        Returns
        -------
        ret : dict, containing:
            * `saved_action_object` : :class:`taniumpy.object_types.saved_action.SavedAction`, the saved_action added for this action (None if 6.2)
            * `action_object` : :class:`taniumpy.object_types.action.Action`, the action object that tanium created for `saved_action`
            * `package_object` : :class:`taniumpy.object_types.package_spec.PackageSPec`, the package object used in `saved_action`
            * `action_info` : :class:`taniumpy.object_types.result_info.ResultInfo`, the initial GetResultInfo call done before getting results
            * `poller_object` : :class:`pollers.ActionPoller`, poller object used to wait until all results are in before getting `action_results`
            * `poller_success` : None if `get_results` == False, elsewise True or False
            * `action_results` : None if `get_results` == False, elsewise :class:`taniumpy.object_types.result_set.ResultSet`, the results for `action_object`
            * `action_result_map` : None if `get_results` == False, elsewise progress map for `action_object` in dictionary form

        Examples
        --------
        >>> # example of str for `package`
        >>> package = 'Package1'

        >>> # example of str for `package` with params
        >>> package = 'Package1{key:value}'

        >>> # example of str for `action_filters` with params and filter for sensors
        >>> action_filters = 'Sensor1{key:value}, that contains:example text'

        >>> # example of list of str for `action_options`
        >>> action_options = ['max_data_age:3600', 'and']

        See Also
        --------
        :data:`constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`constants.OPTION_MAPS` : valid option dictionaries for options
        :func:`pytan.handler.Handler._deploy_action` : private method with the actual workflow used to create and add the action object
        """
        utils.check_for_help(kwargs=kwargs)

        # the human string describing the sensors/filter that user wants
        # to deploy the action against
        action_filters = kwargs.get('action_filters', [])

        # the question options to use on the pre-action question and on the
        # group for the action filters
        action_options = kwargs.get('action_options', [])

        # name of package to deploy with params as {key=value1,key2=value2}
        package = kwargs.get('package', '')

        action_filter_defs = utils.dehumanize_sensors(action_filters, 'action_filters', True)
        action_option_defs = utils.dehumanize_question_options(action_options)
        package_def = utils.dehumanize_package(package)

        clean_keys = ['package_def', 'action_filter_defs', 'action_option_defs']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        deploy_result = self._deploy_action(
            action_filter_defs=action_filter_defs,
            action_option_defs=action_option_defs,
            package_def=package_def,
            **clean_kwargs
        )
        return deploy_result

    def approve_saved_action(self, id, **kwargs):
        """Approve a saved action

        Parameters
        ----------
        id : int
            * id of saved action to approve

        Returns
        -------
        saved_action_approve_obj : :class:`taniumpy.object_types.saved_action_approval.SavedActionApproval`
            * The object containing the return from SavedActionApproval
        """
        clean_keys = ['pytan_help', 'objtype', 'id', 'obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        h = "Issue a GetObject to find saved action objects"
        saved_action_obj = self.get(objtype='saved_action', id=id, pytan_help=h, **clean_kwargs)[0]

        add_sap_obj = taniumpy.SavedActionApproval()
        add_sap_obj.id = saved_action_obj.id
        add_sap_obj.approved_flag = 1

        # we dont want to re-fetch the object, so use sessions add instead of handlers add
        h = "Issue an AddObject to add a SavedActionApproval"
        sap_obj = self.session.add(obj=add_sap_obj, pytan_help=h, **clean_kwargs)

        m = 'Action approved successfully, ID of saved action : {}'.format
        self.mylog.debug(m(sap_obj.id))

        return sap_obj

    def stop_action(self, id, **kwargs):
        """Stop an action

        Parameters
        ----------
        id : int
            * id of action to stop

        Returns
        -------
        action_stop_obj : :class:`taniumpy.object_types.action_stop.ActionStop`
            The object containing the ID of the action stop job
        """
        clean_keys = ['pytan_help', 'objtype', 'id', 'obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        h = "Issue a GetObject to find the action object we want to stop"
        action_obj = self.get(objtype='action', id=id, pytan_help=h, **clean_kwargs)[0]

        add_action_stop_obj = taniumpy.ActionStop()
        add_action_stop_obj.action = action_obj

        h = "Issue an AddObject to add a StopAction"
        action_stop_obj = self.session.add(obj=add_action_stop_obj, pytan_help=h, **clean_kwargs)

        h = "Re-issue a GetObject to ensure the stopped_flag is 1"
        after_action_obj = self.get(objtype='action', id=id, pytan_help=h, **clean_kwargs)[0]

        if after_action_obj.stopped_flag:
            m = 'Action stopped successfully, ID of action stop: {}'.format
            self.mylog.debug(m(action_stop_obj.id))
        else:
            m = (
                "Action not stopped successfully, json of action after issuing StopAction: {}"
            ).format
            raise exceptions.HandlerError(m(self.export_obj(after_action_obj, 'json')))

        return action_stop_obj

    # Result Data / Result Info
    def get_result_data(self, obj, aggregate=False, shrink=True, **kwargs):
        """Get the result data for a python API object

        This method issues a GetResultData command to the SOAP api for `obj`. GetResultData returns the columns and rows that are currently available for `obj`.

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            * object to get result data for
        aggregate : bool, optional
            * default: False
            * False: get all the data
            * True: get just the aggregate data (row counts of matches)
        shrink : bool, optional
            * default: True
            * True: Shrink the object down to just id/name/hash attributes (for smaller request)
            * False: Use the full object as is

        Returns
        -------
        rd : :class:`taniumpy.object_types.result_set.ResultSet`
            The return of GetResultData for `obj`
        """

        """ note #1 from jwk:
        For Action GetResultData: You have to make a ResultInfo request at least once every 2 minutes. The server gathers the result data by asking a saved question. It won't re-issue the saved question unless you make a GetResultInfo request. When you make a GetResultInfo request, if there is no question that is less than 2 minutes old, the server will automatically reissue a new question instance to make sure fresh data is available.

        note #2 from jwk:
        To get the aggregate data (without computer names), set row_counts_only_flag = 1. To get the computer names, use row_counts_only_flag = 0 (default).
        """
        if shrink:
            shrunk_obj = utils.shrink_obj(obj=obj)
        else:
            shrunk_obj = obj

        kwargs['export_flag'] = utils.get_kwargs_int(key='export_flag', default=0, **kwargs)

        if kwargs['export_flag']:
            grd = self.session.get_result_data_sse
        else:
            grd = self.session.get_result_data

        h = "Issue a GetResultData to get answers for a question"
        kwargs['pytan_help'] = kwargs.get('pytan_help', h)
        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)

        if aggregate:
            kwargs['row_counts_only_flag'] = 1

        clean_keys = ['obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        # do a getresultdata
        rd = grd(obj=shrunk_obj, **clean_kwargs)

        return rd

    def get_result_data_sse(self, obj, **kwargs):
        """Get the result data for a python API object using a server side export (sse)

        This method issues a GetResultData command to the SOAP api for `obj` with the option
        `export_flag` set to 1. This will cause the server to process all of the data for a given
        result set and save it as `export_format`. Then the user can use an authenticated GET
        request to get the status of the file via "/export/${export_id}.status". Once the status
        returns "Completed.", the actual report file can be retrieved by an authenticated GET
        request to "/export/${export_id}.gz". This workflow saves a lot of processing time and removes the need to paginate large result sets necessary in normal GetResultData calls.

        *Version support*
            * 6.5.314.4231: initial sse support (csv only)
            * 6.5.314.4300: export_format support (adds xml and cef)
            * 6.5.314.4300: fix core dump if multiple sse done on empty resultset
            * 6.5.314.4300: fix no status file if sse done on empty resultset
            * 6.5.314.4300: fix response if more than two sse done in same second

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            * object to get result data for
        sse_format : str, optional
            * default: 'csv'
            * format to have server create report in, one of: {'csv', 'xml', 'xml_obj', 'cef', 0, 1, 2}
        leading : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to prepend to each row
        trailing : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to append to each row

        See Also
        --------
        :data:`constants.SSE_FORMAT_MAP` : maps `sse_format` to an integer for use by the SOAP API
        :data:`constants.SSE_RESTRICT_MAP` : maps sse_format integers to supported platform versions
        :data:`constants.SSE_CRASH_MAP` : maps platform versions that can cause issues in various scenarios

        Returns
        -------
        export_data : either `str` or :class:`taniumpy.object_types.result_set.ResultSet`
            * If sse_format is one of csv, xml, or cef, export_data will be a `str` containing the contents of the ResultSet in said format
            * If sse_format is xml_obj, export_data will be a :class:`taniumpy.object_types.result_set.ResultSet`
        """
        self._check_sse_version()
        self._check_sse_crash_prevention(obj=obj)

        sse_format = kwargs.get('sse_format', 'csv')
        sse_format_int = self._resolve_sse_format(sse_format=sse_format)

        # add the export_flag = 1 to the kwargs for inclusion in options node
        kwargs['export_flag'] = 1

        # add the export_format to the kwargs for inclusion in options node
        kwargs['export_format'] = sse_format_int

        # add the export_leading_text to the kwargs for inclusion in options node
        leading = kwargs.get('leading', '')
        if leading:
            kwargs['export_leading_text'] = leading

        # add the export_trailing_text to the kwargs for inclusion in options node
        trailing = kwargs.get('trailing', '')
        if trailing:
            kwargs['export_trailing_text'] = trailing

        clean_keys = [
            'obj', 'pytan_help', 'handler', 'export_id', 'leading', 'trailing', 'sse_format',
        ]
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        h = "Issue a GetResultData to start a Server Side Export and get an export_id"
        export_id = self.get_result_data(obj=obj, pytan_help=h, **clean_kwargs)

        m = "Server Side Export Started, id: '{}'".format
        self.mylog.debug(m(export_id))

        poller = pollers.SSEPoller(handler=self, export_id=export_id, **clean_kwargs)
        poller_success = poller.run(**clean_kwargs)

        if not poller_success:
            m = (
                "Server Side Export Poller failed while waiting for completion, last status: {}"
            ).format
            sse_status = getattr(poller, 'sse_status', 'Unknown')
            raise exceptions.ServerSideExportError(m(sse_status))

        export_data = poller.get_sse_data(**clean_kwargs)

        if sse_format.lower() == 'xml_obj':
            export_data = self.xml_to_result_set_obj(x=export_data)

        return export_data

    def xml_to_result_set_obj(self, x, **kwargs):
        """Wraps a Result Set XML from a server side export in the appropriate tags and returns a ResultSet object

        Parameters
        ----------
        x : str
            * str of XML to convert to a ResultSet object

        Returns
        -------
        rs : :class:`taniumpy.object_types.result_set.ResultSet`
            * x converted into a ResultSet object
        """
        rs_xml = '<result_sets><result_set>{}</result_set></result_sets>'.format
        rs_xml = rs_xml(x)
        rs_tree = sessions.ET.fromstring(rs_xml)
        rs = taniumpy.ResultSet.fromSOAPElement(rs_tree)
        rs._RAW_XML = rs_xml
        return rs

    def get_result_info(self, obj, shrink=True, **kwargs):
        """Get the result info for a python API object

        This method issues a GetResultInfo command to the SOAP api for `obj`. GetResultInfo returns information about how many servers have passed the `obj`, total number of servers, and so on.

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            * object to get result data for
        shrink : bool, optional
            * default: True
            * True: Shrink the object down to just id/name/hash attributes (for smaller request)
            * False: Use the full object as is

        Returns
        -------
        ri : :class:`taniumpy.object_types.result_info.ResultInfo`
            * The return of GetResultInfo for `obj`
        """
        if shrink:
            shrunk_obj = utils.shrink_obj(obj=obj)
        else:
            shrunk_obj = obj

        h = "Issue a GetResultData to get answers for a question"
        kwargs['pytan_help'] = kwargs.get('pytan_help', h)
        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)

        clean_keys = ['obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        ri = self.session.get_result_info(obj=shrunk_obj, **clean_kwargs)
        return ri

    # Objects
    def create_from_json(self, objtype, json_file, **kwargs):
        """Creates a new object using the SOAP api from a json file

        Parameters
        ----------
        objtype : str
            * Type of object described in `json_file`
        json_file : str
            * path to JSON file that describes an API object

        Returns
        -------
        ret : :class:`taniumpy.object_types.base.BaseType`
            * TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`constants.GET_OBJ_MAP` : maps objtype to supported 'create_json' types
        """
        obj_map = utils.get_obj_map(objtype=objtype)

        create_json_ok = obj_map['create_json']

        if not create_json_ok:
            json_createable = ', '.join([
                x for x, y in constants.GET_OBJ_MAP.items() if y['create_json']
            ])
            m = "{} is not a json createable object! Supported objects: {}".format
            raise exceptions.HandlerError(m(objtype, json_createable))

        add_obj = utils.load_taniumpy_from_json(json_file=json_file)

        if getattr(add_obj, '_list_properties', ''):
            obj_list = [x for x in add_obj]
        else:
            obj_list = [add_obj]

        del_keys = ['id', 'hash']
        [
            setattr(y, x, None)
            for y in obj_list for x in del_keys
            if hasattr(y, x)
        ]

        if obj_map.get('allfix'):
            all_type = obj_map['allfix']
        else:
            all_type = obj_map['all']

        ret = utils.get_taniumpy_obj(obj_map=all_type)()

        h = "Issue an AddObject to add an object"
        kwargs['pytan_help'] = kwargs.get('pytan_help', h)

        clean_keys = ['obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        for x in obj_list:
            try:
                list_obj = self._add(obj=x, **clean_kwargs)
            except Exception as e:
                m = (
                    "Failure while importing {}: {}\nJSON Dump of object: {}"
                ).format
                raise exceptions.HandlerError(m(x, e, x.to_json(x)))

            m = "New {} (ID: {}) created successfully!".format
            self.mylog.info(m(list_obj, getattr(list_obj, 'id', 'Unknown')))

            ret.append(list_obj)
        return ret

    def create_sensor(self, **kwargs):
        """Create a sensor object

        Warnings
        --------
        Not currently supported, too complicated to add.
        Use :func:`create_from_json` instead for this object type!

        Raises
        ------
        exceptions.HandlerError : :exc:`utils.exceptions.HandlerError`
        """
        m = (
            "Sensor creation not supported via PyTan as of yet, too complex\n"
            "Use create_sensor_from_json() instead!"
        )
        raise exceptions.HandlerError(m)

    def create_package(self, name, command, display_name='', file_urls=[],
                       command_timeout_seconds=600, expire_seconds=600, parameters_json_file='',
                       verify_filters=[], verify_filter_options=[], verify_expire_seconds=600,
                       **kwargs):
        """Create a package object

        Parameters
        ----------
        name : str
            * name of package to create
        command : str
            * command to execute
        display_name : str, optional
            * display name of package
        file_urls : list of strings, optional
            * default: []
            * URL of file to add to package
            * can optionally define download_seconds by using SECONDS::URL
            * can optionally define file name by using FILENAME||URL
            * can combine optionals by using SECONDS::FILENAME||URL
            * FILENAME will be extracted from basename of URL if not provided
        command_timeout_seconds : int, optional
            * default: 600
            * timeout for command execution in seconds
        parameters_json_file : str, optional
            * default: ''
            * path to json file describing parameters for package
        expire_seconds : int, optional
            * default: 600
            * timeout for action expiry in seconds
        verify_filters : str or list of str, optional
            * default: []
            * each string must describe a filter to be used to verify the package
        verify_filter_options : str or list of str, optional
            * default: []
            * each string must describe an option for `verify_filters`
        verify_expire_seconds : int, optional
            * default: 600
            * timeout for verify action expiry in seconds
        filters_help : bool, optional
            * default: False
            * False: do not print the help string for filters
            * True: print the help string for filters and exit
        options_help : bool, optional
            * default: False
            * False: do not print the help string for options
            * True: print the help string for options and exit
        metadata: list of list of strs, optional
            * default: []
            * each list must be a 2 item list:
            * list item 1 property name
            * list item 2 property value

        Returns
        -------
        package_obj : :class:`taniumpy.object_types.package_spec.PackageSpec`
            * TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`constants.FILTER_MAPS` : valid filters for verify_filters
        :data:`constants.OPTION_MAPS` : valid options for verify_filter_options
        """
        utils.check_for_help(kwargs=kwargs)

        clean_keys = ['obj', 'pytan_help', 'defs']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        metadata = kwargs.get('metadata', [])
        metadatalist_obj = utils.build_metadatalist_obj(properties=metadata)

        # bare minimum arguments for new package: name, command
        add_package_obj = taniumpy.PackageSpec()
        add_package_obj.name = name
        if display_name:
            add_package_obj.display_name = display_name
        add_package_obj.command = command
        add_package_obj.command_timeout = command_timeout_seconds
        add_package_obj.expire_seconds = expire_seconds
        add_package_obj.metadata = metadatalist_obj

        # VERIFY FILTERS
        if verify_filters:
            verify_filter_defs = utils.dehumanize_question_filters(
                question_filters=verify_filters
            )
            verify_option_defs = utils.dehumanize_question_options(
                question_options=verify_filter_options
            )
            verify_filter_defs = self._get_sensor_defs(defs=verify_filter_defs, **clean_kwargs)
            add_verify_group = utils.build_group_obj(
                q_filter_defs=verify_filter_defs, q_option_defs=verify_option_defs
            )
            h = "Issue an AddObject to add a Group object for this package"
            verify_group = self._add(obj=add_verify_group, pytan_help=h, **clean_kwargs)

            # this didn't work:
            # add_package_obj.verify_group = verify_group
            add_package_obj.verify_group_id = verify_group.id
            add_package_obj.verify_expire_seconds = verify_expire_seconds

        # PARAMETERS
        if parameters_json_file:
            add_package_obj.parameter_definition = utils.load_param_json_file(
                parameters_json_file=parameters_json_file
            )

        # FILES
        if file_urls:
            filelist_obj = taniumpy.PackageFileList()
            for file_url in file_urls:
                # if :: is in file_url, split on it and use 0 as
                # download_seconds
                if '::' in file_url:
                    download_seconds, file_url = file_url.split('::')
                else:
                    download_seconds = 0
                # if || is in file_url, split on it and use 0 as file name
                # else wise get file name from basename of URL
                if '||' in file_url:
                    filename, file_url = file_url.split('||')
                else:
                    filename = os.path.basename(file_url)
                file_obj = taniumpy.PackageFile()
                file_obj.name = filename
                file_obj.source = file_url
                file_obj.download_seconds = download_seconds
                filelist_obj.append(file_obj)
            add_package_obj.files = filelist_obj

        h = "Issue an AddObject to add a Group object for this package"
        package_obj = self._add(obj=add_package_obj, pytan_help=h, **clean_kwargs)

        m = "New package {!r} created with ID {!r}, command: {!r}".format
        self.mylog.info(m(package_obj.name, package_obj.id, package_obj.command))
        return package_obj

    def create_group(self, groupname, filters=[], filter_options=[], **kwargs):
        """Create a group object

        Parameters
        ----------
        groupname : str
            * name of group to create
        filters : str or list of str, optional
            * default: []
            * each string must describe a filter
        filter_options : str or list of str, optional
            * default: []
            * each string must describe an option for `filters`
        filters_help : bool, optional
            * default: False
            * False: do not print the help string for filters
            * True: print the help string for filters and exit
        options_help : bool, optional
            * default: False
            * False: do not print the help string for options
            * True: print the help string for options and exit

        Returns
        -------
        group_obj : :class:`taniumpy.object_types.group.Group`
            * TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`constants.FILTER_MAPS` : valid filters for filters
        :data:`constants.OPTION_MAPS` : valid options for filter_options
        """
        utils.check_for_help(kwargs=kwargs)
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs)

        filter_defs = utils.dehumanize_question_filters(question_filters=filters)
        option_defs = utils.dehumanize_question_options(question_options=filter_options)

        h = (
            "Issue a GetObject to get the full object of specified sensors for inclusion in a "
            "group"
        )
        filter_defs = self._get_sensor_defs(defs=filter_defs, pytan_help=h, **clean_kwargs)

        add_group_obj = utils.build_group_obj(
            q_filter_defs=filter_defs, q_option_defs=option_defs,
        )
        add_group_obj.name = groupname

        h = "Issue an AddObject to add a Group object"
        group_obj = self._add(obj=add_group_obj, pytan_help=h, **clean_kwargs)

        m = "New group {!r} created with ID {!r}, filter text: {!r}".format
        self.mylog.info(m(group_obj.name, group_obj.id, group_obj.text))

        return group_obj

    def create_user(self, name, rolename=[], roleid=[], properties=[], group='', **kwargs):
        """Create a user object

        Parameters
        ----------
        name : str
            * name of user to create
        rolename : str or list of str, optional
            * default: []
            * name(s) of roles to add to user
        roleid : int or list of int, optional
            * default: []
            * id(s) of roles to add to user
        properties: list of list of strs, optional
            * default: []
            * each list must be a 2 item list:
            * list item 1 property name
            * list item 2 property value
        group: str
            * default: ''
            * name of group to assign to user

        Returns
        -------
        user_obj : :class:`taniumpy.object_types.user.User`
            * TaniumPy object added to Tanium SOAP Server
        """
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs)

        # get the ID for the group if a name was passed in
        if group:
            h = "Issue a GetObject to find the ID of a group name"
            group_id = self.get(objtype='group', name=group, pytan_help=h, **clean_kwargs)[0].id
        else:
            group_id = None

        if roleid or rolename:
            h = "Issue a GetObject to find a user role"
            rolelist_obj = self.get(objtype='userrole', id=roleid, name=rolename, pytan_help=h, **clean_kwargs)
        else:
            rolelist_obj = taniumpy.RoleList()

        metadatalist_obj = utils.build_metadatalist_obj(
            properties=properties, nameprefix='TConsole.User.Property',
        )
        add_user_obj = taniumpy.User()
        add_user_obj.name = name
        add_user_obj.roles = rolelist_obj
        add_user_obj.metadata = metadatalist_obj
        add_user_obj.group_id = group_id

        h = "Issue an AddObject to add a User object"
        user_obj = self._add(obj=add_user_obj, pytan_help=h, **clean_kwargs)

        m = "New user {!r} created with ID {!r}, roles: {!r}".format
        self.mylog.info(m(
            user_obj.name, user_obj.id, [x.name for x in rolelist_obj]
        ))
        return user_obj

    def create_whitelisted_url(self, url, regex=False, download_seconds=86400, properties=[],
                               **kwargs):
        """Create a whitelisted url object

        Parameters
        ----------
        url : str
            * text of new url
        regex : bool, optional
            * default: False
            * False: `url` is not a regex pattern
            * True: `url` is a regex pattern
        download_seconds : int, optional
            * default: 86400
            * how often to re-download `url`
        properties: list of list of strs, optional
            * default: []
            * each list must be a 2 item list:
            * list item 1 property name
            * list item 2 property value

        Returns
        -------
        url_obj : :class:`taniumpy.object_types.white_listed_url.WhiteListedUrl`
            * TaniumPy object added to Tanium SOAP Server
        """
        if regex:
            url = 'regex:' + url

        metadatalist_obj = utils.build_metadatalist_obj(
            properties=properties, nameprefix='TConsole.WhitelistedURL',
        )

        add_url_obj = taniumpy.WhiteListedUrl()
        add_url_obj.url_regex = url
        add_url_obj.download_seconds = download_seconds
        add_url_obj.metadata = metadatalist_obj

        clean_kwargs = utils.clean_kwargs(kwargs=kwargs)

        h = "Issue an AddObject to add a WhitelistedURL object"
        url_obj = self._add(obj=add_url_obj, pytan_help=h, **clean_kwargs)

        m = "New Whitelisted URL {!r} created with ID {!r}".format
        self.mylog.info(m(url_obj.url_regex, url_obj.id))
        return url_obj

    def delete(self, objtype, **kwargs):
        """Delete an object type

        Parameters
        ----------
        objtype : string
            * type of object to delete
        id/name/hash : int or string, list of int or string
            * search attributes of object to delete, must supply at least one valid search attr

        Returns
        -------
        ret : dict
            * dict containing deploy action object and results from deploy action

        See Also
        --------
        :data:`constants.GET_OBJ_MAP` : maps objtype to supported 'search' keys
        """
        obj_map = utils.get_obj_map(objtype=objtype)

        delete_ok = obj_map['delete']

        clean_kwargs = utils.clean_kwargs(kwargs=kwargs)

        if not delete_ok:
            deletable = ', '.join([
                x for x, y in constants.GET_OBJ_MAP.items() if y['delete']
            ])
            m = "{} is not a deletable object! Deletable objects: {}".format
            raise exceptions.HandlerError(m(objtype, deletable))

        h = "Issue a GetObject to find the object to be deleted"
        objs_to_del = self.get(objtype=objtype, pytan_help=h, **clean_kwargs)

        deleted_objects = []
        for obj_to_del in objs_to_del:
            h = "Issue a DeleteObject to delete an object"
            del_obj = self.session.delete(obj=obj_to_del, pytan_help=h, **clean_kwargs)

            deleted_objects.append(del_obj)

            m = "Deleted {!r}".format
            self.mylog.info(m(str(del_obj)))

        return deleted_objects

    def get(self, objtype, **kwargs):  # noqa
        """Get an object type

        Parameters
        ----------
        objtype : string
            * type of object to get
        id/name/hash : int or string, list of int or string
            * search attributes of object to get, must supply at least one valid search attr

        Returns
        -------
        obj_list : :class:`taniumpy.object_types.base.BaseType`
            * The object list of items found for `objtype`

        See Also
        --------
        :data:`constants.GET_OBJ_MAP` : maps objtype to supported 'search' keys
        :func:`pytan.handler.Handler._get_multi` : private method used to get multiple items
        :func:`pytan.handler.Handler._get_single` : private method used to get singular items
        """
        h = "Issue a GetObject to find an object"
        kwargs['pytan_help'] = kwargs.get('pytan_help', h)

        clean_keys = ['obj', 'objtype', 'obj_map']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        err_keys = ['pytan_help']
        err_args = utils.clean_kwargs(kwargs=kwargs, keys=err_keys)

        obj_map = utils.get_obj_map(objtype=objtype)

        manual_search = obj_map['manual']
        api_attrs = obj_map['search']

        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]

        # if the api doesn't support filtering for this object,
        # or if the user didn't supply any api_kwattrs and manual_search
        # is true, get all objects of this type and manually filter
        if not api_attrs or (not any(api_kwattrs) and manual_search):
            all_objs = self.get_all(objtype=objtype, **clean_kwargs)

            return_objs = getattr(taniumpy, all_objs.__class__.__name__)()

            for k, v in kwargs.iteritems():
                if not v:
                    continue
                if not hasattr(all_objs[0], k):
                    continue
                if not utils.is_list(v):
                    v = [v]
                for aobj in all_objs:
                    aobj_val = getattr(aobj, k)
                    aobj_val_str = str(aobj_val)
                    if aobj_val not in v and aobj_val_str not in v:
                        continue
                    return_objs.append(aobj)

            if not return_objs:
                err = "No results found searching for {} with {}!!".format
                raise exceptions.HandlerError(err(objtype, err_args))

            return return_objs

        # if api supports filtering for this object,
        # but no filters supplied in kwargs, raise
        if not any(api_kwattrs):
            err = "Getting a {} requires at least one filter: {}".format
            raise exceptions.HandlerError(err(objtype, api_attrs))

        # if there is a multi in obj_map, that means we can pass a list
        # type to the taniumpy. the list will have an entry for each api_kw
        if obj_map['multi']:
            return self._get_multi(obj_map=obj_map, **clean_kwargs)

        # if there is a single in obj_map but not multi, that means
        # we have to find each object individually
        elif obj_map['single']:
            return self._get_single(obj_map=obj_map, **clean_kwargs)

        err = "No single or multi search defined for {}".format
        raise exceptions.HandlerError(err(objtype))

    def get_all(self, objtype, **kwargs):
        """Get all objects of a type

        Parameters
        ----------
        objtype : string
            * type of object to get

        Returns
        -------
        obj_list : :class:`taniumpy.object_types.base.BaseType`
            * The object list of items found for `objtype`

        See Also
        --------
        :data:`constants.GET_OBJ_MAP` : maps objtype to supported 'search' keys
        :func:`pytan.handler.Handler._find` : private method used to find items
        """
        h = "Issue a GetObject to find an object"
        kwargs['pytan_help'] = kwargs.get('pytan_help', h)

        clean_keys = ['obj', 'objtype', 'obj_map']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        obj_map = utils.get_obj_map(objtype=objtype)

        all_type = obj_map['all']
        api_obj_all = utils.get_taniumpy_obj(obj_map=all_type)()

        found = self._find(obj=api_obj_all, **clean_kwargs)
        return found

    # DOC, TEST
    # ADDED: 3.0.0
    def get_id_from_session_id(self, session_id):
        try:
            ret = int(session_id.split('-')[0])
        except Exception as e:
            m = "Unable to parse user ID from session ID '{s}', error: {e}"
            m = m.format(s=session_id, e=e)
            raise exceptions.HandlerError(m)

        m = "Parsed user ID '{i}' from session ID: '{s}'"
        m = m.format(i=ret, s=session_id)
        self.mylog.debug(m)
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def get_this_user_id(self):
        """Get the user ID from handler.session.session_id."""
        ret = self.get_id_from_session_id(session_id=self.session.session_id)
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def get_this_user_obj(self):
        """Fetch the user info for user ID."""
        user_id = self.get_this_user_id()
        obj = self.build_obj(obj_name="User", attrs={"id": user_id})

        try:
            ret = self._find(obj)
        except Exception as e:
            m = "Failed to find {o}, error: {e}"
            m = m.format(o=obj, e=e)
            raise exceptions.HandlerError(m)

        m = "Successfully retrieved {o}".format(o=obj)
        self.mylog.debug(m)
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # TODO: add user_has_allowed_permission
    # TODO: add user_has_required_permission
    # ADDED: 3.0.0
    def user_has_allowed_roles(self, obj, allowed_roles, **kwargs):
        """Validate that the roles for user are in allowed_roles."""
        error = kwargs.get("error", True)

        ret = []
        roles_txt = joiner(allowed_roles)
        allowed_roles_lower = [str(x).lower() for x in allowed_roles]

        for role_obj in obj.roles:
            role_name = str(role_obj.name).lower()
            if role_name in allowed_roles_lower:
                ret.append(role_obj.name)
            else:
                m = "{r} attached to {o} is not allowed! Allowed roles: {t}"
                m = m.format(r=role_obj, o=obj, t=roles_txt)
                if error:
                    raise exceptions.PermissionError(m)
                else:
                    self.mylog.warning(m)

        if ret:
            m = "{o} has allowed roles: {t}"
            m = m.format(o=obj, t=joiner(ret))
            self.mylog.info(m)
        else:
            m = "{o} has none of the allowed roles: {t}"
            m = m.format(o=obj, t=roles_txt)
            if error:
                raise exceptions.PermissionError(m)
            else:
                self.mylog.warning(m)
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def user_has_required_role(self, obj, role, **kwargs):
        """Validate that one of the roles for user equals role."""
        error = kwargs.get("error", True)
        ret = False

        for role_obj in obj.roles:
            if str(role_obj.name).lower() == str(role).lower():
                ret = True

        if ret:
            m = "{o} has required role: {r}"
            m = m.format(o=obj, r=role)
            self.mylog.info(m)
        else:
            m = "{o} does not have required role: {r}"
            m = m.format(o=obj, r=role)
            if error:
                raise exceptions.PermissionError(m)
            else:
                self.mylog.warning(m)
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def this_user_is_admin(self, **kwargs):
        role = kwargs.get("role", "Administrator")
        obj = self.get_this_user_obj()
        margs = kwmerge(kwargs, obj=obj, role=role)
        ret = self.user_has_required_role(**margs)
        return ret

    # TODO: NEEDS ERROR HANDLING
    # DOC, TEST
    # ADDED: 3.0.0
    def build_obj(self, obj_name="", attrs={}, obj_class=None):
        """
        name = "User"
        attrs = {"name": "Administrator", "roles": [{"name": "Administrator"}]}
        """
        # print(locals())
        if obj_class:
            ret = obj_class()
        elif obj_name:
            ret = getattr(taniumpy, obj_name)()
        else:
            raise Exception()

        ta = "Built"

        if ret._list_properties:
            # raise Exception() if not isinstance(attrs, (list, tuple, dict)) else None
            # print("in list")
            attrs = mklist(attrs)
            list_attr, item_class = ret._list_properties.items()[0]
            list_items = []
            # print(attrs)
            for sub_attrs in attrs:
                list_item = self.build_obj(obj_class=item_class, attrs=sub_attrs)
                ret._track_merge(other=list_item)
                list_items.append(list_item)
            if list_items:
                setattr(ret, list_attr, list_items)
                ret._track(t_attr=list_attr, t_old=attrs, t_new=list_items, t_action=ta)
            return ret

        # raise Exception() if not isinstance(attrs, (dict)) else None
        for attr, val in attrs.items():
            if attr in ret._simple_properties:
                # print("in simple")
                # val needs to be a str/int
                new_val = val
            elif attr in ret._complex_properties:
                # print("in complex")
                # val needs to be a dict for complex type
                # val needs to be a list of dict for multiple list items
                complex_class = ret._complex_properties[attr]
                new_val = self.build_obj(attrs=val, obj_class=complex_class)
                ret._track_merge(other=new_val)
            else:
                # ???
                raise Exception()

            setattr(ret, attr, new_val)
            ret._track(t_attr=attr, t_old=val, t_new=new_val, t_action=ta)

        ret._build_attrs = attrs
        ret._track(t_attr="Build attributes", t_new=attrs, t_action=ta)
        return ret

    # ADDED: 3.0.0
    # DOC, TEST
    def build_params_obj(self, obj, params, delimiter=""):
        """Creates a ParameterList object from params."""
        ret = taniumpy.ParameterList()

        # extract the params from the object
        obj._PARAM_DEF = getattr(obj, "parameter_definition", "{}") or "{}"
        obj._PARAM_DEF = json.loads(obj._PARAM_DEF) if obj._PARAM_DEF else obj._PARAM_DEF
        obj._PARAMS = obj._PARAM_DEF.get("parameters", []) if obj._PARAM_DEF else [] or []

        for p in obj._PARAMS:
            p_key = p["key"]
            p_default = p.get("defaultValue", "")
            p_values = p.get("values", [])
            p_value = p_values[0] if p_values else ""
            default_value = p_default or p_value

            key = "{d}{k}{d}".format(d=delimiter, k=p_key)
            value = params.get(p_key, "")
            value = default_value if not value and constants.DERIVE_PARAMETER_DEFAULTS else value

            if not value and not constants.EMPTY_PARAMETER_VALUES_OK:
                m = "Parameter key '{k}' for object {o} requires a value, parameter definition:\n{d}"
                m = m.format(k=p_key, o=obj, d=pprint.pformat(p))
                raise exceptions.HandlerError(m)

            value = "" if value == "__EMPTY__" else value

            param_obj = self.build_obj(obj_name="Parameter", attrs={"key": key, "value": value})
            ret.append(param_obj)

            m = "Object Parameter key '{k}' for object {o} mapped to: {p}"
            m = m.format(k=p_key, o=obj, p=param_obj)
            utils.manuallog.debug(m)

        processed = [x["key"] for x in obj._PARAMS]

        # ADD SUPPORT FOR PARAMS THAT ARE NOT IN OBJECT
        for k, v in params.iteritems():
            if k not in processed:
                processed.append(k)

                key = "{d}{k}{d}".format(d=delimiter, k=k)
                param_obj = self.build_obj(obj_name="Parameter", attrs={"key": key, "value": v})
                ret.append(param_obj)

                m = "Non-object Parameter key '{k}' for object {o} mapped to: {p}"
                m = m.format(k=p_key, o=obj, p=param_obj)
                utils.manuallog.debug(m)
        return ret

    # ADDED: 3.0.0
    # DOC, TEST
    def build_group_buckets(self, buckets, **kwargs):
        default_bucket = constants.DEFAULT_BUCKET

        ret = self.build_obj(obj_name="Group", attrs={"sub_groups": [], "filters": []})
        ret._BUCKET = default_bucket
        ret._SPEC = buckets.pop(default_bucket) if default_bucket in buckets else {}

        bucket_items = sorted([(k, v) for k, v in buckets.items() if not k.startswith("_")])

        for bucket, spec in bucket_items:
            print(bucket)
            print(spec)
        return buckets

    def build_group_obj(self, group_obj, filters, options, groups):
        ret = self.build_obj(obj_name="Group", attrs={"sub_groups": [], "filters": []})

        for this_filter in filters:
            filter_obj = self.build_filter_obj(sensor_def=this_filter)
            sensor_obj = this_filter["obj"]
            params = this_filter.get("params", {})

            param_objs = self.build_params_obj(obj=sensor_obj, params=params, delimiter="||")

            if param_objs:
                filter_obj.sensor.name = sensor_obj.name
                filter_obj.sensor.source_id = sensor_obj.id
                filter_obj.sensor.parameter_definition = sensor_obj.parameter_definition
                filter_obj.sensor.parameters = param_objs
            else:
                filter_obj.sensor.hash = sensor_obj.hash

            # filter_obj = utils.apply_options_obj(options, filter_obj, "filter")
            # filter_objs.filter.append(filter_obj)

        # ret.filters = filter_objs
        ret = utils.apply_options_obj(options, ret, "group")
        return ret

    # ADDED: 3.0.0
    # DOC, TEST
    def build_filter_obj(self, sensor_def):
        """Creates a Filter object from sensor_def."""
        if "obj" not in sensor_def:
            m = "No sensor object available in filter dictionary: {f}"
            m = m.format(f=sensor_def)
            raise exceptions.DefinitionParserError(m)

        sensor_obj = sensor_def["obj"]

        # create our basic filter that is needed no matter what
        ret = self.build_obj(obj_name="Filter", attrs={"sensor": {"hash": sensor_obj.hash}})

        # get the filter the user supplied
        filter_def = sensor_def.get("filter", {})

        # if user supplied filter options, parse the filter options
        if filter_def:
            op = filter_def.get("operator", "")  # operator required
            value = filter_def.get("value", "")  # value required
            not_flag = filter_def.get("not_flag", None)  # not_flag optional
            match = [x for x in constants.FILTER_MAPS if op.lower() == x["operator"].lower()]

            if not op:
                m = "Filter {f!r} requires an 'operator' key in sensor definition:\n{s}"
                m = m.format(f=filter_def, s=pprint.pformat(sensor_def))
                raise exceptions.DefinitionParserError(m)

            if not value:
                m = "Filter {f!r} requires a 'value' key in sensor definition:\n{s}"
                m = m.format(f=filter_def, s=pprint.pformat(sensor_def))
                raise exceptions.DefinitionParserError(m)

            if not match:
                m = "Operator {o!r} in filter {f!r} is invalid in sensor definition:\n{s}"
                m = m.format(o=op, f=filter_def, s=pprint.pformat(sensor_def))
                raise exceptions.DefinitionParserError(m)

            match = match[0]
            ret.value = value
            ret.operator = match["operator"]
            ret.not_flag = not_flag

            m = "Operator {o!r} in filter {f!r} mapped to filter obj {fo!r}"
            m = m.format(o=op, f=filter_def, fo=ret)
            utils.parselog(m)

        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def get_all_objs(self, objtype, **kwargs):
        obj = get_bt_obj(objtype=objtype)
        obj_info = get_obj_info(obj=obj)

        if obj_info["is_basetype"]:
            tries = [
                {"tryobj": obj_info["list_obj"], "f": "List Object"},
                {"tryobj": obj_info["item_obj"], "f": "Item Object"},
            ]

            ret = None
            exc = None

            for trydict in tries:
                tryobj = trydict["tryobj"]
                margs = kwmerge(kwargs, obj=tryobj)

                try:
                    ret = self.session.find(**margs)
                except Exception as exc:
                    m = "Trying to GetObject using '{f} {o}' failed: {e}"
                    m = m.format(f=trydict["f"], o=tryobj, e=exc)
                    self.mylog.debug(m)

                if ret is not None:
                    break

            if ret is None and exc:
                raise exc

            m = "Got all objects of type '{t}' using GetObject on {o}, result: {r}"
            m = m.format(t=objtype, o=tryobj, r=ret)
            self.mylog.debug(m)
        elif obj_info["is_wraptype"]:
            method_name = obj_info["get_method"]
            method = getattr(self, method_name)
            ret = method(**kwargs)
        return ret

    # DOC, TEST
    # SHELL SCRIPT???
    # ADDED: 3.0.0
    def search_add_obj(self, objtype, searches, **kwargs):
        objs = kwargs.get("objs", None)

        objs = self.get_all_objs(**kwmerge(kwargs, objtype=objtype)) if objs is None else objs
        margs = kwmerge(kwargs, searches=searches, objs=objs, limit_max=1, limit_exact=1, limit_shrink=True)

        try:
            ret = self.search_objs(**margs)
        except exceptions.NotFoundError as exc:
            ret = self.create_missing_obj(**kwmerge(kwargs, searches=searches, objs=objs, exc=exc))
            ret._ADDED = True
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def create_missing_obj(self, objs, searches, **kwargs):
        attrs = kwargs.get("attrs", {})
        create_missing = kwargs.get("create_missing", True)
        delete_existing = kwargs.get("delete_existing", False)
        # exc = kwargs.get("exc", None)  # Not used as of yet

        searches = mklist(searches)
        search = searches[0]
        search_is_simple = is_simple_str(**kwmerge(kwargs, string=search))

        obj_info = get_obj_info(objs)
        tmpls = {}
        tmpls.update(a=attrs, s=search, ss=searches, iname=obj_info["item_name"])
        tmpls["i"] = "a {iname} object named '{s}' using attributes: {a}".format(**tmpls)
        tmpls["c"] = "create_missing={t}".format(t=create_missing)
        tmpls["d"] = "delete_existing={t}".format(t=delete_existing)

        if create_missing and not attrs:
            m = "{c}, but no build attributes supplied, can not create {i}".format(**tmpls)
            self.mylog.error(m)
            raise exceptions.HandlerError(m)

        if create_missing and delete_existing:
            m = "{c} and {d}, will not create then delete {i}".format(**tmpls)
            self.mylog.error(m)
            raise exceptions.HandlerError(m)

        if create_missing and not search_is_simple:
            m = "{c}, but '{s}' is not a simple search string, will not create {i}".format(**tmpls)
            self.mylog.error(m)
            raise exceptions.HandlerError(m)

        if create_missing and attrs:
            m = "Creating {i}".format(**tmpls)
            self.mylog.debug(m)

            if obj_info["is_basetype"]:
                obj = self.build_obj(obj_class=obj_info["item_class"], attrs=attrs)
                margs = kwmerge(kwargs, obj=obj)
                ret = self.add_obj(**margs)
            elif obj_info["is_wraptype"]:
                method_name = obj_info["create_method"]
                method = getattr(self, method_name)
                margs = kwmerge(kwargs, search_precheck=False, **attrs)
                ret = method(**margs)
            else:
                m = "Unexpected type supplied to create_missing_obj!"
                raise exceptions.HandlerError(m)

            m = "Created {i} {o}".format(o=ret, **tmpls)
            self.mylog.debug(m)
        else:
            m = "{c} and no object found using searches {ss}, will not create {i}".format(**tmpls)
            self.mylog.error(m)
            raise exceptions.NotFoundError(m)
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def search_obj(self, obj, search, **kwargs):
        # support FOR "id::2", "name::foo", or "any_attribute::any_value"
        # if no unescaped "::"" in search, search "name" attribute by default
        use_regex = kwargs.get("use_regex", True)
        exact_regex = kwargs.get("exact_regex", True)
        case_sensitive = kwargs.get("case_sensitive", False)
        default_search_attr = kwargs.get("default_search_attr", "name")

        search = str(search) if case_sensitive else str(search).lower()

        if SEARCH_RE.search(search):
            attr, search = SEARCH_RE.split(search)
        else:
            attr, search = (default_search_attr, search)

        value = str(getattr(obj, attr, ""))
        value = value if case_sensitive else value.lower()

        ret, msg = (False, "")

        if search == value:
            ret = True
            msg = "'{s}' equals '{a}'".format(s=search, a=attr)

        if not ret and use_regex:
            regex = re_exact(search) if exact_regex else search
            re_args = (regex, value) if case_sensitive else (regex, value, re.I)

            try:
                ret = re.match(*re_args)
            except Exception as e:
                ret = False
                msg = "'{r}' regex failed '{a}': '{v}', error: {e}"
                msg = msg.format(r=regex, a=attr, v=value, e=e)
                self.mylog.exception(msg)
            else:
                ok = "'{r}' regex matches '{a}': '{v}'"
                bad = "'{r}' regex does not match '{a}': '{v}'"
                msg = ok if ret else bad
                msg = msg.format(r=regex, a=attr, v=value)

        if not ret and not msg:
            msg = "'{s}' does not match '{a}': '{v}'"
            msg = msg.format(s=search, a=attr, v=value)
        return ret, msg

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def search_objs(self, objs, **kwargs):
        """
        objs = list of taniumpy objs
        searches = list of str, name or 'attr:value' to search for in objs
        use_regex = bool, try to find objects using regex against name
        exact_regex = bool, surround search with ^$ when using regex
        case_sensitive = bool, try to find objects matching exact case or not
        # limit_min
        # limit_max
        # limit_exact
        # limit_shrink
        """
        searches = mklist(kwargs.get("searches", []))
        excludes = mklist(kwargs.get("excludes", []))
        limit_exact = kwargs.get("limit_exact", None)
        limit_shrink = kwargs.get("limit_shrink", True)
        search_debug = kwargs.get("search_debug", False)
        refetch = kwargs.get("refetch", False)
        pre_refetch = kwargs.get("pre_refetch", False)

        debug_log = self.mylog.debug if search_debug else lambda *x: None
        obj_info = get_obj_info(obj=objs)
        list_obj = obj_info["list_obj"]
        list_attr = obj_info["list_attr"]

        objs_list = getattr(objs, list_attr)
        new_list = [self.session.find(x) for x in objs_list] if pre_refetch else objs_list
        setattr(objs, list_attr, new_list)

        ret = list_obj
        ret._SEARCH_KWARGS = kwargs

        if (excludes and not searches):
            for obj in objs:
                obj = self.session.find(obj) if refetch and not pre_refetch else obj
                ret.append(obj)

        m = "Searching with searches {s} and excludes {e} against {o}, arguments: {k}"
        m = m.format(s=searches, e=excludes, o=objs, k=kwargs)
        debug_log(m)

        for search in searches:
            for obj in objs:
                check, msg = self.search_obj(**kwmerge(kwargs, obj=obj, search=search))
                found = "Matched" if check else "Did not match"
                added = "added" if check and obj not in ret else "did not add"
                if check and obj not in ret:
                    obj = self.session.find(obj) if refetch and not pre_refetch else obj
                    ret.append(obj)
                m = "{f} search '{s}', {a}: {o} ({m})".format(f=found, a=added, s=search, o=obj, m=msg)
                debug_log(m)

        for exclude in excludes:
            for obj in list(ret):
                check, msg = self.search_obj(**kwmerge(kwargs, obj=obj, search=exclude))
                found = "Matched" if check else "Did not match"
                added = "removed" if check and obj not in ret else "did not remove"
                if check and obj in ret:
                    getattr(ret, list_attr).remove(obj)
                m = "{f} exclude '{e}', {a}: {o} ({m})".format(f=found, e=exclude, a=added, o=obj, m=msg)
                debug_log(m)

        margs = kwmerge(kwargs, ret=ret, objs=objs, searches=searches, excludes=excludes)
        self.check_limits(**margs)

        ret = ret[0] if limit_exact == 1 and limit_shrink else ret
        ret._track_merge(other=objs)

        m = "FOUND: {r} (from {o}) using searches {s} and excludes {e}"
        m = m.format(s=searches, e=excludes, r=ret, o=objs)
        debug_log(m)
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def search_all_objs(self, objtype, searches, **kwargs):
        objs = kwargs.get("objs", None)

        margs = kwmerge(kwargs, objtype=objtype)
        ret = objs or self.get_all_objs(**margs)

        margs = kwmerge(kwargs, objs=ret, searches=searches)
        ret = self.search_objs(**margs)
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def check_limits(self, ret, objs, **kwargs):
        searches = kwargs.get("searches", [])
        excludes = kwargs.get("excludes", [])
        search_debug = kwargs.get("search_debug", False)

        found_items = "Found Items: {o}".format(o=join_list_attrs(ret))
        all_items = "All Items: {o}".format(o=join_list_attrs(objs))

        debug_log = self.mylog.debug if search_debug else lambda *x: None
        t = "Check {k} [{r}] {ret} must be {l} {m} ({e}) using searches {se}, excludes {ex}".format

        limit_maps = constants.CHECK_LIMIT_MAPS
        for limit_map in limit_maps:
            key = limit_map["key"]
            expr = limit_map["expr"]
            msg = limit_map["msg"]
            exc = getattr(exceptions, limit_map["exc"])
            limit = kwargs.get(key, 0)

            if key not in kwargs:
                r = "SKIPPED"
                m = t(k=key, r=r, ret=ret, l=limit, m=msg, e=expr, se=searches, ex=excludes)
                debug_log(m)
                continue

            limit = int(kwargs[key])
            eval_str = "len(ret) {e} limit".format(e=expr)
            check = eval(eval_str)
            msg = msg.format(v=limit)

            if check:
                r = "PASSED"
                m = t(k=key, r=r, ret=ret, l=limit, m=msg, e=expr, se=searches, ex=excludes)
                self.mylog.debug(m)
            else:
                r = "FAILED"
                m = t(k=key, r=r, ret=ret, l=limit, m=msg, e=expr, se=searches, ex=excludes)
                items = found_items if ret else all_items
                m = "{m} - {i}".format(m=m, i=items)
                raise exc(m)

    # DOC, TEST
    # ADDED: 3.0.0
    def run_plugin_obj(self, name, bundle, arguments=[], **kwargs):
        attrs = {"name": name, "bundle": bundle, "arguments": arguments}
        obj = self.build_obj(obj_name="Plugin", attrs=attrs)

        m = "Built Plugin Request: {o}"
        m = m.format(o=obj.str_obj(str_items=True, str_all_attrs=True))
        self.mylog.debug(m)

        margs = kwmerge(kwargs, obj=obj)
        ret = self.session.run_plugin(**margs)
        ret._track_merge(other=obj)
        ret._PLUGIN_REQUEST = obj

        m = "Received Plugin Response"
        ret._track(t_old=obj, t_new=ret, t_action=m, str_all_attrs=True)

        columns = ret.sql_response.columns
        rows = ret.sql_response.result_row

        m = "Received plugin response object: {o} with {c} columns and {r} rows"
        m = m.format(o=ret, c=len(columns), r=len(rows))
        self.mylog.debug(m)

        # crunch sql_response into a list of dicts, should work for all plugins
        try:
            ret._LOD = [dict(zip(columns, x)) for x in rows]
        except Exception as e:
            m = "Failed to create a list of dicts from plugin response: {o} from plugin request {r} error: {e}"
            m = m.format(o=ret, r=obj, e=e)
            raise exceptions.HandlerError(m)
        else:
            m = "Crunched plugin response columns and rows into {l} dicts"
            m = m.format(l=len(ret._LOD))
            self.mylog.debug(m)
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def log_tracker(self, obj, **kwargs):
        log_line_limit = kwargs.get("log_line_limit", 100)
        log_include_build = kwargs.get("log_include_build", False)
        log_include_plugin = kwargs.get("log_include_plugin", False)

        tracker = obj._get_tracker
        if not tracker:
            m = "No Changes made to: {o}".format(o=obj.str_obj(**kwargs))
            self.mylog.info(m)

        for track in tracker:
            if track["action"].lower() in ["build", "built"] and not log_include_build:
                continue
            if "received plugin" in track["action"].lower() and not log_include_plugin:
                continue
            if track.get("already_logged", False):
                continue
            track["already_logged"] = True
            m = "{action} {obj}".format(**track)
            m += " attribute '{attr}'".format(**track) if track["attr"] else ""
            m += "{{sep1}}OLD: {old}".format(**track) if track["old"] else ""
            m += "{{sep2}}NEW: {new}".format(**track) if track["new"] else ""

            use_multiline = len(m) >= log_line_limit
            sep1 = "\n * " if use_multiline else " "
            sep2 = "\n * " if use_multiline else ", "
            m = m.format(sep1=sep1, sep2=sep2)
            self.mylog.info(m)

    # DOC, TEST
    # ADDED: 3.0.0
    def add_obj(self, obj, **kwargs):
        margs = kwmerge(kwargs, obj=obj)
        added_obj = self.session.add(**margs)

        margs = kwmerge(kwargs, obj=added_obj)
        ret = self.session.find(**margs)

        ret._track_merge(other=obj)
        ret._track(t_action="Added new")
        ret._ADDED = True
        ret._ORIGINAL_OBJ = obj
        ret._ADDED_OBJ = added_obj
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def delete_obj(self, obj, **kwargs):
        objinfo = get_obj_info(obj)

        if objinfo["is_basetype"]:
            margs = kwmerge(kwargs, obj=obj)
            ret = self.session.delete(**margs)
            ret._track_merge(other=obj)
            ret._track(t_action="Deleted")

        elif objinfo["is_wraptype"]:
            method_name = objinfo["delete_method"]
            method = getattr(self, method_name)
            margs = kwmerge(kwargs, obj=obj)
            ret = method(**margs)
            ret._track_merge(other=obj)

        ret._DELETED = True
        ret._ORIGINAL_OBJ = obj
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def save_changed_obj(self, obj, **kwargs):
        if obj._CHANGED:
            margs = kwmerge(kwargs, obj=obj)
            ret = self.session.save(**margs)

            ret._track_merge(other=obj, other_first=True)
            t_action = "Saved changes to"
            ret._track(t_action=t_action)
            ret._CHANGED = True
            ret._ORIGINAL_OBJ = obj
        else:
            ret = obj
            ret._track(t_action="No changes made to")
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def save_changed_obj_ag(self, obj, **kwargs):
        if obj._CHANGED:
            g_obj = getattr(obj, "computer_group", None)
            g_sub_objs = getattr(g_obj, "sub_groups", [])

            if len(g_sub_objs) == 0:
                m = "Unable to save {o}, no computer groups specified!"
                m = m.format(o=obj)
                raise exceptions.HandlerError(m)

            try:
                d_obj = self.delete_obj(**kwmerge(kwargs, obj=obj))
            except:
                pass
            else:
                obj._track_merge(other=d_obj)

            try:
                d_obj = self.delete_obj(**kwmerge(kwargs, obj=obj.computer_group))
            except:
                pass
            else:
                obj._track_merge(other=d_obj)

            obj.computer_group.name = obj.name
            obj.computer_group.type = 1
            obj.computer_group.and_flag = obj.and_flag
            obj.computer_group.id = None
            obj.computer_group = self.add_obj(**kwmerge(kwargs, obj=obj.computer_group))
            obj._track_merge(other=obj.computer_group)

            pargs = [
                {"name": "group_id", "type": "Number", "value": obj.computer_group.id},
                {"name": "user_group_xml", "type": "String", "value": obj.user_groups_xml()},
                {"name": "public_flag", "type": "Number", "value": obj.public_flag},
            ]

            margs = {"bundle": "GroupFilter", "name": "AddActionGroup", "arguments": pargs}
            pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

            margs = kwmerge(kwargs, objtype="ActionGroup", searches=obj.name, limit_exact=1)
            ret = self.search_all_objs(**margs)
            ret._track_merge(other=pret, other_first=True)
            ret._track_merge(other=obj, other_first=True)
            ret._track(t_action="Added new")
            ret._PLUGIN_RETURN = pret
            ret._CHANGED = True
        else:
            ret = obj
            ret._track(t_action="No changes made to")
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def save_changed_obj_ug(self, obj, **kwargs):
        if obj._CHANGED:
            pargs = [
                {"name": "user_group_name", "type": "String", "value": obj.name},
                {"name": "user_group_id", "type": "Number", "value": obj.id},
                {"name": "user_xml", "type": "String", "value": obj.users_xml()},
            ]

            margs = {"bundle": "UserGroups", "name": "UpdateUserGroup", "arguments": pargs}
            pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

            margs = kwmerge(kwargs, objtype="UserGroup", searches=obj.name, limit_exact=1)
            ret = self.search_all_objs(**margs)
            ret._track_merge(other=pret, other_first=True)
            ret._track_merge(other=obj, other_first=True)
            ret._track(t_action="Saved changes to")
            ret._PLUGIN_RETURN = pret
            ret._CHANGED = True
        else:
            ret = obj
            ret._track(t_action="No changes made to")
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def save_changed_obj_db(self, obj, **kwargs):
        if obj._CHANGED:
            pargs = [
                {"name": "dash_id", "type": "Number", "value": obj.id},
                {"name": "dash_name", "type": "String", "value": obj.name},
                {"name": "dash_text", "type": "String", "value": ""},
                {"name": "group_id", "type": "Number", "value": obj.computer_group.id},
                {"name": "public_flag", "type": "Number", "value": obj.public_flag},
                {"name": "sqid_xml", "type": "String", "value": obj.saved_questions_xml()},
            ]

            margs = {"bundle": "Dashboards", "name": "UpdateDashboard", "arguments": pargs}
            pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

            margs = kwmerge(kwargs, objtype="Dashboard", searches=obj.name, limit_exact=1)
            ret = self.search_all_objs(**margs)
            ret._track_merge(other=pret, other_first=True)
            ret._track_merge(other=obj, other_first=True)
            ret._track(t_action="Saved changes to")
            ret._PLUGIN_RETURN = pret
            ret._CHANGED = True
        else:
            ret = obj
            ret._track(t_action="No changes made to")
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def save_changed_obj_dbc(self, obj, **kwargs):
        if obj._CHANGED:
            pargs = [
                {"name": "content_group_id", "type": "Number", "value": obj.id},
                {"name": "name", "type": "String", "value": obj.name},
                {"name": "text", "type": "String", "value": ""},
                {"name": "user_id", "type": "Number", "value": obj.user.id},
                {"name": "icon", "type": "String", "value": obj.icon.encode},
                {"name": "public_flag", "type": "Number", "value": obj.public_flag},
                {"name": "editable_flag", "type": "Number", "value": obj.editable_flag},
                {"name": "other_flag", "type": "Number", "value": obj.other_flag},
                {"name": "dashboard_list_xml", "type": "String", "value": obj.dashboard_xml()},
                {"name": "user_group_xml", "type": "String", "value": obj.user_groups_xml()},
            ]

            margs = {"bundle": "DashboardGroups", "name": "UpdateContentGroup", "arguments": pargs}
            pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

            margs = kwmerge(kwargs, objtype="DashboardCategory", searches=obj.name, limit_exact=1)
            ret = self.search_all_objs(**margs)
            ret._track_merge(other=pret, other_first=True)
            ret._track_merge(other=obj, other_first=True)
            ret._track(t_action="Saved changes to")
            ret._PLUGIN_RETURN = pret
            ret._CHANGED = True
        else:
            ret = obj
            ret._track(t_action="No changes made to")
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def save_changed_obj_ugs(self, objs, **kwargs):
        this_s = kwargs.get("searches", [])
        this_e = kwargs.get("excludes", [])

        ret = objs.__class__()
        ret._track_merge(other=objs)
        if not objs:
            t_action = "No User Groups found matching searches {s} and excludes {e}"
            t_action = t_action.format(s=this_s, e=this_e)
            ret._track(t_action=t_action)

        for obj in objs:
            obj = self.save_changed_obj_ug(**kwmerge(kwargs, obj=obj))
            ret._track_merge(other=obj)
            ret.append(obj)
        ret._CHANGED = any([x._CHANGED for x in ret]) or ret._CHANGED
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def get_group_members_by_id(self, group_id, **kwargs):
        objs = kwargs.get("objs", None)

        objs = self.get_all_objs(objtype="Group") if objs is None else objs

        ret = self.build_obj("GroupList")
        ret._IS_MERGED = False
        ret.group = [self.build_obj("Group", attrs={"id": 0, "name": "All Groups"})]

        if group_id == 0:
            ret._MSG = "Computer Group is ID 0, has access to 'All Groups'"
        else:
            searches = ["id:{i}".format(i=group_id)]

            try:
                ret._OBJ_FOUND = self.search_objs(objs=objs, searches=searches, limit_exact=1, use_regex=False)
            except exceptions.NotFoundError:
                m = "Unable to find a pre-existing Computer Group with an ID of {i}, access unknown!"
                ret._MSG = m.format(i=group_id)
            else:
                ret._IS_MERGED = True if re.match("mrgroup_.*", ret._OBJ_FOUND.name) else False

                if ret._IS_MERGED:
                    ret.group = []
                    for x in ret._OBJ_FOUND.sub_groups:
                        if x not in ret.group:
                            ret.group.append(x)
                else:
                    ret.group = [ret._OBJ_FOUND]

                grpjoin = "\n   " if len(ret.group) > 1 else ""
                grps = grpjoin.join([str(x) for x in ret.group])
                m = "{o} (Merged: {im}) has access to {l} groups:\n   {g}"
                ret._MSG = m.format(o=ret._OBJ_FOUND, im=ret._IS_MERGED, l=len(ret.group), g=grps)
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def get_group_members_by_searches(self, **kwargs):
        searches = mklist(kwargs.get("searches", []))
        excludes = mklist(kwargs.get("excludes", []))
        objs = kwargs.get("objs", None)

        objs = self.get_all_objs(objtype="Group") if objs is None else objs

        ret = self.build_obj("GroupList")
        ret._IS_MERGED = False
        ret._IS_ALL = True
        ret._ROOT_GROUP = self.build_obj("Group", attrs={"id": 0, "name": "All Groups"})
        ret._OBJS_FOUND = []
        ret._OBJS_REAL = self.search_objs(objs=objs, excludes="mrgroup_.*", exact_regex=False)
        ret._MSG = "No Computer Groups supplied, will have access to 'All Groups'"
        ret.group = [ret._ROOT_GROUP]

        if searches:
            margs = kwmerge(kwargs, objs=ret._OBJS_REAL, searches=searches, excludes=excludes)
            ret._OBJS_FOUND = self.search_objs(**margs)

            if len(ret._OBJS_FOUND) == 0:
                # ret._OBJS_FOUND is empty, so new group membership will be All Groups
                m = "No Computer Groups found matching {s}, will have access to {g}"
                ret._MSG = m.format(s=searches, g=ret.group)
            elif len(ret._OBJS_FOUND) == 1:
                # ret._OBJS_FOUND == 1, so new group membership will be the found group
                obj_found = ret._OBJS_FOUND[0]

                ret._ROOT_GROUP = obj_found
                ret._IS_ALL = False
                ret.group = [x for x in ret._OBJS_FOUND]

                m = "Computer Groups matching {s} is {l}, will have access to {g}"
                ret._MSG = m.format(s=searches, l=len(ret.group), g=ret.group)
            else:
                # ret._OBJS_FOUND > 1, so new group membership will a merged group of all found groups
                # build a set of attrs for a new merged group if one does not exist
                ids_found = ",".join(list_objs_attr(objs=ret._OBJS_FOUND, attr="id"))
                merged_name = "mrgroup_{i}".format(i=ids_found)
                sub_groups = [{"id": x.id} for x in ret._OBJS_FOUND]
                attrs = {"name": merged_name, "and_flag": 0, "sub_groups": sub_groups}

                # find the merged group in objs or add it using attrs
                margs = kwmerge(kwargs, objtype="Group", searches=[merged_name], attrs=attrs, objs=objs)
                obj_mr = self.search_add_obj(**margs)

                ret.group = [x for x in ret._OBJS_FOUND]
                ret._ROOT_GROUP = obj_mr
                ret._IS_MERGED = True
                ret._IS_ALL = True

                case = "Added new" if ret._ADDED else "Found pre-existing"
                grpjoin = "\n   " if len(ret.group) > 1 else ""
                grps = grpjoin.join([str(x) for x in ret.group])
                m = "Computer Groups matching {s} is {l}, {c} merged {o} with access to groups:\n   {g}"
                ret._MSG = m.format(s=searches, l=len(ret.group), g=grps, c=case, o=obj_mr)
        return ret

    # TODO: RE-FIGURE
    # ADDED: 3.0.0
    def get_min_packagelist(self, **kwargs):
        packages = kwargs.get("packages", [])
        ret = taniumpy.PackageSpecList()
        for p in packages:
            min_obj = taniumpy.PackageSpec()
            min_obj.name = p
            try:
                full_obj = self.session.find(min_obj)
            except:
                m = "Unable to find package named: '{}'"
                m = m.format(p)
                raise exceptions.HandlerError(m)
            min_obj.id = full_obj.id
            ret.append(min_obj)
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def get_user_groups(self, **kwargs):
        include_deleted = kwargs.get("include_deleted", False)
        user_objs = kwargs.get("user_objs", None)

        user_objs = self.get_all_objs("User") if user_objs is None else user_objs

        margs = {"bundle": "UserGroups", "name": "GetUserGroups"}
        ug_pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))
        # {'user_id': '75', 'id': '10', 'user_deleted_flag': '0', 'name': 'Test Group'}
        # {'user_id': '76', 'id': '10', 'user_deleted_flag': '0', 'name': 'Test Group'}

        # collapse individual user ids into lists of user ids keyed off group id
        margs = kwmerge({}, lod=ug_pret._LOD, key="id", attr="user_id")
        margs["skip_map"] = {} if include_deleted else {"user_deleted_flag": "1"}
        coll_lod = collapse_lod(**margs)
        # {'user_ids': [75, 76], 'id': 10, 'name': 'Test Group'}

        m = "Collapsed {b} plugin response dicts into {a} dicts"
        m = m.format(b=len(ug_pret._LOD), a=len(coll_lod))
        self.mylog.debug(m)

        # create a user group list object to store user groups objects in
        ret = taniumpy.UserGroupList()
        ret._UG_PLUGIN_RETURN = ug_pret
        ret._track_merge(other=ug_pret)
        usargs = {"objs": user_objs, "excludes": [], "default_search_attr": "id", "use_regex": False}

        # churn user ids into user objs, create user group objects, and append user group objects to ret
        for lod in coll_lod:
            obj = taniumpy.UserGroup()
            obj.id = int(lod["id"])
            obj.name = lod["name"]
            obj.users = self.search_objs(**kwmerge(usargs, searches=lod["user_ids"]))
            ret.append(obj)

        m = "Retrieved {l} User Groups"
        m = m.format(l=len(ret))
        self.mylog.debug(m)
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def get_dashboard_categories(self, **kwargs):
        """
        Dashboard Category UI Constructs:
        - Name
        - Icon
        - Visibility:
        -   Only current user can see this category
        -   Only administrators can see this category
        -   All users can see this category
        -   Specific User Groups can see this category
        - Dashboards: list of dashboards
        """
        # this is the "categories" section, icon information and such
        margs = kwmerge(kwargs, bundle="DashboardGroups", name="GetContentGroups")
        cat_pret = self.run_plugin_obj(**margs)
        # {'user_id': '0', 'name': 'Tanium Administration', 'public_flag': '0', 'editable_flag': '1',
        #  'text': None, 'other_flag': '0', 'user_name': None, 'id': '4', 'icon': '..b64text..'}

        # this is the dashboards that exist in each category
        margs = kwmerge(kwargs, bundle="DashboardGroups", name="GetContentGroupsDashboards")
        cat_dash_pret = self.run_plugin_obj(**margs)
        # {'dashboard_id': '41', 'content_group_id': '11'}
        # {'dashboard_id': '42', 'content_group_id': '11'}

        # correlates to Categories: Visibility: Specific User Groups can see this category
        margs = kwmerge(kwargs, bundle="DashboardGroups", name="GetContentGroupsUserGroups")
        cat_ug_pret = self.run_plugin_obj(**margs)
        # {'user_group_id': '33', 'content_group_id': '15'}
        # {'user_group_id': '28', 'content_group_id': '15'}

        db_objs = self.get_all_objs("Dashboard")
        db_sargs = {"objs": db_objs, "excludes": [], "default_search_attr": "id", "use_regex": False}
        ug_objs = self.get_all_objs("UserGroup")
        ug_sargs = {"objs": ug_objs, "excludes": [], "default_search_attr": "id", "use_regex": False}
        u_objs = self.get_all_objs("User")
        u_sargs = {"objs": u_objs, "limit_exact": 1, "default_search_attr": "id", "use_regex": False}

        ret = taniumpy.DashboardCategoryList()
        ret._CAT_PLUGIN_RETURN = cat_pret
        ret._CAT_DASH_PLUGIN_RETURN = cat_dash_pret
        ret._CAT_UG_PLUGIN_RETURN = cat_ug_pret
        ret._track_merge(other=cat_pret)
        ret._track_merge(other=cat_dash_pret)
        ret._track_merge(other=cat_ug_pret)

        for lod in sorted(cat_pret._LOD, key=lambda x: x["name"]):
            db_lods = [x for x in cat_dash_pret._LOD if int(x["content_group_id"]) == int(lod["id"])]
            db_ids = [x["dashboard_id"] for x in db_lods]

            ug_lods = [x for x in cat_ug_pret._LOD if int(x["content_group_id"]) == int(lod["id"])]
            ug_ids = [x["user_group_id"] for x in ug_lods]

            all_u_obj = self.build_obj("User", attrs={"id": 0, "name": "All Users"})
            all_u_id = lod["user_id"] == "0"
            u_obj = all_u_obj if all_u_id else self.search_objs(**kwmerge(u_sargs, searches=lod["user_id"]))

            obj = taniumpy.DashboardCategory()
            obj.id = int(lod["id"])
            obj.name = lod["name"]
            obj.public_flag = int(lod["public_flag"])
            obj.other_flag = int(lod["other_flag"])
            obj.editable_flag = int(lod["editable_flag"])
            obj.user = u_obj
            obj.icon = taniumpy.Image(lod["icon"])
            obj.user_groups = self.search_objs(**kwmerge(ug_sargs, searches=ug_ids))
            obj.dashboards = self.search_objs(**kwmerge(db_sargs, searches=db_ids))
            ret.append(obj)

        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def get_dashboards(self, **kwargs):
        """
        Dashboard UI Constructs:
        - Name
        - Filter Computer Group: (single select?) ==> group_id
        - Make dashboard visibile to all users (checkbox) ==> public_flag
        - Saved questions: list of saved questions
        """
        # this is all of the dashboards themselves, but none of their content
        margs = kwmerge(kwargs, bundle="Dashboards", name="GetDashboards")
        dash_pret = self.run_plugin_obj(**margs)
        # {'user_id': '1', 'name': 'VMware Guest CPU and Memory',
        #  'public_flag': '1', 'text': None, 'group_id': '0', 'user_name': 'Administrator', 'id': '41'}

        # actual SQ correlation to dashboards, as well as SQ sort order in dashboard
        margs = kwmerge(kwargs, bundle="Dashboards", name="GetDashboardSQIndices")
        dash_sq_pret = self.run_plugin_obj(**margs)
        # {'dashboard_id': '41', 'saved_question_id': '249', 'dashboard_index': '2'}
        # {'dashboard_id': '41', 'saved_question_id': '250', 'dashboard_index': '1'}

        sq_objs = self.get_all_objs("SavedQuestion")
        sq_sargs = {"objs": sq_objs, "default_search_attr": "id", "use_regex": False}
        u_objs = self.get_all_objs("User")
        u_sargs = {"objs": u_objs, "limit_exact": 1, "default_search_attr": "id", "use_regex": False}
        g_objs = self.get_all_objs("Group")
        g_sargs = {"objs": g_objs, "limit_exact": 1, "default_search_attr": "id", "use_regex": False}

        ret = taniumpy.DashboardList()
        ret._DASH_PLUGIN_RETURN = dash_pret
        ret._DASH_SQ_PLUGIN_RETURN = dash_sq_pret
        ret._track_merge(other=dash_pret)
        ret._track_merge(other=dash_sq_pret)

        for lod in sorted(dash_pret._LOD, key=lambda x: x["name"]):
            sq_lods = [x for x in dash_sq_pret._LOD if int(x["dashboard_id"]) == int(lod["id"])]
            sq_lods = sorted(sq_lods, key=lambda x: x["dashboard_index"])
            sq_ids = [x["saved_question_id"] for x in sq_lods]

            all_g_obj = self.build_obj("Group", attrs={"id": 0, "name": "All Groups"})
            all_g_id = lod["group_id"] == "0"
            g_obj = all_g_obj if all_g_id else self.search_objs(**kwmerge(g_sargs, searches=lod["group_id"]))

            obj = taniumpy.Dashboard()
            obj.id = int(lod["id"])
            obj.name = lod["name"]
            obj.public_flag = int(lod["public_flag"])
            obj.user = self.search_objs(**kwmerge(u_sargs, searches=lod["user_id"]))
            obj.computer_group = g_obj
            obj.saved_questions = self.search_objs(**kwmerge(sq_sargs, searches=sq_ids))
            ret.append(obj)

        m = "Retrieved {l} Dashboards"
        m = m.format(l=len(ret))
        self.mylog.debug(m)
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def get_action_groups(self, **kwargs):
        margs = {"bundle": "GroupFilter", "name": "GetActionGroups"}
        ag_pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

        margs = kwmerge({}, lod=ag_pret._LOD, key="id", attr="group_id")
        coll_lod = collapse_lod(**margs)

        m = "Collapsed {b} plugin response dicts into {a} dicts"
        m = m.format(b=len(ag_pret._LOD), a=len(coll_lod))
        self.mylog.debug(m)

        margs = {"bundle": "GroupFilter", "name": "GetActionGroupsUserGroups"}
        agug_pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

        # FIXBUG: refetch=True need to re-fetch the single group object. group objects returned from get all
        # have duplicate sub_group listings!!
        g_objs = self.get_all_objs("Group")
        g_sargs = kwmerge(kwargs, objs=g_objs, excludes=[], limit_exact=1, refetch=True)
        ug_objs = self.get_all_objs("UserGroup")
        ug_sargs = {"objs": ug_objs, "excludes": [], "default_search_attr": "id", "use_regex": False}

        ret = taniumpy.ActionGroupList()
        ret._AG_PLUGIN_RETURN = ag_pret
        ret._AGUG_PLUGIN_RETURN = agug_pret
        ret._track_merge(other=ag_pret)
        ret._track_merge(other=agug_pret)

        for lod in coll_lod:
            ug_ids = [x["user_group_id"] for x in agug_pret._LOD if x["action_group_id"] == str(lod["id"])]
            ug_ids = list(set(ug_ids))

            obj = taniumpy.ActionGroup()
            obj.id = int(lod["id"])
            obj.name = lod["name"]
            obj.public_flag = int(lod["public_flag"])
            obj.and_flag = int(lod["and_flag"])
            obj.computer_group = self.search_objs(**kwmerge(g_sargs, searches=lod["name"]))
            obj.user_groups = self.search_objs(**kwmerge(ug_sargs, searches=ug_ids))
            ret.append(obj)

        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def create_dashboard_category(self, name, **kwargs):
        """
        Visibility notes:
        - if public_flag = 0 and user specified, then only that user can see
        - if public_flag = 0 and user groups specified, then only users in those user groups can see
        - if public_flag = 0 and no user and no user groups, then only admins can see
        - if public_flag = 1, all users can see
        """
        icon = kwargs.get("icon", "")
        user_s = kwargs.get("user_searches", [])
        user_e = kwargs.get("user_excludes", [])
        ug_s = kwargs.get("ugroup_searches", [])
        ug_e = kwargs.get("ugroup_excludes", [])
        db_s = kwargs.get("dashboard_searches", [])
        db_e = kwargs.get("dashboard_excludes", [])
        public_flag = int(kwargs.get("public_flag", True))
        other_flag = int(kwargs.get("other_flag", False))
        editable_flag = int(kwargs.get("editable_flag", True))
        search_precheck = kwargs.get("search_precheck", True)

        if search_precheck:
            margs = kwmerge(kwargs, objtype="DashboardCategory", searches=name, limit_exact=1)
            try:
                obj = self.search_all_objs(**margs)
            except exceptions.NotFoundError:
                m = "Found no DashboardCategory while searching for '{n}', will create!"
                m = m.format(n=name)
                self.mylog.debug(m)
            else:
                m = "{o} found while searching for '{n}', will not create!"
                m = m.format(o=obj, n=name)
                raise exceptions.HandlerError(m)

        if user_s or user_e:
            margs = kwmerge(kwargs, objtype="User", searches=user_s, excludes=user_e, limit_exact=1)
            u_obj = self.search_all_objs(**margs)
            public_flag = 0
        else:
            u_obj = self.build_obj("User", attrs={"id": 0, "name": "All Users"})

        margs = kwmerge(kwargs, objtype="UserGroup", searches=ug_s, excludes=ug_e)
        ug_objs = self.search_all_objs(**margs)
        public_flag = 0 if ug_objs else public_flag

        margs = kwmerge(kwargs, objtype="Dashboard", searches=db_s, excludes=db_e)
        db_objs = self.search_all_objs(**margs)

        obj = taniumpy.DashboardCategory()
        obj._CHANGED = True
        obj.name = name
        obj.public_flag = public_flag
        obj.other_flag = other_flag
        obj.editable_flag = editable_flag
        obj.icon = taniumpy.Image(icon)
        obj.user = u_obj
        obj.set_user_groups(ug_objs)
        obj.set_dashboards(db_objs)

        pargs = [
            {"name": "name", "type": "String", "value": obj.name},
            {"name": "text", "type": "String", "value": ""},
            {"name": "icon", "type": "String", "value": obj.icon.encode},
            {"name": "user_id", "type": "Number", "value": obj.user.id},
            {"name": "public_flag", "type": "Number", "value": obj.public_flag},
            {"name": "editable_flag", "type": "Number", "value": obj.editable_flag},
            {"name": "other_flag", "type": "Number", "value": obj.other_flag},
            {"name": "dashboard_list_xml", "type": "String", "value": obj.dashboard_xml()},
            {"name": "user_group_xml", "type": "String", "value": obj.user_groups_xml()},
        ]

        margs = {"bundle": "DashboardGroups", "name": "AddContentGroup", "arguments": pargs}
        pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

        if obj.user.id == self.get_this_user_id() or obj.user.id == 0:
            margs = kwmerge(kwargs, objtype="DashboardCategory", searches=name, limit_exact=1)
            ret = self.search_all_objs(**margs)
            ret._PLUGIN_RETURN = pret

            ret._track_merge(other=pret)
            ret._track(t_action="Added new")
            self.log_tracker(**kwmerge(kwargs, obj=ret))
            ret._ADDED = True
        else:
            m = "{o} Added, but unable to re-fetch added object created for a different user ID: {i}"
            m = m.format(o=obj, i=obj.user.id)
            self.mylog.warning(m)
            ret = obj
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def create_dashboard(self, name, **kwargs):
        sq_s = kwargs.get("sq_searches", [])
        sq_e = kwargs.get("sq_excludes", [])
        cgrp_s = kwargs.get("cgroup_searches", [])
        cgrp_e = kwargs.get("cgroup_excludes", [])
        public_flag = int(kwargs.get("public_flag", True))
        search_precheck = kwargs.get("search_precheck", True)

        if search_precheck:
            margs = kwmerge(kwargs, objtype="Dashboard", searches=name, limit_exact=1)
            try:
                obj = self.search_all_objs(**margs)
            except exceptions.NotFoundError:
                m = "Found no Dashboard while searching for '{n}', will create!"
                m = m.format(n=name)
                self.mylog.debug(m)
            else:
                m = "{o} found while searching for '{n}', will not create!"
                m = m.format(o=obj, n=name)
                raise exceptions.HandlerError(m)

        # Get the Computer Group for this Dashboard if supplied
        if cgrp_s or cgrp_e:
            margs = kwmerge(kwargs, objtype="Group", searches=cgrp_s, excludes=cgrp_e, limit_exact=1)
            cg_obj = self.search_all_objs(**margs)
        else:
            cg_obj = self.build_obj("Group", attrs={"id": 0, "name": "All Groups"})

        margs = kwmerge(kwargs, objtype="SavedQuestion", searches=sq_s, excludes=sq_e)
        sq_objs = self.search_all_objs(**margs)

        obj = taniumpy.Dashboard()
        obj._CHANGED = True
        obj.name = name
        obj.public_flag = public_flag
        obj.computer_group = cg_obj
        obj.set_saved_questions(sq_objs)

        pargs = [
            {"name": "dash_name", "type": "String", "value": obj.name},
            {"name": "dash_text", "type": "String", "value": ""},
            {"name": "group_id", "type": "Number", "value": obj.computer_group.id},
            {"name": "public_flag", "type": "Number", "value": obj.public_flag},
            {"name": "sqid_xml", "type": "String", "value": obj.saved_questions_xml()},
        ]

        margs = {"bundle": "Dashboards", "name": "CreateDashboard", "arguments": pargs}
        pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

        margs = kwmerge(kwargs, objtype="Dashboard", searches=name, limit_exact=1)
        ret = self.search_all_objs(**margs)
        ret._PLUGIN_RETURN = pret

        ret._track_merge(other=pret)
        ret._track(t_action="Added new")
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        ret._ADDED = True
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def create_user_group(self, name, **kwargs):
        search_precheck = kwargs.get("search_precheck", True)

        if search_precheck:
            margs = kwmerge(kwargs, objtype="UserGroup", searches=name, limit_exact=1)
            try:
                obj = self.search_all_objs(**margs)
            except exceptions.NotFoundError:
                m = "Found no User Group while searching for '{n}', will create!"
                m = m.format(n=name)
                self.mylog.debug(m)
            else:
                m = "{o} found while searching for '{n}', will not create!"
                m = m.format(o=obj, n=name)
                raise exceptions.HandlerError(m)

        pargs = [{"name": "user_group_name", "type": "String", "value": name}]
        margs = {"bundle": "UserGroups", "name": "AddUserGroup", "arguments": pargs}
        pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

        margs = kwmerge(kwargs, objtype="UserGroup", searches=name, limit_exact=1)
        ret = self.search_all_objs(**margs)
        ret._PLUGIN_RETURN = pret

        ret._track_merge(other=pret)
        ret._track(t_action="Added new")
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        ret._ADDED = True
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def create_action_group(self, name, **kwargs):
        cgrp_s = kwargs.get("cgroup_searches", [])
        cgrp_e = kwargs.get("cgroup_excludes", [])
        ugrp_s = kwargs.get("ugroup_searches", [])
        ugrp_e = kwargs.get("ugroup_excludes", [])
        and_flag = int(kwargs.get("and_flag", False))
        public_flag = int(kwargs.get("public_flag", True))
        search_precheck = kwargs.get("search_precheck", True)

        if search_precheck:
            margs = kwmerge(kwargs, objtype="ActionGroup", searches=name, limit_exact=1)
            try:
                obj = self.search_all_objs(**margs)
            except exceptions.NotFoundError:
                m = "Found no Action Group while searching for '{n}', will create!"
                m = m.format(n=name)
                self.mylog.debug(m)
            else:
                m = "{o} found while searching for '{n}', will not create!"
                m = m.format(o=obj, n=name)
                raise exceptions.HandlerError(m)

        # Get the Computer Groups for this Action Group
        margs = kwmerge(kwargs, objtype="Group", searches=cgrp_s, excludes=cgrp_e)
        cg_objs = self.search_all_objs(**margs)

        # Get the User Groups specified for this Action Group
        margs = kwmerge(kwargs, objtype="UserGroup", searches=ugrp_s, excludes=ugrp_e)
        ug_objs = self.search_all_objs(**margs)

        obj = taniumpy.ActionGroup(name=name, public_flag=public_flag, and_flag=and_flag)
        obj._CHANGED = True
        obj.set_computer_groups(cg_objs)
        obj.set_user_groups(ug_objs)

        ret = self.save_changed_obj_ag(**kwmerge(kwargs, obj=obj))
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def delete_dashboard(self, searches=[], **kwargs):
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        obj = kwargs.get("obj", None)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)
        elif obj is None:
            margs = kwmerge(kwargs, objtype="Dashboard", searches=this_s, excludes=this_e, limit_exact=1)
            try:
                obj = self.search_all_objs(**margs)
            except exceptions.NotFoundError:
                m = "Found no Dashboard while searching for '{s}', will not delete!"
                m = m.format(s=this_s)
                raise exceptions.NotFoundError(m)
            else:
                m = "{o} found while searching for '{s}', will delete!"
                m = m.format(o=obj, s=this_s)
                self.mylog.debug(m)

        arguments = [{"name": "dashboard_ids", "type": "Number_Set", "value": obj.id}]
        margs = {"bundle": "Dashboards", "name": "DeleteDashboards", "arguments": arguments}
        pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

        ret = obj
        ret._PLUGIN_RETURN = pret
        ret._track_merge(other=pret)
        ret._track(t_action="Deleted")
        ret._DELETED = True
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def delete_dashboard_category(self, searches=[], **kwargs):
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        obj = kwargs.get("obj", None)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)
        elif obj is None:
            margs = kwmerge(kwargs, objtype="DashboardCategory", searches=this_s, excludes=this_e, limit_exact=1)
            try:
                obj = self.search_all_objs(**margs)
            except exceptions.NotFoundError:
                m = "Found no DashboardCategory while searching for '{s}', will not delete!"
                m = m.format(s=this_s)
                raise exceptions.NotFoundError(m)
            else:
                m = "{o} found while searching for '{s}', will delete!"
                m = m.format(o=obj, s=this_s)
                self.mylog.debug(m)

        arguments = [{"name": "content_group_ids", "type": "Number_Set", "value": obj.id}]
        margs = {"bundle": "DashboardGroups", "name": "DeleteContentGroups", "arguments": arguments}
        pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

        ret = obj
        ret._PLUGIN_RETURN = pret
        ret._track_merge(other=pret)
        ret._track(t_action="Deleted")
        ret._DELETED = True
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def delete_action_group(self, searches=[], **kwargs):
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        obj = kwargs.get("obj", None)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)
        elif obj is None:
            margs = kwmerge(kwargs, objtype="ActionGroup", searches=this_s, excludes=this_e, limit_exact=1)
            try:
                obj = self.search_all_objs(**margs)
            except exceptions.NotFoundError:
                m = "Found no Action Group while searching for '{s}', will not delete!"
                m = m.format(s=this_s)
                raise exceptions.NotFoundError(m)
            else:
                m = "{o} found while searching for '{s}', will delete!"
                m = m.format(o=obj, s=this_s)
                self.mylog.debug(m)

        arguments = [
            {"name": "new_group_id", "type": "Number", "value": 0},
            {"name": "old_group_id", "type": "Number", "value": obj.id},
        ]

        margs = {"bundle": "GroupFilter", "name": "DeleteActionGroup", "arguments": arguments}
        pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

        ret = obj
        ret._PLUGIN_RETURN = pret
        ret._track_merge(other=pret)
        ret._track(t_action="Deleted")
        ret._DELETED = True
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def delete_user_group(self, searches=[], **kwargs):
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        obj = kwargs.get("obj", None)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)
        elif obj is None:
            margs = kwmerge(kwargs, objtype="UserGroup", searches=this_s, excludes=this_e, limit_exact=1)
            try:
                obj = self.search_all_objs(**margs)
            except exceptions.NotFoundError:
                m = "Found no User Group while searching for '{s}', will not delete!"
                m = m.format(s=this_s)
                raise exceptions.NotFoundError(m)
            else:
                m = "{o} found while searching for '{s}', will delete!"
                m = m.format(o=obj, s=this_s)
                self.mylog.debug(m)

        arguments = [{"name": "user_group_id", "type": "Number", "value": obj.id}]
        margs = {"bundle": "UserGroups", "name": "DeleteUserGroup", "arguments": arguments}
        pret = self.run_plugin_obj(**kwmerge(kwargs, **margs))

        ret = obj
        ret._PLUGIN_RETURN = pret
        ret._track_merge(other=pret)
        ret._track(t_action="Deleted")
        ret._DELETED = True
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # ADDED: 3.0.0
    def modify_metadata_obj(self, obj, **kwargs):
        properties = kwargs.get("properties", {}) or {}
        prefix = kwargs.get("prefix", "")
        add_pytan_property = kwargs.get("add_pytan_property", True)

        if add_pytan_property:
            properties[PP_NAME] = PP_VALUE.format(v=version.__version__, d=seconds_from_now())

        # build a new metadata list if obj is None
        obj = self.build_obj(obj_name="MetadataList") if obj is None else obj

        # build a new metadata lists to return
        ret = self.build_obj(obj_name="MetadataList")

        delete_all = "_DELETEALL_" in properties
        ptmpl = "{p}.{n}".format if prefix else "{n}".format
        properties = {ptmpl(p=prefix, n=k): v for k, v in properties.items()}

        # update/create/delete/skip properties
        for name, value in properties.items():
            # try to find a matching md item by lowercase name
            found = [x for x in obj if str(x.name).lower() == name.lower()]
            t_old = found[0] if found else ""
            t_new = self.build_obj(obj_name="MetadataItem", attrs={"name": name, "value": value})

            if value == "_DELETE_" and found:
                t_action = "Deleted item from"
                t_new = ""
            elif value == "_DELETE_" and not found:
                t_action = "Did not add item to"
            elif name.endswith("_DELETEALL_"):
                continue
            elif t_old:
                t_old._CHANGED = True
                t_action = "Updated item in"
                t_new = t_old
                t_new.value = value
                ret.append(t_new)
            else:
                t_action = "Created new item in"
                ret.append(t_new)

            ret._track(t_old=t_old, t_new=t_new, t_action=t_action, str_all_attrs=True)

        for x in obj:
            touched = getattr(x, "_CHANGED", False)
            if not touched:
                if delete_all:
                    t_action = "Deleted item from"
                else:
                    t_action = "Added untouched item back to"
                    ret.append(x)
                ret._track(t_old=x, t_action=t_action, str_all_attrs=True)
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def modify_user_group(self, searches=[], **kwargs):
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        # set_s = kwargs.get("set_searches", [])
        # set_e = kwargs.get("set_excludes", [])
        # add_s = kwargs.get("add_searches", [])
        # add_e = kwargs.get("add_excludes", [])
        # del_s = kwargs.get("remove_searches", [])
        # del_e = kwargs.get("remove_excludes", [])
        delete_existing = kwargs.get("delete_existing", False)
        obj = kwargs.get("obj", None)
        user_objs = kwargs.get("user_objs", None)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)

        new_a = {"name": this_s[0]}
        margs = kwmerge(kwargs, objtype="UserGroup", searches=this_s, excludes=this_e, attrs=new_a)
        obj = self.search_add_obj(**margs) if obj is None else obj

        if delete_existing:
            ret = self.delete_obj(**kwmerge(kwargs, obj=obj))
            self.log_tracker(**kwmerge(kwargs, obj=ret))
            return ret

        user_objs = self.get_all_objs(objtype="User") if user_objs is None else user_objs
        orig_users = obj.users_str()

        change_map = [
            {
                "searches": "set_searches", "excludes": "set_excludes",
                "method": "set_users", "objs": user_objs,
                "t_action": "Set {l} users on",
            },
            {
                "searches": "add_searches", "excludes": "add_excludes",
                "method": "add_users", "objs": user_objs,
                "t_action": "Added {l} users to",
            },
            {
                "searches": "remove_searches", "excludes": "remove_excludes",
                "method": "remove_users", "objs": user_objs,
                "t_action": "Removed {l} users from",
            },
        ]

        for c in change_map:
            if not (c["searches"] in kwargs or c["excludes"] in kwargs):
                continue
            c["searches"], c["excludes"] = (kwargs.get(c["searches"], []), kwargs.get(c["excludes"], []))
            mod_list = self.search_objs(**kwmerge(kwargs, **c))
            obj._track_merge(other=mod_list)
            getattr(obj, c["method"])(mod_list)
            obj._track(t_action=c["t_action"].format(l=len(mod_list)))

        new_users = obj.users_str() if obj._CHANGED else ""
        obj._track(t_old=orig_users, t_new=new_users, t_action="User Group Membership")

        ret = self.save_changed_obj_ug(**kwmerge(kwargs, obj=obj))
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def modify_action_group(self, searches=[], **kwargs):
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        and_flag = int(kwargs.get("and_flag", False))
        public_flag = int(kwargs.get("public_flag", True))
        delete_existing = kwargs.get("delete_existing", False)
        obj = kwargs.get("obj", None)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)

        try:
            margs = kwmerge(kwargs, objtype="ActionGroup", searches=this_s, excludes=this_e, limit_exact=1)
            obj = self.search_all_objs(**margs) if obj is None else obj
        except exceptions.NotFoundError:
            obj = taniumpy.ActionGroup(name=this_s[0], public_flag=public_flag, and_flag=and_flag)
            obj._CHANGED = True

        if delete_existing:
            ret = self.delete_obj(**kwmerge(kwargs, obj=obj))
            self.log_tracker(**kwmerge(kwargs, obj=ret))
            return ret

        g_objs = self.get_all_objs(objtype="Group")
        ug_objs = self.get_all_objs(objtype="UserGroup")

        orig_cg = obj.computer_groups_str()
        orig_ug = obj.user_groups_str()

        if "and_flag" in kwargs:
            obj._track_set(t_attr="and_flag", t_new=and_flag)

        if "public_flag" in kwargs:
            obj._track_set(t_attr="public_flag", t_new=public_flag)

        change_map = [
            {
                "searches": "cg_set_searches", "excludes": "cg_set_excludes",
                "method": "set_computer_groups", "objs": g_objs,
                "t_action": "Set {l} computer groups on",
            },
            {
                "searches": "cg_add_searches", "excludes": "cg_add_excludes",
                "method": "add_computer_groups", "objs": g_objs,
                "t_action": "Added {l} computer groups to",
            },
            {
                "searches": "cg_remove_searches", "excludes": "cg_remove_excludes",
                "method": "remove_computer_groups", "objs": g_objs,
                "t_action": "Removed {l} computer groups from",
            },
            {
                "searches": "ug_set_searches", "excludes": "ug_set_excludes",
                "method": "set_user_groups", "objs": ug_objs,
                "t_action": "Set {l} user groups on",
            },
            {
                "searches": "ug_add_searches", "excludes": "ug_add_excludes",
                "method": "add_user_groups", "objs": ug_objs,
                "t_action": "Added {l} user groups to",
            },
            {
                "searches": "ug_remove_searches", "excludes": "ug_remove_excludes",
                "method": "remove_user_groups", "objs": ug_objs,
                "t_action": "Removed {l} user groups from",
            },
        ]

        for c in change_map:
            if not (c["searches"] in kwargs or c["excludes"] in kwargs):
                continue
            c["searches"], c["excludes"] = (kwargs.get(c["searches"], []), kwargs.get(c["excludes"], []))
            mod_list = self.search_objs(**kwmerge(kwargs, **c))
            obj._track_merge(other=mod_list)
            getattr(obj, c["method"])(mod_list)
            obj._track(t_action=c["t_action"].format(l=len(mod_list)))

        new_cg = obj.computer_groups_str() if obj._CHANGED else ""
        new_ug = obj.user_groups_str() if obj._CHANGED else ""

        obj._track(t_old=orig_cg, t_new=new_cg, t_action="Computer Group Membership")
        obj._track(t_old=orig_ug, t_new=new_ug, t_action="User Group Membership")

        ret = self.save_changed_obj_ag(**kwmerge(kwargs, obj=obj))
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def modify_user(self, searches=[], **kwargs):
        """Create, modify, or delete a user object.

        Notes
        -----
        * Searches and excludes supplied must equate to ONE user.
        * The first string in searches should be a simple string as it will be used as the name of the
          newly created user if `create_missing` is True and the user does not exist.
        * When creating a missing user and no parameters supplied, the default user will be:

            * Granted the role "Read Only User"
            * Have access to All Computer Groups
            * Have access to No User Groups

        Parameters
        ----------
        searches: :obj:`str` or :obj:`list` of :obj:`str`
            * search strings used to find a single user object to modify
        excludes: :obj:`str` or :obj:`list` of :obj:`str`, optional
            * Default: []
            * search strings to exclude from `searches`
        new_user_default_role: :obj:`str` or :obj:`list` of :obj:`str`, optional
            * Default: "Read Only User"
            * search strings used to find a single user role object if no `role_searches` supplied
              and `create_missing` is True and no user found matching searches
        role_searches: :obj:`str` or :obj:`list` of :obj:`str`, optional
            * Default: []
            * search strings used to find a single user role object to assign to user
        role_excludes: :obj:`str` or :obj:`list` of :obj:`str`, optional
            * Default: []
            * search strings to exclude from `role_searches`
        cgroup_searches: :obj:`str` or :obj:`list` of :obj:`str`, optional
            * Default: []
            * search strings used to find any number of computer group objects to assign to user
            * !names must exist, can not be created!
        cgroup_excludes: :obj:`str` or :obj:`list` of :obj:`str`, optional
            * Default: []
            * search strings to exclude from `cgroup_searches`
        ugroup_searches: :obj:`str` or :obj:`list` of :obj:`str`, optional
            * Default: []
            * search strings used to find any number of user group objects to assign to user
            * !names must exist, can not be created!
        ugroup_excludes: :obj:`str` or :obj:`list` of :obj:`str`, optional
            * Default: []
            * search strings to exclude from `ugroup_searches`
        properties: :obj:`dict`, optional
            * Default: {}
        add_pytan_property: :obj:`bool`, optional
            * Default: True
            * Parameter also used by: update_obj_metadata
        delete_existing: :obj:`bool`, optional
            * Default: False
            * Delete user matching `searches` if found

        Other Parameters
        ----------------
        create_missing: :obj:`bool`, optional
            * Default: True
            * Parameter used by: search_add_obj
        use_regex: :obj:`bool`, optional
            * Default: True
            * Parameter used by: search_obj
        case_sensitive: :obj:`bool`, optional
            * Default: False
            * Parameter used by: search_obj
        default_search_attr: :obj:`str`, optional
            * Default: "name"
            * Parameter used by: search_obj
        search_debug: obj:`str`, optional
            * Default: "name"
            * Parameter used by: search_objs
        any_taniumpy_option: :obj:`obj`, optional
            * any parameter from taniumpy.Options
            * Parameters used by: session.find, session.add, session.save, session.delete
        log_line_limit: :obj:`int`, optional
            * Default: 80
            * Parameter used by: log_tracker
        log_include_build: :obj:`bool`, optional
            * Default: False
            * Parameter used by: log_tracker
        log_include_plugin: :obj:`bool`, optional
            * Default: False
            * Parameter used by: log_tracker
        """
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        role_n = kwargs.get("new_user_default_role", "Read Only User")
        role_s = kwargs.get("role_searches", [])
        role_e = kwargs.get("role_excludes", [])
        cgrp_s = kwargs.get("cgroup_searches", [])
        cgrp_e = kwargs.get("cgroup_excludes", [])
        ugrp_s = kwargs.get("ugroup_searches", [])
        ugrp_e = kwargs.get("ugroup_excludes", [])
        delete_existing = kwargs.get("delete_existing", False)
        add_pytan_property = kwargs.get("add_pytan_property", True)
        obj = kwargs.get("obj", None)

        # find the specified role by name, require at least one match
        margs = kwmerge(kwargs, objtype="UserRole", searches=role_s or role_n, excludes=role_e, limit_exact=1)
        role_obj = self.search_all_objs(**margs)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)
        elif obj is None:
            # find or add the user accordingly
            new_a = {"name": this_s[0], "roles": [{"name": role_obj.name}]}
            margs = kwmerge(kwargs, objtype="User", searches=this_s, excludes=this_e, attrs=new_a)
            obj = self.search_add_obj(**margs)

        if delete_existing:
            ret = self.delete_obj(**kwmerge(kwargs, obj=obj))
            self.log_tracker(**kwmerge(kwargs, obj=ret))
            return ret

        g_objs_all = self.get_all_objs(objtype="Group")
        g_objs_cur = self.get_group_members_by_id(group_id=obj.group_id, objs=g_objs_all)
        margs = kwmerge(kwargs, searches=cgrp_s, excludes=cgrp_e, objs=g_objs_all)
        g_objs_new = self.get_group_members_by_searches(**margs)

        m = "{o} current membership: {msg}"
        m = m.format(o=obj, msg=g_objs_cur._MSG)
        self.mylog.debug(m)

        m = "{o} new membership: {msg}"
        m = m.format(o=obj, msg=g_objs_new._MSG)
        self.mylog.debug(m)

        if "cgroup_searches" in kwargs or "cgroup_excludes" in kwargs:
            t_action = "Updated group membership for"
            obj._track(t_old=g_objs_cur._MSG, t_new=g_objs_new._MSG, t_action=t_action)
            margs = kwmerge(kwargs, t_attr="group_id", t_new=g_objs_new._ROOT_GROUP.id)
            obj._track_set(**margs)
        elif obj._ADDED:
            t_action = "Group membership for new"
            obj._track(t_old=g_objs_cur._MSG, t_action=t_action)

        if "role_searches" in kwargs or "role_excludes" in kwargs:
            roles_obj = self.build_obj(obj_name="UserRoleList")
            roles_obj.append(role_obj)
            margs = kwmerge(kwargs, t_attr="roles", t_new=roles_obj, str_all_attrs=True, str_items=True)
            obj._track_set(**margs)

        if "ugroup_searches" in kwargs or "ugroup_excludes" in kwargs:
            margs = kwmerge(kwargs, objtype="UserGroup", searches=ugrp_s, excludes=ugrp_e)
            ug_objs = self.search_all_objs(**margs)
            ug_objs.add_user(obj)
            margs = kwmerge(kwargs, objs=ug_objs, searches=ugrp_s, excludes=ugrp_e)
            ug_objs = self.save_changed_obj_ugs(**margs)
            obj._track_merge(other=ug_objs)

        if "properties" in kwargs or (add_pytan_property and (obj._CHANGED or obj._ADDED)):
            margs = kwmerge(kwargs, obj=obj.metadata, prefix="TConsole.User.Property")
            md_obj = self.modify_metadata_obj(**margs)
            obj._track_merge(other=md_obj)
            obj._track_set(**kwmerge(kwargs, t_attr="metadata", t_new=md_obj))

        ret = self.save_changed_obj(**kwmerge(kwargs, obj=obj))
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def modify_setting(self, searches=[], **kwargs):
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        value = kwargs.get("value", None)
        value_type = valvalue(key="value_type", valids=["Numeric", "Text"], kwargs=kwargs)
        setting_type = valvalue(key="setting_type", valids=["Server", "Client"], kwargs=kwargs)
        note = kwargs.get("note", None)
        delete_existing = kwargs.get("delete_existing", False)
        add_pytan_property = kwargs.get("add_pytan_property", True)
        obj = kwargs.get("obj", None)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)
        elif obj is None:
            new_a = {"name": this_s[0], "value": value, "value_type": value_type, "setting_type": setting_type}
            margs = kwmerge(kwargs, objtype="SystemSetting", searches=this_s, excludes=this_e, attrs=new_a)
            obj = self.search_add_obj(**margs)

        if delete_existing:
            ret = self.delete_obj(**kwmerge(kwargs, obj=obj))
            self.log_tracker(**kwmerge(kwargs, obj=ret))
            return ret

        note_prop = "TConsole.Setting.Note"

        old_mdl_obj = getattr(obj, "metadata", []) or []
        old_note_obj = [x for x in old_mdl_obj if x.name == note_prop]
        old_note_val = getattr(old_note_obj[0], "value", PP_NAME) if old_note_obj else PP_NAME

        if "value" in kwargs:
            obj._track_set(t_attr="value", t_new=value)

        if "value_type" in kwargs:
            obj._track_set(t_attr="value_type", t_new=value_type)

        if "setting_type" in kwargs:
            obj._track_set(t_attr="setting_type", t_new=setting_type)

        if "note" in kwargs:
            note_attrs = {"name": note_prop, "value": note}
            mdl_obj = self.build_obj(obj_name="MetadataList", attrs=[note_attrs])
            obj._track_set(t_attr="metadata", t_new=mdl_obj, str_items=True, str_all_attrs=True)
        elif add_pytan_property and (obj._ADDED or obj._CHANGED) and old_note_val.startswith(PP_NAME):
            pp_note = "{n} {v}".format(n=PP_NAME, v=PP_VALUE.format(v=version.__version__, d=seconds_from_now()))
            note_attrs = {"name": note_prop, "value": pp_note}
            mdl_obj = self.build_obj(obj_name="MetadataList", attrs=[note_attrs])
            obj._track_set(t_attr="metadata", t_new=mdl_obj, str_items=True, str_all_attrs=True)

        ret = self.save_changed_obj(**kwmerge(kwargs, obj=obj))
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def modify_dashboard(self, searches=[], **kwargs):
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        # sq_s = kwargs.get("sq_searches", [])
        # sq_e = kwargs.get("sq_excludes", [])
        cgrp_s = kwargs.get("cgroup_searches", [])
        cgrp_e = kwargs.get("cgroup_excludes", [])
        public_flag = int(kwargs.get("public_flag", True))
        delete_existing = kwargs.get("delete_existing", False)
        obj = kwargs.get("obj", None)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)
        elif obj is None:
            # find or add the user accordingly
            new_a = kwmerge(kwargs, name=this_s[0])
            margs = kwmerge(kwargs, objtype="Dashboard", searches=this_s, excludes=this_e, attrs=new_a)
            obj = self.search_add_obj(**margs)

        if delete_existing:
            ret = self.delete_obj(**kwmerge(kwargs, obj=obj))
            self.log_tracker(**kwmerge(kwargs, obj=ret))
            return ret

        sq_objs = self.get_all_objs(objtype="SavedQuestion")
        orig_sq = obj.saved_questions_str()

        obj = obj._track_set(t_attr="public_flag", t_new=public_flag) if "public_flag" in kwargs else obj

        if "cgroup_searches" in kwargs or "cgroup_excludes" in kwargs:
            if cgrp_s or cgrp_e:
                margs = kwmerge(kwargs, objtype="Group", searches=cgrp_s, excludes=cgrp_e, limit_exact=1)
                cg_obj = self.search_all_objs(**margs)
            else:
                cg_obj = self.build_obj("Group", attrs={"id": 0, "name": "All Groups"})
            obj._track_set(t_attr="computer_group", t_new=cg_obj)

        change_map = [
            {
                "searches": "sq_set_searches", "excludes": "sq_set_excludes",
                "method": "set_saved_questions", "objs": sq_objs,
                "t_action": "Set {l} saved questions on",
            },
            {
                "searches": "sq_add_searches", "excludes": "sq_add_excludes",
                "method": "add_saved_questions", "objs": sq_objs,
                "t_action": "Added {l} saved questions to",
            },
            {
                "searches": "sq_remove_searches", "excludes": "sq_remove_excludes",
                "method": "remove_saved_questions", "objs": sq_objs,
                "t_action": "Removed {l} saved questions from",
            },
        ]

        for c in change_map:
            if not (c["searches"] in kwargs or c["excludes"] in kwargs):
                continue
            c["searches"], c["excludes"] = (kwargs.get(c["searches"], []), kwargs.get(c["excludes"], []))
            mod_list = self.search_objs(**kwmerge(kwargs, **c))
            obj._track_merge(other=mod_list)
            getattr(obj, c["method"])(mod_list)
            obj._track(t_action=c["t_action"].format(l=len(mod_list)))

        new_sq = obj.saved_questions_str() if obj._CHANGED else ""
        obj._track(t_old=orig_sq, t_new=new_sq, t_action="Saved Question Membership of")

        ret = self.save_changed_obj_db(**kwmerge(kwargs, obj=obj))
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # DOC, TEST
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def modify_dashboard_category(self, searches=[], **kwargs):
        this_s = mklist(searches)
        this_e = mklist(kwargs.get("excludes", []))
        user_s = kwargs.get("user_searches", [])
        user_e = kwargs.get("user_excludes", [])
        icon = kwargs.get("icon", "")
        public_flag = int(kwargs.get("public_flag", True))
        other_flag = int(kwargs.get("other_flag", False))
        editable_flag = int(kwargs.get("editable_flag", True))
        delete_existing = kwargs.get("delete_existing", False)
        obj = kwargs.get("obj", None)

        if not this_s and obj is None:
            m = "Must supply a non-empty list of searches!"
            raise exceptions.HandlerError(m)
        elif obj is None:
            # find or add the user accordingly
            new_a = kwmerge(kwargs, name=this_s[0])
            margs = kwmerge(kwargs, objtype="DashboardCategory", searches=this_s, excludes=this_e, attrs=new_a)
            obj = self.search_add_obj(**margs)

        if delete_existing:
            ret = self.delete_obj(**kwmerge(kwargs, obj=obj))
            self.log_tracker(**kwmerge(kwargs, obj=ret))
            return ret

        ug_objs = self.get_all_objs(objtype="UserGroup")
        db_objs = self.get_all_objs(objtype="Dashboard")
        orig_ug = obj.user_groups_str()
        orig_db = obj.dashboard_str()

        if "user_s_searches" in kwargs or "user_s_excludes" in kwargs:
            if user_s or user_e:
                margs = kwmerge(kwargs, objtype="User", searches=user_s, excludes=user_e, limit_exact=1)
                user_obj = self.search_all_objs(**margs)
                public_flag = 0
            else:
                user_obj = self.build_obj("User", attrs={"id": 0, "name": "All Users"})
            obj._track_set(t_attr="user", t_new=user_obj)

        obj = obj._track_set(t_attr="public_flag", t_new=public_flag) if "public_flag" in kwargs else obj
        obj = obj._track_set(t_attr="other_flag", t_new=other_flag) if "other_flag" in kwargs else obj
        obj = obj._track_set(t_attr="editable_flag", t_new=editable_flag) if "editable_flag" in kwargs else obj
        obj = obj._track_set(t_attr="icon", t_new=taniumpy.Image(icon)) if "icon" in kwargs else obj

        change_map = [
            {
                "searches": "ug_set_searches", "excludes": "ug_set_excludes",
                "method": "set_user_groups", "objs": ug_objs,
                "t_action": "Set {l} user groups on",
            },
            {
                "searches": "ug_add_searches", "excludes": "ug_add_excludes",
                "method": "add_user_groups", "objs": ug_objs,
                "t_action": "Added {l} user groups to",
            },
            {
                "searches": "ug_remove_searches", "excludes": "ug_remove_excludes",
                "method": "remove_user_groups", "objs": ug_objs,
                "t_action": "Removed {l} user groups from",
            },
            {
                "searches": "db_set_searches", "excludes": "db_set_excludes",
                "method": "set_dashboards", "objs": db_objs,
                "t_action": "Set {l} dashboards on",
            },
            {
                "searches": "db_add_searches", "excludes": "db_add_excludes",
                "method": "add_dashboards", "objs": db_objs,
                "t_action": "Added {l} dashboards to",
            },
            {
                "searches": "db_remove_searches", "excludes": "db_remove_excludes",
                "method": "remove_dashboards", "objs": db_objs,
                "t_action": "Removed {l} dashboards from",
            },
        ]

        for c in change_map:
            if not (c["searches"] in kwargs or c["excludes"] in kwargs):
                continue
            c["searches"], c["excludes"] = (kwargs.get(c["searches"], []), kwargs.get(c["excludes"], []))
            mod_list = self.search_objs(**kwmerge(kwargs, **c))
            obj._track_merge(other=mod_list)
            getattr(obj, c["method"])(mod_list)
            obj._track(t_action=c["t_action"].format(l=len(mod_list)))

        new_ug = obj.user_groups_str() if obj._CHANGED else ""
        new_db = obj.dashboard_str() if obj._CHANGED else ""
        obj._track(t_old=orig_ug, t_new=new_ug, t_action="User Group Membership of")
        obj._track(t_old=orig_db, t_new=new_db, t_action="Dashboard Membership of")

        ret = self.save_changed_obj_dbc(**kwmerge(kwargs, obj=obj))
        self.log_tracker(**kwmerge(kwargs, obj=ret))
        return ret

    # TODO: WRITE!!
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def create_manual_group(self, name, **kwargs):
        pass

    # TODO: WRITE!!
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def modify_computer_group(self, name, **kwargs):
        pass

    # TODO: REWRITE!!
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def modify_saved_question(self, name, **kwargs):
        """Create a saved question.

        * Added in: 3.0.0

        Parameters
        ----------
        sensors : str, list of str
            * default: []
            * sensors (columns) to include in question
        question_filters : str, list of str, optional
            * default: []
            * filters that apply to the whole question
        question_options : str, list of str, optional
            * default: []
            * options that apply to the whole question
        sensor_defs : str, dict, list of str or dict
            * default: []
            * sensor definitions, non human form
        question_filter_defs : dict, list of dict, optional
            * default: []
            * question filter definitions, non human form
        question_option_defs : dict, list of dict, optional
            * default: []
            * question option definitions, non human form
        reissue: bool, optional
            * default: False
            * True: Enable re-asking this saved question automatically every reissue_time
            * False: Do not re ask this question
        reissue_time: int, optional
            * default: 1
            * How often to re-ask this question if reissue is True
        reissue_time_frame: str, optional
            * default: hours
            * valid choices: ["days", "seconds", "minutes", "hours", "weeks"]
            * The time frame of reissue_time
        public: bool, optional
            * default: True
            * True: Make this question available to everyone
            * False: Restrict this question to only owner and administrators
        packages: list of str, optional
            * default: []
            * List of packages to be made available for use on results of the question
        properties: dict, optional
            * default: {}
            * Dict of key/value pairs to set as properties (visible in console)
        add_created_by: bool, optional
            * default: "PyTan v{version} on {now}"
            * str template: add "created by" to properties / metadata
            * False: do not add "created by" to properties / metadata

        Notes
        ------
        Can provide defs to bypass humanizing the strings, but only do this if you know what you are doing.

        7.0 Console options => API Object changes => Method argument mappings:

          * Checking the box "Reissue this question every":

            * API Object: "archive_enabled_flag": 0 => 1
            * Method argument: reissue, bool, [False, True]
            * If True, default to 1 hour for reissue_time/reissue_time_frame

          * Checking the box "Reissue this question every" and supplying 30 days:

            * API Object: "archive_enabled_flag": 0 => 1
            * API Object: "keep_seconds": 0 => 2592000
            * Method argument: reissue_time, int
            * Method argument: reissue_time_frame, str ["seconds", "minutes", "hours", "days", "weeks", "months"]

          * Unchecking the box "Reissue this question every" and leaving 30 days alone:

            * API Object: "archive_enabled_flag": 1 => 0
            * Method argument: reissue, bool, [False, True]

          * Checking the box "Restrict this question to only owner and administrators"

            * API Object: "public_flag": 1 => 0
            * Method argument: public, bool, [True, False]

          * Adding package under Associated Actions:

            * API Object: "package_spec": [] => [{"id": 123, "name": "Adobe Flash Player Installer"}]
            * Method argument: packages, list of str
            * Will need to fetch each package spec

        Returns
        -------
        obj : :class:`taniumpy.object_types.saved_question.SavedQuestion`
            * TaniumPy object added to Tanium SOAP Server
        """
        utils.check_for_help(kwargs=kwargs)

        reissue = kwargs.get("reissue", False)
        reissue_time = kwargs.get("reissue_time", 1)
        reissue_time_frame = kwargs.get("reissue_time_frame", "hours")
        public = kwargs.get("public", True)

        margs = dict(**kwargs)
        margs["prefix"] = "TConsole.SavedQuestion"
        md_obj = utils.build_md_obj2(**margs)

        set_reissue_time = "reissue_time" in kwargs or reissue
        actual_reissue_time = utils.resolve_to_seconds(reissue_time, reissue_time_frame)

        pl_obj = self.get_min_packagelist(**kwargs)

        kwargs["sensor_defs"] = kwargs.get(
            "sensor_defs",
            utils.dehumanize_sensors(kwargs.get('sensors', [])),
        )

        kwargs["question_filter_defs"] = kwargs.get(
            "question_filter_defs",
            utils.dehumanize_question_filters(kwargs.get('question_filters', [])),
        )

        kwargs["question_option_defs"] = kwargs.get(
            "question_option_defs",
            utils.dehumanize_question_options(kwargs.get('question_options', [])),
        )

        if not any([kwargs["question_filter_defs"], kwargs["sensor_defs"]]):
            m = "Must supply at least one sensor or filter!"
            raise exceptions.HandlerError(m)

        try:
            search_item = taniumpy.SavedQuestion()
            search_item.name = name
            existing_item = self.session.find(search_item)
        except Exception as e:
            e_str = str(e).lower()
            if "notunique" in e_str:
                m = "Multiple Saved Questions Named: '{}' already exists, will not create more duplicates!"
                m = m.format(name)
                raise exceptions.HandlerError(m)
            elif "notfound" in e_str:
                existing_item = None

        if existing_item is not None:
            m = "A Saved Question Named: '{}' (ID: {}) already exists, will not create duplicates!"
            m = m.format(existing_item.name, existing_item.id)
            raise exceptions.HandlerError(m)

        # get our defs from kwargs and churn them into what we want
        pargs = dict(**kwargs)
        pargs["defname"] = "sensor_defs"
        pargs["deftypes"] = ["list()", "str()", "dict()"]
        pargs["strconv"] = "name"
        pargs["empty_ok"] = True
        sdefs = utils.parse_defs(**pargs)

        pargs = dict(**kwargs)
        pargs["defname"] = "question_filter_defs"
        pargs["deftypes"] = ["list()", "dict()"]
        pargs["empty_ok"] = True
        fdefs = utils.parse_defs(**pargs)

        pargs = dict(**kwargs)
        pargs["defname"] = "question_option_defs"
        pargs["deftypes"] = ["dict()"]
        pargs["empty_ok"] = True
        odefs = utils.parse_defs(**pargs)

        # do basic validation of our defs
        utils.val_sensor_defs(sdefs)
        utils.val_q_filter_defs(fdefs)

        # get the sensor objects that are in our defs and add them as d['sensor_obj']
        h = "Issue a GetObject on a sensor for inclusion in a Questions SelectList"
        sdefs = self._get_sensor_defs(sdefs, pytan_help=h)
        h = "Issue a GetObject on a sensor for inclusion in a Questions Group"
        fdefs = self._get_sensor_defs(fdefs, pytan_help=h)

        # build a SelectList object from our sensor_defs
        sl_obj = utils.build_selectlist_obj(sdefs)

        # build a Group object from our question filters/options
        g_obj = utils.build_group_obj(fdefs, odefs)

        # build a Question object from selectlist_obj and group_obj
        q_obj = utils.build_manual_q(sl_obj, g_obj)

        add_obj = taniumpy.SavedQuestion()
        add_obj.question = q_obj
        add_obj.name = name
        add_obj.archive_enabled_flag = 1 if reissue else 0
        add_obj.keep_seconds = actual_reissue_time if set_reissue_time else 0
        add_obj.public_flag = 1 if public else 0
        add_obj.packages = pl_obj
        add_obj.metadata = md_obj
        # print(self.export_obj(add_obj, "json"))

        # add our Question and get a Question ID back
        h = "Issue an AddObject to add a Saved Question object"
        obj = self._add(obj=add_obj, pytan_help=h)

        m = "Saved Question Created, ID: {}, query text: {!r}, reissue: {}, reissue seconds: {}, public: {}"
        m = m.format(
            obj.id,
            obj.question.query_text,
            bool(obj.archive_enabled_flag),
            obj.keep_seconds,
            bool(obj.public_flag),
        )
        self.mylog.info(m)

        return obj

    # EXPORTING
    def export_obj(self, obj, export_format='csv', **kwargs):
        """Exports a python API object to a given export format

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            * TaniumPy object to export
        export_format : str, optional
            * default: 'csv'
            * the format to export `obj` to, one of: {'csv', 'xml', 'json'}
        header_sort : list of str, bool, optional
            * default: True
            * for `export_format` csv and `obj` types :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            * True: sort the headers automatically
            * False: do not sort the headers at all
            * list of str: sort the headers returned by priority based on provided list
        header_add_sensor : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not prefix the headers with the associated sensor name for each column
            * True: prefix the headers with the associated sensor name for each column
        header_add_type : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not postfix the headers with the result type for each column
            * True: postfix the headers with the result type for each column
        expand_grouped_columns : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not expand multiline row entries into their own rows
            * True: expand multiline row entries into their own rows
        explode_json_string_values : bool, optional
            * default: False
            * for `export_format` json or csv and `obj` type :class:`taniumpy.object_types.base.BaseType`
            * False: do not explode JSON strings in object attributes into their own object attributes
            * True: explode JSON strings in object attributes into their own object attributes
        minimal : bool, optional
            * default: False
            * for `export_format` xml and `obj` type :class:`taniumpy.object_types.base.BaseType`
            * False: include empty attributes in XML output
            * True: do not include empty attributes in XML output

        Returns
        -------
        result : str
            * the contents of exporting `export_format`

        Notes
        -----
        When performing a CSV export and importing that CSV into excel, keep in mind that Excel has a per cell character limit of 32,000. Any cell larger than that will be broken up into a whole new row, which can wreak havoc with data in Excel.

        See Also
        --------
        :data:`constants.EXPORT_MAPS` : maps the type `obj` to `export_format` and the optional args supported for each
        """
        objtype = type(obj)
        try:
            objclassname = objtype.__name__
        except:
            objclassname = 'Unknown'

        # see if supplied obj is a supported object type
        type_match = [
            x for x in constants.EXPORT_MAPS if isinstance(obj, getattr(taniumpy, x))
        ]

        if not type_match:
            err = (
                "{} not a supported object to export, must be one of: {}"
            ).format

            # build a list of supported object types
            supp_types = ', '.join(constants.EXPORT_MAPS.keys())
            raise exceptions.HandlerError(err(objtype, supp_types))

        # get the export formats for this obj type
        export_formats = constants.EXPORT_MAPS.get(type_match[0], '')

        if export_format not in export_formats:
            err = (
                "{!r} not a supported export format for {}, must be one of: {}"
            ).format(export_format, objclassname, ', '.join(export_formats))
            raise exceptions.HandlerError(err)

        # perform validation on optional kwargs, if they exist
        opt_keys = export_formats.get(export_format, [])

        for opt_key in opt_keys:
            check_args = dict(opt_key.items() + {'d': kwargs}.items())
            utils.check_dictkey(**check_args)

        # filter out the kwargs that are specific to this obj type and format type
        format_kwargs = {
            k: v for k, v in kwargs.iteritems()
            if k in [a['key'] for a in opt_keys]
        }

        # run the handler that is specific to this objtype, if it exists
        class_method_str = '_export_class_' + type_match[0]
        class_handler = getattr(self, class_method_str, '')

        if class_handler:
            result = class_handler(obj=obj, export_format=export_format, **format_kwargs)
        else:
            err = "{!r} not supported by Handler!".format
            raise exceptions.HandlerError(err(objclassname))

        return result

    def export_to_report_file(self, obj, export_format='csv', **kwargs):
        """Exports a python API object to a file

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            * TaniumPy object to export
        export_format : str, optional
            * default: 'csv'
            * the format to export `obj` to, one of: {'csv', 'xml', 'json'}
        header_sort : list of str, bool, optional
            * default: True
            * for `export_format` csv and `obj` types :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            * True: sort the headers automatically
            * False: do not sort the headers at all
            * list of str: sort the headers returned by priority based on provided list
        header_add_sensor : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not prefix the headers with the associated sensor name for each column
            * True: prefix the headers with the associated sensor name for each column
        header_add_type : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not postfix the headers with the result type for each column
            * True: postfix the headers with the result type for each column
        expand_grouped_columns : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not expand multiline row entries into their own rows
            * True: expand multiline row entries into their own rows
        explode_json_string_values : bool, optional
            * default: False
            * for `export_format` json or csv and `obj` type :class:`taniumpy.object_types.base.BaseType`
            * False: do not explode JSON strings in object attributes into their own object attributes
            * True: explode JSON strings in object attributes into their own object attributes
        minimal : bool, optional
            * default: False
            * for `export_format` xml and `obj` type :class:`taniumpy.object_types.base.BaseType`
            * False: include empty attributes in XML output
            * True: do not include empty attributes in XML output
        report_file: str, optional
            * default: None
            * filename to save report as, will be automatically generated if not supplied
        report_dir: str, optional
            * default: None
            * directory to save report in, will use current working directory if not supplied
        prefix: str, optional
            * default: ''
            * prefix to add to `report_file`
        postfix: str, optional
            * default: ''
            * postfix to add to `report_file`

        Returns
        -------
        report_path, result : tuple
            * report_path : str, the full path to the file created with contents of `result`
            * result : str, the contents written to report_path

        See Also
        --------
        :func:`pytan.handler.Handler.export_obj` : method that performs the actual work to do the exporting
        :func:`pytan.handler.Handler.create_report_file` : method that performs the actual work to write the report file

        Notes
        -----
        When performing a CSV export and importing that CSV into excel, keep in mind that Excel has a per cell character limit of 32,000. Any cell larger than that will be broken up into a whole new row, which can wreak havoc with data in Excel.
        """
        report_file = kwargs.get('report_file', None)

        if not report_file:
            report_file = "{}_{}.{}".format(
                type(obj).__name__, utils.get_now(), export_format,
            )
            m = "No report file name supplied, generated name: {!r}".format
            self.mylog.debug(m(report_file))

        clean_keys = ['obj', 'export_format', 'contents', 'report_file']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        # get the results of exporting the object
        contents = self.export_obj(obj=obj, export_format=export_format, **clean_kwargs)
        report_path = self.create_report_file(
            report_file=report_file, contents=contents, **clean_kwargs
        )
        return report_path, contents

    def create_report_file(self, contents, report_file=None, **kwargs):
        """Exports a python API object to a file

        Parameters
        ----------
        contents : str
            * contents to write to `report_file`
        report_file : str, optional
            * filename to save report as
        report_dir : str, optional
            * default: None
            * directory to save report in, will use current working directory if not supplied
        prefix : str, optional
            * default: ''
            * prefix to add to `report_file`
        postfix : str, optional
            * default: ''
            * postfix to add to `report_file`

        Returns
        -------
        report_path : str
            * the full path to the file created with `contents`
        """
        if report_file is None:
            report_file = 'pytan_report_{}.txt'.format(utils.get_now())

        # try to get report_dir from the report_file
        report_dir = os.path.dirname(report_file)

        # try to get report_dir from kwargs
        if not report_dir:
            report_dir = kwargs.get('report_dir', None)

        # just use current working dir
        if not report_dir:
            report_dir = os.getcwd()

        # make report_dir if it doesnt exist
        if not os.path.isdir(report_dir):
            os.makedirs(report_dir)

        # remove any path from report_file
        report_file = os.path.basename(report_file)

        # if prefix/postfix, add to report_file
        prefix = kwargs.get('prefix', '')
        postfix = kwargs.get('postfix', '')
        report_file, report_ext = os.path.splitext(report_file)
        report_file = '{}{}{}{}'.format(prefix, report_file, postfix, report_ext)

        # join the report_dir and report_file to come up with report_path
        report_path = os.path.join(report_dir, report_file)

        with open(report_path, 'wb') as fd:
            fd.write(contents)

        m = "Report file {!r} written with {} bytes".format
        self.mylog.info(m(report_path, len(contents)))
        return report_path

    # TODO: WRITE!!
    # SHELL SCRIPT
    # ADDED: 3.0.0
    def create_computer_group(self, name, **kwargs):
        buckets = self.parse_buckets(**kwargs)
        g_obj = self.build_group_buckets(**kwmerge(kwargs, buckets=buckets))
        return g_obj
        """
        def create_group(self, groupname, filters=[], filter_options=[], **kwargs):
        utils.check_for_help(kwargs=kwargs)
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs)

        filter_defs = utils.dehumanize_question_filters(question_filters=filters)
        option_defs = utils.dehumanize_question_options(question_options=filter_options)

        h = (
            "Issue a GetObject to get the full object of specified sensors for inclusion in a "
            "group"
        )
        filter_defs = self._get_sensor_defs(defs=filter_defs, pytan_help=h, **clean_kwargs)

        add_group_obj = utils.build_group_obj(
            q_filter_defs=filter_defs, q_option_defs=option_defs,
        )
        add_group_obj.name = groupname

        h = "Issue an AddObject to add a Group object"
        group_obj = self._add(obj=add_group_obj, pytan_help=h, **clean_kwargs)

        m = "New group {!r} created with ID {!r}, filter text: {!r}".format
        self.mylog.info(m(group_obj.name, group_obj.id, group_obj.text))

        return group_obj
        """

    def token_processor_operator(self, token_name, parsed, **kwargs):
        def striplow(x):
            return x.lower().replace(" ", "")

        if token_name in parsed:
            value = parsed[token_name]

            try:
                match = [x for x in constants.OPERATOR_MAPS if striplow(x) == striplow(value)][0]
            except:
                valid_tmpl = "operator: {k:<20} help: {h}".format
                valids = constants.OPERATOR_MAPS.items()
                valids = [valid_tmpl(k=k, **v) for k, v in valids]
                valids = "\n\t".join(sorted(list(valids)))

                m = "Invalid value '{o}' supplied for token '{t}' in string {s!r}, valid values:\n\t{v}"
                m = m.format(t=token_name, o=value, v=valids, s=parsed["parsed_from"])
                raise exceptions.ParseError(m)
            else:
                match_def = constants.OPERATOR_MAPS[match]

            orig_token_name = "__ORIGINAL_{t}".format(t=token_name)
            parsed[orig_token_name] = parsed[token_name]

            parsed["__MATCHED_OPERATOR"] = {match: match_def}
            parsed["__ORIGINAL_VALUE"] = parsed["value"]
            parsed["value"] = match_def.get("pre", "") + parsed["value"] + match_def.get("post", "")
            parsed[token_name] = match_def["o"]

            if "not" not in parsed and "n" in match_def:
                parsed["not"] = match_def["n"]

        return parsed

    def token_processor_boolean(self, token_name, parsed, **kwargs):
        def coerce_bool(x):
            if str(x).lower() in constants.YES_LIST:
                ret = True
            elif str(x).lower() in constants.NO_LIST:
                ret = False
            else:
                ret = None
            return ret

        if token_name in parsed:
            value = parsed[token_name]
            bool_type = coerce_bool(value)
            if bool_type is None:
                valid_tmpl = "{b} type: {t}".format
                valids = []
                valids += [valid_tmpl(b="True", t=t) for t in constants.YES_LIST]
                valids += [valid_tmpl(b="False", t=t) for t in constants.NO_LIST]
                valids = "\n\t".join(valids)

                m = "Invalid boolean '{o}' supplied for token '{t}' in string {s!r}, valid values:\n\t{v}"
                m = m.format(o=value, t=token_name, v=valids, s=parsed["parsed_from"])
                raise exceptions.ParseError(m)

            orig_token_name = "__ORIGINAL_{t}".format(t=token_name)
            parsed[orig_token_name] = value
            parsed[token_name] = bool_type

        return parsed

    def token_processor_integer(self, token_name, parsed, **kwargs):
        if token_name in parsed:
            value = parsed[token_name]

            try:
                int_type = int(value)
            except:
                m = "Invalid integer '{o}' supplied for token '{t}' in string {s!r}"
                m = m.format(o=value, t=token_name, s=parsed["parsed_from"])
                raise exceptions.ParseError(m)

            orig_token_name = "__ORIGINAL_{t}".format(t=token_name)
            parsed[orig_token_name] = value
            parsed[token_name] = int_type

        return parsed

    def token_processor_type(self, token_name, parsed, **kwargs):
        def striplow(x):
            return x.lower().replace(" ", "")

        if token_name in parsed:
            value = parsed[token_name]

            try:
                match = [x for x in constants.VALUE_TYPES if striplow(x) == striplow(value)][0]
            except:
                valid_tmpl = "type: {k:<20} help: {h}".format
                valids = constants.VALUE_TYPES.items()
                valids = [valid_tmpl(k=k, **v) for k, v in valids]
                valids = "\n\t".join(sorted(list(valids)))

                m = "Invalid value '{o}' supplied for token '{t}' in string {s!r}, valid values:\n\t{v}"
                m = m.format(t=token_name, o=value, v=valids, s=parsed["parsed_from"])
                raise exceptions.ParseError(m)
            else:
                match_def = constants.VALUE_TYPES[match]

            orig_token_name = "__ORIGINAL_{t}".format(t=token_name)
            parsed[orig_token_name] = parsed[token_name]

            parsed["__MATCHED_TYPE"] = {match: match_def}
            parsed[token_name] = match_def["t"]

        return parsed

    def token_processor_params(self, token_name, parsed, **kwargs):

        # found_params =
        return parsed

    def token_processor_required(self, token_name, parsed, **kwargs):
        if token_name not in parsed:
            m = "Token '{k}' not found in string '{s}', tokens found: {t}"
            m = m.format(k=token_name, s=parsed["parsed_from"], t=parsed.keys())
            PARSELOG.error(m)
            raise exceptions.ParseError(m)
        return parsed

    def token_processor_search_obj(self, token_name, parsed, **kwargs):
        search_ot = kwargs.get("search_obj_type", "")
        valid_sf = kwargs.get("search_valid_fields", [])
        include_hidden = kwargs.get("search_include_hidden", False)

        if search_ot:
            search_obj = parsed["search_obj"] = getattr(taniumpy, search_ot)()
            parsed_from = parsed["parsed_from"]
            search = parsed["search"]
            search_field = parsed["search_field"]

            try:
                match = [x for x in valid_sf if search_field.lower() == x.lower()][0]
            except:
                valids = "\n\t".join(valid_sf)
                m = "Invalid value '{o}' supplied for token '{t}' in string {s!r}, valid values:\n\t{v}"
                m = m.format(t="search_field", o=search_field, v=valids, s=parsed_from)
                raise exceptions.ParseError(m)
            else:
                search_field = parsed["search_field"] = match

            setattr(search_obj, search_field, search)
            margs = kwmerge(kwargs, obj=search_obj, include_hidden_flag=int(include_hidden))

            if "source_id" in dir(search_obj) and not include_hidden:
                cf_obj = self.build_obj(obj_name="CacheFilter", attrs={"value": 0, "field": "source_id"})
                margs["cache_filters"] = margs.get("cache_filters", taniumpy.CacheFilterList())
                margs["cache_filters"].append(cf_obj)

            try:
                obj = parsed["obj"] = self.session.find(**margs)
            except:
                m = "Unable to find {o} by search_field '{f}' using search '{s}' (from string {os!r})"
                m = m.format(o=search_obj, f=search_field, s=search, os=parsed_from)
                raise exceptions.NotFoundError(m)
            else:
                m = "Found {o} by search_field '{f}' using search '{s}' (from string {os!r})"
                m = m.format(o=obj, f=search_field, s=search, os=parsed_from)
                PARSELOG.debug(m)

        return parsed

    def parse_string_to_tokens(self, string, unnamed, **kwargs):
        defaults = kwargs.get("defaults", {})
        processors = kwargs.get("processors", {})

        tokens = [x.lstrip() for x in ESCAPED_COMMAS_RE.split(string)]

        parsed = {}

        for token in tokens:
            split_token = ESCAPED_COLONS_RE.split(token, maxsplit=1)
            name, value = split_token if len(split_token) == 2 else (unnamed, split_token[0])

            if name in parsed:
                m = "Duplicate token found with name '{n}' value '{v}', other value '{o}' in string '{s}'"
                m = m.format(n=name, v=value, o=parsed[name], s=string)
                PARSELOG.error(m)
                raise exceptions.ParseError(m)

            parsed[name] = value

        parsed["parsed_from"] = string

        for name, default_value in defaults.items():
            parsed[name] = parsed.get(name, default_value)

        for name, token_processors in processors:
            for token_processor in token_processors:
                method = getattr(self, "token_processor_{tp}".format(tp=token_processor))
                parsed = method(**kwmerge(kwargs, token_name=name, parsed=parsed))

        m = "Parsed string '{s}' into:\n{t}"
        m = m.format(s=string, t=pprint.pformat(parsed))
        PARSELOG.debug(m)
        return parsed

    def parse_filters(self, buckets, **kwargs):
        strings = mklist(kwargs.get("filters", []))
        pargs = kwmerge(kwargs, **constants.FILTER_PARSE_ARGS)

        for string in strings:
            parsed = self.parse_string_to_tokens(**kwmerge(pargs, string=string))

            buckets[parsed["bucket"]] = buckets.get(parsed["bucket"], {})
            buckets[parsed["bucket"]]["filters"] = buckets[parsed["bucket"]].get("filters", [])
            buckets[parsed["bucket"]]["filters"].append(parsed)
        return buckets

    def parse_buckets(self, **kwargs):
        buckets = kwargs.get("buckets", {})

        buckets = self.parse_filters(buckets=buckets, **kwargs)
        # ret["groups"] = self.parse_groups(**kwargs)

        # buckets = {}
        # buckets = self.parse_filter_buckets(parses=filters, buckets=buckets)
        # buckets = self.parse_group_buckets(parses=groups, buckets=buckets)
        # buckets = self.parse_option_buckets(parses=options, buckets=buckets)
        return buckets

    # BEGIN PRIVATE METHODS
    def _add(self, obj, **kwargs):
        """Wrapper for interfacing with :func:`taniumpy.session.Session.add`

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            * object to add

        Returns
        -------
        added_obj : :class:`taniumpy.object_types.base.BaseType`
           * full object that was added
        """
        # TODO 3.0.0 bug fix
        try:
            search_str = obj.str_obj(str_all_attrs=True)
        except:
            search_str = obj

        self.mylog.debug("Adding object {}".format(search_str))

        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)

        clean_keys = ['obj', 'objtype', 'obj_map']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        h = "Issue an AddObject to add an object"
        clean_kwargs['pytan_help'] = clean_kwargs.get('pytan_help', h)

        try:
            added_obj = self.session.add(obj=obj, **clean_kwargs)
        except Exception as e:
            err = "Error while trying to add object '{}': {}!!".format
            raise exceptions.HandlerError(err(search_str, e))

        h = "Issue a GetObject on the recently added object in order to get the full object"
        clean_kwargs['pytan_help'] = h

        try:
            added_obj = self._find(obj=added_obj, **clean_kwargs)
        except Exception as e:
            self.mylog.error(e)
            err = "Error while trying to find recently added object {}!!".format
            raise exceptions.HandlerError(err(search_str))

        self.mylog.debug("Added object {}".format(added_obj))
        return added_obj

    def _find(self, obj, **kwargs):
        """Wrapper for interfacing with :func:`taniumpy.session.Session.find`

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            * object to find

        Returns
        -------
        found : :class:`taniumpy.object_types.base.BaseType`
           * full object that was found
        """
        # TODO 3.0.0 bug fix
        try:
            search_str = obj.str_obj(str_all_attrs=True)
        except:
            search_str = obj

        self.mylog.debug("Searching for {}".format(search_str))

        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)

        clean_keys = ['obj', 'objtype', 'obj_map']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        h = "Issue a GetObject to find an object"
        clean_kwargs['pytan_help'] = clean_kwargs.get('pytan_help', h)

        try:
            found = self.session.find(obj=obj, **clean_kwargs)
        except Exception as e:
            self.mylog.debug(e)
            err = "No results found searching for {} (error: {})!!".format
            raise exceptions.NotFoundError(err(search_str, e))

        if utils.empty_obj(found):
            err = "No results found searching for {}!!".format
            raise exceptions.NotFoundError(err(search_str))

        self.mylog.debug("Found {}".format(found))
        return found

    def _get_multi(self, obj_map, **kwargs):
        """Find multiple item wrapper using :func:`_find`

        Parameters
        ----------
        obj_map : dict
            * dict containing the map for a given object type

        Returns
        -------
        found : :class:`taniumpy.object_types.base.BaseType`
           * full object that was found
        """
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]
        api_kw = {k: v for k, v in zip(api_attrs, api_kwattrs)}

        multi_type = obj_map['multi']
        single_type = obj_map['single']

        # create a list object to append our searches to
        api_obj_multi = utils.get_taniumpy_obj(obj_map=multi_type)()

        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if utils.is_list(v):
                for i in v:
                    api_obj_single = utils.get_taniumpy_obj(obj_map=single_type)()
                    setattr(api_obj_single, k, i)
                    api_obj_multi.append(api_obj_single)
            else:
                api_obj_single = utils.get_taniumpy_obj(obj_map=single_type)()
                setattr(api_obj_single, k, v)
                api_obj_multi.append(api_obj_single)

        clean_keys = ['obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        # find the multi list object
        found = self._find(obj=api_obj_multi, **clean_kwargs)
        return found

    def _get_single(self, obj_map, **kwargs):
        """Find single item wrapper using :func:`_find`

        Parameters
        ----------
        obj_map : dict
            * dict containing the map for a given object type

        Returns
        -------
        found : :class:`taniumpy.object_types.base.BaseType`
           * full object that was found
        """
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]
        api_kw = {k: v for k, v in zip(api_attrs, api_kwattrs)}

        # we create a list object to append our single item searches to
        if obj_map.get('allfix', ''):
            all_type = obj_map['allfix']
        else:
            all_type = obj_map['all']

        found = utils.get_taniumpy_obj(obj_map=all_type)()

        clean_keys = ['obj_map', 'k', 'v']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if utils.is_list(v):
                for i in v:
                    for x in self._single_find(obj_map=obj_map, k=k, v=i, **clean_kwargs):
                        found.append(x)
            else:
                for x in self._single_find(obj_map=obj_map, k=k, v=v, **clean_kwargs):
                    found.append(x)

        return found

    def _single_find(self, obj_map, k, v, **kwargs):
        """Wrapper for single item searches interfacing with :func:`taniumpy.session.Session.find`

        Parameters
        ----------
        obj_map : dict
            * dict containing the map for a given object type
        k : str
            * attribute name to set to `v`
        v : str
            * attribute value to set on `k`

        Returns
        -------
        found : :class:`taniumpy.object_types.base.BaseType`
           * full object that was found
        """
        found = []

        single_type = obj_map['single']
        api_obj_single = utils.get_taniumpy_obj(obj_map=single_type)()

        setattr(api_obj_single, k, v)

        clean_keys = ['obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        obj_ret = self._find(obj=api_obj_single, **clean_kwargs)

        if getattr(obj_ret, '_list_properties', ''):
            for i in obj_ret:
                found.append(i)
        else:
            found.append(obj_ret)

        return found

    def _get_sensor_defs(self, defs, **kwargs):
        """Uses :func:`get` to update a definition with a sensor object

        Parameters
        ----------
        defs : list of dict
            * list of dicts containing sensor definitions

        Returns
        -------
        defs : list of dict
           * list of dicts containing sensor definitions with sensor object in 'sensor_obj'
        """
        s_obj_map = constants.GET_OBJ_MAP['sensor']
        search_keys = s_obj_map['search']

        kwargs['include_hidden_flag'] = kwargs.get('include_hidden_flag', 0)

        clean_keys = ['objtype']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        for d in defs:
            def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}
            def_search.update(clean_kwargs)

            # get the sensor object
            if 'sensor_obj' not in d:
                h = (
                    "Issue a GetObject to get the full object of a sensor for inclusion in a "
                    "question or action"
                )
                def_search['pytan_help'] = def_search.get('pytan_help', h)
                d['sensor_obj'] = self.get(objtype='sensor', **def_search)[0]
        return defs

    def _get_package_def(self, d, **kwargs):
        """Uses :func:`get` to update a definition with a package object

        Parameters
        ----------
        d : dict
            * dict containing package definition

        Returns
        -------
        d : dict
           * dict containing package definitions with package object in 'package_obj'
        """
        s_obj_map = constants.GET_OBJ_MAP['package']
        search_keys = s_obj_map['search']

        kwargs['include_hidden_flag'] = kwargs.get('include_hidden_flag', 0)

        clean_keys = ['objtype']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}
        def_search.update(clean_kwargs)

        # get the package object
        if 'package_obj' not in d:
            h = (
                "Issue a GetObject to get the full object of a package for inclusion in an "
                "action"
            )
            def_search['pytan_help'] = def_search.get('pytan_help', h)
            d['package_obj'] = self.get(objtype='package', **def_search)[0]
        return d

    def _export_class_BaseType(self, obj, export_format, **kwargs): # noqa
        """Handles exporting :class:`taniumpy.object_types.base.BaseType`

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            * taniumpy object to export
        export_format : str
            * str of format to perform export in

        Returns
        -------
        result : str
           * results of exporting `obj` into format `export_format`
        """
        # run the handler that is specific to this export_format, if it exists
        format_method_str = '_export_format_' + export_format
        format_handler = getattr(self, format_method_str, '')

        clean_keys = ['obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        if format_handler:
            result = format_handler(obj=obj, **clean_kwargs)
        else:
            err = "{!r} not coded for in Handler!".format
            raise exceptions.HandlerError(err(export_format))

        return result

    def _export_class_ResultSet(self, obj, export_format, **kwargs): # noqa
        """Handles exporting :class:`taniumpy.object_types.result_set.ResultSet`

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.result_set.ResultSet`
            * taniumpy object to export
        export_format : str
            * str of format to perform export in

        Returns
        -------
        result : str
           * results of exporting `obj` into format `export_format`
        """

        """
        ensure kwargs[sensors] has all the sensors that correlate
        to the what_hash of each column, but only if header_add_sensor=True
        needed for: ResultSet.write_csv(header_add_sensor=True)
        """
        header_add_sensor = kwargs.get('header_add_sensor', False)
        sensors = kwargs.get('sensors', []) or getattr(obj, 'sensors', [])

        clean_keys = ['objtype', 'hash', 'obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        if header_add_sensor and export_format == 'csv':
            clean_kwargs['sensors'] = sensors
            sensor_hashes = [x.hash for x in sensors]
            column_hashes = [x.what_hash for x in obj.columns]
            missing_hashes = [
                x for x in column_hashes if x not in sensor_hashes and x > 1
            ]
            if missing_hashes:
                missing_sensors = self.get(objtype='sensor', hash=missing_hashes, **clean_kwargs)
                clean_kwargs['sensors'] += list(missing_sensors)

        # run the handler that is specific to this export_format, if it exists
        format_method_str = '_export_format_' + export_format
        format_handler = getattr(self, format_method_str, '')

        if format_handler:
            result = format_handler(obj=obj, **clean_kwargs)
        else:
            err = "{!r} not coded for in Handler!".format
            raise exceptions.HandlerError(err(export_format))

        return result

    def _export_format_csv(self, obj, **kwargs):
        """Handles exporting format: CSV

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.result_set.ResultSet` or :class:`taniumpy.object_types.base.BaseType`
            * taniumpy object to export

        Returns
        -------
        result : str
           * results of exporting `obj` into csv format
        """
        if not hasattr(obj, 'write_csv'):
            err = "{!r} has no write_csv() method!".format
            raise exceptions.HandlerError(err(obj))

        out = io.BytesIO()

        clean_keys = ['fd', 'val']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        if getattr(obj, '_list_properties', ''):
            result = obj.write_csv(fd=out, val=list(obj), **clean_kwargs)
        else:
            result = obj.write_csv(fd=out, val=obj, **clean_kwargs)

        result = out.getvalue()
        return result

    def _export_format_json(self, obj, **kwargs):
        """Handles exporting format: JSON

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.result_set.ResultSet` or :class:`taniumpy.object_types.base.BaseType`
            * taniumpy object to export

        Returns
        -------
        result : str
           * results of exporting `obj` into json format
        """
        if not hasattr(obj, 'to_json'):
            err = "{!r} has no to_json() method!".format
            raise exceptions.HandlerError(err(obj))

        clean_keys = ['jsonable']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        result = obj.to_json(jsonable=obj, **clean_kwargs)
        return result

    def _export_format_xml(self, obj, **kwargs):
        """Handles exporting format: XML

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.result_set.ResultSet` or :class:`taniumpy.object_types.base.BaseType`
            * taniumpy object to export

        Returns
        -------
        result : str
           * results of exporting `obj` into XML format
        """
        result = None

        if hasattr(obj, 'toSOAPBody'):
            raw_xml = obj.toSOAPBody(**kwargs)
        elif hasattr(obj, '_RAW_XML'):
            raw_xml = obj._RAW_XML
        else:
            err = "{!r} has no toSOAPBody() method or _RAW_XML attribute!".format
            raise exceptions.HandlerError(err(obj))

        clean_keys = ['x']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        result = utils.xml_pretty(x=raw_xml, **clean_kwargs)
        return result

    def _deploy_action(self, run=False, get_results=True, **kwargs):  # noqa
        """Deploy an action and get the results back

        This method requires in-depth knowledge of how filters and options are created in the API, and as such is not meant for human consumption. Use :func:`deploy_action` instead.

        Parameters
        ----------
        package_def : dict
            * definition that describes a package
        action_filter_defs : str, dict, list of str or dict, optional
            * default: []
            * action filter definitions
        action_option_defs : dict, list of dict, optional
            * default: []
            * action filter option definitions
        start_seconds_from_now : int, optional
            * default: 0
            * start action N seconds from now
        distribute_seconds : int, optional
            * default: 0
            * distribute action evenly over clients over N seconds
        issue_seconds : int, optional
            * default: 0
            * have the server re-ask the action status question if performing a GetResultData over N seconds ago
        expire_seconds : int, optional
            * default: package.expire_seconds
            * expire action N seconds from now, will be derived from package if not supplied
        run : bool, optional
            * default: False
            * False: just ask the question that pertains to verify action, export the results to CSV, and raise exceptions.RunFalse -- does not deploy the action
            * True: actually deploy the action
        get_results : bool, optional
            * default: True
            * True: wait for result completion after deploying action
            * False: just deploy the action and return the object in `ret`
        action_name : str, optional
            * default: prepend package name with "API Deploy "
            * custom name for action
        action_comment : str, optional
            * default:
            * custom comment for action
        polling_secs : int, optional
            * default: 5
            * Number of seconds to wait in between GetResultInfo loops
            * This is passed through to :class:`pollers.ActionPoller`
        complete_pct : int/float, optional
            * default: 100
            * Percentage of passed_count out of successfully run actions to consider the action "done"
            * This is passed through to :class:`pollers.ActionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`pollers.ActionPoller`
        override_passed_count : int, optional
            * instead of getting number of systems that should run this action by asking a question, use this number
            * This is passed through to :class:`pollers.ActionPoller`

        Returns
        -------
        ret : dict, containing:
            * `saved_action_object` : :class:`taniumpy.object_types.saved_action.SavedAction`, the saved_action added for this action (None if 6.2)
            * `action_object` : :class:`taniumpy.object_types.action.Action`, the action object that tanium created for `saved_action`
            * `package_object` : :class:`taniumpy.object_types.package_spec.PackageSPec`, the package object used in `saved_action`
            * `action_info` : :class:`taniumpy.object_types.result_info.ResultInfo`, the initial GetResultInfo call done before getting results
            * `poller_object` : :class:`pollers.ActionPoller`, poller object used to wait until all results are in before getting `action_results`
            * `poller_success` : None if `get_results` == False, elsewise True or False
            * `action_results` : None if `get_results` == False, elsewise :class:`taniumpy.object_types.result_set.ResultSet`, the results for `action_object`
            * `action_result_map` : None if `get_results` == False, elsewise progress map for `action_object` in dictionary form

        Examples
        --------
        >>> # example of dict for `package_def`
        >>> package_def = {'name': 'PackageName1', 'params':{'param1': 'value1'}}

        >>> # example of str for `action_filter_defs`
        >>> action_filter_defs = 'Sensor1'

        >>> # example of dict for `action_filter_defs`
        >>> action_filter_defs = {
        ... 'name': 'Sensor1',
        ...     'filter': {
        ...         'operator': 'RegexMatch',
        ...         'not_flag': 0,
        ...         'value': '.*'
        ...     },
        ...     'options': {'and_flag': 1}
        ... }

        See Also
        --------
        :data:`constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`constants.OPTION_MAPS` : valid option dictionaries for options

        Notes
        -----
            * For 6.2:
                * We need to add an Action object
                * The Action object should not be in an ActionList
                * Action.start_time must be specified, if it is not specified the action shows up as expired immediately. We default to 1 second from current time if start_seconds_from_now is not passed in

            * For 6.5 / 6.6:
                * We need to add a SavedAction object, the server creates the Action object for us
                * To emulate what the console does, the SavedAction should be in a SavedActionList
                * Action.start_time does not need to be specified
        """
        utils.check_for_help(kwargs=kwargs)

        clean_keys = [
            'defs',
            'd',
            'obj',
            'objtype',
            'key',
            'default',
            'defname',
            'deftypes',
            'empty_ok',
            'id',
            'pytan_help',
            'handler',
        ]

        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        if not self.session.platform_is_6_5(**kwargs):
            objtype = taniumpy.Action
            objlisttype = None
            force_start_time = True
        else:
            objtype = taniumpy.SavedAction
            objlisttype = taniumpy.SavedActionList
            force_start_time = False

        package_def = utils.parse_defs(
            defname='package_def',
            deftypes=['dict()'],
            empty_ok=False,
            **clean_kwargs
        )
        action_filter_defs = utils.parse_defs(
            defname='action_filter_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=True,
            **clean_kwargs
        )
        action_option_defs = utils.parse_defs(
            defname='action_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **clean_kwargs
        )

        utils.val_package_def(package_def=package_def)
        utils.val_sensor_defs(sensor_defs=action_filter_defs)

        package_def = self._get_package_def(d=package_def, **clean_kwargs)
        h = (
            "Issue a GetObject to get the full object of a sensor for inclusion in a "
            "Group for an Action"
        )
        action_filter_defs = self._get_sensor_defs(
            defs=action_filter_defs, pytan_help=h, **clean_kwargs
        )

        start_seconds_from_now = utils.get_kwargs_int(
            key='start_seconds_from_now', default=0, **clean_kwargs
        )

        expire_seconds = utils.get_kwargs_int(key='expire_seconds', **clean_kwargs)

        action_name_default = "API Deploy {0.name}".format(package_def['package_obj'])
        action_name = kwargs.get('action_name', action_name_default)

        action_comment_default = 'Created by PyTan v{}'.format(version.__version__)
        action_comment = kwargs.get('action_comment', action_comment_default)

        issue_seconds_default = 0
        issue_seconds = kwargs.get('issue_seconds', issue_seconds_default)

        distribute_seconds_default = 0
        distribute_seconds = kwargs.get('distribute_seconds', distribute_seconds_default)

        """
        ask the question that pertains to the action filter, save the result as CSV,
        and raise a RunFalse exception

        this will be used to get a count for how many servers should be seen
        in the deploy action resultdata as 'completed'

        We supply Computer Name and Online = True as the sensors if run is
        False, then exit out after asking the question to allow the user
        to verify the results by looking at the CSV file

        The action filter for the deploy action is used as the question
        filter

        note from jwk: passed_count == the number of machines that pass the filter and
        therefore the number that should take the action
        """
        if not run:
            pre_action_sensors = ['Computer Name', 'Online, that =:True']
            pre_action_sensor_defs = utils.dehumanize_sensors(sensors=pre_action_sensors)

            q_clean_keys = [
                'sensor_defs',
                'question_filter_defs',
                'question_option_defs',
                'hide_no_results_flag',
                'pytan_help',
                'get_results',
            ]
            q_clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=q_clean_keys)

            h = (
                "Ask a question to determine the number of systems this action would affect if it "
                "was actually run"
            )
            q_clean_kwargs['sensor_defs'] = pre_action_sensor_defs
            q_clean_kwargs['question_filter_defs'] = action_filter_defs
            q_clean_kwargs['question_option_defs'] = action_option_defs
            q_clean_kwargs['hide_no_results_flag'] = 1

            pre_action_question = self._ask_manual(pytan_help=h, **q_clean_kwargs)

            passed_count = pre_action_question['question_results'].passed
            m = "Number of systems that match action filter (passed_count): {}".format
            self.mylog.debug(m(passed_count))

            if passed_count == 0:
                m = "Number of systems that match the action filters provided is zero!"
                raise exceptions.HandlerError(m)

            default_format = 'csv'
            export_format = kwargs.get('export_format', default_format)

            default_prefix = 'VERIFY_BEFORE_DEPLOY_ACTION_'
            export_prefix = kwargs.get('prefix', default_prefix)

            e_clean_keys = [
                'obj',
                'export_format',
                'prefix',
            ]
            e_clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=e_clean_keys)
            e_clean_kwargs['obj'] = pre_action_question['question_results']
            e_clean_kwargs['export_format'] = export_format
            e_clean_kwargs['prefix'] = export_prefix
            report_path, result = self.export_to_report_file(**e_clean_kwargs)

            m = (
                "'Run' is not True!!\n"
                "View and verify the contents of {} (length: {} bytes)\n"
                "Re-run this deploy action with run=True after verifying"
            ).format
            raise exceptions.RunFalse(m(report_path, len(result)))

        # BUILD THE PACKAGE OBJECT TO BE ADDED TO THE ACTION
        add_package_obj = utils.copy_package_obj_for_action(obj=package_def['package_obj'])

        # if source_id is specified, a new package will be created with the parameters
        # for this action embedded into it - specifying hidden = 1 will ensure the new package
        # is hidden
        add_package_obj.hidden_flag = 1

        param_objlist = utils.build_param_objlist(
            obj=package_def['package_obj'],
            user_params=package_def['params'],
            delim='',
            derive_def=False,
            empty_ok=False,
        )

        if param_objlist:
            add_package_obj.source_id = package_def['package_obj'].id
            add_package_obj.parameters = param_objlist
        else:
            add_package_obj.id = package_def['package_obj'].id
            add_package_obj.name = package_def['package_obj'].name
            add_package_obj.source_id = None

        m = "DEPLOY_ACTION objtype: {}, objlisttype: {}, force_start_time: {}, version: {}".format
        self.mylog.debug(m(objtype, objlisttype, force_start_time, self.session.server_version))

        # BUILD THE ACTION OBJECT TO BE ADDED
        add_obj = objtype()
        add_obj.package_spec = add_package_obj
        add_obj.id = -1
        add_obj.name = action_name
        add_obj.issue_seconds = issue_seconds
        add_obj.distribute_seconds = distribute_seconds
        add_obj.comment = action_comment
        add_obj.status = 0
        add_obj.start_time = ''
        add_obj.end_time = ''
        add_obj.public_flag = 0
        add_obj.policy_flag = 0
        add_obj.approved_flag = 0
        add_obj.issue_count = 0

        if action_filter_defs or action_option_defs:
            targetgroup_obj = utils.build_group_obj(
                q_filter_defs=action_filter_defs, q_option_defs=action_option_defs,
            )
            add_obj.target_group = targetgroup_obj
        else:
            targetgroup_obj = None

        if start_seconds_from_now:
            add_obj.start_time = utils.seconds_from_now(secs=start_seconds_from_now)

        if force_start_time and not add_obj.start_time:
            if not start_seconds_from_now:
                start_seconds_from_now = 1
            add_obj.start_time = utils.seconds_from_now(secs=start_seconds_from_now)

        if package_def['package_obj'].expire_seconds:
            add_obj.expire_seconds = package_def['package_obj'].expire_seconds

        if expire_seconds:
            add_obj.expire_seconds = expire_seconds

        if objlisttype:
            add_objs = objlisttype()
            add_objs.append(add_obj)
            h = "Issue an AddObject to add a list of SavedActions (6.5 logic)"
            added_objs = self._add(obj=add_objs, pytan_help=h, **clean_kwargs)
            added_obj = added_objs[0]

            m = "DEPLOY_ACTION ADDED: {}, ID: {}".format
            self.mylog.debug(m(added_obj.__class__.__name__, added_obj.id))

            h = "Issue a GetObject to get the last action created for a SavedAction"
            action_obj = self._find(obj=added_obj.last_action, pytan_help=h, **clean_kwargs)
        else:
            added_obj = None
            h = "Issue an AddObject to add a single Action (6.2 logic)"
            action_obj = self._add(obj=add_obj, pytan_help=h, **clean_kwargs)

        h = "Issue a GetObject to get the package for an Action"
        action_package = self._find(obj=action_obj.package_spec, pytan_help=h, **clean_kwargs)

        m = "DEPLOY_ACTION ADDED: {}, ID: {}".format
        self.mylog.debug(m(action_package.__class__.__name__, action_package.id))

        m = "DEPLOY_ACTION ADDED: {}, ID: {}".format
        self.mylog.debug(m(action_obj.__class__.__name__, action_obj.id))

        h = (
            "Issue a GetResultInfo on an Action to have the Server create a question that "
            "tracks the results for a Deployed Action"
        )
        action_info = self.get_result_info(obj=action_obj, pytan_help=h, **clean_kwargs)

        m = "DEPLOY_ACTION ADDED: Question for Action Results, ID: {}".format
        self.mylog.debug(m(action_info.question_id))

        poller = pollers.ActionPoller(handler=self, obj=action_obj, **clean_kwargs)
        ret = {
            'saved_action_object': added_obj,
            'action_object': action_obj,
            'package_object': action_package,
            'group_object': targetgroup_obj,
            'action_info': action_info,
            'poller_object': poller,
            'action_results': None,
            'action_result_map': None,
            'poller_success': None,
        }

        if get_results:
            ret['poller_success'] = ret['poller_object'].run(**kwargs)
            ret['action_results'] = ret['poller_object'].result_data
            ret['action_result_map'] = ret['poller_object'].result_map

        return ret

    def _ask_manual(self, get_results=True, **kwargs):
        """Ask a manual question using definitions and get the results back

        This method requires in-depth knowledge of how filters and options are created in the API,
        and as such is not meant for human consumption. Use :func:`ask_manual` instead.

        Parameters
        ----------
        sensor_defs : str, dict, list of str or dict
            * default: []
            * sensor definitions
        question_filter_defs : dict, list of dict, optional
            * default: []
            * question filter definitions
        question_option_defs : dict, list of dict, optional
            * default: []
            * question option definitions
        get_results : bool, optional
            * default: True
            * True: wait for result completion after asking question
            * False: just ask the question and return it in `ret`
        sse : bool, optional
            * default: False
            * True: perform a server side export when getting result data
            * False: perform a normal get result data (default for 6.2)
            * Keeping False by default for now until the columnset's are properly identified in the server export
        sse_format : str, optional
            * default: 'xml_obj'
            * format to have server side export report in, one of: {'csv', 'xml', 'xml_obj', 'cef', 0, 1, 2}
        leading : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to prepend to each row
        trailing : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to append to each row
        polling_secs : int, optional
            * default: 5
            * Number of seconds to wait in between GetResultInfo loops
            * This is passed through to :class:`pollers.QuestionPoller`
        complete_pct : int/float, optional
            * default: 99
            * Percentage of mr_tested out of estimated_total to consider the question "done"
            * This is passed through to :class:`pollers.QuestionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`pollers.QuestionPoller`
        callbacks : dict, optional
            * default: {}
            * can be a dict of functions to be run with the key names being the various state changes: 'ProgressChanged', 'AnswersChanged', 'AnswersComplete'
            * This is passed through to :func:`pollers.QuestionPoller.run`
        override_estimated_total : int, optional
            * instead of getting number of systems that should see this question from result_info.estimated_total, use this number
            * This is passed through to :func:`pollers.QuestionPoller`
        force_passed_done_count : int, optional
            * when this number of systems have passed the right hand side of the question, consider the question complete
            * This is passed through to :func:`pollers.QuestionPoller`

        Returns
        -------
        ret : dict, containing:
            * `question_object` : :class:`taniumpy.object_types.question.Question`, the actual question created and added by PyTan
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`, the Result Set for `question_object` if `get_results` == True
            * `poller_object` : :class:`pollers.QuestionPoller`, poller object used to wait until all results are in before getting `question_results`
            * `poller_success` : None if `get_results` == True, elsewise True or False

        Examples
        --------
        >>> # example of str for sensor_defs
        >>> sensor_defs = 'Sensor1'

        >>> # example of dict for sensor_defs
        >>> sensor_defs = {
        ... 'name': 'Sensor1',
        ...     'filter': {
        ...         'operator': 'RegexMatch',
        ...         'not_flag': 0,
        ...         'value': '.*'
        ...     },
        ...     'params': {'key': 'value'},
        ...     'options': {'and_flag': 1}
        ... }

        >>> # example of dict for question_filter_defs
        >>> question_filter_defs = {
        ...     'operator': 'RegexMatch',
        ...     'not_flag': 0,
        ...     'value': '.*'
        ... }

        See Also
        --------
        :data:`constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`constants.OPTION_MAPS` : valid option dictionaries for options
        """
        utils.check_for_help(kwargs=kwargs)

        clean_keys = [
            'defs',
            'd',
            'obj',
            'objtype',
            'key',
            'default',
            'defname',
            'deftypes',
            'empty_ok',
            'id',
            'pytan_help',
            'handler',
            'sse',
        ]
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        # get our defs from kwargs and churn them into what we want
        sensor_defs = utils.parse_defs(
            defname='sensor_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=True,
            **clean_kwargs
        )

        q_filter_defs = utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **clean_kwargs
        )

        q_option_defs = utils.parse_defs(
            defname='question_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **clean_kwargs
        )

        sse = kwargs.get('sse', False)
        clean_kwargs['sse_format'] = clean_kwargs.get('sse_format', 'xml_obj')

        max_age_seconds = utils.get_kwargs_int(
            key='max_age_seconds', default=600, **clean_kwargs
        )

        # do basic validation of our defs
        utils.val_sensor_defs(sensor_defs=sensor_defs)
        utils.val_q_filter_defs(q_filter_defs=q_filter_defs)

        # get the sensor objects that are in our defs and add them as d['sensor_obj']
        h = (
            "Issue a GetObject to get the full object of a sensor for inclusion in a "
            "Select for a Question"
        )
        sensor_defs = self._get_sensor_defs(defs=sensor_defs, pytan_help=h, **clean_kwargs)
        h = (
            "Issue a GetObject to get the full object of a sensor for inclusion in a "
            "Group for a Question"
        )
        q_filter_defs = self._get_sensor_defs(defs=q_filter_defs, pytan_help=h, **clean_kwargs)

        # build a SelectList object from our sensor_defs
        selectlist_obj = utils.build_selectlist_obj(sensor_defs=sensor_defs)

        # build a Group object from our question filters/options
        group_obj = utils.build_group_obj(
            q_filter_defs=q_filter_defs, q_option_defs=q_option_defs,
        )

        # build a Question object from selectlist_obj and group_obj
        add_obj = utils.build_manual_q(selectlist_obj=selectlist_obj, group_obj=group_obj)

        add_obj.max_age_seconds = max_age_seconds

        # add our Question and get a Question ID back
        h = "Issue an AddObject to add a Question object"
        added_obj = self._add(obj=add_obj, pytan_help=h, **clean_kwargs)

        m = "Question Added, ID: {}, query text: {!r}, expires: {}".format
        self.mylog.debug(m(added_obj.id, added_obj.query_text, added_obj.expiration))

        poller = pollers.QuestionPoller(handler=self, obj=added_obj, **clean_kwargs)

        ret = {
            'question_object': added_obj,
            'poller_object': poller,
            'question_results': None,
            'poller_success': None,
        }

        if get_results:
            # poll the Question ID returned above to wait for results
            ret['poller_success'] = ret['poller_object'].run(**clean_kwargs)

            # get the results
            if sse and self.session.platform_is_6_5(**clean_kwargs):
                rd = self.get_result_data_sse(obj=added_obj, **clean_kwargs)
            else:
                rd = self.get_result_data(obj=added_obj, **clean_kwargs)

            if isinstance(rd, taniumpy.object_types.result_set.ResultSet):
                # add the sensors from this question to the ResultSet object for reporting
                rd.sensors = [x['sensor_obj'] for x in sensor_defs]

            ret['question_results'] = rd
        return ret

    def _version_support_check(self, v_maps, **kwargs):
        """Checks that each of the version maps in v_maps is greater than or equal to
        the current servers version

        Parameters
        ----------
        v_maps : list of str
            * each str should be a platform version
            * each str will be checked against self.session.server_version
            * if self.session.server_version is not greater than or equal to any str in v_maps, return will be False
            * if self.session.server_version is greater than all strs in v_maps, return will be True
            * if self.server_version is invalid/can't be determined, return will be False

        Returns
        -------
        bool
            * True if all values in all v_maps are greater than or equal to self.session.server_version
            * False otherwise
        """
        if self.session._invalid_server_version():
            # server version is not valid, force a refresh right now
            self.session.get_server_version(**kwargs)

        if self.session._invalid_server_version():
            # server version is STILL invalid, return False
            return False

        for v_map in v_maps:
            if not self.session.server_version >= v_map:
                return False
        return True

    def _check_sse_format_support(self, sse_format, sse_format_int, **kwargs):
        """Determines if the export format integer is supported in the server version

        Parameters
        ----------
        sse_format : str or int
            * user supplied export format
        sse_format_int : int
            * `sse_format` parsed into an int
        """
        if sse_format_int not in constants.SSE_RESTRICT_MAP:
            return

        restrict_maps = constants.SSE_RESTRICT_MAP[sse_format_int]

        if not self._version_support_check(v_maps=restrict_maps, **kwargs):
            restrict_maps_txt = '\n'.join([str(x) for x in restrict_maps])

            m = (
                "Server version {} does not support export format {!r}, "
                "server version must be equal to or greater than one of:\n{}"
            ).format

            m = m(self.session.server_version, sse_format, restrict_maps_txt)

            raise exceptions.UnsupportedVersionError(m)

    def _resolve_sse_format(self, sse_format, **kwargs):
        """Resolves the server side export format the user supplied to an integer for the API

        Parameters
        ----------
        sse_format : str or int
            * user supplied export format

        Returns
        -------
        sse_format_int : int
            * `sse_format` parsed into an int
        """
        sse_format_int = [x[-1] for x in constants.SSE_FORMAT_MAP if sse_format.lower() in x]

        if not sse_format_int:
            m = "Unsupport export format {!r}, must be one of:\n{}".format
            ef_map_txt = '\n'.join(
                [', '.join(['{!r}'.format(x) for x in y]) for y in constants.SSE_FORMAT_MAP]
            )
            raise exceptions.HandlerError(m(sse_format, ef_map_txt))

        sse_format_int = sse_format_int[0]

        m = "'sse_format resolved from '{}' to '{}'".format
        self.mylog.debug(m(sse_format, sse_format_int))

        self._check_sse_format_support(
            sse_format=sse_format, sse_format_int=sse_format_int, **kwargs
        )

        return sse_format_int

    def _check_sse_version(self, **kwargs):
        """Validates that the server version supports server side export"""
        if not self.session.platform_is_6_5(**kwargs):
            m = "Server side export not supported in version: {}".format
            m = m(self.session.server_version)
            raise exceptions.UnsupportedVersionError(m)

    def _check_sse_crash_prevention(self, obj, **kwargs):
        """Runs a number of methods used to prevent crashing the platform server when performing server side exports

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            * object to pass to self._check_sse_empty_rs
        """
        clean_keys = ['obj', 'v_maps', 'ok_version']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        restrict_maps = constants.SSE_CRASH_MAP

        ok_version = self._version_support_check(v_maps=restrict_maps, **clean_kwargs)

        self._check_sse_timing(ok_version=ok_version, **clean_kwargs)
        self._check_sse_empty_rs(obj=obj, ok_version=ok_version, **clean_kwargs)

    def _check_sse_timing(self, ok_version, **kwargs):
        """Checks that the last server side export was at least 1 second ago if server version is less than any versions in constants.SSE_CRASH_MAP

        Parameters
        ----------
        ok_version : bool
            * if the version currently running is an "ok" version
        """
        last_get_rd_sse = getattr(self, 'last_get_rd_sse', None)

        if last_get_rd_sse:
            last_elapsed = datetime.datetime.utcnow() - last_get_rd_sse
            if last_elapsed.seconds == 0 and not ok_version:
                m = "You must wait at least one second between server side export requests!".format
                raise exceptions.ServerSideExportError(m())

        self.last_get_rd_sse = datetime.datetime.utcnow()

    def _check_sse_empty_rs(self, obj, ok_version, **kwargs):
        """Checks if the server version is less than any versions in constants.SSE_CRASH_MAP, if so verifies that the result set is not empty

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            * object to get result info for to ensure non-empty answers
        ok_version : bool
            * if the version currently running is an "ok" version
        """
        clean_keys = ['obj']
        clean_kwargs = utils.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        if not ok_version:
            ri = self.get_result_info(obj=obj, **clean_kwargs)
            if ri.row_count == 0:
                m = (
                    "No rows available to perform a server side export with, result info: {}"
                ).format
                raise exceptions.ServerSideExportError(m(ri))
