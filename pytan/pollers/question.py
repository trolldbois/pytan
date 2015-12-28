#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Collection of classes and methods for polling of actions/questions in :mod:`pytan`"""

import time
import logging
import datetime

from pytan import PytanError, Store, tanium_ng
from pytan.utils import get_percent
from pytan.tickle.tools import secs_from_now, str_to_dt
from pytan.pollers.constants import Q_COMPLETE_PCT
from pytan.pollers.constants import Q_POLLING_SECS
from pytan.pollers.constants import Q_TIMEOUT_SECS
from pytan.pollers.constants import Q_EXPIRE_SECS
from pytan.pollers.constants import Q_PASSED_DONE
from pytan.pollers.constants import Q_EST_TOTAL_DONE

MYLOG = logging.getLogger(__name__)
PROGRESSLOG = logging.getLogger(__name__ + ".progress")
RESOLVERLOG = logging.getLogger(__name__ + ".resolver")

HELPS = Store()
HELPS.gri = "Re-issuing a GetResultInfo since the estimated_total came back 0, {}"
HELPS.reget = "ID: {} attribute {!r} is not set, issuing GetObject to get the full object"


class QuestionPollingError(PytanError):
    pass


class QuestionPoller(object):
    """A class to poll the progress of a Question.

    The primary function of this class is to poll for result info for a question, and fire off
    events:

        * ProgressChanged
        * AnswersChanged
        * AnswersComplete

    Parameters
    ----------
    handler : :class:`handler.Handler`
        * PyTan handler to use for GetResultInfo calls
    obj : :class:`tanium_ng.Question`
        * object to poll for progress
    polling_secs : int, optional
        * default: 5
        * Number of seconds to wait in between GetResultInfo loops
    complete_pct : int/float, optional
        * default: 99
        * Percentage of mr_tested out of estimated_total to consider the question "done"
    TIMEOUT_secs : int, optional
        * default: 0
        * If supplied and not 0, timeout in seconds instead of when object expires
    est_total_done : int, optional
        * instead of getting number of systems that should see this question from
        result_info.estimated_total, use this number
    passed_done : int, optional
        * when this number of systems have passed the right hand side of the question, consider
        the question complete
    """

    OBJ = None
    """The object for this poller"""

    HANDLER = None
    """The handler.Handler object for this poller"""

    INFO = None
    """This will be updated with the ResultInfo object during run() calls"""

    LAST_INFO = None
    """This will be updated with previous ResultInfo object during run() calls"""

    RUN_START = None
    """datetime.datetime object that indicates when run() was started"""

    TIMEOUT = None
    """
    datetime.datetime object that will be created when run() starts if
    self.OVERRIDE_TIMEOUT_SECS is not 0. this will be self.RUN_START + self.TIMEOUT_SECS.
    """

    POLLER_RESULT = None
    """bool that run() stores the overall result in"""

    PASSED_EQ_TOTAL = None
    """bool that run() stores the result of passed_eq_est_total_loop()"""

    CURRENT_PCT = 0
    """int/float that run() stores the current percent completion in"""

    LOOP_COUNT = 0
    """int/float that run() stores the current loop count in"""

    PROGRESS_STR = ''
    """str that run() stores the current progress in"""

    TIMING_STR = ''
    """str that run() stores the current timing info in"""

    COMPLETE_PCT = Q_COMPLETE_PCT
    """int/float to consider the question done when mr_tested is percent of estimated_total"""

    POLLING_SECS = Q_POLLING_SECS
    """int of seconds to wait in between run() loops"""

    TIMEOUT_SECS = Q_TIMEOUT_SECS
    """int of timeout in seconds instead of when object expires, 0 uses objects expiration"""

    EXPIRE_SECS = Q_EXPIRE_SECS
    """int of timeout in seconds to use if the EXPIRATION_ATTR of `obj` can't be determined"""

    EST_TOTAL_DONE = Q_EST_TOTAL_DONE
    """int to use in place of estimated_total from result info when considering COMPLETE_PCT"""

    PASSED_DONE = Q_PASSED_DONE
    """
    int of passed_count to consider question done instead of using estimated_total
    passed_count is the number of systems that have passed the right hand side of the question
    """

    EXPIRATION = None
    """datetime.datetime object created from the _EXPIRATION_ATTR of self.OBJ"""

    MYLOG = MYLOG
    """logger used by this class for logging general messages"""

    RESOLVERLOG = RESOLVERLOG
    """logger used by this class for logging attribute resolving messages"""

    PROGRESSLOG = PROGRESSLOG
    """logger used by this class for logging progress messages"""

    _ARG_OVERRIDES = [
        'polling_secs',
        'timeout_secs',
        'complete_pct',
        'est_total_done',
        'passed_done',
    ]
    """list of arguments that can be overridden via kwargs to __init__"""

    _OBJECT_TYPE = tanium_ng.Question
    """valid type of tanium_ng object that can be passed in as obj to __init__"""

    _STR_ATTRS = [
        'OBJECT_INFO',
        'POLLING_SECS',
        'TIMEOUT',
        'COMPLETE_PCT',
        'CURRENT_PCT',
        'EXPIRATION',
    ]
    """list of str of class attributes to include in __str__ output"""

    _EXPIRATION_ATTR = 'expiration'
    """attribute of self.OBJ that contains the expiration for this object"""

    _STOP = False
    """Controls whether a run() loop should stop or not"""

    _ID = -1
    """int that stores the ID of OBJ"""

    def __init__(self, handler, obj, **kwargs):
        self.HANDLER = handler
        self.OBJ = obj
        self.setup_logging()
        self.check_handler()
        self.check_obj()
        self.get_overrides(**kwargs)
        self._post_init(**kwargs)

    def __str__(self):
        class_name = self.__class__.__name__
        attrs = ['{0}: "{1}"'.format(x.lower(), getattr(self, x, None)) for x in self.STR_ATTRS]
        attrs = ", ".join(attrs)
        result = "{} {}".format(class_name, attrs)
        return result

    def get_overrides(self, **kwargs):
        [
            setattr(self, k.upper(), kwargs.get(k, getattr(self, k.upper())))
            for k in self._ARG_OVERRIDES
        ]

    def check_handler(self):
        if self.HANDLER.__class__.__name__ != 'Handler':
            err = "{} is not a valid Pytan Handler instance!"
            err = err.format(type(self.HANDLER))
            self.MYLOG.critical(err)
            raise QuestionPollingError(err)

    def check_obj(self):
        if not isinstance(self.OBJ, self._OBJECT_TYPE):
            err = "{} is not a valid object type! Must be a: {}"
            err = err.format(type(self.OBJ), self._OBJECT_TYPE)
            self.MYLOG.critical(err)
            raise QuestionPollingError(err)

    def setup_logging(self):
        """Setup loggers for this object"""
        self.MYLOG = MYLOG
        self.PROGRESSLOG = PROGRESSLOG
        self.RESOLVERLOG = RESOLVERLOG

    def _post_init(self, **kwargs):
        """Post init class setup"""

        self._ID = getattr(self.OBJ, 'id', self._ID)
        self._ID = self._derive_attribute(attr='id', fallback=None)
        self.POLLER_RESULT = None

        self._derive_expiration(**kwargs)
        self._derive_object_info(**kwargs)

    def _refetch_obj(self, **kwargs):
        """Utility method to re-fetch a object

        This is used in the case that the obj supplied does not have all the metadata
        available
        """
        kwargs['obj'] = self.OBJ
        obj = self.HANDLER.SESSION.find(kwargs)

        if not obj:
            err = "Unable to find object: {}"
            err = err.format(self.OBJ)
            self.MYLOG.critical(err)
            raise QuestionPollingError(err)

        self.OBJ = obj

    def _derive_attribute(self, attr, **kwargs):
        """Derive an attributes value from self.OBJ

        Will re-fetch self.OBJ if the attribute is not set

        Parameters
        ----------
        attr : string
            string of attribute name to fetch from self.OBJ
        fallback : string
            value to fallback to if it still can't be accessed after re-fetching the obj
            if fallback is None, an exception will be raised

        Returns
        -------
        val : perspective
            The value of the attr from self.OBJ

        """
        fallback = kwargs.get('fallback', '')

        result = getattr(self.OBJ, attr, None)

        # if attr isn't available on the object, maybe it's only a partial object
        # let's use the handler to re-fetch it
        if result is None:
            kwargs['pytan_help'] = HELPS.reget.format(self._ID, attr)
            self.RESOLVERLOG.debug(kwargs['pytan_help'])
            self._refetch_obj(**kwargs)

        result = getattr(self.OBJ, attr, '')
        if result is None:
            if fallback is None:
                err = "ID: {} {!r} is None, even after re-fetching object"
                err = err.format(self._ID, attr)
                self.MYLOG.critical(err)
                raise QuestionPollingError(err)

            m = "ID: {} attribute {!r} is not set after re-fetching object - using fallback of {}"
            m = m.format(self._ID, attr, fallback)
            self.RESOLVERLOG.debug(m)
            result = fallback

        m = "ID: {} attribute '{}' resolved to '{}'"
        m = m.format(self._ID, attr, result)
        self.MYLOG.debug(m)
        return result

    def _derive_object_info(self, **kwargs):
        """Derive self.OBJECT_INFO from self.OBJ"""
        kwargs['attr'] = 'query_text'
        kwargs['fallback'] = 'Unable to fetch question text'
        question_text = self._derive_attribute(**kwargs)

        kwargs['attr'] = 'id'
        kwargs['fallback'] = -1
        question_id = self._derive_attribute(**kwargs)

        object_info = "Question ID: {}, Query: {}"
        object_info = object_info.format(question_id, question_text)

        m = "ID: {} 'object_info' resolved to '{}'"
        m = m.format(self._ID, object_info)
        self.RESOLVERLOG.debug(m)
        self.OBJECT_INFO = object_info

    def _derive_expiration(self, **kwargs):
        """Derive the expiration datetime string from a object

        Will generate a datetime string from self.EXPIRE_SECS if unable to get the
        expiration from the object (self.OBJ) itself.
        """
        kwargs['attr'] = self._EXPIRATION_ATTR
        kwargs['fallback'] = secs_from_now(secs=self.EXPIRE_SECS)
        self.EXPIRATION = self._derive_attribute(**kwargs)
        self.EXPIRATION = str_to_dt(timestr=self.EXPIRATION)

    def run_callback(self, callback, pct, **kwargs):
        """Utility method to find a callback in callbacks dict and run it"""
        callbacks = kwargs.get('callbacks', {})
        if not callbacks.get(callback, ''):
            return

        kwargs['poller'] = self
        kwargs['pct'] = pct

        m = "Running callback: {} with args: {}"
        m = m.format(callback, kwargs)
        self.MYLOG.debug(m)

        try:
            callbacks[callback](**kwargs)
        except Exception as e:
            err = "Exception occurred in '{}' Callback: {}"
            err = err.format(callback, e)
            self.MYLOG.warning(err)

    def set_complect_pct(self, val): # noqa
        """Set the complete_pct to a new value

        Parameters
        ----------
        val : int/float
            float value representing the new percentage to consider self.OBJ complete
        """
        self.COMPLETE_PCT = val

    def get_result_info(self, **kwargs):
        """Simple utility wrapper around :func:`handler.Handler.get_result_info`

        Parameters
        ----------
        gri_retry_count : int, optional
            * default: 10
            * Number of times to re-try GetResultInfo when estimated_total comes back as 0

        Returns
        -------
        result_info : :class:`tanium_ng.ResultInfo`
        """
        # add a retry to re-fetch result info if estimated_total == 0
        gri_retry_count = kwargs.get('gri_retry_count', 10)
        gri_retry_sleep = kwargs.get('gri_retry_sleep', 1)

        kwargs['obj'] = self.OBJ
        current_try = 1

        while True:
            result = self.HANDLER.get_result_info(**kwargs)

            if result.estimated_total != 0:
                break

            attempt_text = "attempt {} out of {}".format(current_try, gri_retry_count)
            if current_try >= gri_retry_count:
                err = "Estimated Total of Clients is 0 -- no clients available?, {}"
                err = err.format(attempt_text)
                raise QuestionPollingError(err)
            else:
                current_try += 1
                kwargs['pytan_help'] = HELPS.gri.format(attempt_text)
                self.MYLOG.debug(kwargs['pytan_help'])
                time.sleep(gri_retry_sleep)
                continue
        return result

    def get_result_data(self, **kwargs):
        """Simple utility wrapper around :func:`handler.Handler.get_result_data`

        Returns
        -------
        result_data : :class:`tanium_ng.ResultSet`
        """
        kwargs['obj'] = self.OBJ
        result = self.HANDLER.get_result_data(**kwargs)
        return result

    def run(self, **kwargs):
        """Poll for question data and issue callbacks.

        Parameters
        ----------
        callbacks : dict
            * Callbacks should be a dict with any of these members:
                * 'ProgressChanged'
                * 'AnswersChanged'
                * 'AnswersComplete'

            * Each callback should be a function that accepts:
                * 'poller': a poller instance
                * 'pct': a percent complete
                * 'kwargs': a dict of other args
        gri_retry_count : int, optional
            * default: 10
            * Number of times to re-try GetResultInfo when estimated_total comes back as 0

        Notes
        -----
            * Any callback can choose to get data from the session by calling
            poller.get_result_data() or new info by calling poller.get_result_info()
            * Any callback can choose to stop the poller by calling poller.stop()
            * Polling will be stopped only when one of the callbacks calls the stop() method or
            the answers are complete.
            * Any callback can call setPercentCompleteThreshold to change what "done" means on the
            fly
        """
        self.RUN_START = datetime.datetime.utcnow()

        if self.TIMEOUT_SECS:
            td_obj = datetime.timedelta(seconds=self.TIMEOUT_SECS)
            self.TIMEOUT = self.RUN_START + td_obj
        else:
            self.TIMEOUT = None

        self.PASSED_EQ_TOTAL = self.passed_eq_est_total_loop(**kwargs)
        self.POLLER_RESULT = all([self.PASSED_EQ_TOTAL])
        return self.POLLER_RESULT

    def passed_eq_est_total_loop(self, **kwargs):
        """Method to poll Result Info for self.OBJ until the percentage of 'passed' out of
        'estimated_total' is greater than or equal to self.complete_pct
        """
        # current percentage tracker
        self.CURRENT_PCT = None
        # loop counter
        self.LOOP_COUNT = 1
        # establish a previous result_info that's empty
        self.LAST_INFO = tanium_ng.ResultInfo()  # TODO FIX FOR NEW RI OBJ

        while not self._STOP:
            # perform a GetResultInfo SOAP call
            del(kwargs['pytan_help'])
            self.INFO = self.get_result_info(**kwargs)

            # derive the current percentage of completion by calculating percentage of
            # mr_tested out of estimated_total
            # mr_tested = number of systems that have seen the question
            # estimated_total = rough estimate of total number of systems
            # passed = number of systems that have passed any filters for the question
            tested = self.INFO.mr_tested
            est_total = self.EST_TOTAL_DONE or self.INFO.estimated_total
            passed = self.INFO.passed

            new_pct = get_percent(base=tested, amount=est_total)
            new_pct_str = "{0:.0f}%".format(new_pct)
            complete_pct_str = "{0:.0f}%".format(self.complete_pct)

            prog = (
                "Progress: Tested: {0.tested}, Passed: {0.passed}, "
                "MR Tested: {0.mr_tested}, MR Passed: {0.mr_passed}, "
                "Est Total: {0.estimated_total}, Row Count: {0.row_count}, Override Est Total: {1}"
            )
            prog = prog.format(self.INFO, self.EST_TOTAL_DONE)
            self.PROGRESS_STR = prog

            if self.TIMEOUT:
                time_till_expiry = self.TIMEOUT - datetime.datetime.utcnow()
            else:
                time_till_expiry = self.EXPIRATION - datetime.datetime.utcnow()

            timing = (
                "Timing: Started: {}, Expiration: {}, Override Timeout: {}, "
                "Elapsed Time: {}, Left till expiry: {}, Loop Count: {}"
            )
            timing = timing.format(
                self.RUN_START,
                self.EXPIRATION,
                self.TIMEOUT,
                datetime.datetime.utcnow() - self.RUN_START,
                time_till_expiry,
                self.LOOP_COUNT,
            )
            self.TIMING_STR = timing

            # print a progress debug string
            m = "ID: {} {}"
            m = m.format(self._ID, prog)
            self.PROGRESSLOG.debug(m)

            # print a timing debug string
            m = "ID: {} {}"
            m = m.format(self._ID, timing)
            self.PROGRESSLOG.debug(m)

            # check to see if progress has changed, if so run the callback
            progress_changed = any([
                self.LAST_INFO.tested != self.INFO.tested,
                self.LAST_INFO.passed != self.INFO.passed,
                self.LAST_INFO.mr_tested != self.INFO.mr_tested,
                self.LAST_INFO.mr_passed != self.INFO.mr_passed,
                self.LAST_INFO.estimated_total != self.INFO.estimated_total,
                self.CURRENT_PCT != new_pct,
            ])

            if progress_changed:
                m = "ID: {} Progress Changed {} ({} of {})"
                m = m.format(self._ID, new_pct_str, tested, est_total)
                self.PROGRESSLOG.info(m)
                kwargs['callback'] = 'ProgressChanged'
                kwargs['pct'] = new_pct
                self.run_callback(**kwargs)

            # check to see if answers have changed, if so run the callback
            answers_changed = any([
                self.LAST_INFO.tested != self.INFO.tested,
                self.LAST_INFO.passed != self.INFO.passed,
            ])

            if answers_changed:
                kwargs['callback'] = 'AnswersChanged'
                kwargs['pct'] = new_pct
                self.run_callback(**kwargs)

            # check to see if new_pct has reached complete_pct threshold, if so return True
            if new_pct >= self.complete_pct:
                m = "ID: {} Reached Threshold of {} ({} of {})"
                m = m.format(self._ID, complete_pct_str, tested, est_total)
                self.MYLOG.info(m)
                kwargs['callback'] = 'AnswersComplete'
                kwargs['pct'] = new_pct
                self.run_callback(**kwargs)
                return True

            if self.PASSED_DONE and passed >= self.PASSED_DONE:
                m = "ID: {} Reached forced passed done count of {} ({} of {})"
                m = m.format(self._ID, self.PASSED_DONE, tested, est_total)
                self.MYLOG.info(m)
                kwargs['callback'] = 'AnswersComplete'
                kwargs['pct'] = new_pct
                self.run_callback(**kwargs)
                return True

            # check to see if timeout is specified, if so and we have passed it, return False
            if self.TIMEOUT and datetime.datetime.utcnow() >= self.TIMEOUT:
                m = "ID: {} Reached timeout of {}"
                m = m.format(self._ID, self.TIMEOUT)
                self.MYLOG.warning(m)
                return False

            # check to see if we have passed the actions expiration timeout, if so return False
            if datetime.datetime.utcnow() >= self.EXPIRATION_TIMEOUT:
                m = "ID: {} Reached expiration timeout of {}"
                m = m.format(self._ID, self.EXPIRATION_TIMEOUT)
                self.MYLOG.warning(m)
                return False

            # if stop is called, return True
            if self._STOP:
                m = "ID: {} Stop called at {}"
                m = m.format(self._ID, new_pct_str)
                self.MYLOG.info(m)
                return False

            # update our class variables to the new values determined by this loop
            self.CURRENT_PCT = new_pct
            self.LAST_INFO = self.INFO

            time.sleep(self.POLLING_SECS)
            self.LOOP_COUNT += 1

    def stop(self):
        self._STOP = True
