
taniumpy.question_asker module
******************************

**class taniumpy.question_asker.QuestionAsker(session, question,
polling_interval=None, pct_complete_threshold=99, timeout=300)**

   Bases: `object
   <http://docs.python.org/2.7/library/functions.html#object>`_

   A class to aid in asking a Question.

   The primary function of this class is to poll for result info for
   question, and fire off events:

   ProgressChanged AnswersChanged AnswersComplete

   ``POLLING_INTERVAL = 5``

   **run(callbacks={}, **kwargs)**

      Poll for question data and issue callbacks.

      Callbacks should be a dict with members: 'ProgressChanged'
      'AnswersChanged' 'AnswersComplete'

      Each should be a function that accepts a QuestionAsker and a
      percent complete.

      Any callback can choose to get data from the session by calling
      asker.session.getResultData(asker.question)

      Polling will be stopped only when one of the callbacks calls the
      stop() method or the answers are complete. Note that callbacks
      can call setPercentCompleteThreshold to change what done means
      on the fly

   **setPctCompleteThreshold(val)**

   **stop()**

**exception taniumpy.question_asker.QuestionTimeoutException**

   Bases: `exceptions.Exception
   <http://docs.python.org/2.7/library/exceptions.html#exceptions.Exception>`_
