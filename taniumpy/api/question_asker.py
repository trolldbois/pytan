import time


class QuestionTimeoutException(Exception):
    pass

class QuestionAsker(object):
    """A class to aid in asking a Question.

    The primary function of this class is to poll for
    result info for question, and fire off events:

    ProgressChanged
    AnswersChanged
    AnswersComplete

    """

    POLLING_INTERVAL = 5

    def __init__(self, session,
            question,
            polling_interval=None,
            pct_complete_threshold=99,
            timeout=300):
        self.session = session
        self.question = question
        self._polling_interval = polling_interval or self.POLLING_INTERVAL
        self.pct_complete_threshold = pct_complete_threshold
        self._timeout = timeout
        self.result_info = None
        self._stop = False

    def setPctCompleteThreshold(self, val):
        self.pct_complete_threshold = val

    def run(self, callbacks={}):
        """Poll for question data and issue callbacks.

        Callbacks should be a dict with members:
        'ProgressChanged'
        'AnswersChanged'
        'AnswersComplete'

        Each should be a function that accepts a QuestionAsker
        and a percent complete.

        Any callback can choose to get data from the session
        by calling asker.session.getResultData(asker.question)

        Polling will be stopped only when one of the callbacks
        calls the stop() method or the answers are complete. Note
        that callbacks can call setPercentCompleteThreshold to
        change what done means on the fly

        """
        tested = None
        passed = None
        mr_tested = None
        mr_passed = None
        estimated_total = None
        pct = None

        start = time.time()
        while not self._stop:
            if time.time() - start > self._timeout:
                 raise QuestionTimeoutException()
            result_info = self.session.getResultInfo(self.question)
            new_pct = (result_info.mr_tested * 100) / (result_info.estimated_total + .01)
            if callbacks.get('ProgressChanged') and \
                    (tested != result_info.tested or \
                    passed != result_info.passed or \
                    mr_tested != result_info.mr_tested or \
                    mr_passed != result_info.mr_passed or \
                    estimated_total != result_info.estimated_total or \
                    pct != new_pct):
                callbacks['ProgressChanged'](self, new_pct)
            pct = new_pct
            if callbacks.get('AnswersChanged') and ( \
                    tested != result_info.tested or \
                    passed != result_info.passed):
                callbacks['AnswersChanged'](self, new_pct)
            if pct > self.pct_complete_threshold:
                if callbacks.get('AnswersComplete'):
                    callbacks['AnswersComplete'](self, new_pct)
                return
            tested = result_info.tested
            passed = result_info.passed
            mr_tested = result_info.mr_tested
            mr_passed = result_info.mr_passed
            if not self._stop:
                time.sleep(self._polling_interval)

    def stop(self):
        self._stop = True
