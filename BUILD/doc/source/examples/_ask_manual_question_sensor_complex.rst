
Ask Manual Question Sensor Complex
========================================================================================

This provides an example for asking a manual question without using human strings.

It uses the Computer Name and Folder Contents sensors.

The second sensor has a single parameter, folderPath, with a value of 'c:\Program Files'.

The second sensor also has 3 sensor filter options that set the max data age to 3600 seconds, does NOT ignore case, and treats all values as string.

There is also a question filter supplied that limits the rows that are displayed to computers that match an Operating System that contains Windows, and has 3 question filter options supplied that set the max data age to 3600 seconds, does NOT ignore case, and uses 'and' to join all question filters.


* `STDOUT from Example Python Code <../_static/pytan_outputs/_ask_manual_question_sensor_complex_stdout.txt>`_
* `STDERR from Example Python Code <../_static/pytan_outputs/_ask_manual_question_sensor_complex_stderr.txt>`_
* Example Python Code

.. literalinclude:: _ask_manual_question_sensor_complex_code.py
    :linenos:
    :language: python

.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
