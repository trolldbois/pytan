# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""The main :mod:`pytan` module that provides first level entities for programmatic use."""

import os
import logging
import io
import datetime
import json

from . import __version__
from . import utils
from . import session
from . import pollers

mylog = logging.getLogger(__name__)


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
    gmt_log : bool, optional
        * default: True
        * True: use GMT timezone for log output
        * False: use local time for log output
    session_id : str, optional
        * default: None
        * session_id to use while authenticating instead of username/password
    pytan_user_config : str, optional
        * default: utils.constants.PYTAN_USER_CONFIG
        * JSON file containing key/value pairs to override class variables

    Other Parameters
    ----------------
    http_debug : bool, optional
        * default: False
        * False: do not print requests package debug
        * True: do print requests package debug
        * This is passed through to :class:`session.Sessions`
    http_auth_retry: bool, optional
        * default: True
        * True: retry HTTP GET/POST's
        * False: do not retry HTTP GET/POST's
        * This is passed through to :class:`session.Sessions`
    http_retry_count: int, optional
        * default: 5
        * number of times to retry HTTP GET/POST's if the connection times out/fails
        * This is passed through to :class:`session.Sessions`
    soap_request_headers : dict, optional
        * default: {'Content-Type': 'text/xml; charset=utf-8', 'Accept-Encoding': 'gzip'}
        * dictionary of headers to add to every HTTP GET/POST
        * This is passed through to :class:`session.Sessions`
    auth_connect_timeout_sec : int, optional
        * default: 5
        * number of seconds before timing out for a connection while authenticating
        * This is passed through to :class:`session.Sessions`
    auth_response_timeout_sec : int, optional
        * default: 15
        * number of seconds before timing out for a response while authenticating
        * This is passed through to :class:`session.Sessions`
    info_connect_timeout_sec : int, optional
        * default: 5
        * number of seconds before timing out for a connection while getting /info.json
        * This is passed through to :class:`session.Sessions`
    info_response_timeout_sec : int, optional
        * default: 15
        * number of seconds before timing out for a response while getting /info.json
        * This is passed through to :class:`session.Sessions`
    soap_connect_timeout_sec : int, optional
        * default: 15
        * number of seconds before timing out for a connection for a SOAP request
        * This is passed through to :class:`session.Sessions`
    soap_response_timeout_sec : int, optional
        * default: 540
        * number of seconds before timing out for a response for a SOAP request
        * This is passed through to :class:`session.Sessions`
    stats_loop_enabled : bool, optional
        * default: False
        * False: do not enable the statistics loop thread
        * True: enable the statistics loop thread
        * This is passed through to :class:`session.Sessions`
    stats_loop_sleep_sec : int, optional
        * default: 5
        * number of seconds to sleep in between printing the statistics when stats_loop_enabled is True
        * This is passed through to :class:`session.Sessions`
    record_all_requests: bool, optional
        * default: False
        * False: do not add each requests response object to session.ALL_REQUESTS_RESPONSES
        * True: add each requests response object to session.ALL_REQUESTS_RESPONSES
        * This is passed through to :class:`session.Sessions`
    stats_loop_targets : list of dict, optional
        * default: [{'Version': 'Settings/Version'}, {'Active Questions': 'Active Question Cache/Active Question Estimate'}, {'Clients': 'Active Question Cache/Active Client Estimate'}, {'Strings': 'String Cache/Total String Count'}, {'Handles': 'System Performance Info/HandleCount'}, {'Processes': 'System Performance Info/ProcessCount'}, {'Memory Available': 'percentage(System Performance Info/PhysicalAvailable,System Performance Info/PhysicalTotal)'}]
        * list of dictionaries with the key being the section of info.json to print info from, and the value being the item with in that section to print the value
        * This is passed through to :class:`session.Sessions`
    persistent: bool, optional
        * default: False
        * False: do not request a persistent session
        * True: do request a persistent
        * This is passed through to :func:`session.Sessions.authenticate`
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
    :data:`utils.constants.LOG_LEVEL_MAPS` : maps a given `loglevel` to respective logger names and their logger levels
    :class:`session.Session` : Session object used by Handler

    Examples
    --------
    Setup a Handler() object::

        >>> import sys
        >>> sys.path.append('/path/to/pytan/')
        >>> import pytan
        >>> handler = pytan.Handler('username', 'password', 'host')
    """

    def __init__(self, **kwargs):
        super(Handler, self).__init__()
        self.mylog = mylog
        if kwargs.get('loglevel', 0) >= 30:
            utils.log.install_console()
            utils.log.set_all_levels()

        self._parse_args(kwargs)
        self._validate_args()
        utils.log.setup(**self.args_db['parsed_args'])
        self._log_args()

        # establish our Session to the Tanium server
        self.session = session.Session(**self.args_db['parsed_args'])

        # authenticate to the Tanium server using the Session class
        self.session.authenticate(**self.args_db['parsed_args'])

    def __str__(self):
        str_tpl = "PyTan v{} Handler for {}".format
        ret = str_tpl(__version__, self.session)
        return ret

    def read_config_file(self):
        """Read a PyTan User Config and update the current class variables"""
        puc_env = self.args_db['env_args'].get('config_file', '')
        puc_kwarg = self.args_db['original_args'].get('config_file', '')
        puc_def = self.args_db['default_args']['config_file']
        puc = puc_env or puc_kwarg or puc_def
        puc = os.path.expanduser(puc)
        puc_dict = {}

        if not os.path.isfile(puc):
            m = "Unable to find PyTan User config file at: {}".format
            self.mylog.debug(m(puc))
            return puc_dict

        try:
            with open(puc) as fh:
                puc_dict = json.load(fh)
            m = "PyTan User config file successfully loaded: {} "
            m = m.format(puc)
            self.mylog.debug(m)
        except Exception as e:
            err = "PyTan User config file at: {} is invalid, exception: {}"
            err = err.format(puc, e)
            raise utils.exceptions.PytanError(err)
        return puc_dict

    def write_config_file(self, **kwargs):
        """Write a PyTan User Config with the current class variables for use with pytan_user_config in instantiating Handler()

        Parameters
        ----------
        new_config : str, optional
            * default: self.pytan_user_config
            * JSON file to wite with current class variables

        Returns
        -------
        puc : str
            * filename of PyTan User Config that was written to
        """
        puc = kwargs.get('new_config', '') or self.args_db['parsed_args']['config_file']
        puc = os.path.expanduser(puc)

        puc_dict = dict(self.args_db['parsed_args'])

        # obfuscate the password
        if puc_dict['password']:
            puc_dict['password'] = utils.coder.vig_decode(
                key=utils.constants.PYTAN_KEY,
                string=puc_dict['password'],
            )

        try:
            with open(puc, 'w+') as fh:
                json.dump(puc_dict, fh, skipkeys=True, indent=2)
        except Exception as e:
            err = "Failed to write PyTan User config: '{}', exception: {}"
            err = err.format(puc, e)
            raise utils.exceptions.PytanError(err)
        else:
            m = "PyTan User config file successfully written: {} "
            m = m.format(puc)
            self.mylog.info(m)
        return puc

    def get_server_version(self, **kwargs):
        """Uses :func:`session.Session.get_server_version` to get the version of the Tanium Server

        Returns
        -------
        server_version: str
            * Version of Tanium Server in string format
        """

        server_version = self.session.get_server_version(**kwargs)
        return server_version

    def ask_manual(self, **kwargs):
        """pass."""
        utils.helpers.check_for_help(kwargs=kwargs)
        left = kwargs.get('left', [])
        right = kwargs.get('right', [])
        # max_age_seconds = utils.validate.get_kwargs_int(key='max_age_seconds', default=600, **kwargs)

        # parser = utils.parsers.LeftSide(left)
        # print parser.parsed_specs

        left = self._get_spec_objects(left)
        right = self._get_spec_objects(right)

        kwargs['obj'] = utils.tanium_obj.create_question_obj(left=left, right=right)
        # kwargs['obj'].max_age_seconds = max_age_seconds

        m = "Question Built: {}"
        m = m.format(kwargs['obj'].to_json(kwargs['obj']))
        self.mylog.debug(m)

        kwargs['obj'] = self._add(**kwargs)

        m = "Question Added, ID: {0.id}, query text: {0.query_text!r}, expires: {0.expiration}"
        m = m.format(kwargs['obj'])
        self.mylog.debug(m)

        ret = {
            'question_object': kwargs['obj'],
            'poller_object': pollers.QuestionPoller(handler=self, **kwargs),
            'question_results': None,
            'poller_success': None,
        }

        if kwargs.get('get_results', True):
            # poll the Question ID returned above to wait for results
            ret['poller_success'] = ret['poller_object'].run(**kwargs)
            kwargs['sse_format'] = kwargs.get('sse_format', 'xml_obj')
            ret['question_results'] = self.get_result_data(**kwargs)
        return ret

    def ask_saved(self, **kwargs):
        """Ask a saved question and get the results back

        Parameters
        ----------
        id : int, list of int, optional
            * id of saved question to ask
        name : str, list of str
            * name of saved question
        refresh: bool, optional
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
            * This is passed through to :class:`QuestionPoller`
        complete_pct : int/float, optional
            * default: 99
            * Percentage of mr_tested out of estimated_total to consider the question "done"
            * This is passed through to :class:`QuestionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`QuestionPoller`
        callbacks : dict, optional
            * default: {}
            * can be a dict of functions to be run with the key names being the various state changes: 'ProgressChanged', 'AnswersChanged', 'AnswersComplete'
            * This is passed through to :func:`QuestionPoller.run`
        override_estimated_total : int, optional
            * instead of getting number of systems that should see this question from result_info.estimated_total, use this number
            * This is passed through to :func:`QuestionPoller`
        force_passed_done_count : int, optional
            * when this number of systems have passed the right hand side of the question, consider the question complete
            * This is passed through to :func:`QuestionPoller`

        Returns
        -------
        ret : dict, containing
            * `question_object` : :class:`utils.taniumpy.object_types.saved_question.SavedQuestion`, the saved question object
            * `question_object` : :class:`utils.taniumpy.object_types.question.Question`, the question asked by `saved_question_object`
            * `question_results` : :class:`utils.taniumpy.object_types.result_set.ResultSet`, the results for `question_object`
            * `poller_object` : None if `refresh` == False, elsewise :class:`QuestionPoller`, poller object used to wait until all results are in before getting `question_results`,
            * `poller_success` : None if `refresh` == False, elsewise True or False

        Notes
        -----
        id or name must be supplied
        """
        specs = kwargs.get('specs', [])
        if not specs:
            err = "Must supply arg 'specs' for identifying the saved question to ask"
            raise utils.exceptions.PytanError(err)

        # get the saved_question object the user passed in
        sq_obj = self.get_saved_questions(limit=1, **kwargs)

        find_args = {}
        find_args.update(kwargs)
        find_args['pytan_help'] = utils.helpstr.SQ_GETQ
        find_args['obj'] = sq_obj.question
        q_obj = self.session.find(**find_args)

        poller = None

        refresh = kwargs.get('refresh', False)
        if refresh:
            # if GetResultInfo is issued on a saved question, Tanium will issue a new question
            # to fetch new/updated results
            gri_args = {}
            gri_args.update(kwargs)
            gri_args['pytan_help'] = utils.helpstr.SQ_RD
            gri_args['obj'] = sq_obj
            self.get_result_info(**gri_args)

            # re-fetch the saved question object to get the newly asked question info
            find_args = {}
            find_args.update(kwargs)
            find_args['pytan_help'] = utils.helpstr.SQ_RESQ
            find_args['obj'] = utils.tanium_obj.shrink_obj(obj=sq_obj)
            sq_obj = self.session.find(**find_args)

            find_args = {}
            find_args.update(kwargs)
            find_args['pytan_help'] = utils.helpstr.SQ_GETQ
            find_args['obj'] = sq_obj.question
            q_obj = self.session.find(**find_args)

            m = "Question Added, ID: {}, query text: {!r}, expires: {}"
            m = m.format(q_obj.id, q_obj.query_text, q_obj.expiration)
            self.mylog.debug(m)

            # poll the new question for this saved question to wait for results
            poll_args = {}
            poll_args.update(kwargs)
            poll_args['obj'] = q_obj
            poll_args['handler'] = self
            poller = pollers.QuestionPoller(**poll_args)

        ret = {
            'saved_question_object': sq_obj,
            'poller_object': poller,
            'poller_success': None,
            'question_object': q_obj,
            'question_results': None,
        }

        if kwargs.get('get_results', True):
            if ret['poller_object']:
                ret['poller_success'] = ret['poller_object'].run(**kwargs)
            grd_args = {}
            grd_args.update(kwargs)
            grd_args['obj'] = q_obj
            grd_args['sse_format'] = kwargs.get('sse_format', 'xml_obj')
            ret['question_results'] = self.get_result_data(**grd_args)
        return ret

    def parse_query(self, question_text, **kwargs):
        """Ask a parsed question as `question_text` and get a list of parsed results back

        Parameters
        ----------
        question_text : str
            * The question text you want the server to parse into a list of parsed results

        Returns
        -------
        parse_job_results : :class:`utils.taniumpy.object_types.parse_result_group.ParseResultGroup`
        """
        if not self.session.platform_is_6_5(**kwargs):
            m = "ParseJob not supported in version: {}"
            m = m.format(self.session.server_version)
            raise utils.exceptions.UnsupportedVersionError(m)

        parse_job = utils.taniumpy.ParseJob()
        parse_job.question_text = question_text
        parse_job.parser_version = 2

        pq_args = {}
        pq_args.update(kwargs)
        pq_args['obj'] = parse_job

        parse_job_results = self.session.add(**pq_args)
        return parse_job_results

    def ask_parsed(self, question_text, picker=None, **kwargs):
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
            * This is passed through to :class:`QuestionPoller`
        complete_pct : int/float, optional
            * default: 99
            * Percentage of mr_tested out of estimated_total to consider the question "done"
            * This is passed through to :class:`QuestionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`QuestionPoller`
        callbacks : dict, optional
            * default: {}
            * can be a dict of functions to be run with the key names being the various state changes: 'ProgressChanged', 'AnswersChanged', 'AnswersComplete'
            * This is passed through to :func:`QuestionPoller.run`
        override_estimated_total : int, optional
            * instead of getting number of systems that should see this question from result_info.estimated_total, use this number
            * This is passed through to :func:`QuestionPoller`
        force_passed_done_count : int, optional
            * when this number of systems have passed the right hand side of the question, consider the question complete
            * This is passed through to :func:`QuestionPoller`

        Returns
        -------
        ret : dict, containing:
            * `question_object` : :class:`utils.taniumpy.object_types.question.Question`, the actual question added by PyTan
            * `question_results` : :class:`utils.taniumpy.object_types.result_set.ResultSet`, the Result Set for `question_object` if `get_results` == True
            * `poller_object` : :class:`QuestionPoller`, poller object used to wait until all results are in before getting `question_results`
            * `poller_success` : None if `get_results` == True, elsewise True or False
            * `parse_results` : :class:`utils.taniumpy.object_types.parse_result_group_list.ParseResultGroupList`, the parse result group returned from Tanium after parsing `question_text`

        Examples
        --------

        Ask the server to parse 'computer name', but don't pick a choice (will print out a list of choices at critical logging level and then throw an exception):
            >>> v = handler.ask_parsed('computer name')

        Ask the server to parse 'computer name' and pick index 1 as the question you want to run:
            >>> v = handler.ask_parsed('computer name', picker=1)
        """
        if not self.session.platform_is_6_5(**kwargs):
            m = "ParseJob not supported in version: {}"
            m = m.format(self.session.server_version)
            raise utils.exceptions.UnsupportedVersionError(m)

        pq_args = {}
        pq_args.update(kwargs)
        pq_args['question_text'] = question_text
        pq_args['pytan_help'] = utils.helpstr.PJ
        parse_job_results = self.parse_query(**pq_args)

        if not parse_job_results:
            m = "Question Text '{}' was unable to be parsed into a valid query text by the server"
            raise utils.exceptions.ServerParseError(m)

        pi = "Index {0}, Score: {1.score}, Query: {1.question_text!r}"
        pw = (
            "You must supply an index as picker=$index to choose one of the parse "
            "responses -- re-run ask_parsed with picker set to one of these indexes!!"
        )

        if picker is None:
            self.mylog.critical(pw)
            for idx, x in enumerate(parse_job_results):
                self.mylog.critical(pi.format(idx + 1, x))
            raise utils.exceptions.PickerError(pw)

        try:
            picked_parse_job = parse_job_results[picker - 1]
        except:
            m = "You supplied an invalid picker index {} - {}"
            m = m.format(picker, pw)
            self.mylog.critical(m)

            for idx, x in enumerate(parse_job_results):
                self.mylog.critical(pi.format(idx + 1, x))
            raise utils.exceptions.PickerError(pw)

        add_obj = picked_parse_job.question

        # add our Question and get a Question ID back
        add_args = {}
        add_args.update(kwargs)
        add_args['obj'] = add_obj
        add_args['pytan_help'] = utils.helpstr.PJ_ADD
        q_obj = self._add(**add_args)

        m = "Question Added, ID: {}, query text: {!r}, expires: {}"
        m = m.format(q_obj.id, q_obj.query_text, q_obj.expiration)
        self.mylog.debug(m)

        poll_args = {}
        poll_args.update(kwargs)
        poll_args['handler'] = self
        poll_args['obj'] = q_obj
        poller = pollers.QuestionPoller(**poll_args)

        ret = {
            'question_object': q_obj,
            'poller_object': poller,
            'question_results': None,
            'poller_success': None,
            'parse_results': parse_job_results,
        }

        get_results = kwargs.get('get_results', True)
        if get_results:
            # poll the Question ID returned above to wait for results
            ret['poller_success'] = ret['poller_object'].run(**kwargs)

            grd_args = {}
            grd_args.update(kwargs)
            grd_args['obj'] = q_obj
            grd_args['sse_format'] = kwargs.get('sse_format', 'xml_obj')
            ret['question_results'] = self.get_result_data(**grd_args)

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
        filters : str, list of str, optional
            * default: []
            * each string must describe a sensor and a filter which limits which computers the action will deploy `package` to
        options : str, list of str, optional
            * default: []
            * options to apply to `filters`
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
            * False: just ask the question that pertains to verify action, export the results to CSV, and raise RunFalse -- does not deploy the action
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
            * This is passed through to :class:`pytan.pollers.ActionPoller`
        complete_pct : int/float, optional
            * default: 100
            * Percentage of passed_count out of successfully run actions to consider the action "done"
            * This is passed through to :class:`pytan.pollers.ActionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`pytan.pollers.ActionPoller`
        override_passed_count : int, optional
            * instead of getting number of systems that should run this action by asking a question, use this number
            * This is passed through to :class:`pytan.pollers.ActionPoller`

        Returns
        -------
        ret : dict, containing:
            * `saved_action_object` : :class:`utils.taniumpy.object_types.saved_action.SavedAction`, the saved_action added for this action (None if 6.2)
            * `action_object` : :class:`utils.taniumpy.object_types.action.Action`, the action object that tanium created for `saved_action`
            * `package_object` : :class:`utils.taniumpy.object_types.package_spec.PackageSPec`, the package object used in `saved_action`
            * `action_info` : :class:`utils.taniumpy.object_types.result_info.ResultInfo`, the initial GetResultInfo call done before getting results
            * `poller_object` : :class:`pytan.pollers.ActionPoller`, poller object used to wait until all results are in before getting `action_results`
            * `poller_success` : None if `get_results` == False, elsewise True or False
            * `action_results` : None if `get_results` == False, elsewise :class:`utils.taniumpy.object_types.result_set.ResultSet`, the results for `action_object`
            * `action_result_map` : None if `get_results` == False, elsewise progress map for `action_object` in dictionary form

        Examples
        --------
        >>> # example of str for `package`
        >>> package = 'Package1'

        >>> # example of str for `package` with params
        >>> package = 'Package1{key:value}'

        >>> # example of str for `filters` with params and filter for sensors
        >>> filters = 'Sensor1{key:value}, that contains:example text'

        >>> # example of list of str for `options`
        >>> options = ['max_data_age:3600', 'and']

        See Also
        --------
        :data:`utils.constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`utils.constants.OPTION_MAPS` : valid option dictionaries for options
        :func:`pytan.handler.Handler._deploy_action` : private method with the actual workflow used to create and add the action object
        """

        utils.helpers.check_for_help(kwargs=kwargs)

        # the human string describing the sensors/filter that user wants
        # to deploy the action against
        filters = kwargs.get('filters', [])

        # the question options to use on the pre-action question and on the
        # group for the action filters
        options = kwargs.get('options', [])

        # name of package to deploy with params as {key=value1,key2=value2}
        package = kwargs.get('package', '')

        filter_defs = utils.parsers.parse_sensors(filters, 'filters', True)
        option_defs = utils.parsers.parse_options(options)
        package_def = utils.parsers.parse_package(package)

        clean_keys = ['package_def', 'filter_defs', 'option_defs']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        deploy_result = self._deploy_action(
            filter_defs=filter_defs,
            option_defs=option_defs,
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
        saved_action_approve_obj : :class:`utils.taniumpy.object_types.saved_action_approval.SavedActionApproval`
            * The object containing the return from SavedActionApproval
        """

        clean_keys = ['pytan_help', 'objtype', 'id', 'obj']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        h = "Issue a GetObject to find saved action objects"
        saved_action_obj = self.get(objtype='saved_action', id=id, pytan_help=h, **clean_kwargs)[0]

        add_sap_obj = utils.taniumpy.SavedActionApproval()
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
        action_stop_obj : :class:`utils.taniumpy.object_types.action_stop.ActionStop`
            The object containing the ID of the action stop job
        """

        clean_keys = ['pytan_help', 'objtype', 'id', 'obj']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        h = "Issue a GetObject to find the action object we want to stop"
        action_obj = self.get(objtype='action', id=id, pytan_help=h, **clean_kwargs)[0]

        add_action_stop_obj = utils.taniumpy.ActionStop()
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
            raise utils.exceptions.PytanError(m(self.export_obj(after_action_obj, 'json')))

        return action_stop_obj

    # Result Data / Result Info
    def get_result_data(self, obj, **kwargs):
        """Get the result data for a python API object

        This method issues a GetResultData command to the SOAP api for `obj`. GetResultData returns the columns and rows that are currently available for `obj`.

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.base.BaseType`
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
        rd : :class:`utils.taniumpy.object_types.result_set.ResultSet`
            The return of GetResultData for `obj`
        """
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
        obj : :class:`utils.taniumpy.object_types.base.BaseType`
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
        :data:`utils.constants.SSE_FORMAT_MAP` : maps `sse_format` to an integer for use by the SOAP API
        :data:`utils.constants.SSE_RESTRICT_MAP` : maps sse_format integers to supported platform versions
        :data:`utils.constants.SSE_CRASH_MAP` : maps platform versions that can cause issues in various scenarios

        Returns
        -------
        export_data : either `str` or :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * If sse_format is one of csv, xml, or cef, export_data will be a `str` containing the contents of the ResultSet in said format
            * If sse_format is xml_obj, export_data will be a :class:`utils.taniumpy.object_types.result_set.ResultSet`
        """
        """ note #1 from jwk:
        For Action GetResultData: You have to make a ResultInfo request at least once every 2 minutes. The server gathers the result data by asking a saved question. It won't re-issue the saved question unless you make a GetResultInfo request. When you make a GetResultInfo request, if there is no question that is less than 2 minutes old, the server will automatically reissue a new question instance to make sure fresh data is available.

        note #2 from jwk:
        To get the aggregate data (without computer names), set row_counts_only_flag = 1. To get the computer names, use row_counts_only_flag = 0 (default).
        """
        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)

        if kwargs.get('shrink', True):
            kwargs['obj'] = utils.tanium_obj.shrink_obj(obj=obj)

        if kwargs.get('aggregate', False):
            kwargs['row_counts_only_flag'] = 1

        if kwargs.get('sse', True):
            self._check_sse_version()
            self._check_sse_crash_prevention(obj=obj)
            sse_format = kwargs.get('sse_format', 'csv')
            sse_format_int = self._resolve_sse_format(sse_format=sse_format)

            grd_args = {}
            grd_args.update(kwargs)
            grd_args['pytan_help'] = kwargs.get('pytan_help', utils.helpstr.GRD_SSE)
            # add the export_flag = 1 to the kwargs for inclusion in options node
            grd_args['export_flag'] = 1
            # add the export_format to the kwargs for inclusion in options node
            grd_args['export_format'] = sse_format_int
            # add the export_leading_text to the kwargs for inclusion in options node
            if kwargs.get('leading', ''):
                grd_args['export_leading_text'] = kwargs.get('leading', '')
            # add the export_trailing_text to the kwargs for inclusion in options node
            if kwargs.get('trailing', ''):
                grd_args['export_trailing_text'] = kwargs.get('trailing', '')

            # do a getresultdata to start the SSE and get
            export_id = self.session.get_result_data_sse(**grd_args)

            m = "Server Side Export Started, id: '{}'"
            m = m.format(export_id)
            self.mylog.debug(m)

            poll_args = {}
            poll_args.update(kwargs)
            poll_args['export_id'] = export_id
            poll_args['handler'] = self

            poller = pollers.SSEPoller(**poll_args)
            poller_success = poller.run(**kwargs)

            if not poller_success:
                m = "SSE Poller failed while waiting for completion, last status: {}"
                m = m.format(getattr(poller, 'sse_status', 'Unknown'))
                raise utils.exceptions.ServerSideExportError(m)

            rd = poller.get_sse_data(**kwargs)

            if sse_format.lower() == 'xml_obj':
                rd = utils.tanium_obj.xml_to_result_set_obj(x=rd)
        else:
            # do a normal getresultdata
            grd_args = {}
            grd_args.update(kwargs)
            grd_args['pytan_help'] = utils.helpstr.GRD
            rd = self.session.get_result_data(**grd_args)

        return rd

    def get_result_info(self, obj, **kwargs):
        """Get the result info for a python API object

        This method issues a GetResultInfo command to the SOAP api for `obj`. GetResultInfo returns information about how many servers have passed the `obj`, total number of servers, and so on.

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.base.BaseType`
            * object to get result data for
        shrink : bool, optional
            * default: True
            * True: Shrink the object down to just id/name/hash attributes (for smaller request)
            * False: Use the full object as is

        Returns
        -------
        ri : :class:`utils.taniumpy.object_types.result_info.ResultInfo`
            * The return of GetResultInfo for `obj`
        """
        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)
        kwargs['pytan_help'] = kwargs.get('pytan_help', utils.helpstr.GRI)
        if kwargs.get('shrink', True):
            kwargs['obj'] = utils.tanium_obj.shrink_obj(obj=obj)
        ri = self.session.get_result_info(**kwargs)
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
        ret : :class:`utils.taniumpy.object_types.base.BaseType`
            * TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`utils.constants.GET_OBJ_MAP` : maps objtype to supported 'create_json' types
        """

        obj_map = utils.tanium_obj.get_obj_map(objtype=objtype)

        create_json_ok = obj_map['create_json']

        if not create_json_ok:
            json_createable = ', '.join([
                x for x, y in utils.constants.GET_OBJ_MAP.items() if y['create_json']
            ])
            m = "{} is not a json createable object! Supported objects: {}".format
            raise utils.exceptions.PytanError(m(objtype, json_createable))

        add_obj = utils.tanium_obj.load_taniumpy_from_json(json_file=json_file)

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

        ret = utils.tanium_obj.get_taniumpy_obj(obj_map=all_type)()

        h = "Issue an AddObject to add an object"
        kwargs['pytan_help'] = kwargs.get('pytan_help', h)

        clean_keys = ['obj']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        for x in obj_list:
            try:
                list_obj = self._add(obj=x, **clean_kwargs)
            except Exception as e:
                m = (
                    "Failure while importing {}: {}\nJSON Dump of object: {}"
                ).format
                raise utils.exceptions.PytanError(m(x, e, x.to_json(x)))

            m = "New {} (ID: {}) created successfully!".format
            self.mylog.info(m(list_obj, getattr(list_obj, 'id', 'Unknown')))

            ret.append(list_obj)
        return ret

    def run_plugin(self, obj, **kwargs):
        """Wrapper around :func:`pytan.session.Session.run_plugin` to run the plugin and zip up the SQL results into a python dictionary

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.plugin.Plugin`
            * Plugin object to run

        Returns
        -------
        plugin_result, sql_zipped : tuple
            * plugin_result will be the taniumpy object representation of the SOAP response from Tanium server
            * sql_zipped will be a dict with the SQL results embedded in the SOAP response
        """

        # run the plugin
        h = "Issue a RunPlugin run a plugin and get results back"
        kwargs['pytan_help'] = kwargs.get('pytan_help', h)

        clean_keys = ['obj', 'p']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        plugin_result = self.session.run_plugin(obj=obj, **clean_kwargs)

        # zip up the sql results into a list of python dictionaries
        sql_zipped = utils.tanium_obj.plugin_zip(p=plugin_result)

        # return the plugin result and the python dictionary of results
        return plugin_result, sql_zipped

    def create_dashboard(self, name, text='', group='', public_flag=True, **kwargs):
        """Calls :func:`pytan.handler.Handler.run_plugin` to run the CreateDashboard plugin and parse the response

        Parameters
        ----------
        name : str
            * name of dashboard to create
        text : str, optional
            * default: ''
            * text for this dashboard
        group : str, optional
            * default: ''
            * group name for this dashboard
        public_flag : bool, optional
            * default: True
            * True: make this dashboard public
            * False: do not make this dashboard public

        Returns
        -------
        plugin_result, sql_zipped : tuple
            * plugin_result will be the taniumpy object representation of the SOAP response from Tanium server
            * sql_zipped will be a dict with the SQL results embedded in the SOAP response
        """

        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs)

        # get the ID for the group if a name was passed in
        if group:
            h = "Issue a GetObject to find the ID of a group name"
            group_id = self.get(objtype='group', name=group, pytan_help=h, **clean_kwargs)[0].id
        else:
            group_id = 0

        if public_flag:
            public_flag = 1
        else:
            public_flag = 0

        # create the plugin parent
        plugin = utils.taniumpy.Plugin()
        plugin.name = 'CreateDashboard'
        plugin.bundle = 'Dashboards'

        # create the plugin arguments
        plugin.arguments = utils.taniumpy.PluginArgumentList()

        arg1 = utils.taniumpy.PluginArgument()
        arg1.name = 'dash_name'
        arg1.type = 'String'
        arg1.value = name
        plugin.arguments.append(arg1)

        arg2 = utils.taniumpy.PluginArgument()
        arg2.name = 'dash_text'
        arg2.type = 'String'
        arg2.value = text
        plugin.arguments.append(arg2)

        arg3 = utils.taniumpy.PluginArgument()
        arg3.name = 'group_id'
        arg3.type = 'Number'
        arg3.value = group_id
        plugin.arguments.append(arg3)

        arg4 = utils.taniumpy.PluginArgument()
        arg4.name = 'public_flag'
        arg4.type = 'Number'
        arg4.value = public_flag
        plugin.arguments.append(arg4)

        arg5 = utils.taniumpy.PluginArgument()
        arg5.name = 'sqid_xml'
        arg5.type = 'String'
        arg5.value = ''
        plugin.arguments.append(arg5)

        # run the plugin
        h = "Issue a RunPlugin for the CreateDashboard plugin to create a dashboard"
        plugin_result, sql_zipped = self.run_plugin(obj=plugin, pytan_help=h, **clean_kwargs)

        # return the plugin result and the python dictionary of results
        return plugin_result, sql_zipped

    def delete_dashboard(self, name, **kwargs):
        """Calls :func:`pytan.handler.Handler.run_plugin` to run the DeleteDashboards plugin and parse the response

        Parameters
        ----------
        name : str
            * name of dashboard to delete

        Returns
        -------
        plugin_result, sql_zipped : tuple
            * plugin_result will be the taniumpy object representation of the SOAP response from Tanium server
            * sql_zipped will be a dict with the SQL results embedded in the SOAP response
        """

        clean_keys = ['obj', 'name', 'pytan_help']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        dashboards_to_del = self.get_dashboards(name=name, **clean_kwargs)[1]

        # create the plugin parent
        plugin = utils.taniumpy.Plugin()
        plugin.name = 'DeleteDashboards'
        plugin.bundle = 'Dashboards'

        # create the plugin arguments
        plugin.arguments = utils.taniumpy.PluginArgumentList()

        arg1 = utils.taniumpy.PluginArgument()
        arg1.name = 'dashboard_ids'
        arg1.type = 'Number_Set'
        arg1.value = ','.join([x['id'] for x in dashboards_to_del])
        plugin.arguments.append(arg1)

        # run the plugin
        h = "Issue a RunPlugin for the DeleteDashboards plugin to delete a dashboard"
        plugin_result, sql_zipped = self.run_plugin(obj=plugin, pytan_help=h, **clean_kwargs)

        # return the plugin result and the python dictionary of results
        return plugin_result, sql_zipped

    def get_dashboards(self, name='', **kwargs):
        """Calls :func:`pytan.handler.Handler.run_plugin` to run the GetDashboards plugin and parse the response

        Parameters
        ----------
        name : str, optional
            * default: ''
            * name of dashboard to get, if empty will return all dashboards

        Returns
        -------
        plugin_result, sql_zipped : tuple
            * plugin_result will be the taniumpy object representation of the SOAP response from Tanium server
            * sql_zipped will be a dict with the SQL results embedded in the SOAP response
        """

        clean_keys = ['obj', 'name', 'pytan_help']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        # create the plugin parent
        plugin = utils.taniumpy.Plugin()
        plugin.name = 'GetDashboards'
        plugin.bundle = 'Dashboards'

        # run the plugin
        h = "Issue a RunPlugin for the GetDashboards plugin to get all dashboards"
        plugin_result, sql_zipped = self.run_plugin(obj=plugin, pytan_help=h, **clean_kwargs)

        # if name specified, filter the list of dicts for matching name
        if name:
            sql_zipped = [x for x in sql_zipped if x['name'] == name]
            if not sql_zipped:
                m = "No dashboards found that match name: {!r}".format
                raise utils.exceptions.NotFoundError(m(name))

        # return the plugin result and the python dictionary of results
        return plugin_result, sql_zipped

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
        package_obj : :class:`utils.taniumpy.object_types.package_spec.PackageSpec`
            * TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`utils.constants.FILTER_MAPS` : valid filters for verify_filters
        :data:`utils.constants.OPTION_MAPS` : valid options for verify_filter_options
        """
        utils.helpers.check_for_help(kwargs=kwargs)

        clean_keys = ['obj', 'pytan_help', 'defs']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        metadata = kwargs.get('metadata', [])
        metadatalist_obj = utils.tanium_obj.build_metadatalist_obj(properties=metadata)

        # bare minimum arguments for new package: name, command
        add_package_obj = utils.taniumpy.PackageSpec()
        add_package_obj.name = name
        if display_name:
            add_package_obj.display_name = display_name
        add_package_obj.command = command
        add_package_obj.command_timeout = command_timeout_seconds
        add_package_obj.expire_seconds = expire_seconds
        add_package_obj.metadata = metadatalist_obj

        # VERIFY FILTERS
        if verify_filters:
            v_filter_defs = utils.parsers.parse_filters(filters=verify_filters)
            v_option_defs = utils.parsers.parse_options(options=verify_filter_options)
            v_filter_defs = self._get_sensor_defs(defs=v_filter_defs, **clean_kwargs)
            add_verify_group = utils.tanium_obj.build_group_obj(
                filter_defs=v_filter_defs,
                option_defs=v_option_defs,
            )
            h = "Issue an AddObject to add a Group object for this package"
            verify_group = self._add(obj=add_verify_group, pytan_help=h, **clean_kwargs)

            # this didn't work:
            # add_package_obj.verify_group = verify_group
            add_package_obj.verify_group_id = verify_group.id
            add_package_obj.verify_expire_seconds = verify_expire_seconds

        # PARAMETERS
        if parameters_json_file:
            add_package_obj.parameter_definition = utils.tanium_obj.load_param_json_file(
                parameters_json_file=parameters_json_file
            )

        # FILES
        if file_urls:
            filelist_obj = utils.taniumpy.PackageFileList()
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
                file_obj = utils.taniumpy.PackageFile()
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
        group_obj : :class:`utils.taniumpy.object_types.group.Group`
            * TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`utils.constants.FILTER_MAPS` : valid filters for filters
        :data:`utils.constants.OPTION_MAPS` : valid options for filter_options
        """

        utils.helpers.check_for_help(kwargs=kwargs)
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs)

        filter_defs = utils.parsers.parse_filters(filters=filters)
        option_defs = utils.parsers.parse_options(options=filter_options)

        h = (
            "Issue a GetObject to get the full object of specified sensors for inclusion in a "
            "group"
        )
        filter_defs = self._get_sensor_defs(defs=filter_defs, pytan_help=h, **clean_kwargs)

        add_group_obj = utils.tanium_obj.build_group_obj(
            filter_defs=filter_defs, option_defs=option_defs,
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
        user_obj : :class:`utils.taniumpy.object_types.user.User`
            * TaniumPy object added to Tanium SOAP Server
        """

        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs)

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
            rolelist_obj = utils.taniumpy.RoleList()

        metadatalist_obj = utils.tanium_obj.build_metadatalist_obj(
            properties=properties, nameprefix='TConsole.User.Property',
        )
        add_user_obj = utils.taniumpy.User()
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
        url_obj : :class:`utils.taniumpy.object_types.white_listed_url.WhiteListedUrl`
            * TaniumPy object added to Tanium SOAP Server
        """

        if regex:
            url = 'regex:' + url

        metadatalist_obj = utils.tanium_obj.build_metadatalist_obj(
            properties=properties, nameprefix='TConsole.WhitelistedURL',
        )

        add_url_obj = utils.taniumpy.WhiteListedUrl()
        add_url_obj.url_regex = url
        add_url_obj.download_seconds = download_seconds
        add_url_obj.metadata = metadatalist_obj

        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs)

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
        :data:`utils.constants.GET_OBJ_MAP` : maps objtype to supported 'search' keys
        """

        obj_map = utils.tanium_obj.get_obj_map(objtype=objtype)

        delete_ok = obj_map['delete']

        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs)

        if not delete_ok:
            deletable = ', '.join([
                x for x, y in utils.constants.GET_OBJ_MAP.items() if y['delete']
            ])
            m = "{} is not a deletable object! Deletable objects: {}".format
            raise utils.exceptions.PytanError(m(objtype, deletable))

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

    def export_obj(self, obj, export_format='csv', **kwargs):
        """Exports a python API object to a given export format

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.base.BaseType` or :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * TaniumPy object to export
        export_format : str, optional
            * default: 'csv'
            * the format to export `obj` to, one of: {'csv', 'xml', 'json'}
        header_sort : list of str, bool, optional
            * default: True
            * for `export_format` csv and `obj` types :class:`utils.taniumpy.object_types.base.BaseType` or :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * True: sort the headers automatically
            * False: do not sort the headers at all
            * list of str: sort the headers returned by priority based on provided list
        header_add_sensor : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * False: do not prefix the headers with the associated sensor name for each column
            * True: prefix the headers with the associated sensor name for each column
        header_add_type : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * False: do not postfix the headers with the result type for each column
            * True: postfix the headers with the result type for each column
        expand_grouped_columns : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * False: do not expand multiline row entries into their own rows
            * True: expand multiline row entries into their own rows
        explode_json_string_values : bool, optional
            * default: False
            * for `export_format` json or csv and `obj` type :class:`utils.taniumpy.object_types.base.BaseType`
            * False: do not explode JSON strings in object attributes into their own object attributes
            * True: explode JSON strings in object attributes into their own object attributes
        minimal : bool, optional
            * default: False
            * for `export_format` xml and `obj` type :class:`utils.taniumpy.object_types.base.BaseType`
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
        :data:`utils.constants.EXPORT_MAPS` : maps the type `obj` to `export_format` and the optional args supported for each
        """

        objtype = type(obj)
        try:
            objclassname = objtype.__name__
        except:
            objclassname = 'Unknown'

        # see if supplied obj is a supported object type
        type_match = [
            x for x in utils.constants.EXPORT_MAPS if isinstance(obj, getattr(utils.taniumpy, x))
        ]

        if not type_match:
            err = (
                "{} not a supported object to export, must be one of: {}"
            ).format

            # build a list of supported object types
            supp_types = ', '.join(utils.constants.EXPORT_MAPS.keys())
            raise utils.exceptions.PytanError(err(objtype, supp_types))

        # get the export formats for this obj type
        export_formats = utils.constants.EXPORT_MAPS.get(type_match[0], '')

        if export_format not in export_formats:
            err = (
                "{!r} not a supported export format for {}, must be one of: {}"
            ).format(export_format, objclassname, ', '.join(export_formats))
            raise utils.exceptions.PytanError(err)

        # perform validation on optional kwargs, if they exist
        opt_keys = export_formats.get(export_format, [])

        for opt_key in opt_keys:
            check_args = dict(opt_key.items() + {'d': kwargs}.items())
            utils.validate.check_dictkey(**check_args)

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
            raise utils.exceptions.PytanError(err(objclassname))

        return result

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
            report_file = 'pytan_report_{}.txt'.format(utils.calc.get_now())

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

    def export_to_report_file(self, obj, export_format='csv', **kwargs):
        """Exports a python API object to a file

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.base.BaseType` or :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * TaniumPy object to export
        export_format : str, optional
            * default: 'csv'
            * the format to export `obj` to, one of: {'csv', 'xml', 'json'}
        header_sort : list of str, bool, optional
            * default: True
            * for `export_format` csv and `obj` types :class:`utils.taniumpy.object_types.base.BaseType` or :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * True: sort the headers automatically
            * False: do not sort the headers at all
            * list of str: sort the headers returned by priority based on provided list
        header_add_sensor : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * False: do not prefix the headers with the associated sensor name for each column
            * True: prefix the headers with the associated sensor name for each column
        header_add_type : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * False: do not postfix the headers with the result type for each column
            * True: postfix the headers with the result type for each column
        expand_grouped_columns : bool, optional
            * default: False
            * for `export_format` csv and `obj` type :class:`utils.taniumpy.object_types.result_set.ResultSet`
            * False: do not expand multiline row entries into their own rows
            * True: expand multiline row entries into their own rows
        explode_json_string_values : bool, optional
            * default: False
            * for `export_format` json or csv and `obj` type :class:`utils.taniumpy.object_types.base.BaseType`
            * False: do not explode JSON strings in object attributes into their own object attributes
            * True: explode JSON strings in object attributes into their own object attributes
        minimal : bool, optional
            * default: False
            * for `export_format` xml and `obj` type :class:`utils.taniumpy.object_types.base.BaseType`
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
                type(obj).__name__, utils.calc.get_now(), export_format,
            )
            m = "No report file name supplied, generated name: {!r}".format
            self.mylog.debug(m(report_file))

        clean_keys = ['obj', 'export_format', 'contents', 'report_file']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        # get the results of exporting the object
        contents = self.export_obj(obj=obj, export_format=export_format, **clean_kwargs)
        report_path = self.create_report_file(
            report_file=report_file, contents=contents, **clean_kwargs
        )
        return report_path, contents

    # get objects
    def get_sensors(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = utils.taniumpy.SensorList
        kwargs['specs_from_args'] = args
        kwargs['hide_sourced_sensors'] = kwargs.get('hide_sourced_sensors', True)
        result = self._get(**kwargs)
        return result

    def get_packages(self, *args, **kwargs):
        """pass. cache_filters need single fix"""
        kwargs['all_class'] = utils.taniumpy.PackageSpecList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_actions(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = utils.taniumpy.ActionList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_clients(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = utils.taniumpy.SystemStatusList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_groups(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = utils.taniumpy.GroupList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_questions(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = utils.taniumpy.QuestionList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_saved_actions(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = utils.taniumpy.SavedActionList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_saved_questions(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = utils.taniumpy.SavedQuestionList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_settings(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = utils.taniumpy.SystemSettingList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_users(self, *args, **kwargs):
        """pass. cache_filters fail"""
        kwargs['all_class'] = utils.taniumpy.UserList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_user_roles(self, *args, **kwargs):
        """pass. cache_filters fail"""
        kwargs['all_class'] = utils.taniumpy.UserRoleList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    def get_whitelisted_urls(self, *args, **kwargs):
        """pass. cache_filters fail"""
        kwargs['all_class'] = utils.taniumpy.WhiteListedUrlList
        kwargs['specs_from_args'] = args
        result = self._get(**kwargs)
        return result

    # BEGIN PRIVATE METHODS
    def _get(self, all_class, **kwargs):
        """pass."""
        hide_sourced_sensors = kwargs.get('hide_sourced_sensors', False)
        limit = kwargs.get('limit', None)

        # don't include hidden objects by default
        kwargs['include_hidden_flag'] = kwargs.get('include_hidden_flag', 0)
        kwargs['all_class'] = all_class
        kwargs['specs'] = kwargs.get('specs', []) or kwargs.get('specs_from_args', [])

        # packagespec doesnt work with GetObject in List form, so we need to use the singular form
        if all_class.__name__ == 'PackageSpecList':
            kwargs['obj'] = all_class()._list_properties.values()[0]()
        else:
            kwargs['obj'] = all_class()

        if kwargs['specs'] or hide_sourced_sensors:
            # get objects using cache filter
            myhelp = utils.helpstr.GETF.format(all_class.__name__)
            kwargs['pytan_help'] = kwargs.get('pytan_help', '') or myhelp
            result = self._find_filter(**kwargs)
        else:
            # get all objects
            myhelp = utils.helpstr.GET.format(all_class.__name__)
            kwargs['pytan_help'] = kwargs.get('pytan_help', '') or myhelp
            result = self.session.find(**kwargs)

        if limit is not None:
            if len(result) != int(limit):
                txt = '\n\t'.join([str(x) for x in result])
                err = "{} {} found, specs {!r} must return {}, returned items:\n\t{}"
                err = err.format(len(result), all_class.__name__, kwargs['specs'], limit, txt)
                raise utils.exceptions.PytanError(err)

            # if just one item returned, return it as a single item
            if len(result) == 1:
                result = result[0]

        m = "{} found, specs {!r}"
        m = m.format(result, kwargs['specs'])
        self.mylog.debug(m)
        return result

    def _get_spec_objects(self, specs):
        """pass."""
        for spec in specs:
            if 'sensor' in spec:
                spec['sensor_object'] = self.get_sensors(limit=1, specs=spec['sensor'])
            if 'group' in spec:
                spec['group_object'] = self.get_groups(limit=1, specs=spec['group'])
            if 'package' in spec:
                spec['package_object'] = self.get_packages(limit=1, specs=spec['package'])
        return specs

    def _find_filter(self, all_class, specs, **kwargs):
        """pass.
        all_class
        specs
        """
        # create a base instance of all_class which all results will be added to
        result = all_class()

        hide_spec = {'value': 0, 'field': 'source_id'}

        hide_sourced_sensors = kwargs.get('hide_sourced_sensors', False)
        if hide_sourced_sensors and not specs:
            specs = hide_spec

        if not isinstance(specs, (list, tuple)):
            specs = [specs]

        for spec in specs:
            # TODO: AWAITING MANUAL PARSER
            # validate & parse a string into a spec
            if not isinstance(spec, (dict,)):
                spec = utils.parsers.get_str(spec)

            # validate & parse the spec
            parsed_spec = utils.parsers.GetObject(all_class, spec).parsed_spec

            # groups have to be searched for using non cache filters!
            if all_class.__name__ in ['GroupList']:
                kwargs['obj'] = utils.taniumpy.Group()
                setattr(kwargs['obj'], parsed_spec['field'], parsed_spec['value'])

            parsed_specs = [parsed_spec]
            if hide_sourced_sensors:
                parsed_specs.append(hide_spec)

            # create a cache filter list object using the parsed_spec
            kwargs['cache_filters'] = utils.tanium_obj.create_cf_listobj(parsed_specs)

            # use getobject to find the results using the cache_filters to limit the returns
            cf_result = self.session.find(**kwargs)

            # groups only return a single item!
            if all_class.__name__ in ['GroupList']:
                result.append(cf_result)
            else:
                # add each result to the base instance
                [result.append(r) for r in cf_result]
        return result

    def _add(self, obj, **kwargs):
        """Wrapper for interfacing with :func:`utils.taniumpy.session.Session.add`

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.base.BaseType`
            * object to add

        Returns
        -------
        added_obj : :class:`utils.taniumpy.object_types.base.BaseType`
           * full object that was added
        """
        try:
            search_str = '; '.join([str(x) for x in obj])
        except:
            search_str = obj

        self.mylog.debug("Adding object {}".format(search_str))

        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)
        kwargs['pytan_help'] = utils.helpstr.ADD.format(obj.__class__.__name__)
        kwargs['obj'] = obj

        try:
            added_obj = self.session.add(**kwargs)
        except Exception as e:
            err = "Error while trying to add object '{}': {}!!".format
            raise utils.exceptions.PytanError(err(search_str, e))

        kwargs['pytan_help'] = utils.helpstr.ADDGET.format(obj.__class__.__name__)
        kwargs['obj'] = added_obj

        try:
            found_obj = self.session.find(**kwargs)
        except Exception as e:
            self.utils.exceptions.mylog.error(e)
            err = "Error while trying to find recently added object {}!!"
            err = err.format(search_str)
            raise utils.exceptions.PytanError(err)

        self.mylog.debug("Added object {}".format(found_obj))
        return found_obj

    def _export_class_BaseType(self, obj, export_format, **kwargs): # noqa
        """Handles exporting :class:`utils.taniumpy.object_types.base.BaseType`

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.base.BaseType`
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
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        if format_handler:
            result = format_handler(obj=obj, **clean_kwargs)
        else:
            err = "{!r} not coded for in Handler!".format
            raise utils.exceptions.PytanError(err(export_format))

        return result

    def _export_class_ResultSet(self, obj, export_format, **kwargs): # noqa
        """Handles exporting :class:`utils.taniumpy.object_types.result_set.ResultSet`

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.result_set.ResultSet`
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
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

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
            raise utils.exceptions.PytanError(err(export_format))

        return result

    def _export_format_csv(self, obj, **kwargs):
        """Handles exporting format: CSV

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.result_set.ResultSet` or :class:`utils.taniumpy.object_types.base.BaseType`
            * taniumpy object to export

        Returns
        -------
        result : str
           * results of exporting `obj` into csv format
        """

        if not hasattr(obj, 'write_csv'):
            err = "{!r} has no write_csv() method!".format
            raise utils.exceptions.PytanError(err(obj))

        out = io.BytesIO()

        clean_keys = ['fd', 'val']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

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
        obj : :class:`utils.taniumpy.object_types.result_set.ResultSet` or :class:`utils.taniumpy.object_types.base.BaseType`
            * taniumpy object to export

        Returns
        -------
        result : str
           * results of exporting `obj` into json format
        """

        if not hasattr(obj, 'to_json'):
            err = "{!r} has no to_json() method!".format
            raise utils.exceptions.PytanError(err(obj))

        clean_keys = ['jsonable']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        result = obj.to_json(jsonable=obj, **clean_kwargs)
        return result

    def _export_format_xml(self, obj, **kwargs):
        """Handles exporting format: XML

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.result_set.ResultSet` or :class:`utils.taniumpy.object_types.base.BaseType`
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
            raise utils.exceptions.PytanError(err(obj))

        clean_keys = ['x']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        result = utils.pretty.xml_pretty(x=raw_xml, **clean_kwargs)
        return result

    def _deploy_action(self, run=False, get_results=True, **kwargs):
        """Deploy an action and get the results back

        This method requires in-depth knowledge of how filters and options are created in the API, and as such is not meant for human consumption. Use :func:`deploy_action` instead.

        Parameters
        ----------
        package_def : dict
            * definition that describes a package
        filter_defs : str, dict, list of str or dict, optional
            * default: []
            * action filter definitions
        option_defs : dict, list of dict, optional
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
            * False: just ask the question that pertains to verify action, export the results to CSV, and raise RunFalse -- does not deploy the action
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
            * This is passed through to :class:`pytan.pollers.ActionPoller`
        complete_pct : int/float, optional
            * default: 100
            * Percentage of passed_count out of successfully run actions to consider the action "done"
            * This is passed through to :class:`pytan.pollers.ActionPoller`
        override_timeout_secs : int, optional
            * default: 0
            * If supplied and not 0, timeout in seconds instead of when object expires
            * This is passed through to :class:`pytan.pollers.ActionPoller`
        override_passed_count : int, optional
            * instead of getting number of systems that should run this action by asking a question, use this number
            * This is passed through to :class:`pytan.pollers.ActionPoller`

        Returns
        -------
        ret : dict, containing:
            * `saved_action_object` : :class:`utils.taniumpy.object_types.saved_action.SavedAction`, the saved_action added for this action (None if 6.2)
            * `action_object` : :class:`utils.taniumpy.object_types.action.Action`, the action object that tanium created for `saved_action`
            * `package_object` : :class:`utils.taniumpy.object_types.package_spec.PackageSPec`, the package object used in `saved_action`
            * `action_info` : :class:`utils.taniumpy.object_types.result_info.ResultInfo`, the initial GetResultInfo call done before getting results
            * `poller_object` : :class:`pytan.pollers.ActionPoller`, poller object used to wait until all results are in before getting `action_results`
            * `poller_success` : None if `get_results` == False, elsewise True or False
            * `action_results` : None if `get_results` == False, elsewise :class:`utils.taniumpy.object_types.result_set.ResultSet`, the results for `action_object`
            * `action_result_map` : None if `get_results` == False, elsewise progress map for `action_object` in dictionary form

        Examples
        --------
        >>> # example of dict for `package_def`
        >>> package_def = {'name': 'PackageName1', 'params':{'param1': 'value1'}}

        >>> # example of str for `filter_defs`
        >>> filter_defs = 'Sensor1'

        >>> # example of dict for `filter_defs`
        >>> filter_defs = {
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
        :data:`utils.constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`utils.constants.OPTION_MAPS` : valid option dictionaries for options

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

        utils.helpers.check_for_help(kwargs=kwargs)

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

        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        if not self.session.platform_is_6_5(**kwargs):
            objtype = utils.taniumpy.Action
            objlisttype = None
            force_start_time = True
        else:
            objtype = utils.taniumpy.SavedAction
            objlisttype = utils.taniumpy.SavedActionList
            force_start_time = False

        package_def = utils.validate.defs_gen(
            defname='package_def',
            deftypes=['dict()'],
            empty_ok=False,
            **clean_kwargs
        )
        filter_defs = utils.validate.defs_gen(
            defname='filter_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=True,
            **clean_kwargs
        )
        option_defs = utils.validate.defs_gen(
            defname='option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **clean_kwargs
        )

        utils.validate.def_package(package_def=package_def)
        utils.validate.def_sensors(sensor_defs=filter_defs)

        package_def = self._get_package_def(d=package_def, **clean_kwargs)
        h = (
            "Issue a GetObject to get the full object of a sensor for inclusion in a "
            "Group for an Action"
        )
        filter_defs = self._get_sensor_defs(
            defs=filter_defs,
            pytan_help=h,
            **clean_kwargs
        )

        start_seconds_from_now = utils.validate.get_kwargs_int(
            key='start_seconds_from_now',
            default=0,
            **clean_kwargs
        )

        expire_seconds = utils.validate.get_kwargs_int(key='expire_seconds', **clean_kwargs)

        action_name_default = "API Deploy {0.name}".format(package_def['package_obj'])
        action_name = kwargs.get('action_name', action_name_default)

        action_comment_default = 'Created by PyTan v{}'.format(__version__)
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
            pa_sensors = ['Computer Name', 'Online, that =:True']
            pa_sensor_defs = utils.parsers.parse_sensors(sensors=pa_sensors)

            q_clean_keys = [
                'sensor_defs',
                'filter_defs',
                'option_defs',
                'hide_no_results_flag',
                'pytan_help',
                'get_results',
            ]
            q_clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=q_clean_keys)

            h = (
                "Ask a question to determine the number of systems this action would affect if it "
                "was actually run"
            )
            q_clean_kwargs['sensor_defs'] = pa_sensor_defs
            q_clean_kwargs['filter_defs'] = filter_defs
            q_clean_kwargs['option_defs'] = option_defs
            q_clean_kwargs['hide_no_results_flag'] = 1

            pre_action_question = self._ask_manual(pytan_help=h, **q_clean_kwargs)

            passed_count = pre_action_question['question_results'].passed
            m = "Number of systems that match action filter (passed_count): {}".format
            self.mylog.debug(m(passed_count))

            if passed_count == 0:
                m = "Number of systems that match the action filters provided is zero!"
                raise utils.exceptions.PytanError(m)

            default_format = 'csv'
            export_format = kwargs.get('export_format', default_format)

            default_prefix = 'VERIFY_BEFORE_DEPLOY_ACTION_'
            export_prefix = kwargs.get('prefix', default_prefix)

            e_clean_keys = [
                'obj',
                'export_format',
                'prefix',
            ]
            e_clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=e_clean_keys)
            e_clean_kwargs['obj'] = pre_action_question['question_results']
            e_clean_kwargs['export_format'] = export_format
            e_clean_kwargs['prefix'] = export_prefix
            report_path, result = self.export_to_report_file(**e_clean_kwargs)

            m = (
                "'Run' is not True!!\n"
                "View and verify the contents of {} (length: {} bytes)\n"
                "Re-run this deploy action with run=True after verifying"
            ).format
            raise utils.exceptions.RunError(m(report_path, len(result)))

        # BUILD THE PACKAGE OBJECT TO BE ADDED TO THE ACTION
        add_package_obj = utils.tanium_obj.copy_package_obj_for_action(obj=package_def['package_obj'])

        # if source_id is specified, a new package will be created with the parameters
        # for this action embedded into it - specifying hidden = 1 will ensure the new package
        # is hidden
        add_package_obj.hidden_flag = 1

        param_objlist = utils.tanium_obj.build_param_objlist(
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

        if filter_defs or option_defs:
            targetgroup_obj = utils.tanium_obj.build_group_obj(
                filter_defs=filter_defs, option_defs=option_defs,
            )
            add_obj.target_group = targetgroup_obj
        else:
            targetgroup_obj = None

        if start_seconds_from_now:
            add_obj.start_time = utils.calc.seconds_from_now(secs=start_seconds_from_now)

        if force_start_time and not add_obj.start_time:
            if not start_seconds_from_now:
                start_seconds_from_now = 1
            add_obj.start_time = utils.calc.seconds_from_now(secs=start_seconds_from_now)

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

        if sse_format_int not in utils.constants.SSE_RESTRICT_MAP:
            return

        restrict_maps = utils.constants.SSE_RESTRICT_MAP[sse_format_int]

        if not self._version_support_check(v_maps=restrict_maps, **kwargs):
            restrict_maps_txt = '\n'.join([str(x) for x in restrict_maps])

            m = (
                "Server version {} does not support export format {!r}, "
                "server version must be equal to or greater than one of:\n{}"
            ).format

            m = m(self.session.server_version, sse_format, restrict_maps_txt)

            raise utils.exceptions.UnsupportedVersionError(m)

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

        sse_format_int = [x[-1] for x in utils.constants.SSE_FORMAT_MAP if sse_format.lower() in x]

        if not sse_format_int:
            m = "Unsupport export format {!r}, must be one of:\n{}".format
            ef_map_txt = '\n'.join(
                [', '.join(['{!r}'.format(x) for x in y]) for y in utils.constants.SSE_FORMAT_MAP]
            )
            raise utils.exceptions.PytanError(m(sse_format, ef_map_txt))

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
            raise utils.exceptions.UnsupportedVersionError(m)

    def _check_sse_crash_prevention(self, obj, **kwargs):
        """Runs a number of methods used to prevent crashing the platform server when performing server side exports

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.base.BaseType`
            * object to pass to self._check_sse_empty_rs
        """

        clean_keys = ['obj', 'v_maps', 'ok_version']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        restrict_maps = utils.constants.SSE_CRASH_MAP

        ok_version = self._version_support_check(v_maps=restrict_maps, **clean_kwargs)

        self._check_sse_timing(ok_version=ok_version, **clean_kwargs)
        self._check_sse_empty_rs(obj=obj, ok_version=ok_version, **clean_kwargs)

    def _check_sse_timing(self, ok_version, **kwargs):
        """Checks that the last server side export was at least 1 second ago if server version is less than any versions in utils.constants.SSE_CRASH_MAP

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
                raise utils.exceptions.ServerSideExportError(m())

        self.last_get_rd_sse = datetime.datetime.utcnow()

    def _check_sse_empty_rs(self, obj, ok_version, **kwargs):
        """Checks if the server version is less than any versions in utils.constants.SSE_CRASH_MAP, if so verifies that the result set is not empty

        Parameters
        ----------
        obj : :class:`utils.taniumpy.object_types.base.BaseType`
            * object to get result info for to ensure non-empty answers
        ok_version : bool
            * if the version currently running is an "ok" version
        """

        clean_keys = ['obj']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        if not ok_version:
            ri = self.get_result_info(obj=obj, **clean_kwargs)
            if ri.row_count == 0:
                m = (
                    "No rows available to perform a server side export with, result info: {}"
                ).format
                raise utils.exceptions.ServerSideExportError(m(ri))

    def _parse_args(self, kwargs):
        self.args_db = {}
        self.args_db['original_args'] = kwargs
        self.args_db['handler_args'] = self._get_src_args(kwargs)
        self.args_db['default_args'] = self._get_src_args(utils.constants.DEFAULTS)
        self.args_db['env_args'] = {
            k.lower().replace('pytan_', ''): v
            for k, v in os.environ.iteritems()
            if k.lower().startswith('pytan_')
        }
        self.args_db['env_args'] = self._get_src_args(self.args_db['env_args'])
        self.args_db['puc_dict'] = self.read_config_file()
        self.args_db['config_args'] = self._get_src_args(self.args_db['puc_dict'])
        self.args_db['parsed_args_source'] = {}
        self.args_db['parsed_args'] = {}

        args_order = ['config_args', 'env_args', 'handler_args', 'default_args']
        for k in utils.constants.HANDLER_ARGS:
            src = None
            def_val = self.args_db['default_args'].get(k, None)
            for args in args_order:
                if src is not None:
                    break
                args_dict = self.args_db[args]
                if k in args_dict and args_dict[k] != def_val:
                    val = args_dict[k]
                    src = args

            if src is None and def_val is not None:
                src = 'default_args'
                val = def_val
            if src is None and def_val is None:
                continue

            self.args_db['parsed_args'][k] = val
            self.args_db['parsed_args_source'][k] = src

            if k == 'password':
                pval = '{}'.format('*' * len(val))
            else:
                pval = val

            m = "_parse_args(): arg = {!r}, val = {!r}, type = {!r}, src = {!r}"
            m = m.format(k, pval, type(val).__name__, src)
            self.mylog.debug(m)

        if self.args_db['parsed_args']['password']:
            self.args_db['parsed_args']['password'] = utils.coder.vig_decode(
                key=utils.constants.PYTAN_KEY,
                string=self.args_db['parsed_args']['password'],
            )

    def _validate_args(self):
        pa = self.args_db['parsed_args']
        pas = self.args_db['parsed_args_source']
        for arg, argtype in utils.constants.HANDLER_ARGS.iteritems():
            if arg not in pa:
                continue

            pa_type = type(pa[arg]).__name__
            err = "Argument {!r} must be type {!r}, supplied type {!r} via {!r}".format
            err = err(arg, argtype.__name__, pa_type, pas[arg])

            # handle string types that actually should be other types
            if isinstance(pa[arg], basestring):
                if argtype == bool:
                    if pa[arg].capitalize() in ["True", "False"]:
                        pa[arg] = eval(pa[arg])
                    else:
                        raise utils.exceptions.PytanError(err)

                if argtype == dict:
                    try:
                        pa[arg] = dict(eval(pa[arg]))
                    except Exception as e:
                        err = "{} exception: {}".format(err, e)
                        raise utils.exceptions.PytanError(err)

            try:
                pa[arg] = argtype(pa[arg])
            except Exception as e:
                err = "{} exception: {}".format(err, e)
                raise utils.exceptions.PytanError(err)

        if not pa['host']:
            raise utils.exceptions.PytanError("Must supply host!")

        if not pa['port']:
            raise utils.exceptions.PytanError("Must supply port!")

        if not pa['session_id']:
            if not pa['username']:
                raise utils.exceptions.PytanError("Must supply username if no session_id!")

            if not pa['password']:
                raise utils.exceptions.PytanError("Must supply password if no session_id!")

    def _log_args(self):
        m = "Argument {!r} supplied by {!r} type {!r}".format
        for k, v in self.args_db['parsed_args'].iteritems():
            self.mylog.debug(m(k, self.args_db['parsed_args_source'][k], type(v).__name__))

    def _get_src_args(self, kwargs):
        src_args = {k: kwargs[k] for k in utils.constants.HANDLER_ARGS if k in kwargs}
        return src_args
