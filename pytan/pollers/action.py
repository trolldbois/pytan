#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Action Poller for :mod:`pytan`"""

import logging
import time
from datetime import datetime
from datetime import timedelta

from . import question
from .. import utils
from .. import tanium_ng

mylog = logging.getLogger(__name__)
progresslog = logging.getLogger(__name__ + ".progress")
resolverlog = logging.getLogger(__name__ + ".resolver")


class ActionPoller(question.QuestionPoller):
    """A class to poll the progress of an Action.

    The primary function of this class is to poll for result info for an action, and fire off events:
        * 'SeenProgressChanged'
        * 'SeenAnswersComplete'
        * 'FinishedProgressChanged'
        * 'FinishedAnswersComplete'

    Parameters
    ----------
    handler : :class:`handler.Handler`
        * PyTan handler to use for GetResultInfo calls
    obj : :class:`tanium_ng.Action`
        * object to poll for progress
    polling_secs : int, optional
        * default: 5
        * Number of seconds to wait in between GetResultInfo loops
    complete_pct : int/float, optional
        * default: 100
        * Percentage of passed_count out of successfully run actions to consider the action "done"
    override_timeout_secs : int, optional
        * default: 0
        * If supplied and not 0, timeout in seconds instead of when object expires
    override_passed_count : int, optional
        * instead of getting number of systems that should run this action by asking a question, use this number
    """

    OBJECT_TYPE = tanium_ng.Action
    """valid type of object that can be passed in as obj to __init__"""

    COMPLETE_PCT_DEFAULT = utils.constants.A_COMPLETE_PCT_DEFAULT
    """default value for self.complete_pct"""

    ACTION_DONE_KEY = utils.constants.A_ACTION_DONE_KEY
    """key in action_result_map that maps to an action being done"""

    RUNNING_STATUSES = utils.constants.A_RUNNING_STATUSES
    """values for status attribute of action object that mean the action is running"""

    EXPIRATION_ATTR = utils.constants.A_EXPIRATION_ATTR
    """attribute of self.obj that contains the expiration for this object"""

    def setup_logging(self):
        """Setup loggers for this object"""
        self.mylog = mylog
        self.progresslog = progresslog
        self.resolverlog = resolverlog

    def _post_init(self, **kwargs):
        """Post init class setup"""
        self.override_passed_count = kwargs.get('override_passed_count', 0)
        self._derive_package_spec(**kwargs)
        self._derive_target_group(**kwargs)
        self._derive_verify_enabled(**kwargs)
        self._derive_result_map(**kwargs)
        self._derive_expiration(**kwargs)
        self._derive_status(**kwargs)
        self._derive_stopped_flag(**kwargs)
        self._derive_object_info(**kwargs)

    def _derive_status(self, **kwargs):
        """Get the status attribute for self.obj"""
        clean_keys = ['attr', 'fallback']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        attr_name = 'status'
        fb = None
        self.status = self._derive_attribute(attr=attr_name, fallback=fb, **clean_kwargs)

    def _derive_stopped_flag(self, **kwargs):
        """Get the stopped_flag attribute for self.obj"""
        clean_keys = ['attr', 'fallback']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        attr_name = 'stopped_flag'
        fb = None
        self.stopped_flag = self._derive_attribute(attr=attr_name, fallback=fb, **clean_kwargs)
        self.stopped_flag = int(self.stopped_flag)
        self.stopped_flag = bool(self.stopped_flag)

    def _derive_package_spec(self, **kwargs):
        """Get the package_spec attribute for self.obj, then fetch the full package_spec object"""
        clean_keys = ['attr', 'fallback', 'obj']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        attr_name = 'package_spec'
        fb = None
        self.package_spec = self._derive_attribute(attr=attr_name, fallback=fb, **clean_kwargs)

        # get the full package object associated with this action
        h = "Issue a GetObject on the package for an action to get the full object"
        clean_kwargs['pytan_help'] = h
        self.package_spec = self.handler._find(obj=self.package_spec, **clean_kwargs)

    def _derive_target_group(self, **kwargs):
        """Get the target_group attribute for self.obj, then fetch the full group object"""
        clean_keys = ['attr', 'fallback', 'obj']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        attr_name = 'target_group'
        fb = None
        self.target_group = self._derive_attribute(attr=attr_name, fallback=fb, **clean_kwargs)

        # if the target group id is not 0, re-fetch the full group object
        if int(self.target_group.id) != 0:
            h = (
                "Issue a GetObject on the target_group for an action to get the full Group "
                "object"
            )
            clean_kwargs['pytan_help'] = h
            try:
                self.target_group = self.handler._find(obj=self.target_group, **clean_kwargs)
                self._fix_group(g=self.target_group)
                self.passed_count_reliable = True
            except:
                self.passed_count_reliable = False
                m = "{}Passed Count unreliable! Unable to find Actions Target Group: {}".format
                self.mylog.exception(m(self.id_str, self.target_group))

    def _fix_group(self, g, **kwargs):
        """Sets ID to null on a group object and all of it's sub_groups, needed for 6.5"""
        g.id = None
        if g.sub_groups:
            for x in g.sub_groups:
                self._fix_group(g=x)

    def _derive_verify_enabled(self, **kwargs):
        """Determine if this action has verification enabled"""
        self.verify_enabled = False
        package_spec = getattr(self, 'package_spec', None)
        ps_verify_group_id = getattr(package_spec, 'verify_group_id', None)
        vg = getattr(package_spec, 'verify_group', None)
        vg_id = getattr(vg, 'id', None)
        if ps_verify_group_id or vg_id:
            self.verify_enabled = True

    def _derive_result_map(self, **kwargs):
        """Determine what self.result_map should contain for the various statuses an action can have

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
        for k, v in self.result_map.items():
            v['total'] = 0

        m = "{}Result Map resolved to {}".format
        self.resolverlog.debug(m(self.id_str, self.result_map))

    def _derive_object_info(self, **kwargs):
        """Derive self.object_info from self.obj"""
        m = "{}Package: '{}', Target: '{}', Verify: {}, Stopped: {}, Status: {}".format

        object_info = m(
            self.id_str, self.package_spec.name, self.target_group.text, self.verify_enabled,
            self.stopped_flag, self.status,
        )

        m = "{}Object Info resolved to {}".format
        self.resolverlog.debug(m(self.id_str, object_info))

        self.object_info = object_info

    def run(self, callbacks={}, **kwargs):
        """Poll for action data and issue callbacks.

        Parameters
        ----------
        callbacks : dict
            * Callbacks should be a dict with any of these members:
                * 'SeenProgressChanged'
                * 'SeenAnswersComplete'
                * 'FinishedProgressChanged'
                * 'FinishedAnswersComplete'

            * Each callback should be a function that accepts:
                * 'poller': a poller instance
                * 'pct': a percent complete
                * 'kwargs': a dict of other args

        Notes
        -----
            * Any callback can choose to get data from the session by calling :func:`pytan.poller.QuestionPoller.get_result_data` or new info by calling :func:`pytan.poller.QuestionPoller.get_result_info`
            * Any callback can choose to stop the poller by calling :func:`pytan.poller.QuestionPoller.stop`
            * Polling will be stopped only when one of the callbacks calls the :func:`pytan.poller.QuestionPoller.stop` method or the answers are complete.
            * Any callbacks can call :func:`pytan.poller.QuestionPoller.setPercentCompleteThreshold` to change what "done" means on the fly
        """
        self.start = datetime.utcnow()
        self.expiration_timeout = utils.calc.timestr_to_datetime(timestr=self.expiration)

        if self.override_timeout_secs:
            td_obj = timedelta(seconds=self.override_timeout_secs)
            self.override_timeout = self.start + td_obj
        else:
            self.override_timeout = None

        clean_keys = ['callbacks', 'obj', 'pytan_help', 'handler']
        clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

        if self.override_passed_count:
            self.passed_count = self.override_passed_count
            m = "{}passed_count resolved override of {}".format
            self.mylog.debug(m(self.id_str, self.override_passed_count))
        else:
            m = (
                "{}Issuing an AddObject of a Question object with no Selects and the same Group "
                "used by the Action object. The number of systems that should successfully run "
                "the Action will be taken from result_info.passed_count for the Question asked "
                "when all answers for the question have reported in."
            ).format
            self.mylog.debug(m(self.id_str, self.obj))

            self.pre_question = tanium_ng.Question()
            self.pre_question.group = self.target_group
            self.pre_question = self.handler._add(
                obj=self.pre_question, pytan_help=m(self.id_str, self.obj), **clean_kwargs
            )

            self.pre_question_poller = question.QuestionPoller(
                handler=self.handler, obj=self.pre_question, **clean_kwargs
            )

            self.pre_question_poller.run(callbacks=callbacks, **clean_kwargs)

            self.passed_count = self.pre_question_poller.result_info.passed

            m = "{}passed_count resolved to {}".format
            self.mylog.debug(m(self.id_str, self.passed_count))

        self.seen_eq_passed = self.seen_eq_passed_loop(callbacks=callbacks, **clean_kwargs)
        self.finished_eq_passed = self.finished_eq_passed_loop(callbacks=callbacks, **clean_kwargs)
        self.poller_result = all([self.seen_eq_passed, self.finished_eq_passed])
        return self.poller_result

    def seen_eq_passed_loop(self, callbacks={}, **kwargs):
        """Method to poll Result Info for self.obj until the percentage of 'seen_count' out of 'self.passed_count' is greater than or equal to self.complete_pct

        * seen_count is calculated from an aggregate GetResultData
        * self.passed_count is calculated by the question asked before this method is called. that question has no selects, but has a group that is the same group as the action for this object
        """
        # number of systems that have SEEN the action
        self.seen_count = None
        # current percentage tracker
        self.seen_pct = None
        # loop counter
        self.seen_loop_count = 1
        # establish a previous result_info that's empty
        self.previous_result_info = tanium_ng.ResultInfo()
        # establish a previous result_data that's empty
        self.previous_result_data = tanium_ng.ResultSet()

        if self.passed_count == 0:
            m = "Passed Count of Clients for filter {} is 0 -- no clients match filter".format
            self.mylog.warning(m(self.target_group.text))
            return False

        while not self._stop:
            clean_keys = ['pytan_help', 'aggregate', 'callback', 'pct']
            clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

            # re-fetch object and re-derive stopped flag and status
            h = (
                "Issue a GetObject for an Action in order to have access to the latest values for "
                "stopped_flag and status"
            )
            self._refetch_obj(pytan_help=h, **clean_kwargs)
            self._derive_stopped_flag(**clean_kwargs)
            self._derive_status(**clean_kwargs)

            # perform a GetResultInfo SOAP call, this ensures fresh data is available for
            # GetResultData
            h = (
                "Issue a GetResultInfo for an Action to ensure fresh data is available for a "
                "GetResultData call"
            )
            self.result_info = self.get_result_info(pytan_help=h, **clean_kwargs)

            # get the aggregate resultdata
            h = (
                "Issue a GetResultData with the aggregate option set to True."
                "This will return row counts of machines that have answered instead of"
                " all the data"
            )
            self.result_data = self.get_result_data(aggregate=True, pytan_help=h, **clean_kwargs)

            # add up the Count column for all rows
            # this count will equate to the number of systems that have started to process
            # this action in any way
            seen_count = sum([int(x['Count'][0]) for x in self.result_data.rows])

            # we use self.passed_count from the question we asked to get the number of matching
            # systems for determining the current pct of completion
            new_pct = utils.calc.get_percent(base=seen_count, amount=self.passed_count)
            new_pct_str = "{0:.0f}%".format(new_pct)
            complete_pct_str = "{0:.0f}%".format(self.complete_pct)

            # print a progress debug string
            self.progress_str = (
                "Progress: Seen Action: {}, Expected Seen: {}, Percent: {}"
            ).format(seen_count, self.passed_count, new_pct_str)
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
                self.seen_loop_count,
            )
            self.progresslog.debug("{}{}".format(self.id_str, self.timing_str))

            # check to see if progress has changed, if so run the callback
            seen_changed = seen_count != self.seen_count
            pct_changed = self.seen_pct != new_pct
            progress_changed = any([seen_changed, pct_changed])

            if progress_changed:
                m = "{}Progress Changed for Seen Count {} ({} of {})".format
                self.progresslog.info(m(self.id_str, new_pct_str, seen_count, self.passed_count))
                cb = 'SeenProgressChanged'
                self.run_callback(callbacks=callbacks, callback=cb, pct=new_pct, **clean_kwargs)

            # check to see if new_pct has reached complete_pct threshold, if so return True
            if new_pct >= self.complete_pct:
                m = "{}Reached Threshold for Seen Count of {} ({} of {})".format
                m = m(self.id_str, complete_pct_str, seen_count, self.passed_count)
                self.mylog.info(m)
                cb = 'SeenAnswersComplete'
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
                self.mylog.warning(m(self.id_str, self.expiration))
                return False

            # check to see if action is stopped, if it is, return False
            if self.stopped_flag:
                m = "{}Actions stopped flag is True".format
                self.mylog.warning(m(self.id_str))
                return False

            # check to see if action is not active, if it is not, False
            if self.status.lower() not in self.RUNNING_STATUSES:
                m = "{}Action status is {}, which is not one of: {}".format
                m = m(self.id_str, self.status, ', '.join(self.RUNNING_STATUSES))
                self.mylog.warning(m)
                return False

            # if stop is called, return True
            if self._stop:
                m = "{}Stop called at {}".format
                self.mylog.info(m(self.id_str, new_pct_str))
                return True

            # update our class variables to the new values determined by this loop
            self.seen_pct = new_pct
            self.seen_count = seen_count
            self.previous_result_info = self.result_info
            self.previous_result_data = self.result_data

            time.sleep(self.polling_secs)
            self.seen_loop_count += 1

    def finished_eq_passed_loop(self, callbacks={}, **kwargs):
        """Method to poll Result Info for self.obj until the percentage of 'finished_count' out of 'self.passed_count' is greater than or equal to self.complete_pct

        * finished_count is calculated from a full GetResultData call that is parsed into self.action_result_map
        * self.passed_count is calculated by the question asked before this method is called. that question has no selects, but has a group that is the same group as the action for this object
        """
        # number of systems that have FINISHED the action
        self.finished_count = None
        # current percentage tracker
        self.finished_pct = None
        # loop counter
        self.loop_count = 1
        # establish a previous result_info that's empty
        self.previous_result_info = tanium_ng.ResultInfo()
        # establish a previous result_data that's empty
        self.previous_result_data = tanium_ng.ResultSet()

        while not self._stop:
            clean_keys = ['pytan_help', 'aggregate', 'callback', 'pct']
            clean_kwargs = utils.validate.clean_kwargs(kwargs=kwargs, keys=clean_keys)

            # re-fetch object and re-derive stopped flag and status
            h = (
                "Issue a GetObject for an Action in order to have access to the latest values for "
                "stopped_flag and status"
            )
            self._refetch_obj(pytan_help=h, **clean_kwargs)
            self._derive_stopped_flag(**clean_kwargs)
            self._derive_status(**clean_kwargs)

            # perform a GetResultInfo SOAP call, this ensures fresh data is available for
            # GetResultData
            h = (
                "Issue a GetResultInfo for an Action to ensure fresh data is available for a "
                "GetResultData call"
            )
            self.result_info = self.get_result_info(pytan_help=h, **clean_kwargs)

            # get the NON aggregate resultdata
            h = (
                "Issue a GetResultData for an Action with the aggregate option set to False. "
                "This will return all of the Action Statuses for each computer that have run this "
                "Action"
            )
            self.result_data = self.get_result_data(aggregate=False, pytan_help=h, **clean_kwargs)

            """
            for each row from the result data
            get the computer name and the action status for this row
            add the computer name to the appropriate action status in self.result_map
            """
            for row in self.result_data.rows:
                action_status = row['Action Statuses'][0]
                comp_name = row['Computer Name'][0]
                known = False

                for s, smap in self.result_map.items():
                    if action_status in smap:
                        known = True
                        if comp_name not in self.result_map[s][action_status]:
                            self.result_map[s][action_status].append(comp_name)

                if not known:
                    if action_status not in self.result_map['unknown']:
                        self.result_map['unknown'][action_status] = []

                    if comp_name not in self.result_map['unknown'][action_status]:
                        self.result_map['unknown'][action_status].append(comp_name)

                for s, smap in self.result_map.items():
                    smap['total'] = sum([len(y) for x, y in smap.items() if x != 'total'])

            # Use the total from the key defined in self.ACTION_DONE_KEY in self.result_map
            # this total will equate to the number of systems that have finished this action
            finished_count = self.result_map[self.ACTION_DONE_KEY]['total']

            # we use self.passed_count from the question we asked to get the number of matching
            # systems for determining the current pct of completion
            new_pct = utils.calc.get_percent(base=finished_count, amount=self.passed_count)
            new_pct_str = "{0:.0f}%".format(new_pct)
            complete_pct_str = "{0:.0f}%".format(self.complete_pct)

            # print a progress debug string
            p = "{}: {}".format
            progress_list = [p(s, smap['total']) for s, smap in self.result_map.items()]
            progress_list.append("Done Key: {}".format(self.ACTION_DONE_KEY))
            progress_list.append("Passed Count: {}".format(self.passed_count))
            self.progress_str = ', '.join(progress_list)
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
            finished_changed = finished_count != self.finished_count
            pct_changed = self.finished_pct != new_pct
            progress_changed = any([finished_changed, pct_changed])

            if progress_changed:
                m = "{}Progress Changed for Finished Count {} ({} of {})".format
                m = m(self.id_str, new_pct_str, finished_count, self.passed_count)
                self.progresslog.info(m)
                cb = 'FinishedProgressChanged'
                self.run_callback(callbacks=callbacks, callback=cb, pct=new_pct, **clean_kwargs)

            # check to see if new_pct has reached complete_pct threshold, if so return True
            if new_pct >= self.complete_pct:
                m = "{}Reached Threshold for Finished Count of {} ({} of {})".format
                m = m(self.id_str, complete_pct_str, finished_count, self.passed_count)
                self.mylog.info(m)
                cb = 'FinishedAnswersComplete'
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
                self.mylog.warning(m(self.id_str, self.expiration))
                return False

            # check to see if action is stopped, if it is, return False
            if self.stopped_flag:
                m = "{}Actions stopped flag is True".format
                self.mylog.warning(m(self.id_str))
                return False

            # check to see if action is not active, if it is not, False
            if self.status.lower() not in self.RUNNING_STATUSES:
                m = "{}Action status is {}, which is not one of: {}".format
                m = m(self.id_str, self.status, ', '.join(self.RUNNING_STATUSES))
                self.mylog.warning(m)
                return False

            # if stop is called, return True
            if self._stop:
                m = "{}Stop called at {}".format
                self.mylog.info(m(self.id_str, new_pct_str))
                return True

            # update our class variables to the new values determined by this loop
            self.finished_pct = new_pct
            self.finished_count = finished_count
            self.previous_result_info = self.result_info
            self.previous_result_data = self.result_data

            time.sleep(self.polling_secs)
            self.loop_count += 1
