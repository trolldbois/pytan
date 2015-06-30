#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Collection of classes and methods for polling of actions/questions in :mod:`pytan`"""

import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import logging
import time
from datetime import datetime
from datetime import timedelta

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)


import taniumpy
import pytan


class QuestionPoller(object):
    """A class to poll the progress of a Question.

    The primary function of this class is to poll for result info for questions, and fire off events:

    ProgressChanged
    AnswersChanged
    AnswersComplete

    Parameters
    ----------
    handler : :class:`pytan.handler.Handler`
        PyTan handler to use for GetResultInfo calls
    obj : :class:`taniumpy.object_types.question.Question`
        object to poll for progress
    polling_secs : int, optional
        Number of seconds to wait in between GetResultInfo loops
    complete_pct : int/float, optional
        Percentage of mr_tested out of estimated_total to consider the question "done"
    override_timeout_secs : int, optional
        If supplied and not 0, timeout in seconds instead of when object expires
    """

    # valid types of objects that can be passed in as obj to __init__
    OBJECT_TYPE = taniumpy.object_types.question.Question

    # if we can't identify the expiration of the object, then we will consider the polling
    # "failed" after this many seconds
    EXPIRY_FALLBACK_SECS = 600

    # class attributes to include in __str__ output
    STR_ATTRS = [
        'obj_info',
        'polling_secs',
        'override_timeout_secs',
        'complete_pct',
        'expiration',
    ]

    COMPLETE_PCT = 99
    POLLING_SECS = 5

    qplog = logging.getLogger("pytan.handler.QuestionPoller")
    qpplog = logging.getLogger("pytan.handler.QuestionPoller.progress")

    def __init__(self, handler, obj, override_timeout_secs=0, **kwargs):

        if not isinstance(handler, pytan.handler.Handler):
            m = "{} is not a valid handler instance! Must be a: {!r}".format
            raise pytan.exceptions.PollingError(m(type(handler), pytan.handler.Handler))

        if not isinstance(obj, self.OBJECT_TYPE):
            m = "{} is not a valid object type! Must be a: {}".format
            raise pytan.exceptions.PollingError(m(type(obj), self.OBJECT_TYPE))

        self.handler = handler
        self.obj = obj
        self.polling_secs = kwargs.get('polling_secs', self.POLLING_SECS)
        self.complete_pct = kwargs.get('complete_pct', self.COMPLETE_PCT)
        self.override_timeout_secs = override_timeout_secs
        self.result_info = None
        self._stop = False
        self.id_str = "ID {}: ".format(getattr(self.obj, 'id', '-1'))
        self.obj_id = self._derive_attribute('id', None)
        self.id_str = "ID {}: ".format(self.obj_id)
        self.poller_result = None
        self._post_init()

    def __str__(self):
        class_name = self.__class__.__name__
        attrs = ", ".join(['{0}: "{1}"'.format(x, getattr(self, x, None)) for x in self.STR_ATTRS])
        ret = "{} {}".format(class_name, attrs)
        return ret

    def _post_init(self):
        """Post init class setup"""
        self._derive_expiration()
        self._derive_info()

    def _refetch_obj(self):
        """Utility method to re-fetch a object

        This is used in the case that the obj supplied does not have all the metadata
        available
        """
        obj = self.handler._find(self.obj)
        if pytan.utils.empty_obj(obj):
            m = "Unable to find object: {}".format
            raise pytan.exceptions.PollingError(m(self.obj))
        self.obj = obj

    def _derive_attribute(self, attr, fallback=''):
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
        val = getattr(self.obj, attr, None)

        # if attr isn't available on the object, maybe it's only a partial object
        # let's use the handler to re-fetch it
        if val is None:
            m = "{}{!r} not available, re-fetching object".format
            self.qplog.debug(m(self.id_str, attr))
            self._refetch_obj()

        val = getattr(self.obj, attr, '')
        if val is None:
            if fallback is None:
                m = "{}{!r} is None, even after re-fetching object".format
                raise pytan.exceptions.PollingError(m(self.id_str, attr))

            m = "{0}{!r} is None even after re-fetching object - using fallback of {}".format
            self.qplog.debug(m(self.id_str, attr, fallback))
            val = fallback

        m = "{}{} resolved to {}".format
        self.qplog.debug(m(self.id_str, attr, val))
        return val

    def _derive_info(self):
        """Derive self.obj_info from self.obj"""
        question_text = self._derive_attribute('query_text', 'Unable to fetch question text')
        question_id = self._derive_attribute('id', -1)
        obj_info = "Question ID: {}, Query: {}".format(question_id, question_text)

        m = "{}Object Info resolved to {}".format
        self.qplog.debug(m(self.id_str, obj_info))
        self.obj_info = obj_info

    def _derive_expiration(self):
        """Derive the expiration datetime string from a object

        Will generate a datetime string from self.EXPIRY_FALLBACK_SECS if unable to get the expiration from the object (self.obj) itself.
        """
        fallback = pytan.utils.seconds_from_now(self.EXPIRY_FALLBACK_SECS)
        self.expiration = self._derive_attribute('expiration', fallback)

    def set_complect_pct(self, val): # noqa
        """Set the complete_pct to a new value

        Parameters
        ----------
        val : int/float
            float value representing the new percentage to consider self.obj complete
        """
        self.complete_pct = val

    def get_result_info(self, **kwargs):
        """Simple utility wrapper around handler.get_result_info()"""
        result_info = self.handler.get_result_info(self.obj, **kwargs)
        if result_info.estimated_total == 0:
            m = "Estimated Total of Clients is 0 -- no clients available?".format
            raise pytan.exceptions.PollingError(m())
        return result_info

    def get_result_data(self, **kwargs):
        """Simple utility wrapper around handler.get_result_data()"""
        return self.handler.get_result_data(self.obj, **kwargs)

    def run(self, callbacks={}, **kwargs):
        """Poll for question data and issue callbacks.

        Parameters
        ----------
        callbacks : dict
            Callbacks should be a dict with any of these members:
            'ProgressChanged'
            'AnswersChanged'
            'AnswersComplete'

            Each callback should be a function that accepts a poller instance and a percent complete.

            Any callback can choose to get data from the session by calling poller.get_result_data() or new info by calling poller.get_result_info()

            Any callback can choose to stop the poller by calling poller.stop()

            Polling will be stopped only when one of the callbacks calls the stop() method or the answers are complete. Note that callbacks can call setPercentCompleteThreshold to change what "done" means on the fly
        """

        self.start = datetime.utcnow()
        self.expiration_timeout = pytan.utils.timestr_to_datetime(self.expiration)
        if self.override_timeout_secs:
            self.override_timeout = self.start + timedelta(seconds=self.override_timeout_secs)
        else:
            self.override_timeout = None

        self.passed_eq_total = self.passed_eq_est_total_loop(callbacks, **kwargs)
        self.poller_result = all([self.passed_eq_total])
        return self.poller_result

    def passed_eq_est_total_loop(self, callbacks={}, **kwargs):
        # current percentage tracker
        self.pct = None
        # loop counter
        self.loop_count = 1
        # establish a previous result_info that's empty
        self.previous_result_info = taniumpy.object_types.result_info.ResultInfo()

        while not self._stop:
            # perform a GetResultInfo SOAP call
            self.result_info = self.get_result_info(**kwargs)

            # derive the current percentage of completion by calculating percentage of
            # mr_tested out of estimated_total
            # mr_tested = number of systems that have seen the question
            # estimated_total = rough estimate of total number of systems
            # passed = number of systems that have passed any filters for the question
            new_pct = pytan.utils.get_percentage(
                self.result_info.mr_tested, self.result_info.estimated_total,
            )
            new_pct_str = "{0:.0f}%".format(new_pct)
            complete_pct_str = "{0:.0f}%".format(self.complete_pct)

            # print a progress debug string
            self.progress_str = (
                "Progress: Tested: {0.tested}, Passed: {0.passed}, "
                "MR Tested: {0.mr_tested}, MR Passed: {0.mr_passed}, "
                "Est Total: {0.estimated_total}, Row Count: {0.row_count}"
            ).format(self.result_info)
            self.qplog.debug("{}{}".format(self.id_str, self.progress_str))

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
            self.qplog.debug("{}{}".format(self.id_str, self.timing_str))

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
                self.qplog.info(m(
                    self.id_str,
                    new_pct_str,
                    self.result_info.mr_tested,
                    self.result_info.estimated_total,
                ))
                if callbacks.get('ProgressChanged'):
                    callbacks['ProgressChanged'](self, new_pct)

            # check to see if answers have changed, if so run the callback
            answers_changed = any([
                self.previous_result_info.tested != self.result_info.tested,
                self.previous_result_info.passed != self.result_info.passed,
            ])

            if answers_changed:
                if callbacks.get('AnswersChanged'):
                    callbacks['AnswersChanged'](self, new_pct)

            # check to see if new_pct has reached complete_pct threshold, if so return True
            if new_pct >= self.complete_pct:
                m = "{}Reached Threshold of {} ({} of {})".format
                self.qplog.info(m(
                    self.id_str,
                    complete_pct_str,
                    self.result_info.mr_tested,
                    self.result_info.estimated_total,
                ))

                if callbacks.get('AnswersComplete'):
                    callbacks['AnswersComplete'](self, new_pct)
                return True

            # check to see if override timeout is specified, if so and we have passed it, return
            # False
            if self.override_timeout and datetime.utcnow() >= self.override_timeout:
                m = "{}Reached override timeout of {}".format
                self.qplog.warning(m(self.id_str, self.override_timeout))
                return False

            # check to see if we have passed the actions expiration timeout, if so return False
            if datetime.utcnow() >= self.expiration_timeout:
                m = "{}Reached expiration timeout of {}".format
                self.qplog.warning(m(self.id_str, self.expiration_timeout))
                return False

            # if stop is called, return True
            if self._stop:
                m = "{}Stop called at {}".format
                self.qplog.info(m(self.id_str, new_pct_str))
                return False

            # update our class variables to the new values determined by this loop
            self.pct = new_pct
            self.previous_result_info = self.result_info

            time.sleep(self.polling_secs)
            self.loop_count += 1

    def stop(self):
        self._stop = True


class ActionPoller(QuestionPoller):
    """A class to poll the progress of an Action.

    The primary function of this class is to poll for result info for actions, and fire off events:

    ProgressChanged
    AnswersChanged
    AnswersComplete

    Parameters
    ----------
    handler : :class:`pytan.handler.Handler`
        PyTan handler to use for GetResultInfo calls
    obj : :class:`taniumpy.object_types.action.Action`
        object to poll for progress
    polling_secs : int, optional
        Number of seconds to wait in between GetResultInfo loops
    complete_pct : int/float, optional
        Percentage of mr_tested out of estimated_total to consider the action "done"
    override_timeout_secs : int, optional
        If supplied and not 0, timeout in seconds instead of when object expires
    """

    # valid types of objects that can be passed in as obj to __init__
    OBJECT_TYPE = taniumpy.object_types.action.Action
    COMPLETE_PCT = 100
    ACTION_DONE_KEY = 'success'
    RUNNING_STATUSES = ["active", "open"]

    qplog = logging.getLogger("pytan.handler.ActionPoller")
    qpplog = logging.getLogger("pytan.handler.ActionPoller.progress")

    def _post_init(self):
        """Post init class setup"""
        self._derive_package_spec()
        self._derive_target_group()
        self._derive_verify_enabled()
        self._derive_result_map()
        self._derive_expiration()
        self._derive_status()
        self._derive_stopped_flag()
        self._derive_info()

    def _derive_status(self):
        self.status = self._derive_attribute('status', None)

    def _derive_stopped_flag(self):
        self.stopped_flag = self._derive_attribute('stopped_flag', None)
        self.stopped_flag = bool(int(self.stopped_flag))

    def _derive_expiration(self):
        """Derive the expiration datetime string from a object

        Will generate a datetime string from self.EXPIRY_FALLBACK_SECS if unable to get the expiration from the object (self.obj) itself.
        """
        fallback = pytan.utils.seconds_from_now(self.EXPIRY_FALLBACK_SECS)
        self.expiration = self._derive_attribute('expiration_time', fallback)

    def _derive_package_spec(self):
        self.package_spec = self._derive_attribute('package_spec', None)

        # get the full package object associated with this action
        self.package_spec = self.handler._find(self.package_spec)

    def _derive_target_group(self):
        self.target_group = self._derive_attribute('target_group', None)

        # if the target group id is not 0, re-fetch the full group object
        if int(self.target_group.id) != 0:
            try:
                self.target_group = self.handler._find(self.target_group)
                self._fix_group(self.target_group)
                self.passed_count_reliable = True
            except:
                self.passed_count_reliable = False
                m = "{}Passed Count unreliable! Unable to find Actions Target Group: {}".format
                self.qplog.exception(m(self.id_str, self.target_group))

    def _fix_group(self, g):
        '''Sets ID to null on a group object and all of it's sub_groups, needed for 6.5'''
        g.id = None
        if g.sub_groups:
            for x in g.sub_groups:
                self._fix_group(x)

    def _derive_verify_enabled(self):
        self.verify_enabled = False
        if self.package_spec.verify_group_id:
            self.verify_enabled = True
        if self.package_spec.verify_group is not None and self.package_spec.verify_group.id:
            self.verify_enabled = True

    def _derive_result_map(self):
        """
        A package object has to have a verify_group defined on it in order
        for deploy action verification to trigger. That can be only done
        at package creation/update

        If verify_enable is True, then the various result states for an action change
        """
        if self.verify_enabled:
            finished = [
                'Verified.', 'Succeeded.', 'Expired.', 'Stopped.', 'NotSucceeded.', 'Failed.',
            ]
            success = [
                'Verified.',
            ]
            running = [
                'Completed.', 'PendingVerification.', 'Copying.', 'Waiting.', 'Downloading.',
                'Running.',
            ]
            failed = [
                'Expired.', 'Stopped.', 'NotSucceeded.', 'Failed.',
            ]
        else:
            finished = [
                'Verified.', 'Succeeded.', 'Completed.', 'Expired.', 'Stopped.', 'NotSucceeded.',
                'Failed.',
            ]
            success = [
                'Verified.', 'Completed.',
            ]
            running = [
                'PendingVerification.', 'Copying.', 'Waiting.', 'Downloading.', 'Running.',
            ]
            failed = [
                'Expired.', 'Stopped.', 'NotSucceeded.', 'Failed.',
            ]

        self.result_map = {
            'finished': {"{}:{}".format(self.obj.id, k): [] for k in finished},
            'success': {"{}:{}".format(self.obj.id, k): [] for k in success},
            'running': {"{}:{}".format(self.obj.id, k): [] for k in running},
            'failed': {"{}:{}".format(self.obj.id, k): [] for k in failed},
            'unknown': {},
        }
        for k, v in self.result_map.iteritems():
            v['total'] = 0

        m = "{}Result Map resolved to {}".format
        self.qplog.debug(m(self.id_str, self.result_map))

    def _derive_info(self):
        """Derive self.obj_info from self.obj"""
        m = "{}Package: '{}', Target: '{}', Verify: {}, Stopped: {}, Status: {}".format

        obj_info = m(
            self.id_str, self.package_spec.name, self.target_group.text, self.verify_enabled,
            self.stopped_flag, self.status,
        )

        m = "{}Object Info resolved to {}".format
        self.qplog.debug(m(self.id_str, obj_info))

        self.obj_info = obj_info

    def run(self, callbacks={}, **kwargs):
        """Poll for action data and issue callbacks.

        Parameters
        ----------
        callbacks : dict
            Callbacks should be a dict with any of these members:
            'ProgressChanged'
            'AnswersChanged'
            'AnswersComplete'

            Each callback should be a function that accepts a poller instance and a percent complete.

            Any callback can choose to get data from the session by calling poller.get_result_data() or new info by calling poller.get_result_info()

            Any callback can choose to stop the poller by calling poller.stop()

            Polling will be stopped only when one of the callbacks calls the stop() method or the answers are complete. Note that callbacks can call setPercentCompleteThreshold to change what "done" means on the fly
        """

        self.start = datetime.utcnow()
        self.expiration_timeout = pytan.utils.timestr_to_datetime(self.expiration)
        if self.override_timeout_secs:
            self.override_timeout = self.start + timedelta(seconds=self.override_timeout_secs)
        else:
            self.override_timeout = None

        m = "{}Adding Question to derive passed count".format
        self.qplog.debug(m(self.id_str, self.obj))

        self.pre_question = taniumpy.Question()
        self.pre_question.group = self.target_group
        self.pre_question = self.handler._add(self.pre_question)

        poller = pytan.pollers.QuestionPoller(self.handler, self.pre_question)
        poller.run()

        self.passed_count = poller.result_info.passed
        m = "{}Passed Count resolved to {}".format
        self.qplog.debug(m(self.id_str, self.passed_count))

        self.seen_eq_passed = self.seen_eq_passed_loop(callbacks, **kwargs)
        self.finished_eq_passed = self.finished_eq_passed_loop(callbacks, **kwargs)
        self.poller_result = all([self.seen_eq_passed, self.finished_eq_passed])
        return self.poller_result

    def seen_eq_passed_loop(self, callbacks={}, **kwargs):

        # number of systems that have SEEN the action
        self.seen_count = None
        # current percentage tracker
        self.seen_pct = None
        # loop counter
        self.seen_loop_count = 1
        # establish a previous result_info that's empty
        self.previous_result_info = taniumpy.object_types.result_info.ResultInfo()
        # establish a previous result_data that's empty
        self.previous_result_data = taniumpy.object_types.result_set.ResultSet()

        if self.passed_count == 0:
            m = "Passed Count of Clients for filter {} is 0 -- no clients match filter".format
            self.qplog.warning(m(self.target_group.text))
            return False

        while not self._stop:
            # perform a GetResultInfo SOAP call, this ensures fresh data is available for
            # GetResultData
            self.result_info = self.get_result_info(**kwargs)

            # get the aggregate resultdata
            self.result_data = self.get_result_data(aggregate=True, **kwargs)

            # add up the Count column for all rows
            # this count will equate to the number of systems that have started to process
            # this action in any way
            seen_count = sum([int(x['Count'][0]) for x in self.result_data.rows])

            # we use self.passed_count from the question we asked to get the number of matching
            # systems for determining the current pct of completion
            new_pct = pytan.utils.get_percentage(seen_count, self.passed_count)
            new_pct_str = "{0:.0f}%".format(new_pct)
            complete_pct_str = "{0:.0f}%".format(self.complete_pct)

            # print a progress debug string
            self.progress_str = (
                "Progress: Seen Action: {}, Expected Seen: {}, Percent: {}"
            ).format(seen_count, self.passed_count, new_pct_str)
            self.qplog.debug("{}{}".format(self.id_str, self.progress_str))

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
                self.seen_loop_count,
            )
            self.qplog.debug("{}{}".format(self.id_str, self.timing_str))

            # check to see if progress has changed, if so run the callback
            seen_changed = seen_count != self.seen_count
            pct_changed = self.seen_pct != new_pct
            progress_changed = any([seen_changed, pct_changed])

            if progress_changed:
                m = "{}Progress Changed for Seen Count {} ({} of {})".format
                self.qplog.info(m(self.id_str, new_pct_str, seen_count, self.passed_count))
                if callbacks.get('SeenProgressChanged'):
                    callbacks['SeenProgressChanged'](self, new_pct)

            # check to see if action is stopped, if it is, return False
            if self.stopped_flag:
                m = "{}Actions stopped flag is True".format
                self.qplog.warning(m(self.id_str))
                return False

            # check to see if action is not active, if it is not, False
            if self.status.lower() not in self.RUNNING_STATUSES:
                m = "{}Action status is {}, which is not one of: {}".format
                self.qplog.warning(m(self.id_str, self.status, ', '.join(self.RUNNING_STATUSES)))
                return False

            # check to see if new_pct has reached complete_pct threshold, if so return True
            if new_pct >= self.complete_pct:
                m = "{}Reached Threshold for Seen Count of {} ({} of {})".format
                self.qplog.info(m(self.id_str, complete_pct_str, seen_count, self.passed_count))

                if callbacks.get('SeenAnswersComplete'):
                    callbacks['SeenAnswersComplete'](self, new_pct)
                return True

            # check to see if override timeout is specified, if so and we have passed it, return
            # False
            if self.override_timeout and datetime.utcnow() >= self.override_timeout:
                m = "{}Reached override timeout of {}".format
                self.qplog.warning(m(self.id_str, self.override_timeout))
                return False

            # check to see if we have passed the actions expiration timeout, if so return False
            if datetime.utcnow() >= self.expiration_timeout:
                m = "{}Reached expiration timeout of {}".format
                self.qplog.warning(m(self.id_str, self.expiration))
                return False

            # if stop is called, return True
            if self._stop:
                m = "{}Stop called at {}".format
                self.qplog.info(m(self.id_str, new_pct_str))
                return True

            # update our class variables to the new values determined by this loop
            self.seen_pct = new_pct
            self.seen_count = seen_count
            self.previous_result_info = self.result_info
            self.previous_result_data = self.result_data

            time.sleep(self.polling_secs)
            self.seen_loop_count += 1

    def finished_eq_passed_loop(self, callbacks={}, **kwargs):

        # number of systems that have FINISHED the action
        self.finished_count = None
        # current percentage tracker
        self.finished_pct = None
        # loop counter
        self.loop_count = 1
        # establish a previous result_info that's empty
        self.previous_result_info = taniumpy.object_types.result_info.ResultInfo()
        # establish a previous result_data that's empty
        self.previous_result_data = taniumpy.object_types.result_set.ResultSet()

        while not self._stop:
            # perform a GetResultInfo SOAP call, this ensures fresh data is available for
            # GetResultData
            self.result_info = self.get_result_info(**kwargs)

            # get the NON aggregate resultdata
            self.result_data = self.get_result_data(**kwargs)

            '''
            for each row from the result data
            get the computer name and the action status for this row
            add the computer name to the appropriate action status in self.result_map
            '''
            for row in self.result_data.rows:
                action_status = row['Action Statuses'][0]
                comp_name = row['Computer Name'][0]
                known = False

                for s, smap in self.result_map.iteritems():
                    if action_status in smap:
                        known = True
                        if comp_name not in self.result_map[s][action_status]:
                            self.result_map[s][action_status].append(comp_name)

                if not known:
                    if action_status not in self.result_map['unknown']:
                        self.result_map['unknown'][action_status] = []

                    if comp_name not in self.result_map['unknown'][action_status]:
                        self.result_map['unknown'][action_status].append(comp_name)

                for s, smap in self.result_map.iteritems():
                    smap['total'] = sum([len(y) for x, y in smap.iteritems() if x != 'total'])

            # Use the total from the key defined in self.ACTION_DONE_KEY in self.result_map
            # this total will equate to the number of systems that have finished this action
            finished_count = self.result_map[self.ACTION_DONE_KEY]['total']

            # we use self.passed_count from the question we asked to get the number of matching
            # systems for determining the current pct of completion
            new_pct = pytan.utils.get_percentage(finished_count, self.passed_count)
            new_pct_str = "{0:.0f}%".format(new_pct)
            complete_pct_str = "{0:.0f}%".format(self.complete_pct)

            # print a progress debug string
            p = "{}: {}".format
            progress_list = [p(s, smap['total']) for s, smap in self.result_map.iteritems()]
            progress_list.append("Done Key: {}".format(self.ACTION_DONE_KEY))
            progress_list.append("Passed Count: {}".format(self.passed_count))
            self.progress_str = ', '.join(progress_list)
            self.qplog.debug("{}{}".format(self.id_str, self.progress_str))

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
            self.qplog.debug("{}{}".format(self.id_str, self.timing_str))

            # check to see if progress has changed, if so run the callback
            finished_changed = finished_count != self.finished_count
            pct_changed = self.finished_pct != new_pct
            progress_changed = any([finished_changed, pct_changed])

            if progress_changed:
                m = "{}Progress Changed for Finished Count {} ({} of {})".format
                self.qplog.info(m(self.id_str, new_pct_str, finished_count, self.passed_count))
                if callbacks.get('SeenProgressChanged'):
                    callbacks['SeenProgressChanged'](self, new_pct)

            # check to see if action is stopped, if it is, return False
            if self.stopped_flag:
                m = "{}Actions stopped flag is True".format
                self.qplog.warning(m(self.id_str))
                return False

            # check to see if action is not active, if it is not, False
            if self.status.lower() not in self.RUNNING_STATUSES:
                m = "{}Action status is {}, which is not one of: {}".format
                self.qplog.warning(m(self.id_str, self.status, ', '.join(self.RUNNING_STATUSES)))
                return False

            # check to see if new_pct has reached complete_pct threshold, if so return True
            if new_pct >= self.complete_pct:
                m = "{}Reached Threshold for Finished Count of {} ({} of {})".format
                self.qplog.info(
                    m(self.id_str, complete_pct_str, finished_count, self.passed_count)
                )

                if callbacks.get('SeenAnswersComplete'):
                    callbacks['SeenAnswersComplete'](self, new_pct)
                return True

            # check to see if override timeout is specified, if so and we have passed it, return
            # False
            if self.override_timeout and datetime.utcnow() >= self.override_timeout:
                m = "{}Reached override timeout of {}".format
                self.qplog.warning(m(self.id_str, self.override_timeout))
                return False

            # check to see if we have passed the actions expiration timeout, if so return False
            if datetime.utcnow() >= self.expiration_timeout:
                m = "{}Reached expiration timeout of {}".format
                self.qplog.warning(m(self.id_str, self.expiration))
                return False

            # if stop is called, return True
            if self._stop:
                m = "{}Stop called at {}".format
                self.qplog.info(m(self.id_str, new_pct_str))
                return True

            # update our class variables to the new values determined by this loop
            self.finished_pct = new_pct
            self.finished_count = finished_count
            self.previous_result_info = self.result_info
            self.previous_result_data = self.result_data

            time.sleep(self.polling_secs)
            self.loop_count += 1
