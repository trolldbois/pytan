#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Server Side Export Poller for :mod:`pytan`"""
import logging
import time

from datetime import datetime
from datetime import timedelta

from pytan.pollers import question
from pytan.utils import constants, exceptions, helpstr

mylog = logging.getLogger(__name__)
progresslog = logging.getLogger(__name__ + ".progress")
resolverlog = logging.getLogger(__name__ + ".resolver")


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
    STR_ATTRS = constants.S_STR_ATTRS
    """Class attributes to include in __str__ output"""

    POLLING_SECS_DEFAULT = constants.S_POLLING_SECS_DEFAULT
    """default value for self.polling_secs"""

    TIMEOUT_SECS_DEFAULT = constants.S_TIMEOUT_SECS_DEFAULT
    """default value for self.timeout_secs"""

    export_id = None
    """The export_id for this poller"""

    def __init__(self, handler, export_id, **kwargs):
        polling_secs = kwargs.get('polling_secs', self.POLLING_SECS_DEFAULT)
        timeout_secs = kwargs.get('timeout_secs', self.TIMEOUT_SECS_DEFAULT)

        from ..handler import Handler as BaseHandler

        self.mylog = mylog
        self.progresslog = progresslog
        self.resolverlog = resolverlog

        if not isinstance(handler, BaseHandler):
            err = "{} is not a valid handler instance! Must be a: {!r}"
            err = err.format(type(handler), BaseHandler)
            raise exceptions.PollingError(err)

        self.handler = handler
        self.export_id = export_id
        self.polling_secs = polling_secs
        self.timeout_secs = timeout_secs

        self.id_str = "ID '{}': ".format(export_id)
        self.poller_result = None
        self.sse_status = "Not yet run"
        self._post_init(**kwargs)

    def setup_logging(self):
        """Setup loggers for this object"""
        self.mylog = mylog
        self.progresslog = progresslog
        self.resolverlog = resolverlog

    def _post_init(self, **kwargs):
        """Post init class setup"""
        pass

    def get_sse_status(self, **kwargs):
        """Function to get the status of a server side export

        Constructs a URL via: export/${export_id}.status and performs an authenticated HTTP get
        """
        export_id = kwargs.get('export_id', self.export_id)

        kwargs['pytan_help'] = kwargs.get('pytan_help', helpstr.SSE_PROGRESS)
        kwargs['url'] = 'export/{}.status'.format(export_id)
        result = self.handler.session.http_request_auth(**kwargs).strip()

        # print a progress debug string
        full_url = self.handler.session._get_full_url(url=kwargs['url'])
        m = "{}Server Side Export Progress: '{}' from URL: {}"
        m = m.format(self.id_str, result, full_url)
        self.progresslog.debug(m)
        return result

    def get_sse_data(self, **kwargs):
        """Function to get the data of a server side export

        Constructs a URL via: export/${export_id}.gz and performs an authenticated HTTP get
        """
        export_id = kwargs.get('export_id', self.export_id)

        kwargs['pytan_help'] = kwargs.get('pytan_help', helpstr.SSE_GET)
        kwargs['url'] = 'export/{}.gz'.format(export_id)
        kwargs['empty_ok'] = True
        result = self.handler.session.http_request_auth(**kwargs).strip()

        # print a progress debug string
        full_url = self.handler.session._get_full_url(url=kwargs['url'])
        m = "{}Server Side Export Data Length: {} from URL: {}"
        m = m.format(self.id_str, len(result), full_url)
        self.progresslog.debug(m)
        return result

    def run(self, **kwargs):
        """Poll for server side export status"""
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

            timing = (
                "Timing: Started: {}, Timeout: {}, Elapsed Time: {}, Left till expiry: {}, "
                "Loop Count: {}"
            )
            timing = timing.format(
                self.start,
                self.timeout,
                datetime.utcnow() - self.start,
                time_till_expiry,
                self.loop_count,
            )
            self.timing_str = timing

            m = "{}{}"
            m = m.format(self.id_str, timing)
            self.progresslog.debug(m)

            # check to see if progress has changed, if so print progress log info
            progress_changed = any([
                self.previous_sse_status != self.sse_status,
            ])

            if progress_changed:
                m = "{}Progress Changed: '{}'"
                m = m.format(self.id_str, self.sse_status)
                self.progresslog.info(m)

            if 'failed' in self.sse_status.lower():
                err = "{}Server Side Export Failed: '{}'"
                err = err.format(self.id_str, self.sse_status)
                raise exceptions.ServerSideExportError(err)

            if 'completed' in self.sse_status.lower():
                m = "{}Server Side Export Completed: '{}'"
                m = m.format(self.id_str, self.sse_status)
                self.mylog.info(m)
                return True

            # check to see if timeout is specified, if so and we have passed it, return
            # False
            if self.timeout and datetime.utcnow() >= self.timeout:
                m = "{}Reached timeout of {}"
                m = m.format(self.id_str, self.timeout)
                self.mylog.warning(m)
                return False

            # if stop is called, return True
            if self._stop:
                m = "{}Stop called at {}"
                m = m.format(self.id_str, self.sse_status)
                self.mylog.info(m)
                return False

            # update our class variables to the new values determined by this loop
            self.previous_sse_status = self.sse_status

            time.sleep(self.polling_secs)
            self.loop_count += 1
