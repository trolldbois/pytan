
Ask Manual Question Simple Multiple Sensors
==========================================================================================

Ask the question 'Get Computer Name and Installed Applications from all machines', wait for result data to be complete, and get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.060169
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_1_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "password": "VGFuaXVtMjAxNSE=", 
      "username": "QWRtaW5pc3RyYXRvcg=="
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "134", 
      "content-type": "text/plain; charset=us-ascii"
    }


Step 2 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/info.json
* HTTP Method: GET
* Elapsed Time: 0:00:00.019010
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-685-7f6bf3c54ea3f7e1bf73584af90643b6d64168a24f3b57da4e2aaae4980e154ad63fd4a69b5d677d51946da29053221bee206d3e0620288969b817245c908785"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "20906", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.006969
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "565", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-685-7f6bf3c54ea3f7e1bf73584af90643b6d64168a24f3b57da4e2aaae4980e154ad63fd4a69b5d677d51946da29053221bee206d3e0620288969b817245c908785"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-encoding": "gzip", 
      "content-type": "text/xml;charset=UTF-8", 
      "transfer-encoding": "chunked"
    }


Step 4 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.032278
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "574", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-685-7f6bf3c54ea3f7e1bf73584af90643b6d64168a24f3b57da4e2aaae4980e154ad63fd4a69b5d677d51946da29053221bee206d3e0620288969b817245c908785"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-encoding": "gzip", 
      "content-type": "text/xml;charset=UTF-8", 
      "transfer-encoding": "chunked"
    }


Step 5 - Issue an AddObject to add a Question object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.014303
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "753", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-685-7f6bf3c54ea3f7e1bf73584af90643b6d64168a24f3b57da4e2aaae4980e154ad63fd4a69b5d677d51946da29053221bee206d3e0620288969b817245c908785"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "766", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 6 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.058660
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "492", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-685-7f6bf3c54ea3f7e1bf73584af90643b6d64168a24f3b57da4e2aaae4980e154ad63fd4a69b5d677d51946da29053221bee206d3e0620288969b817245c908785"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-encoding": "gzip", 
      "content-type": "text/xml;charset=UTF-8", 
      "transfer-encoding": "chunked"
    }


Step 7 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.035616
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "496", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-685-7f6bf3c54ea3f7e1bf73584af90643b6d64168a24f3b57da4e2aaae4980e154ad63fd4a69b5d677d51946da29053221bee206d3e0620288969b817245c908785"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-encoding": "gzip", 
      "content-type": "text/xml;charset=UTF-8", 
      "transfer-encoding": "chunked"
    }


Step 8 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.066067
* `Step 8 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "496", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-685-7f6bf3c54ea3f7e1bf73584af90643b6d64168a24f3b57da4e2aaae4980e154ad63fd4a69b5d677d51946da29053221bee206d3e0620288969b817245c908785"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-encoding": "gzip", 
      "content-type": "text/xml;charset=UTF-8", 
      "transfer-encoding": "chunked"
    }


Step 9 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.119950
* `Step 9 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_9_request.xml>`_
* `Step 9 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_9_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "496", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-685-7f6bf3c54ea3f7e1bf73584af90643b6d64168a24f3b57da4e2aaae4980e154ad63fd4a69b5d677d51946da29053221bee206d3e0620288969b817245c908785"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-encoding": "gzip", 
      "content-type": "text/xml;charset=UTF-8", 
      "transfer-encoding": "chunked"
    }


Step 10 - Issue a GetResultData to get answers for a question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.009759
* `Step 10 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_10_request.xml>`_
* `Step 10 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_multiple_sensors_step_10_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "524", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-685-7f6bf3c54ea3f7e1bf73584af90643b6d64168a24f3b57da4e2aaae4980e154ad63fd4a69b5d677d51946da29053221bee206d3e0620288969b817245c908785"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-encoding": "gzip", 
      "content-type": "text/xml;charset=UTF-8", 
      "transfer-encoding": "chunked"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
