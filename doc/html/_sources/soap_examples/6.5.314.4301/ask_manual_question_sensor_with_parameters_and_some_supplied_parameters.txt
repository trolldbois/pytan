
Ask Manual Question Sensor With Parameters And Some Supplied Parameters
==========================================================================================

Ask the question 'Get Folder Name Search with RegEx Match[Program Files,Microsoft.*] from all machines', wait for result data to be complete, and get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.008065
* `Step 1 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_1_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "password": "VGFuaXVtMjAxNSE=", 
      "username": "QWRtaW5pc3RyYXRvcg=="
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "135", 
      "content-type": "text/plain; charset=us-ascii"
    }


Step 2 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/info.json
* HTTP Method: GET
* Elapsed Time: 0:00:00.013871
* `Step 2 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "87511", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002496
* `Step 3 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_3_request.xml>`_
* `Step 3 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "587", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 4 - Issue an AddObject to add a Question object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.021312
* `Step 4 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_4_request.xml>`_
* `Step 4 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1003", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "769", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 5 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.040338
* `Step 5 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_5_request.xml>`_
* `Step 5 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "494", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 6 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001756
* `Step 6 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_6_request.xml>`_
* `Step 6 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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
* Elapsed Time: 0:00:00.002215
* `Step 7 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_7_request.xml>`_
* `Step 7 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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
* Elapsed Time: 0:00:00.002240
* `Step 8 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_8_request.xml>`_
* `Step 8 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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
* Elapsed Time: 0:00:00.002076
* `Step 9 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_9_request.xml>`_
* `Step 9 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_9_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 10 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002232
* `Step 10 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_10_request.xml>`_
* `Step 10 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_10_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 11 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002211
* `Step 11 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_11_request.xml>`_
* `Step 11 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_11_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 12 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001850
* `Step 12 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_12_request.xml>`_
* `Step 12 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_12_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 13 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002142
* `Step 13 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_13_request.xml>`_
* `Step 13 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_13_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 14 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002194
* `Step 14 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_14_request.xml>`_
* `Step 14 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_14_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 15 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002162
* `Step 15 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_15_request.xml>`_
* `Step 15 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_15_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 16 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002877
* `Step 16 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_16_request.xml>`_
* `Step 16 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_16_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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


Step 17 - Issue a GetResultData to get answers for a question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.005290
* `Step 17 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_17_request.xml>`_
* `Step 17 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_some_supplied_parameters_step_17_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "526", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6988-05836d41c7be5addca66f76227a78b0d47fead12ac9dd8b6b2af69ce4387d294ba47baf393a4fd0e38e9671d16594fbb57a602d2a6ad39d434965fdc66b845ca"
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
