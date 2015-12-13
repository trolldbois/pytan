#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Collection of classes and methods for polling of actions/questions in :mod:`pytan`"""

import logging
import time
from datetime import datetime
from datetime import timedelta

from .. import utils

mylog = logging.getLogger(__name__)
progresslog = logging.getLogger(__name__ + ".progress")
resolverlog = logging.getLogger(__name__ + ".resolver")


class QuestionPoller(object):
    """A class to poll the progress of a Question.

    The primary function of this class is to poll for result info for a question, and fire off events:

        * ProgressChanged
        * AnswersChanged
        * AnswersComplete

    Parameters
    ----------
    handler : :class:`handler.Handler`
        * PyTan handler to use for GetResultInfo calls
    obj : :class:`utils.taniumpy.object_types.question.Question`
        * object to poll for progress
    polling_secs : int, optional
        * default: 5
        * Number of seconds to wait in between GetResultInfo loops
    complete_pct : int/float, optional
        * default: 99
        * Percentage of mr_tested out of estimated_total to consider the question "done"
    override_timeout_secs : int, optional
        * default: 0
        * If supplied and not 0, timeout in seconds instead of when object expires
    override_estimated_total : int, optional
        * instead of getting number of systems that should see this question from result_info.estimated_total, use this number
    force_passed_done_count : int, optional
        * when this number of systems have passed the right hand side of the question, consider the question complete
    """

    OBJECT_TYPE = utils.taniumpy.object_types.question.Question
    """valid type of object that can be passed in as obj to __init__"""

    STR_ATTRS = utils.constants.Q_STR_ATTRS
    """Class attributes to include in __str__ output"""

    COMPLETE_PCT_DEFAULT = utils.constants.Q_COMPLETE_PCT_DEFAULT
    """default value for self.complete_pct"""

    POLLING_SECS_DEFAULT = utils.constants.Q_POLLING_SECS_DEFAULT
    """default value for self.polling_secs"""

    OVERRIDE_TIMEOUT_SECS_DEFAULT = utils.constants.Q_OVERRIDE_TIMEOUT_SECS_DEFAULT
    """default value for self.override_timeout_secs"""

    EXPIRATION_ATTR = utils.constants.Q_EXPIRATION_ATTR
    """attribute of self.obj that contains the expiration for this object"""

    EXPIRY_FALLBACK_SECS = utils.constants.Q_EXPIRY_FALLBACK_SECS
    """If the EXPIRATION_ATTR of `obj` can't be automatically determined, then this is used as a fallback for timeout - polling will failed after this many seconds if completion not reached"""

    obj = None
    """The object for this poller"""

    handler = None
    """The handler.Handler object for this poller"""

    result_info = None
    """This will be updated with the ResultInfo object during run() calls"""

    _stop = False
    """Controls whether a run() loop should stop or not"""

    def __init__(self, handler, obj, **kwargs):
        from ..handler import Handler as BaseHandler
        self.setup_logging()

        if not isinstance(handler, BaseHandler):
            m = "{} is not a valid handler instance! Must be a: {!r}".format
            raise utils.exceptions.PollingError(m(type(handler), BaseHandler))

        if not isinstance(obj, self.OBJECT_TYPE):
            m = "{} is not a valid object type! Must be a: {}".format
            raise utils.exceptions.PollingError(m(type(obj), self.OBJECT_TYPE))

        self.handler = handler
        self.obj = obj
        self.polling_secs = kwargs.get('polling_secs', self.POLLING_SECS_DEFAULT)
        self.complete_pct = kwargs.get('complete_pct', self.COMPLETE_PCT_DEFAULT)
        self.override_timeout_secs = kwargs.get(
            'override_timeout_secs', self.OVERRIDE_TIMEOUT_SECS_DEFAULT,
        )
        self.force_passed_done_count = kwargs.get('force_passed_done_count', 0)

        self.id_str = "ID {}: ".format(getattr(self.obj, 'id', '-1'))
        self.obj_id = self._derive_attribute(attr='id', fallback=None)
        self.id_str = "ID {}: ".format(self.obj_id)
        self.poller_result = None
        self._post_init(**kwargs)

    def __str__(self):
        class_name = self.__class__.__name__
        attrs = ", ".join(['{0}: "{1}"'.format(x, getattr(self, x, None)) for x in self.STR_ATTRS])
        ret = "{} {}".format(class_name, attrs)
        return ret

    def setup_logging(self):
        """Setup loggers for this object"""
        self.mylog = mylog
        self.progresslog = progresslog
        self.resolverlog = resolverlog

    def _post_init(self, **kwargs):
        """Post init class setup"""

        self.override_estimated_total = kwargs.get('override_estimated_total', 0)
        self._derive_expiration(**kwargs)
        self._derive_object_info(**kwargs)

    def _refetch_obj(self, **kwargs):
        """Utility method to re-fetch a object

        This is used in the case that the obj supplied does not have all the metadata
        available
        """

        clean_keys = ['obj']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        obj = self.handler._find(obj=self.obj, **clean_kwargs)

        if utils.tanium_obj(obj):
            m = "Unable to find object: {}".format
            raise utils.exceptions.PollingError(m(self.obj))

        self.obj = obj

    def _derive_attribute(self, attr, fallback='', **kwargs):
        """Derive an attributes value from self.obj

        Will re-fetch self.obj if the attribute is not set

        Parameters
        ----------
        attr : string
            string of attribute name to fetch from self.obj
        fallback : string
            value to fallback to if it still can't be accessed after re-fetching the obj
            if fallback is None, an exception will be raised

        Returns
        -------
        val : perspective
            The value of the attr from self.obj

        """

        clean_keys = ['obj', 'pytan_help']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        val = getattr(self.obj, attr, None)

        # if attr isn't available on the object, maybe it's only a partial object
        # let's use the handler to re-fetch it
        if val is None:
            m = "{}attribute {!r} is not set, issuing GetObject to get the full object".format
            m = m(self.id_str, attr)
            self.resolverlog.debug(m)
            self._refetch_obj(pytan_help=m, **clean_kwargs)

        val = getattr(self.obj, attr, '')
        if val is None:
            if fallback is None:
                m = "{}{!r} is None, even after re-fetching object".format
                raise utils.exceptions.PollingError(m(self.id_str, attr))

            m = (
                "{}attribute {!r} is not set after re-fetching object - using fallback of {}"
            ).format

            self.resolverlog.debug(m(self.id_str, attr, fallback))
            val = fallback

        m = "{}attribute '{}' resolved to '{}'".format
        self.mylog.debug(m(self.id_str, attr, val))
        return val

    def _derive_object_info(self, **kwargs):
        """Derive self.object_info from self.obj"""

        clean_keys = ['attr', 'fallback']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        attr_name = 'query_text'
        fb = 'Unable to fetch question text'
        question_text = self._derive_attribute(attr=attr_name, fallback=fb, **clean_kwargs)

        attr_name = 'id'
        fb = -1
        question_id = self._derive_attribute(attr=attr_name, fallback=fb, **clean_kwargs)

        object_info = "Question ID: {}, Query: {}".format(question_id, question_text)

        m = "{}'object_info' resolved to '{}'".format
        self.resolverlog.debug(m(self.id_str, object_info))
        self.object_info = object_info

    def _derive_expiration(self, **kwargs):
        """Derive the expiration datetime string from a object

        Will generate a datetime string from self.EXPIRY_FALLBACK_SECS if unable to get the expiration from the object (self.obj) itself.
        """

        clean_keys = ['attr', 'fallback']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        attr_name = self.EXPIRATION_ATTR
        fb = utils.calc.seconds_from_now(secs=self.EXPIRY_FALLBACK_SECS)
        self.expiration = self._derive_attribute(attr=attr_name, fallback=fb, **clean_kwargs)

    def run_callback(self, callbacks, callback, pct, **kwargs):
        """Utility method to find a callback in callbacks dict and run it
        """

        if not callbacks.get(callback, ''):
            return

        cb_clean_keys = ['poller', 'pct']
        cb_clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=cb_clean_keys)

        try:
            m = "Running callback: {}".format
            self.mylog.debug(m(callback))
            callbacks[callback](poller=self, pct=pct, **cb_clean_kwargs)
        except Exception as e:
            m = "Exception occurred in '{}' Callback: {}".format
            self.mylog.warning(m(callback, e))

    def set_complect_pct(self, val): # noqa
        """Set the complete_pct to a new value

        Parameters
        ----------
        val : int/float
            float value representing the new percentage to consider self.obj complete
        """

        self.complete_pct = val

    def get_result_info(self, **kwargs):
        """Simple utility wrapper around :func:`handler.Handler.get_result_info`

        Parameters
        ----------
        gri_retry_count : int, optional
            * default: 10
            * Number of times to re-try GetResultInfo when estimated_total comes back as 0

        Returns
        -------
        result_info : :class:`utils.taniumpy.object_types.result_info.ResultInfo`
        """

        # add a retry to re-fetch result info if estimated_total == 0
        gri_retry_count = kwargs.get('gri_retry_count', 10)

        clean_keys = ['obj', 'gri_retry_count']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        current_try = 1

        while True:
            result_info = self.handler.get_result_info(obj=self.obj, **clean_kwargs)

            if result_info.estimated_total != 0:
                break

            attempt_text = "attempt {} out of {}".format(current_try, gri_retry_count)
            if current_try >= gri_retry_count:
                m = "Estimated Total of Clients is 0 -- no clients available?, {}".format
                raise utils.exceptions.PollingError(m(attempt_text))
            else:
                current_try += 1
                h = "Re-issuing a GetResultInfo since the estimated_total came back 0, {}".format
                clean_kwargs['pytan_help'] = h(attempt_text)
                self.mylog.debug(h(attempt_text))
                time.sleep(1)
                continue

        return result_info

    def get_result_data(self, **kwargs):
        """Simple utility wrapper around :func:`handler.Handler.get_result_data`

        Returns
        -------
        result_data : :class:`utils.taniumpy.object_types.result_set.ResultSet`
        """

        clean_keys = ['obj']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)
        result_data = self.handler.get_result_data(obj=self.obj, **clean_kwargs)
        return result_data

    def run(self, callbacks={}, **kwargs):
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
            * Any callback can choose to get data from the session by calling poller.get_result_data() or new info by calling poller.get_result_info()
            * Any callback can choose to stop the poller by calling poller.stop()
            * Polling will be stopped only when one of the callbacks calls the stop() method or the answers are complete.
            * Any callback can call setPercentCompleteThreshold to change what "done" means on the fly
        """

        self.start = datetime.utcnow()
        self.expiration_timeout = utils.calc.timestr_to_datetime(timestr=self.expiration)

        if self.override_timeout_secs:
            td_obj = timedelta(seconds=self.override_timeout_secs)
            self.override_timeout = self.start + td_obj
        else:
            self.override_timeout = None

        clean_keys = ['callbacks']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        self.passed_eq_total = self.passed_eq_est_total_loop(callbacks=callbacks, **clean_kwargs)
        self.poller_result = all([self.passed_eq_total])
        return self.poller_result

    def passed_eq_est_total_loop(self, callbacks={}, **kwargs):
        """Method to poll Result Info for self.obj until the percentage of 'passed' out of 'estimated_total' is greater than or equal to self.complete_pct
        """

        # current percentage tracker
        self.pct = None
        # loop counter
        self.loop_count = 1
        # establish a previous result_info that's empty
        self.previous_result_info = utils.taniumpy.object_types.result_info.ResultInfo()

        while not self._stop:
            # perform a GetResultInfo SOAP call
            clean_keys = ['pytan_help', 'callback', 'pct']
            clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

            h = "Issue a GetResultInfo for a Question to check the current progress of answers"
            self.result_info = self.get_result_info(pytan_help=h, **clean_kwargs)

            # derive the current percentage of completion by calculating percentage of
            # mr_tested out of estimated_total
            # mr_tested = number of systems that have seen the question
            # estimated_total = rough estimate of total number of systems
            # passed = number of systems that have passed any filters for the question
            tested = self.result_info.mr_tested
            est_total = self.override_estimated_total or self.result_info.estimated_total
            passed = self.result_info.passed

            new_pct = utils.calc.get_percent(base=tested, amount=est_total)
            new_pct_str = "{0:.0f}%".format(new_pct)
            complete_pct_str = "{0:.0f}%".format(self.complete_pct)

            # print a progress debug string
            self.progress_str = (
                "Progress: Tested: {0.tested}, Passed: {0.passed}, "
                "MR Tested: {0.mr_tested}, MR Passed: {0.mr_passed}, "
                "Est Total: {0.estimated_total}, Row Count: {0.row_count}, Override Est Total: {1}"
            ).format(self.result_info, self.override_estimated_total)
            self.progresslog.debug("{}{}".format(self.id_str, self.progress_str))

            # print a timing debug string
            if self.override_timeout:
                time_till_expiry = self.override_timeout - datetime.utcnow()
            else:
                time_till_expiry = self.expiration_timeout - datetime.utcnow()

            self.timing_str = (
                "Timing: Started: {}, Expiration: {}, Override Timeout: {}, "
                "Elapsed Time: {}, Left till expiry: {}, Loop Count: {}"
            ).format(
                self.start,
                self.expiration_timeout,
                self.override_timeout,
                datetime.utcnow() - self.start,
                time_till_expiry,
                self.loop_count,
            )
            self.progresslog.debug("{}{}".format(self.id_str, self.timing_str))

            # check to see if progress has changed, if so run the callback
            progress_changed = any([
                self.previous_result_info.tested != self.result_info.tested,
                self.previous_result_info.passed != self.result_info.passed,
                self.previous_result_info.mr_tested != self.result_info.mr_tested,
                self.previous_result_info.mr_passed != self.result_info.mr_passed,
                self.previous_result_info.estimated_total != self.result_info.estimated_total,
                self.pct != new_pct,
            ])

            if progress_changed:
                m = "{}Progress Changed {} ({} of {})".format
                self.progresslog.info(m(self.id_str, new_pct_str, tested, est_total))
                cb = 'ProgressChanged'
                self.run_callback(callbacks=callbacks, callback=cb, pct=new_pct, **clean_kwargs)

            # check to see if answers have changed, if so run the callback
            answers_changed = any([
                self.previous_result_info.tested != self.result_info.tested,
                self.previous_result_info.passed != self.result_info.passed,
            ])

            if answers_changed:
                cb = 'AnswersChanged'
                self.run_callback(callbacks=callbacks, callback=cb, pct=new_pct, **clean_kwargs)

            # check to see if new_pct has reached complete_pct threshold, if so return True
            if new_pct >= self.complete_pct:
                m = "{}Reached Threshold of {} ({} of {})".format
                self.mylog.info(m(self.id_str, complete_pct_str, tested, est_total))
                cb = 'AnswersComplete'
                self.run_callback(callbacks=callbacks, callback=cb, pct=new_pct, **clean_kwargs)
                return True

            if self.force_passed_done_count and passed >= self.force_passed_done_count:
                m = "{}Reached forced passed done count of {} ({} of {})".format
                self.mylog.info(m(self.id_str, self.force_passed_done_count, tested, est_total))
                cb = 'AnswersComplete'
                self.run_callback(callbacks=callbacks, callback=cb, pct=new_pct, **clean_kwargs)
                return True

            # check to see if override timeout is specified, if so and we have passed it, return
            # False
            if self.override_timeout and datetime.utcnow() >= self.override_timeout:
                m = "{}Reached override timeout of {}".format
                self.mylog.warning(m(self.id_str, self.override_timeout))
                return False

            # check to see if we have passed the actions expiration timeout, if so return False
            if datetime.utcnow() >= self.expiration_timeout:
                m = "{}Reached expiration timeout of {}".format
                self.mylog.warning(m(self.id_str, self.expiration_timeout))
                return False

            # if stop is called, return True
            if self._stop:
                m = "{}Stop called at {}".format
                self.mylog.info(m(self.id_str, new_pct_str))
                return False

            # update our class variables to the new values determined by this loop
            self.pct = new_pct
            self.previous_result_info = self.result_info

            time.sleep(self.polling_secs)
            self.loop_count += 1

    def stop(self):
        self._stop = True
