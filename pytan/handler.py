"""The main :mod:`pytan` module that provides first level entities for programmatic use."""

import logging
import datetime

from pytan import PytanError, tanium_ng
from pytan.tanium_ng import BaseType
from pytan.store import HelpStore, ResultStore
from pytan.utils import coerce_list
from pytan.session import Session
from pytan.pollers import QuestionPoller, SSEPoller
from pytan.parsers import GetObject
from pytan.version import __version__
from pytan.tickle import from_sse_xml
from pytan.tickle.to__dict_resultset import ToDictResultSet
from pytan.handler_args import create_argstore
from pytan.handler_logs import setup_log
from pytan.tickle.tools import shrink_obj, check_limits, create_cachefilterlist
from pytan.tickle.create__question import create_question

MYLOG = logging.getLogger(__name__)

HELPS = HelpStore()
HELPS.sq_getq = "Use GetObject to get the last question asked by a saved question"
HELPS.sq_ri = (
    "Use GetResultInfo on a saved question in order to issue a new question, "
    "which refreshes the data for that saved question"
)
HELPS.sq_resq = (
    "Use GetObject to re-fetch the saved question in order get the ID of the newly asked question"
)
HELPS.pj = "Use AddObject to add a ParseJob for question_text and get back ParseResultGroups"
HELPS.pj_add = "Use AddObject to add the Question object from the chosen ParseResultGroup"
HELPS.grd = "Use GetResultData to get answers for {} object"
HELPS.grd_sse = "Issue a GetResultData on {} to start a Server Side Export and get an export_id"
HELPS.gri = "Issue a GetResultInfo for a {} to check the current progress of answers"
HELPS.saa = "Issue an AddObject to add a SavedActionApproval"
HELPS.stopa = "Issue an AddObject to add a StopAction"
HELPS.stopar = "Re-issue a GetObject to ensure the actions stopped_flag is 1"
HELPS.getf = "Use GetObject to find {} objects with cache filters to limit the results"
HELPS.geta = "Use GetObject to find all {} objects"
HELPS.addobj = "Issue an AddObject to add a {} object"
HELPS.addget = "Issue a GetObject on the recently added {} object in order to get the full object"
HELPS.delobj = "Issue a DeleteObject to delete an object"


SSE_FORMAT_MAP = [
    ('csv', '0', 0),
    ('xml', '1', 1),
    ('xml_obj', '1', 1),
    ('cef', '2', 2),
]
"""
Mapping of human friendly strings to API integers for server side export
"""

SSE_RESTRICT_MAP = {
    1: ['6.5.314.4300'],
    2: ['6.5.314.4300'],
}
"""
Mapping of API integers for server side export format to version support
"""

SSE_CRASH_MAP = ['6.5.314.4300']
"""
Mapping of versions to watch out for crashes/handle bugs for server side export
"""


class ServerSideExportError(PytanError):
    pass


class UnsupportedVersionError(PytanError):
    pass


class PickerError(PytanError):
    pass


class ParseJobError(PytanError):
    pass


class Handler(object):
    """Creates a connection to a Tanium SOAP Server on host:port.

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
        * default: PYTAN_USER_CONFIG
        * JSON file containing key/value pairs to override class variables

    Notes
    -----
      * for 6.2: port 444 is the default SOAP port, port 443 forwards /soap/ URLs to the SOAP port,
        Use port 444 if you have direct access to it. However, port 444 is the only port that
        exposes the /info page in 6.2
      * for 6.5: port 443 is the default SOAP port, there is no port 444

    See Also
    --------
    :data:`LOG_LEVEL_MAPS` : maps a given `loglevel` to respective logger names
    and their logger levels
    :class:`session.Session` : Session object used by Handler

    Examples
    --------
    Setup a Handler() object::

        >>> import sys
        >>> sys.path.append('/path/to/pytan/')
        >>> import pytan
        >>> handler = pytan.Handler(username='username', password='password', host='host')
    """

    MYLOG = logging.getLogger(__name__)
    SESSION = None
    HANDLER_ARGS = None

    def __init__(self, **kwargs):
        super(Handler, self).__init__()
        self.MYLOG = logging.getLogger(__name__)

        parsed_handler_args = kwargs.get('parsed_handler_args', None)
        if parsed_handler_args:
            self.HANDLER_ARGS = parsed_handler_args
            m = "Using handler arguments from 'parsed_handler_args'"
        else:
            argstore = create_argstore(**kwargs)
            self.HANDLER_ARGS = argstore.handler_args
            m = "Using handler arguments from 'create_argstore()'"

        setup_log(**self.HANDLER_ARGS)
        self.MYLOG.debug(m)

        # establish our Session to the Tanium server
        self.SESSION = Session(**self.HANDLER_ARGS)

        # monkey patch handler into BaseType and ToDictResultSet
        BaseType._HANDLER = self
        ToDictResultSet._HANDLER = self

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        str_tpl = "PyTan v{} Handler for {}".format
        ret = str_tpl(__version__, self.SESSION)
        return ret

    def get_server_version(self, **kwargs):
        """Uses :func:`session.Session.get_server_version` to get the version of the Tanium Server

        Returns
        -------
        result: str
            * Version of Tanium Server in string format
        """
        result = self.SESSION.get_server_version(**kwargs)
        return result

    def ask_manual(self, **kwargs):
        """pass."""
        # helpers.check_for_help(kwargs)
        # parser = parsers.LeftSide(left)
        # print parser.parsed_specs

        get_results = kwargs.get('get_results', True)
        kwargs = self._get_spec_objects('left', **kwargs)
        kwargs = self._get_spec_objects('right', **kwargs)

        kwargs['obj'] = create_question(**kwargs)
        kwargs['obj'] = self._add(**kwargs)

        m = "Question Added, ID: {0.id}, query text: {0.query_text!r}, expires: {0.expiration}"
        m = m.format(kwargs['obj'])
        self.MYLOG.info(m)

        result = ResultStore()
        result.question_object = kwargs['obj']
        result.poller_object = QuestionPoller(handler=self, **kwargs)
        result.question_results = None
        result.poller_success = None

        if get_results:
            # poll the Question ID returned above to wait for results
            result.poller_success = result.poller_object.run(**kwargs)
            # get the answers for this question
            result.question_results = self.get_result_data(**kwargs)
        return result

    def ask_saved(self, *args, **kwargs):
        """Ask a saved question and get the results back

        Parameters
        ----------
        id : int, list of int, optional
            * id of saved question to ask
        name : str, list of str
            * name of saved question
        refresh: bool, optional
            * default False
            * False: Get the answers that are currently available for this saved question
            * True: Ask a new question to gather new answers for this saved question
        get_results : bool, optional
            * default: True
            * True: wait for result completion after asking question
            * False: just ask the question and return it in `ret`

        Returns
        -------
        result : dict, containing
            * `question_object` :
            :class:`tanium_ng.saved_question.SavedQuestion`
            the saved question object
            * `question_object` :
            :class:`tanium_ng.question.Question`
            the question asked by `saved_question_object`
            * ``question_results`` :
            :class:`tanium_ng.result_set.ResultSet`
            the results for `question_object`
            * ``poller_object`` :
            None if `refresh` == False
            elsewise :class:`QuestionPoller`,
            poller object used to wait until all results are in before getting `question_results`
            * ``poller_success`` : None if ``refresh`` == False, elsewise True or False
        """
        kwargs['specs'] = kwargs.get('specs', []) or list(args)
        refresh = kwargs.get('refresh', False)
        get_results = kwargs.get('get_results', True)

        if not kwargs['specs']:
            err = "Must supply arg 'specs' for identifying the saved question to ask"
            raise PytanError(err)

        # creatStore() object for storing the results
        result = ResultStore()
        result.poller_object = None
        result.poller_success = None
        result.question_results = None

        # get the saved_question object the user passed in
        result.saved_question_object = self.get_saved_questions(limit_exact=1, **kwargs)

        # get the last asked question for this saved question
        kwargs['pytan_help'] = HELPS.sq_getq
        kwargs['obj'] = result['saved_question_object'].question
        result.question_object = self.SESSION.find(**kwargs)

        if refresh:
            # if GetResultInfo is issued on a saved question, Tanium will issue a new question
            # to fetch new/updated results
            kwargs['pytan_help'] = HELPS.sq_ri
            kwargs['obj'] = result.saved_question_object
            self.get_result_info(**kwargs)

            # re-fetch the saved question object to get the newly asked question info
            kwargs['pytan_help'] = HELPS.sq_resq
            kwargs['obj'] = shrink_obj(obj=result.saved_question_object)
            result.saved_question_object = self.SESSION.find(**kwargs)

            # get the last asked question for this saved question
            kwargs['pytan_help'] = HELPS.sq_getq
            kwargs['obj'] = result.saved_question_object.question
            result.question_object = self.SESSION.find(**kwargs)

            m = "Question Added, ID: {0.id}, query text: {0.query_text!r}, expires: {0.expiration}"
            m = m.format(kwargs['obj'])
            self.MYLOG.info(m)

            # setup a poller for the last question for this saved question
            poll_args = {}
            poll_args.update(kwargs)
            poll_args['obj'] = result.question_object
            poll_args['handler'] = self
            result.poller_object = QuestionPoller(**poll_args)

        if get_results:
            # run the poller if one exists to wait for answers to complete
            if result.poller_object is not None:
                result.poller_success = result.poller_object.run(**kwargs)

            # get the answers for the last asked question for this saved question
            kwargs['obj'] = result.question_object
            result.question_results = self.get_result_data(**kwargs)
        return result

    def parse_query(self, question_text, **kwargs):
        """Ask a parsed question as `question_text` and get a list of parsed results back

        Parameters
        ----------
        question_text : str
            * The question text you want the server to parse into a list of parsed results

        Returns
        -------
        result : :class:`tanium_ng.parse_result_group.ParseResultGroup`
        """
        if not self.SESSION.platform_is_6_5(**kwargs):
            m = "ParseJob not supported in version: {}"
            m = m.format(self.get_server_version(**kwargs))
            raise UnsupportedVersionError(m)

        obj = tanium_ng.ParseJob()
        obj.question_text = question_text
        obj.parser_version = 2

        m = "ParseJob Built: {}"
        m = m.format(obj.to_json())
        self.MYLOG.debug(m)

        pq_args = {}
        pq_args.update(kwargs)
        pq_args['obj'] = obj

        result = self.SESSION.add(**pq_args)
        return result

    def ask_parsed(self, question_text, **kwargs):
        """Ask a parsed question as `question_text` and use the index of the parsed results from `picker`

        Parameters
        ----------
        question_text : str
            * The question text you want the server to parse into a list of parsed results
        picker : int, optional
            * default: 0
            * The index number of the parsed results that correlates to the actual question you
            wish to run
        get_results : bool, optional
            * default: True
            * True: wait for result completion after asking question
            * False: just ask the question and return it in `ret`

        Returns
        -------
        result : dict, containing:
            * `question_object` :
            :class:`tanium_ng.question.Question`
            the actual question added by PyTan
            * `question_results` :
            :class:`tanium_ng.result_set.ResultSet`
            the Result Set for `question_object` if `get_results` == True
            * `poller_object` :
            :class:`QuestionPoller`
            poller object used to wait until all results are in before getting `question_results`
            * `poller_success` : None if `get_results` == True, elsewise True or False
            * `parse_results` :
            :class:`tanium_ng.parse_result_group_list.ParseResultGroupList`
            the parse result group returned from Tanium after parsing `question_text`

        Examples
        --------

        Ask the server to parse 'computer name', but don't pick a choice
        (will print out a list of choices at critical logging level and then throw an exception):
            >>> v = handler.ask_parsed('computer name')

        Ask the server to parse 'computer name' and pick index 1 as the question you want to run:
            >>> v = handler.ask_parsed('computer name', picker=1)
        """
        picker = kwargs.get('picker', 0)
        get_results = kwargs.get('get_results', True)

        if not self.SESSION.platform_is_6_5(**kwargs):
            m = "ParseJob not supported in version: {}"
            m = m.format(self.SESSION.server_version)
            raise UnsupportedVersionError(m)

        pq_args = {}
        pq_args.update(kwargs)
        pq_args['question_text'] = question_text
        pq_args['pytan_help'] = HELPS.pj
        parse_job_results = self.parse_query(**pq_args)

        if not parse_job_results:
            m = "Question Text '{}' was unable to be parsed into a valid query text by the server"
            raise ParseJobError(m)

        pi = "Index {0}, Score: {1.score}, Query: {1.question_text!r}"
        pw = (
            "You must supply an index as picker=$index to choose one of the parse "
            "responses -- re-run ask_parsed with picker set to one of these indexes!!"
        )

        if picker is 0:
            self.MYLOG.critical(pw)
            for idx, x in enumerate(parse_job_results):
                self.MYLOG.critical(pi.format(idx + 1, x))
            raise PickerError(pw)

        try:
            picked_parse_job = parse_job_results[picker - 1]
        except:
            m = "You supplied an invalid picker index {} - {}"
            m = m.format(picker, pw)
            self.MYLOG.critical(m)

            for idx, x in enumerate(parse_job_results):
                self.MYLOG.critical(pi.format(idx + 1, x))
            raise PickerError(pw)

        # add our Question and get a Question ID back
        kwargs['obj'] = picked_parse_job.question

        m = "Question Picked: {}"
        m = m.format(kwargs['obj'].to_json())
        self.MYLOG.debug(m)

        kwargs['pytan_help'] = HELPS.pj_add
        kwargs['obj'] = self._add(**kwargs)

        m = "Question Added, ID: {0.id}, query text: {0.query_text!r}, expires: {0.expiration}"
        m = m.format(kwargs['obj'])
        self.MYLOG.info(m)

        result = ResultStore()
        result.parse_results = parse_job_results
        result.question_object = kwargs['obj']
        result.question_results = None
        result.poller_success = None

        poll_args = {}
        poll_args.update(kwargs)
        poll_args['handler'] = self
        result.poller_object = QuestionPoller(**poll_args)

        if get_results:
            # poll the Question ID returned above to wait for results
            result.poller_success = result.poller_object.run(**kwargs)
            result.question_results = self.get_result_data(**kwargs)
        return result

    def approve_saved_action(self, *args, **kwargs):
        """Approve a saved action

        Parameters
        ----------
        id : int
            * id of saved action to approve

        Returns
        -------
        result : :class:`tanium_ng.saved_action_approval.SavedActionApproval`
            * The object containing the return from SavedActionApproval
        """
        kwargs['specs'] = kwargs.get('specs', []) or list(args)

        if not kwargs['specs']:
            err = "Must supply arg 'specs' for identifying the saved action to approve"
            raise PytanError(err)

        # get the saved_question object the user passed in
        sa_obj = self.get_saved_actions(limit_exact=1, **kwargs)

        result = tanium_ng.SavedActionApproval()
        result.id = sa_obj.id
        result.approved_flag = 1

        # we dont want to re-fetch the object, so use sessions add instead of handlers add
        kwargs['pytan_help'] = HELPS.saa
        kwargs['obj'] = result
        result = self.SESSION.add(**kwargs)

        m = 'Action approved successfully: {}'
        m = m.format(result)
        self.MYLOG.debug(m)
        return result

    def stop_action(self, *args, **kwargs):
        """Stop an action

        Parameters
        ----------
        id : int
            * id of action to stop

        Returns
        -------
        action_stop_obj : :class:`tanium_ng.action_stop.ActionStop`
            The object containing the ID of the action stop job
        """
        kwargs['specs'] = kwargs.get('specs', []) or list(args)

        if not kwargs['specs']:
            err = "Must supply arg 'specs' for identifying the saved action to approve"
            raise PytanError(err)

        # get the action object the user passed in
        a_obj_before = self.get_actions(limit_exact=1, **kwargs)

        result = tanium_ng.ActionStop()
        result.action = a_obj_before

        kwargs['pytan_help'] = HELPS.stopa
        kwargs['obj'] = result
        result = self.SESSION.add(**kwargs)

        kwargs['pytan_help'] = HELPS.stopar
        kwargs['obj'] = a_obj_before
        a_obj_after = self.SESSION.find(**kwargs)

        if a_obj_after.stopped_flag:
            m = 'Action stopped successfully, ID of action stop: {0.id}'
            m = m.format(result)
            self.MYLOG.debug(m)
        else:
            m = "Action not stopped successfully, json of action after issuing StopAction: {}"
            m = m.format(self.export_obj(a_obj_after, 'json'))
            raise PytanError(m)
        return result

    # TODO: add question/saved_question/action grd/gri

    # Result Data / Result Info
    def get_result_data(self, obj, **kwargs):
        """Get the result data for a python API object

        This method issues a GetResultData command to the SOAP api for `obj`. GetResultData
        returns the columns and rows that are currently available for `obj`.

        Parameters
        ----------
        obj : :class:`tanium_ng.base.BaseType`
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
        rd : :class:`tanium_ng.result_set.ResultSet`
            The return of GetResultData for `obj`
        """

        """ note #1 from jwk:
        For Action GetResultData: You have to make a ResultInfo request at least once every 2
        minutes. The server gathers the result data by asking a saved question. It won't re-issue
        the saved question unless you make a GetResultInfo request. When you make a GetResultInfo
        request, if there is no question that is less than 2 minutes old, the server will
        automatically reissue a new question instance to make sure fresh data is available.

        note #2 from jwk:
        To get the aggregate data (without computer names), set row_counts_only_flag = 1. To get
        the computer names, use row_counts_only_flag = 0 (default).
        """
        shrink = kwargs.get('shrink', True)
        aggregate = kwargs.get('aggregate', False)
        sse = kwargs.get('sse', False)
        export_flag = kwargs.get('export_flag', 0)

        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)

        if shrink:
            kwargs['obj'] = shrink_obj(obj=obj)
        else:
            kwargs['obj'] = obj

        if aggregate:
            kwargs['row_counts_only_flag'] = 1

        if sse or export_flag:
            result = self.get_result_data_sse(**kwargs)
        else:
            # do a normal getresultdata
            kwargs['pytan_help'] = HELPS.grd.format(obj.__class__.__name__)
            result = self.SESSION.get_result_data(**kwargs)

        return result

    def get_result_data_sse(self, obj, **kwargs):
        """Get the result data for a python API object using a server side export (sse)

        This method issues a GetResultData command to the SOAP api for `obj` with the option
        `export_flag` set to 1. This will cause the server to process all of the data for a given
        result set and save it as `export_format`. Then the user can use an authenticated GET
        request to get the status of the file via "/export/${export_id}.status". Once the status
        returns "Completed.", the actual report file can be retrieved by an authenticated GET
        request to "/export/${export_id}.gz". This workflow saves a lot of processing time and
        removes the need to paginate large result sets necessary in normal GetResultData calls.

        *Version support*
            * 6.5.314.4231: initial sse support (csv only)
            * 6.5.314.4300: export_format support (adds xml and cef)
            * 6.5.314.4300: fix core dump if multiple sse done on empty resultset
            * 6.5.314.4300: fix no status file if sse done on empty resultset
            * 6.5.314.4300: fix response if more than two sse done in same second

        Parameters
        ----------
        obj : :class:`tanium_ng.base.BaseType`
            * object to get result data for
        sse_format : str, optional
            * default: 'csv'
            * format to have server create report in, one of:
            {'csv', 'xml', 'xml_obj', 'cef', 0, 1, 2}
        leading : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to prepend to each row
        trailing : str, optional
            * default: ''
            * used for sse_format 'cef' only, the string to append to each row

        See Also
        --------
        :data:`SSE_FORMAT_MAP` :
        maps `sse_format` to an integer for use by the SOAP API
        :data:`SSE_RESTRICT_MAP` :
        maps sse_format integers to supported platform versions
        :data:`SSE_CRASH_MAP` :
        maps platform versions that can cause issues in various scenarios

        Returns
        -------
        export_data : either `str` or :class:`tanium_ng.result_set.ResultSet`
            * If sse_format is one of csv, xml, or cef, export_data will be a `str` containing the
            contents of the ResultSet in said format
            * If sse_format is xml_obj, export_data will be a :class:`tanium_ng.
            result_set.ResultSet`
        """
        sse_format = kwargs.get('sse_format', 'xml_obj')
        sse_leading = kwargs.get('sse_leading', '')
        sse_trailing = kwargs.get('trailing', '')
        shrink = kwargs.get('shrink', True)

        self._check_sse_version()
        self._check_sse_crash_prevention(obj=obj)

        if shrink:
            kwargs['obj'] = shrink_obj(obj=obj)
        else:
            kwargs['obj'] = obj

        grd_args = {}
        grd_args.update(kwargs)
        grd_args['pytan_help'] = HELPS.grd_sse.format(obj.__class__.__name__)
        # add the export_flag = 1 to the kwargs for inclusion in options node
        grd_args['export_flag'] = 1
        # add the export_format to the kwargs for inclusion in options node
        grd_args['export_format'] = self._resolve_sse_format(sse_format)
        # add the export_leading_text to the kwargs for inclusion in options node
        if sse_leading:
            grd_args['export_leading_text'] = sse_leading
        # add the export_trailing_text to the kwargs for inclusion in options node
        if sse_trailing:
            grd_args['export_trailing_text'] = sse_trailing

        # do a getresultdata to start the SSE and get
        export_id = self.SESSION.get_result_data_sse(**grd_args)

        m = "Server Side Export Started, id: '{}'"
        m = m.format(export_id)
        self.MYLOG.debug(m)

        poll_args = {}
        poll_args.update(kwargs)
        poll_args['export_id'] = export_id
        poll_args['handler'] = self

        poller = SSEPoller(**poll_args)
        poller_success = poller.run(**kwargs)
        sse_status = getattr(poller, 'STATUS', 'Unknown')

        if not poller_success:
            m = "SSE Poller failed while waiting for completion, last status: {}"
            m = m.format(sse_status)
            raise ServerSideExportError(m)

        result = poller.get_sse_data(**kwargs)

        if sse_format.lower() == 'xml_obj':
            if not result:
                result = sse_status
            else:
                info_overlay = self.get_result_info(**kwargs)
                result = from_sse_xml(result, info_overlay=info_overlay)
        return result

    def get_result_info(self, obj, **kwargs):
        """Get the result info for a python API object

        This method issues a GetResultInfo command to the SOAP api for `obj`. GetResultInfo
        returns information about how many servers have passed the `obj`, total number of servers,
        and so on.

        Parameters
        ----------
        obj : :class:`tanium_ng.base.BaseType`
            * object to get result data for
        shrink : bool, optional
            * default: True
            * True: Shrink the object down to just id/name/hash attributes (for smaller request)
            * False: Use the full object as is

        Returns
        -------
        ri : :class:`tanium_ng.result_info.ResultInfo`
            * The return of GetResultInfo for `obj`
        """
        shrink = kwargs.get('shrink', True)
        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)
        kwargs['pytan_help'] = kwargs.get('pytan_help', HELPS.gri)
        if shrink:
            kwargs['obj'] = shrink_obj(obj=obj)
        else:
            kwargs['obj'] = obj
        ri = self.SESSION.get_result_info(**kwargs)
        return ri

    # get objects
    def delete_groups(self, *args, **kwargs):
        """pass."""
        result = self.get_groups(*args, **kwargs)
        result = self._delete_objects(result)
        return result

    def delete_packages(self, *args, **kwargs):
        """pass."""
        result = self.get_packages(*args, **kwargs)
        result = self._delete_objects(result, **kwargs)
        return result

    def delete_saved_questions(self, *args, **kwargs):
        """pass."""
        result = self.get_saved_questions(*args, **kwargs)
        result = self._delete_objects(result, **kwargs)
        return result

    def delete_sensors(self, *args, **kwargs):
        """pass."""
        result = self.get_sensors(*args, **kwargs)
        result = self._delete_objects(result, **kwargs)
        return result

    def delete_users(self, *args, **kwargs):
        """pass."""
        result = self.get_users(*args, **kwargs)
        result = self._delete_objects(result, **kwargs)
        return result

    def delete_whitelisted_urls(self, *args, **kwargs):
        """pass."""
        result = self.get_whitelisted_urls(*args, **kwargs)
        result = self._delete_objects(result, **kwargs)
        return result

    def get_sensors(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = tanium_ng.SensorList
        kwargs['specs_from_args'] = args
        kwargs['hide_sourced_sensors'] = kwargs.get('hide_sourced_sensors', True)
        result = self._get_objects(**kwargs)
        return result

    def get_packages(self, *args, **kwargs):
        """pass. cache_filters need single fix"""
        kwargs['all_class'] = tanium_ng.PackageSpecList
        kwargs['specs_from_args'] = args
        kwargs['FIXIT_SINGLE'] = True
        result = self._get_objects(**kwargs)
        return result

    def get_actions(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = tanium_ng.ActionList
        kwargs['specs_from_args'] = args
        result = self._get_objects(**kwargs)
        return result

    def get_clients(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = tanium_ng.SystemStatusList
        kwargs['specs_from_args'] = args
        result = self._get_objects(**kwargs)
        return result

    def get_groups(self, *args, **kwargs):
        """pass. cant find unnamed groups by id using cache filters"""
        kwargs['all_class'] = tanium_ng.GroupList
        kwargs['specs_from_args'] = args
        kwargs['FIXIT_GROUP_ID'] = True
        result = self._get_objects(**kwargs)
        return result

    def get_questions(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = tanium_ng.QuestionList
        kwargs['specs_from_args'] = args
        result = self._get_objects(**kwargs)
        return result

    def get_saved_actions(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = tanium_ng.SavedActionList
        kwargs['specs_from_args'] = args
        result = self._get_objects(**kwargs)
        return result

    def get_saved_questions(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = tanium_ng.SavedQuestionList
        kwargs['specs_from_args'] = args
        result = self._get_objects(**kwargs)
        return result

    def get_settings(self, *args, **kwargs):
        """pass."""
        kwargs['all_class'] = tanium_ng.SystemSettingList
        kwargs['specs_from_args'] = args
        result = self._get_objects(**kwargs)
        return result

    def get_users(self, *args, **kwargs):
        """pass. cache_filters fail"""
        kwargs['all_class'] = tanium_ng.UserList
        kwargs['specs_from_args'] = args
        kwargs['FIXIT_BROKEN_FILTER'] = True
        result = self._get_objects(**kwargs)
        return result

    def get_user_roles(self, *args, **kwargs):
        """pass. cache_filters fail"""
        kwargs['all_class'] = tanium_ng.UserRoleList
        kwargs['specs_from_args'] = args
        kwargs['FIXIT_BROKEN_FILTER'] = True
        result = self._get_objects(**kwargs)
        return result

    def get_whitelisted_urls(self, *args, **kwargs):
        """pass. cache_filters fail"""
        kwargs['all_class'] = tanium_ng.WhiteListedUrlList
        kwargs['specs_from_args'] = args
        kwargs['FIXIT_BROKEN_FILTER'] = True
        result = self._get_objects(**kwargs)
        return result

    # BEGIN PRIVATE METHODS
    def _get_objects(self, all_class, **kwargs):
        """pass."""
        limit_exact = kwargs.get('limit_exact', None)
        hide_sourced_sensors = kwargs.get('hide_sourced_sensors', False)
        # get specs from kwargs or from args (assuming calling method put them in specs_from_args)
        kwargs['specs'] = kwargs.get('specs', []) or kwargs.get('specs_from_args', [])
        # don't include hidden objects by default
        kwargs['include_hidden_flag'] = kwargs.get('include_hidden_flag', 0)
        kwargs['all_class'] = all_class
        kwargs['obj'] = self._fixit_single(**kwargs)

        use_filters = False

        # if specs or hide_sourced_sensors, build cache filters and find results
        if kwargs['specs'] or hide_sourced_sensors:
            use_filters = True

        if use_filters:
            # get objects using cache filter
            kwargs['pytan_help'] = HELPS.getf.format(all_class.__name__)
            result = self._find_filter(**kwargs)
        else:
            # get all objects
            kwargs['pytan_help'] = HELPS.geta.format(all_class.__name__)
            result = self.SESSION.find(**kwargs)
            kwargs['objects'] = result
            check_limits(**kwargs)

        if limit_exact is not None:
            # if just one item returned and limit_exact == 1, return result as a single item
            # if result is a list
            if len(result) == 1 and limit_exact == 1:
                try:
                    result = result[0]
                except:
                    pass

        m = "get_objects found '{}' (using filters: {})"
        m = m.format(result, use_filters)
        self.MYLOG.info(m)
        return result

    def _get_spec_objects(self, side, **kwargs):
        """pass."""
        specs = kwargs.get(side, [])
        for spec in specs:
            if 'sensor' in spec:
                spec['sensor_object'] = self.get_sensors(limit_exact=1, specs=spec['sensor'])
            if 'group' in spec:
                spec['group_object'] = self.get_groups(limit_exact=1, specs=spec['group'])
            if 'package' in spec:
                spec['package_object'] = self.get_packages(limit_exact=1, specs=spec['package'])
        kwargs[side] = specs
        return kwargs

    def _fixit_single(self, **kwargs):
        """pass."""
        # FIXIT_SINGLE: GetObject in list form fails, so we need to use the singular form
        fixit = kwargs.get('FIXIT_SINGLE', False)
        result = kwargs['all_class']()
        if fixit:
            result = kwargs['all_class']._LIST_TYPE()
            m = "FIXIT_SINGLE: changed class from {} to {}"
            m = m.format(kwargs['all_class'].__name__, result.__name__)
            self.MYLOG.debug(m)
        return result

    def _fixit_group_id(self, specs, **kwargs):
        """pass."""
        # FIXIT_GROUP_ID: unnamed groups have to be searched for manually, cache filters dont work
        fixit = kwargs.get('FIXIT_GROUP_ID', False)
        result = kwargs['obj']
        if fixit:
            for spec in specs:
                if spec['field'] == 'id':
                    result = tanium_ng.Group()
                    setattr(result, spec['field'], spec['value'])
                    m = "FIXIT_GROUP_ID: changed class to 'Group' and set {field!r} to {value!r}"
                    m = m.format(**spec)
                    self.MYLOG.debug(m)
        return result

    def _fixit_broken_filter(self, objects, specs, **kwargs):
        """pass."""
        fixit = kwargs.get('FIXIT_BROKEN_FILTER', False)
        result = objects
        # FIXIT_BROKEN_FILTER: the API returns all objects even if using a cache filter
        if fixit:
            # create a new objects of the same class to store matching objects in
            m = "FIXIT_BROKEN_FILTER: Match {}: '{}' using specs: {}".format
            new_objects = objects.__class__()
            for spec in specs:
                for r in objects:
                    match_found = True
                    for subspec in spec:
                        if getattr(r, subspec['field']) != subspec['value']:
                            match_found = False

                    if match_found:
                        if r not in new_objects:
                            self.MYLOG.debug(m('found', r, spec))
                            new_objects.append(r)
                    else:
                        self.MYLOG.debug(m('not found', r, spec))

            m = "FIXIT_BROKEN_FILTER: original objects '{}', new objects '{}'"
            m = m.format(objects, new_objects)
            self.MYLOG.debug(m)
            result = new_objects
        return result

    def _find_filter(self, all_class, specs, **kwargs):
        """pass."""
        hide_sourced_sensors = kwargs.get('hide_sourced_sensors', False)

        # ensure specs is a list of lists
        specs = [coerce_list(s) for s in coerce_list(specs)]

        # create a base instance of all_class which all results will be added to
        result = all_class()

        # if we want to hide sourced sensors, add hide_spec
        hide_spec = {'value': '0', 'field': 'source_id'}
        if hide_sourced_sensors and not specs:
            specs = [[hide_spec]]

        all_parsed_specs = []

        for spec in specs:
            if hide_sourced_sensors and hide_spec not in spec:
                spec.append(hide_spec)

            # TODO: AWAITING MANUAL PARSER
            # validate & parse a string into a spec
            # if not isinstance(spec, (dict,)):
            #     spec = parsers.get_str(spec)

            # validate & parse the specs
            parsed_specs = [GetObject(all_class=all_class, spec=x).parsed_spec for x in spec]

            kwargs['specs'] = parsed_specs
            kwargs['obj'] = self._fixit_group_id(**kwargs)

            # create a cache filter list object using the parsed_specs
            kwargs['cache_filters'] = create_cachefilterlist(parsed_specs)

            # use getobject to find the results using the cache_filters to limit the returns
            cf_result = self.SESSION.find(**kwargs)

            m = "{} found using parsed specs: {!r}"
            m = m.format(cf_result, parsed_specs)
            self.MYLOG.debug(m)

            # if cf_result is a list, append each item to result
            try:
                cf_result[0]
                [result.append(r) for r in cf_result if r]
            # otherwise just append cf_result directly to result
            except:
                if cf_result:
                    result.append(cf_result)

            all_parsed_specs.append(parsed_specs)

        kwargs['specs'] = all_parsed_specs
        kwargs['objects'] = result
        result = self._fixit_broken_filter(**kwargs)

        kwargs['objects'] = result
        check_limits(**kwargs)
        return result

    def _add(self, obj, **kwargs):
        """Wrapper for interfacing with :func:`tanium_ng.session.Session.add`

        Parameters
        ----------
        obj : :class:`tanium_ng.base.BaseType`
            * object to add

        Returns
        -------
        added_obj : :class:`tanium_ng.base.BaseType`
           * full object that was added
        """
        kwargs['suppress_object_list'] = kwargs.get('suppress_object_list', 1)

        try:
            search_str = '; '.join([str(x) for x in obj])
        except:
            search_str = obj

        m = "Adding object {}"
        m = m.format(search_str)
        self.MYLOG.debug(m)

        kwargs['pytan_help'] = HELPS.addobj.format(obj.__class__.__name__)
        kwargs['obj'] = obj

        try:
            added_obj = self.SESSION.add(**kwargs)
        except:
            err = "Error while trying to add object: '{}'!!"
            err = err.format(search_str)
            self.MYLOG.critical(err)
            raise

        m = "Added Object: {}"
        m = m.format(added_obj)
        self.MYLOG.debug(m)

        kwargs['pytan_help'] = HELPS.addget.format(obj.__class__.__name__)
        kwargs['obj'] = added_obj

        try:
            result = self.SESSION.find(**kwargs)
        except:
            err = "Error while trying to find recently added object {}!!"
            err = err.format(search_str)
            self.MYLOG.critical(err)
            raise

        m = "Successfully added and fetched full object: {}"
        m = m.format(result)
        self.MYLOG.debug(m)
        return result

    def _delete_objects(self, objs, **kwargs):
        """pass."""
        # TODO
        # really_delete = kwargs.get('really_delete', False)
        # export_before_delete = kwargs.get('export_before_delete', True)
        result = [self._delete(o) for o in objs]
        return result

    def _delete(self, obj, **kwargs):
        """pass."""
        kwargs['obj'] = obj
        kwargs['pytan_help'] = kwargs.get('pytan_help', HELPS.delobj)
        result = self.SESSION.delete(**kwargs)
        m = "Deleted '{}'"
        m = m.format(result)
        self.MYLOG.info(m)
        return result

    def _version_support_check(self, v_maps, **kwargs):
        """Checks that each of the version maps in v_maps is greater than or equal to
        the current servers version

        Parameters
        ----------
        v_maps : list of str
            * each str should be a platform version
            * each str will be checked against self.SESSION.server_version
            * if self.SESSION.server_version is not greater than or equal to any str in v_maps,
            return will be False
            * if self.SESSION.server_version is greater than all strs in v_maps, return will be True
            * if self.server_version is invalid/can't be determined, return will be False

        Returns
        -------
        bool
            * True if all values in all v_maps are greater than or equal to
            self.SESSION.server_version
            * False otherwise
        """
        result = True
        if self.SESSION._invalid_server_version():
            # server version is not valid, force a refresh right now
            self.get_server_version(**kwargs)

        if self.SESSION._invalid_server_version():
            # server version is STILL invalid, return False
            result = False
        else:
            for v_map in v_maps:
                if not self.get_server_version(**kwargs) >= v_map:
                    result = False
        return result

    def _check_sse_format_support(self, sse_format, sse_format_int, **kwargs):
        """Determines if the export format integer is supported in the server version

        Parameters
        ----------
        sse_format : str or int
            * user supplied export format
        sse_format_int : int
            * `sse_format` parsed into an int
        """
        if sse_format_int not in SSE_RESTRICT_MAP:
            return

        restrict_maps = SSE_RESTRICT_MAP[sse_format_int]
        kwargs['v_maps'] = restrict_maps
        if not self._version_support_check(**kwargs):
            restrict_maps_txt = '\n'.join([str(x) for x in restrict_maps])
            err = (
                "Server version {} does not support export format {!r}, "
                "server version must be equal to or greater than one of:\n{}"
            )
            err = err.format(self.SESSION.server_version, sse_format, restrict_maps_txt)
            raise UnsupportedVersionError(err)

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
        result = [x[-1] for x in SSE_FORMAT_MAP if sse_format.lower() in x]

        if not result:
            ef_map_txt = '\n'.join(
                [', '.join(['{!r}'.format(x) for x in y]) for y in SSE_FORMAT_MAP]
            )
            err = "Unsupport export format {!r}, must be one of:\n{}"
            err = err.format(sse_format, ef_map_txt)
            raise PytanError(err)

        result = result[0]

        m = "'sse_format resolved from '{}' to '{}'"
        m = m.format(sse_format, result)
        self.MYLOG.debug(m)

        kwargs['sse_format'] = sse_format
        kwargs['sse_format_int'] = result
        self._check_sse_format_support(**kwargs)
        return result

    def _check_sse_version(self, **kwargs):
        """Validates that the server version supports server side export"""
        if not self.SESSION.platform_is_6_5(**kwargs):
            err = "Server side export not supported in version: {}"
            err = err.format(self.get_server_version())
            raise UnsupportedVersionError(err)

    def _check_sse_crash_prevention(self, obj, **kwargs):
        """Runs a number of methods used to prevent crashing the platform server when performing
        server side exports

        Parameters
        ----------
        obj : :class:`tanium_ng.base.BaseType`
            * object to pass to self._check_sse_empty_rs
        """
        kwargs['v_maps'] = SSE_CRASH_MAP
        kwargs['ok_version'] = self._version_support_check(**kwargs)
        kwargs['obj'] = obj
        self._check_sse_timing(**kwargs)
        self._check_sse_empty_rs(**kwargs)

    def _check_sse_timing(self, ok_version, **kwargs):
        """Checks that the last server side export was at least 1 second ago if server version is
        less than any versions in SSE_CRASH_MAP

        Parameters
        ----------
        ok_version : bool
            * if the version currently running is an "ok" version
        """
        last_get_rd_sse = getattr(self, 'last_get_rd_sse', None)
        if last_get_rd_sse:
            last_elapsed = datetime.datetime.utcnow() - last_get_rd_sse
            if last_elapsed.seconds == 0 and not ok_version:
                err = "You must wait at least one second between server side export requests!"
                raise ServerSideExportError(err)
        self.last_get_rd_sse = datetime.datetime.utcnow()

    def _check_sse_empty_rs(self, obj, ok_version, **kwargs):
        """Checks if the server version is less than any versions in
        SSE_CRASH_MAP, if so verifies that the result set is not empty

        Parameters
        ----------
        obj : :class:`tanium_ng.base.BaseType`
            * object to get result info for to ensure non-empty answers
        ok_version : bool
            * if the version currently running is an "ok" version
        """
        if not ok_version:
            kwargs['obj'] = obj
            ri = self.get_result_info(**kwargs)
            if ri.row_count == 0:
                err = "No rows available to perform a server side export with, result info: {}"
                err = err.format(ri)
                raise ServerSideExportError(err)
