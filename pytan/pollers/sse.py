#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Server Side Export Poller for :mod:`pytan`"""
import time
import logging
import datetime

from pytan import PytanError, Store
from pytan.pollers.question import QuestionPoller
from pytan.pollers.constants import S_POLLING_SECS
from pytan.pollers.constants import S_TIMEOUT_SECS

MYLOG = logging.getLogger(__name__)
PROGRESSLOG = logging.getLogger(__name__ + ".progress")
RESOLVERLOG = logging.getLogger(__name__ + ".resolver")

HELPS = Store()
HELPS.progress = "Perform an HTTP get to retrieve the status of a server side export"
HELPS.getdata = "Perform an HTTP get to retrieve the data of a server side export"


class SSEPollingError(PytanError):
    pass


class SSEPoller(QuestionPoller):
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
        * timeout in seconds for waiting for status completion
    """

    POLLING_SECS = S_POLLING_SECS
    """int of seconds to wait in between run() loops"""

    TIMEOUT_SECS = S_TIMEOUT_SECS
    """int of timeout in seconds"""

    EXPORT_ID = ''
    """str of export_id to poll"""

    LOOP_COUNT = 0
    """int/float that run() stores the current loop count in"""

    STATUS = None
    """This will be updated with the current SSE status during run() calls"""

    LAST_STATUS = None
    """This will be updated with previous SSE status during run() calls"""

    STATUS = "Not yet run"
    """str of status updated by run()"""

    PROGRESS_STR = ''
    """str that run() stores the current progress in"""

    TIMING_STR = ''
    """str that run() stores the current timing info in"""

    TIMEOUT = None
    """datetime.datetime object created from RUN_START + TIMEOUT_SECS"""

    RUN_START = None
    """datetime.datetime object that indicates when run() was started"""

    LOOP_COUNT = 0
    """int/float that run() stores the current loop count in"""

    MYLOG = MYLOG
    """logger used by this class for logging general messages"""

    PROGRESSLOG = PROGRESSLOG
    """logger used by this class for logging progress messages"""

    _ARG_OVERRIDES = [
        'polling_secs',
        'timeout_secs',
    ]
    """list of arguments that can be overridden via kwargs to __init__"""

    _STR_ATTRS = [
        'export_id',
        'polling_secs',
        'timeout_secs',
        'sse_status',
    ]
    """Class attributes to include in __str__ output"""

    def __init__(self, handler, export_id, **kwargs):
        self.HANDLER = handler
        self.EXPORT_ID = export_id
        self.setup_logging()
        self.check_handler()
        self.get_overrides(**kwargs)

    def setup_logging(self):
        """Setup loggers for this object"""
        self.MYLOG = MYLOG
        self.PROGRESSLOG = PROGRESSLOG

    def get_sse_status(self, **kwargs):
        """Function to get the status of a server side export

        Constructs a URL via: export/${export_id}.status and performs an authenticated HTTP get
        """
        export_id = kwargs.get('export_id', self.EXPORT_ID)

        kwargs['pytan_help'] = kwargs.get('pytan_help', HELPS.progress)
        kwargs['url'] = 'export/{}.status'.format(export_id)
        result = self.HANDLER.SESSION.http_request_auth(**kwargs).strip()

        # print a progress debug string
        full_url = self.HANDLER.SESSION._get_full_url(url=kwargs['url'])
        m = "ID: {} Server Side Export Progress: '{}' from URL: {}"
        m = m.format(export_id, result, full_url)
        self.PROGRESSLOG.debug(m)
        return result

    def get_sse_data(self, **kwargs):
        """Function to get the data of a server side export

        Constructs a URL via: export/${export_id}.gz and performs an authenticated HTTP get
        """
        export_id = kwargs.get('export_id', self.EXPORT_ID)

        kwargs['pytan_help'] = kwargs.get('pytan_help', HELPS.getdata)
        kwargs['url'] = 'export/{}.gz'.format(export_id)
        kwargs['empty_ok'] = True
        result = self.HANDLER.SESSION.http_request_auth(**kwargs).strip()

        # print a progress debug string
        full_url = self.HANDLER.SESSION._get_full_url(url=kwargs['url'])
        m = "ID: {} Server Side Export Data Length: {} from URL: {}"
        m = m.format(export_id, len(result), full_url)
        self.PROGRESSLOG.debug(m)
        return result

    def run(self, **kwargs):
        """Poll for server side export status"""
        self.RUN_START = datetime.datetime.utcnow()

        td_obj = datetime.timedelta(seconds=self.TIMEOUT_SECS)
        self.TIMEOUT = self.RUN_START + td_obj

        self.STATUS = self.status_loop(**kwargs)
        self.POLLER_RESULT = all([self.STATUS])
        return self.POLLER_RESULT

    def status_loop(self, **kwargs):
        """Method to poll the status file for a server side export until it contains 'Completed'"""
        self.LOOP_COUNT = 1
        self.LAST_STATUS = ''

        while not self._STOP:
            self.STATUS = self.get_sse_status(**kwargs)

            timing = (
                "Timing: Started: {}, Timeout: {}, Elapsed Time: {}, Left till expiry: {}, "
                "Loop Count: {}"
            )

            timing = timing.format(
                self.RUN_START,
                self.TIMEOUT,
                datetime.datetime.utcnow() - self.RUN_START,
                self.TIMEOUT - datetime.datetime.utcnow(),
                self.LOOP_COUNT,
            )
            self.TIMING_STR = timing

            m = "ID: {} {}"
            m = m.format(self.EXPORT_ID, timing)
            self.PROGRESSLOG.debug(m)

            progress_changed = any([
                self.LAST_STATUS != self.STATUS,
            ])

            print(1)
            if progress_changed:
                m = "ID: {} Progress Changed: '{}'"
                m = m.format(self.EXPORT_ID, self.STATUS)
                self.PROGRESSLOG.info(m)

            print(2)

            if 'failed' in self.STATUS.lower():
                err = "ID: {} Server Side Export Failed: '{}'"
                err = err.format(self.EXPORT_ID, self.STATUS)
                raise SSEPollingError(err)

            print(3)

            if 'completed' in self.STATUS.lower():
                m = "ID: {} Server Side Export Completed: '{}'"
                m = m.format(self.EXPORT_ID, self.STATUS)
                self.MYLOG.info(m)
                return True

            print(4)

            if self.TIMEOUT and datetime.datetime.utcnow() >= self.TIMEOUT:
                m = "ID: {} Reached timeout of {}"
                m = m.format(self.EXPORT_ID, self.TIMEOUT)
                self.MYLOG.warning(m)
                return False

            print(5)

            if self._STOP:
                m = "ID: {} Stop called at {}"
                m = m.format(self.EXPORT_ID, self.STATUS)
                self.MYLOG.info(m)
                return False

            # update our class variables to the new values determined by this loop
            self.LAST_STATUS = self.STATUS

            time.sleep(self.POLLING_SECS)
            self.LOOP_COUNT += 1
