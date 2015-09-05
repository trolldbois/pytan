
Ask Manual Question Complex Query1
========================================================================================

Ask a manual question using human strings by referencing the name of a two sensors sensor.

Supply 3 parameters for the second sensor, one of which is not a valid parameter (and will be ignored).

Supply one option to the second sensor.

Supply two question filters that limit the rows returned in the result to computers that match the sensor Operating System that contains Windows and does not contain Windows.

Supply two question options that 'or' the two question filters and ignore the case of any values while matching the question filters.


* `STDOUT from Example Python Code <../_static/pytan_outputs/ask_manual_question_complex_query1_stdout.txt>`_
* `STDERR from Example Python Code <../_static/pytan_outputs/ask_manual_question_complex_query1_stderr.txt>`_
* Example Python Code

.. literalinclude:: ask_manual_question_complex_query1_code.py
    :linenos:
    :language: python

.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
