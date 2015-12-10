#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Server Side Export Poller for :mod:`pytan`"""

import sys
import logging
import time
from datetime import datetime
from datetime import timedelta

from . import question
from .. import utils


class SSEPoller(question.QuestionPoller):
    """A class to poll the progress of a Server Side Export.

    The primary function of this class is to poll for status of server side exports.

    Parameters
    ----------
    handler : :class:`Handler`
        PyTan handler to use for GetResultInfo calls
    export_id : str
        * ID of server side export
    polling_secs : int, optional
        * default: 2
        * Number of seconds to wait in between status check loops
    timeout_secs : int, optional
        * default: 600
        * timeout in seconds for waiting for status completion, 0 does not time out
    """
    STR_ATTRS = utils.constants.S_STR_ATTRS
    """Class attributes to include in __str__ output"""

    POLLING_SECS_DEFAULT = utils.constants.S_POLLING_SECS_DEFAULT
    """default value for self.polling_secs"""

    TIMEOUT_SECS_DEFAULT = utils.constants.S_TIMEOUT_SECS_DEFAULT
    """default value for self.timeout_secs"""

    export_id = None
    """The export_id for this poller"""

    def __init__(self, handler, export_id, **kwargs):
        from ..handler import Handler as BaseHandler
        self.methodlog = logging.getLogger("method_debug")
        self.DEBUG_METHOD_LOCALS = kwargs.get('debug_method_locals', False)

        self._debug_locals(sys._getframe().f_code.co_name, locals())

        self.setup_logging()

        if not isinstance(handler, BaseHandler):
            m = "{} is not a valid handler instance! Must be a: {!r}".format
            raise utils.exceptions.PollingError(m(type(handler), BaseHandler))

        self.handler = handler
        self.export_id = export_id
        self.polling_secs = kwargs.get('polling_secs', self.POLLING_SECS_DEFAULT)
        self.timeout_secs = kwargs.get('timeout_secs', self.TIMEOUT_SECS_DEFAULT)

        self.id_str = "ID '{}': ".format(export_id)
        self.poller_result = None
        self.sse_status = "Not yet run"
        self._post_init(**kwargs)

    def _post_init(self, **kwargs):
        """Post init class setup"""
        self._debug_locals(sys._getframe().f_code.co_name, locals())

        pass

    def get_sse_status(self, **kwargs):
        """Function to get the status of a server side export

        Constructs a URL via: export/${export_id}.status and performs an authenticated HTTP get
        """
        self._debug_locals(sys._getframe().f_code.co_name, locals())

        clean_keys = ['url']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        export_id = kwargs.get('export_id', self.export_id)
        short_url = 'export/{}.status'.format(export_id)
        full_url = self.handler.session._full_url(url=short_url)

        h = "Perform an HTTP get to retrieve the status of a server side export"
        clean_kwargs['pytan_help'] = clean_kwargs.get('pytan_help', h)

        ret = self.handler.session.http_get(url=short_url, **clean_kwargs).strip()

        # print a progress debug string
        progress_str = "Server Side Export Progress: '{}' from URL: {}".format
        progress_str = progress_str(ret, full_url)
        self.progresslog.debug("{}{}".format(self.id_str, progress_str))

        return ret

    def get_sse_data(self, **kwargs):
        """Function to get the data of a server side export

        Constructs a URL via: export/${export_id}.gz and performs an authenticated HTTP get
        """
        self._debug_locals(sys._getframe().f_code.co_name, locals())

        clean_keys = ['url']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        export_id = kwargs.get('export_id', self.export_id)
        short_url = 'export/{}.gz'.format(export_id)
        full_url = self.handler.session._full_url(url=short_url)

        h = "Perform an HTTP get to retrieve the data of a server side export"
        clean_kwargs['pytan_help'] = clean_kwargs.get('pytan_help', h)

        ret = self.handler.session.http_get(url=short_url, **clean_kwargs)

        # print a progress debug string
        progress_str = "Server Side Export Data Length: {} from URL: {}".format
        progress_str = progress_str(len(ret), full_url)
        self.progresslog.debug("{}{}".format(self.id_str, progress_str))

        return ret

    def run(self, **kwargs):
        """Poll for server side export status"""
        self._debug_locals(sys._getframe().f_code.co_name, locals())

        self.start = datetime.utcnow()

        if self.timeout_secs:
            td_obj = timedelta(seconds=self.timeout_secs)
            self.timeout = self.start + td_obj
        else:
            self.timeout = None

        self.sse_status_completed = self.sse_status_has_completed_loop(**kwargs)
        self.poller_result = all([self.sse_status_completed])
        return self.poller_result

    def sse_status_has_completed_loop(self, **kwargs):
        """Method to poll the status file for a server side export until it contains 'Completed'"""
        self._debug_locals(sys._getframe().f_code.co_name, locals())

        # loop counter
        self.loop_count = 1
        # establish a previous result_info that's empty
        self.previous_sse_status = ''

        while not self._stop:
            # get the SSE status
            self.sse_status = self.get_sse_status(**kwargs)

            # print a timing debug string
            if self.timeout:
                time_till_expiry = self.timeout - datetime.utcnow()
            else:
                time_till_expiry = 'Never'

            self.timing_str = (
                "Timing: Started: {}, Timeout: {}, Elapsed Time: {}, Left till expiry: {}, "
                "Loop Count: {}"
            ).format(
                self.start,
                self.timeout,
                datetime.utcnow() - self.start,
                time_till_expiry,
                self.loop_count,
            )
            self.progresslog.debug("{}{}".format(self.id_str, self.timing_str))

            # check to see if progress has changed, if so print progress log info
            progress_changed = any([
                self.previous_sse_status != self.sse_status,
            ])

            if progress_changed:
                m = "{}Progress Changed: '{}'".format
                self.progresslog.info(m(self.id_str, self.sse_status))

            if 'failed' in self.sse_status.lower():
                m = "{}Server Side Export Failed: '{}'".format
                raise utils.exceptions.ServerSideExportError(m(self.id_str, self.sse_status))

            if 'completed' in self.sse_status.lower():
                m = "{}Server Side Export Completed: '{}'".format
                self.mylog.info(m(self.id_str, self.sse_status))
                return True

            # check to see if timeout is specified, if so and we have passed it, return
            # False
            if self.timeout and datetime.utcnow() >= self.timeout:
                m = "{}Reached timeout of {}".format
                self.mylog.warning(m(self.id_str, self.timeout))
                return False

            # if stop is called, return True
            if self._stop:
                m = "{}Stop called at {}".format
                self.mylog.info(m(self.id_str, self.sse_status))
                return False

            # update our class variables to the new values determined by this loop
            self.previous_sse_status = self.sse_status

            time.sleep(self.polling_secs)
            self.loop_count += 1
