
Ask Manual Question Sensor With Filter And 3 Options
========================================================================================

Ask a manual question using human strings by referencing the name of a single sensor.

Also supply a sensor filter that limits the column data that is shown to values that contain Windows (which is short hand for regex match against .*Windows.*).

Also supply filter options that re-fetches any cached data that is older than 3600 seconds, matches all values supplied in the filter, and ignores case for any value match of the filter.

No sensor paramaters, question filters, or question options supplied.


* `STDOUT from Example Python Code <../_static/pytan_outputs/ask_manual_question_sensor_with_filter_and_3_options_stdout.txt>`_
* `STDERR from Example Python Code <../_static/pytan_outputs/ask_manual_question_sensor_with_filter_and_3_options_stderr.txt>`_
* Example Python Code

.. literalinclude:: ask_manual_question_sensor_with_filter_and_3_options_code.py
    :linenos:
    :language: python

.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
