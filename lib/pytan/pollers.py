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

qplog = logging.getLogger("pytan.handler.question_poller")


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

    def __init__(self, handler, obj, override_timeout_secs=0, **kwargs):

        if not isinstance(handler, pytan.handler.Handler):
            m = "{} is not a valid handler instance! Must be a: {!r}".format
            raise pytan.exceptions.PollingError(m(type(handler), pytan.handler.Handler))

        if not isinstance(obj, self.OBJECT_TYPE):
            m = "{} is not a valid object type! Must be a: {}".format
            raise pytan.exceptions.PollingError(m(type(handler), self.OBJECT_TYPE))

        self.handler = handler
        self.obj = obj
        self.polling_secs = kwargs.get('polling_secs', self.POLLING_SECS)
        self.complete_pct = kwargs.get('complete_pct', self.COMPLETE_PCT)
        self.override_timeout_secs = override_timeout_secs
        self.result_info = None
        self._stop = False
        self._post_init()

    def __str__(self):
        class_name = self.__class__.__name__
        attrs = ", ".join(["{0}: {0}".format(getattr(self, x, None)) for x in self.STR_ATTRS])
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
        obj = self.handler.session.find(self.obj)
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

        Returns
        -------
        val : perspective
            The value of the attr from self.obj

        """
        val = getattr(self.obj, attr, '')

        # if attr isn't available on the object, maybe it's only a partial object
        # let's use the handler to re-fetch it
        if not val:
            m = "{} not available on {}, re-fetching object".format
            qplog.debug(m(attr, self.obj))
            self._refetch_obj()

        val = getattr(self.obj, attr, '')
        if not val:
            m = (
                "{} not available on {}, even after re-fetching object - using fallback {} of {}"
            ).format
            qplog.debug(m(attr, self.obj, attr, fallback))
            val = fallback
        return val

    def _derive_info(self):
        """Derive the self.obj_info from self.obj"""
        question_text = self._derive_attribute('query_text', 'Unable to fetch question text')
        question_id = self._derive_attribute('id', -1)
        obj_info = "Question ID: {}, Query: {}".format(question_id, question_text)

        m = "Object Info of {} resolved to {}".format
        qplog.debug(m(self.obj, obj_info))
        self.obj_info = obj_info

    def _derive_expiration(self):
        """Derive the expiration datetime string from a object

        Will generate a datetime string from self.EXPIRY_FALLBACK_SECS if unable to get the expiration from the object (self.obj) itself.
        """
        fallback = pytan.utils.seconds_from_now(self.EXPIRY_FALLBACK_SECS)
        expiration = self._derive_attribute('expiration', fallback)

        m = "Expiration of {} resolved to {}".format
        qplog.debug(m(self.obj, expiration))
        self.expiration = expiration

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
        return self.handler.get_result_info(self.obj, **kwargs)

    def get_result_data(self, **kwargs):
        """Simple utility wrapper around handler.get_result_data()"""
        return self.handler.get_result_data(self.obj, **kwargs)

    def run(self, callbacks={}, **kwargs):
        """Poll for question data and issue callbacks.

        Parameters
        ----------
        callbacks : dict
            Callbacks should be a dict with members:
            'ProgressChanged'
            'AnswersChanged'
            'AnswersComplete'

            Each should be a function that accepts a QuestionPoller instance and a percent complete.

            Any callback can choose to get data from the session by calling asker.get_result_data()

            Polling will be stopped only when one of the callbacks calls the stop() method or the answers are complete. Note that callbacks can call setPercentCompleteThreshold to change what done means on the fly
        """
        tested = None
        passed = None
        mr_tested = None
        mr_passed = None
        estimated_total = None
        pct = None

        start = datetime.utcnow()

        override_timeout = None
        if self.override_timeout_secs:
            override_timeout = start + timedelta(seconds=self.override_timeout_secs)

        expiration_timeout = pytan.utils.timestr_to_datetime(self.expiration)
        loop_count = 1

        while not self._stop:
            now = datetime.utcnow()
            elapsed = now - start

            if override_timeout:
                time_till_expiry = override_timeout - now
            else:
                time_till_expiry = expiration_timeout - now

            # perform a GetResultInfo SOAP call
            self.result_info = self.get_result_info(**kwargs)

            # mr_tested is the number of machines that have "seen" the question
            tested_pct = self.result_info.mr_tested * 100

            # estimated_total is the number of machines that could see the question
            estimated_total_pct = self.result_info.estimated_total + .01

            # derive the current percentage of completion
            new_pct = tested_pct / estimated_total_pct

            # store a number of tests to check timeouts/changes/progress
            tested_changed = tested != self.result_info.tested
            passed_changed = passed != self.result_info.passed
            mr_tested_changed = mr_tested != self.result_info.mr_tested
            mr_passed_changed = mr_passed != self.result_info.mr_passed
            est_total_changed = estimated_total != self.result_info.estimated_total
            pct_changed = pct != new_pct
            threshold_reached = new_pct >= self.complete_pct
            override_timeout_reached = override_timeout and now >= override_timeout
            expiration_timeout_reached = now >= expiration_timeout

            progress_changed = any([
                tested_changed, passed_changed, mr_tested_changed, mr_passed_changed,
                est_total_changed, pct_changed,
            ])

            answers_changed = any([tested_changed, passed_changed])

            progress_str = (
                "{0} Progress: Tested: {1.tested}, Passed: {1.passed}, "
                "MR Tested: {1.mr_tested}, MR Passed: {1.mr_passed}, "
                "Est Total: {1.estimated_total}, Row Count: {1.row_count}"
            ).format(self.obj_info, self.result_info)

            timing_str = (
                "{} Timing: Started: {}, Expiration: {}, Override Timeout: {}, "
                "Elapsed Time: {}, Left till expiry: {}, Loop Count: {}"
            ).format(
                self.obj_info,
                start,
                expiration_timeout,
                override_timeout,
                elapsed,
                time_till_expiry,
                loop_count,
            )

            qplog.debug(progress_str)
            qplog.debug(timing_str)

            if progress_changed:
                m = "Progress Changed {0:.0f}% ({1.mr_tested} of {1.estimated_total}) ({2})".format
                qplog.info(m(new_pct, self.result_info, self.obj_info))
                if callbacks.get('ProgressChanged'):
                    callbacks['ProgressChanged'](self, new_pct)

            if answers_changed:
                if callbacks.get('AnswersChanged'):
                    callbacks['AnswersChanged'](self, new_pct)

            if threshold_reached:
                m = (
                    "Reached Threshold of {0:.0f}% ({1.mr_tested} of {1.estimated_total}) ({2})"
                ).format
                qplog.info(m(self.complete_pct, self.result_info, self.obj_info))

                if callbacks.get('AnswersComplete'):
                    callbacks['AnswersComplete'](self, new_pct)
                return

            if override_timeout_reached:
                timeout_str = pytan.utils.datetime_to_timestr(override_timeout)
                m = "Reached override timeout of {} -- {}".format
                raise pytan.exceptions.TimeoutException(m(timeout_str, progress_str))

            if expiration_timeout_reached:
                m = "Reached expiration timeout of {} seconds -- {}".format
                raise pytan.exceptions.TimeoutException(m(self.expiration, progress_str))

            pct = new_pct
            tested = self.result_info.tested
            passed = self.result_info.passed
            mr_tested = self.result_info.mr_tested
            mr_passed = self.result_info.mr_passed

            if self._stop:
                m = "Stop called at {0:.0f}% ({1})".format
                qplog.info(m(new_pct, self.obj_info))
                return

            time.sleep(self.polling_secs)
            loop_count += 1

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

    def run(self, callbacks={}, **kwargs):
        """Poll for action data and issue callbacks.

        Parameters
        ----------
        callbacks : dict
            Callbacks should be a dict with members:
            'ProgressChanged'
            'AnswersChanged'
            'AnswersComplete'

            Each should be a function that accepts a QuestionPoller instance and a percent complete.

            Any callback can choose to get data from the session by calling asker.get_result_data()

            Polling will be stopped only when one of the callbacks calls the stop() method or the answers are complete. Note that callbacks can call setPercentCompleteThreshold to change what done means on the fly

        check expiration of action (is it closed? does that matter?)
        get group = target_group_id
        ask question with group
        use # from RI.passed as check for complete


        """

    def deploy_action_asker(self, action_id, passed_count=0):
        if passed_count == 0:
            passed_base = (100.0 / float(1))
        else:
            passed_base = (100.0 / float(passed_count))

        action_obj = self.get('action', id=action_id)[0]

        ps = action_obj.package_spec
        """
        A package_spec has to have a verify_group defined on it in order
        for deploy action verification to trigger. That can be only done
        at package_spec create or update time
        """
        if ps.verify_group or ps.verify_group_id:
            m = "Setting up 'finished' for verify"
            finished_keys = ['done', 'verify_done']
            success_keys = ['verify_done']
            running_keys = ['running', 'verify_running']
            failed_keys = ['failed']
        else:
            m = "Setting up 'finished' for no_verify"
            finished_keys = ['done', 'no_verify_done']
            success_keys = ['no_verify_done']
            running_keys = ['running']
            failed_keys = ['failed']

        qplog.debug(m)
        finished_keys = pytan.utils.get_dict_list_items(
            pytan.constants.ACTION_RESULT_STATUS, finished_keys)
        success_keys = pytan.utils.get_dict_list_items(
            pytan.constants.ACTION_RESULT_STATUS, success_keys)
        running_keys = pytan.utils.get_dict_list_items(
            pytan.constants.ACTION_RESULT_STATUS, running_keys)
        failed_keys = pytan.utils.get_dict_list_items(
            pytan.constants.ACTION_RESULT_STATUS, failed_keys)

        passed_count_reached = False
        finished = False
        while not passed_count_reached or not finished:
            m = "Deploy Action Asker loop for {!r}: {}".format
            qplog.debug(m(action_obj.name, pytan.utils.seconds_from_now(0, '')))

            if not passed_count_reached:
                # do a getresultinfo to ensure fresh data is available for
                # getresultdata
                self.get_result_info(action_obj)

                # get the aggregate resultdata
                rd = self.get_result_data(action_obj, True)

                current_passed = sum([int(x['Count'][0]) for x in rd.rows])
                passed_pct = current_passed * passed_base

                m = (
                    "Deploy Action {} Current Passed: {}, Expected Passed: {}"
                ).format
                qplog.debug(m(action_obj.name, current_passed, passed_count))

                m = "Action Results Passed: {1:.0f}% ({0})".format
                qplog.info(m(action_obj.name, passed_pct))

                # if current_passed matches passed_count, then set
                # passed_count_reached = True
                if current_passed >= passed_count:
                    passed_count_reached = True

                if not passed_count_reached:
                    time.sleep(1)
                    continue

            # if passed_count was reached (the sum of Count from all rows from
            # the aggregate getresultdata is the same or greater as the number
            # of servers that matched the pre-action question), determine
            # if all servers have "finished"

            # do a getresultinfo to ensure fresh data is available for
            # getresultdata
            self.get_result_info(action_obj)

            # get the full resultdata
            rd = self.get_result_data(action_obj, False)

            # create a dictionary to hold action statuses and the
            # computer names for each action status
            as_map = {}

            for row in rd.rows:
                computer_name = row['Computer Name'][0]
                action_status = row['Action Statuses'][0]
                action_status = action_status.split(':')[1]
                if action_status not in as_map:
                    as_map[action_status] = []
                as_map[action_status].append(computer_name)

            total_count = pytan.utils.get_dict_list_len(as_map)
            finished_count = pytan.utils.get_dict_list_len(as_map, finished_keys)
            success_count = pytan.utils.get_dict_list_len(as_map, success_keys)
            running_count = pytan.utils.get_dict_list_len(as_map, running_keys)
            failed_count = pytan.utils.get_dict_list_len(as_map, failed_keys)
            unknown_count = pytan.utils.get_dict_list_len(
                as_map, pytan.constants.ACTION_RESULT_STATUS, True)

            finished_pct = finished_count * passed_base

            m = "Action Results Completed: {1:.0f}% ({0})".format
            qplog.info(m(action_obj.name, finished_pct))

            progress = (
                "{} Result Counts:\n"
                "\tRunning Count: {}\n"
                "\tSuccess Count: {}\n"
                "\tFailed Count: {}\n"
                "\tUnknown Count: {}\n"
                "\tFinished Count: {}\n"
                "\tTotal Count: {}\n"
                "\tFinished Count must equal: {}"
            ).format(
                action_obj.name,
                running_count,
                success_count,
                failed_count,
                unknown_count,
                finished_count,
                total_count,
                passed_count,
            )

            if finished_count >= passed_count:
                qplog.info(progress)
                finished = True
                break

            qplog.debug(progress)
            time.sleep(1)

        ret = {
            'action_object': action_obj,
            'action_results': rd,
            'action_progress_human': progress,
            'action_progress_map': as_map,
        }

        return ret
