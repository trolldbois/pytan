
Ask Manual Question Multiple Sensors With Parameters And Some Supplied Parameters
==========================================================================================

Ask the question 'Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] and Computer Name from all machines', wait for result data to be complete, and get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.014172
* `Step 1 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_1_response.txt>`_

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
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "111", 
      "content-type": "text/plain; charset=us-ascii", 
      "date": "Sat, 05 Sep 2015 05:37:55 GMT", 
      "keep-alive": "timeout=5, max=100", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "vary": "Accept-Encoding", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 2 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/info.json
* HTTP Method: GET
* Elapsed Time: 0:00:00.000999
* `Step 2 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_2_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-length": "207", 
      "content-type": "text/html; charset=iso-8859-1", 
      "date": "Sat, 05 Sep 2015 05:37:55 GMT", 
      "keep-alive": "timeout=5, max=99", 
      "server": "Apache", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 3 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:444/info.json
* HTTP Method: POST
* Elapsed Time: 0:00:00.012727
* `Step 3 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_3_request.txt>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_3_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "Content-Length": "0", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "11073", 
      "content-type": "application/json"
    }


Step 4 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.005101
* `Step 4 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "587", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "5237", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:37:55 GMT", 
      "keep-alive": "timeout=5, max=98", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 5 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003734
* `Step 5 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_5_response.xml>`_

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
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "784", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:37:55 GMT", 
      "keep-alive": "timeout=5, max=97", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 6 - Issue an AddObject to add a Question object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.026844
* `Step 6 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1117", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "653", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:37:55 GMT", 
      "keep-alive": "timeout=5, max=96", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 7 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.188873
* `Step 7 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "493", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "1263", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:37:55 GMT", 
      "keep-alive": "timeout=5, max=95", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 8 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003272
* `Step 8 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "702", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:37:55 GMT", 
      "keep-alive": "timeout=5, max=94", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 9 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004163
* `Step 9 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_9_request.xml>`_
* `Step 9 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_9_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:00 GMT", 
      "keep-alive": "timeout=5, max=93", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 10 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003148
* `Step 10 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_10_request.xml>`_
* `Step 10 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_10_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:05 GMT", 
      "keep-alive": "timeout=5, max=92", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 11 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003618
* `Step 11 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_11_request.xml>`_
* `Step 11 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_11_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:10 GMT", 
      "keep-alive": "timeout=5, max=91", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 12 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003663
* `Step 12 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_12_request.xml>`_
* `Step 12 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_12_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:15 GMT", 
      "keep-alive": "timeout=5, max=90", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 13 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003614
* `Step 13 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_13_request.xml>`_
* `Step 13 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_13_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:20 GMT", 
      "keep-alive": "timeout=5, max=89", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 14 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003815
* `Step 14 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_14_request.xml>`_
* `Step 14 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_14_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:25 GMT", 
      "keep-alive": "timeout=5, max=88", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 15 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003675
* `Step 15 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_15_request.xml>`_
* `Step 15 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_15_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:30 GMT", 
      "keep-alive": "timeout=5, max=87", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 16 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003932
* `Step 16 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_16_request.xml>`_
* `Step 16 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_16_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:35 GMT", 
      "keep-alive": "timeout=5, max=86", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 17 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003682
* `Step 17 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_17_request.xml>`_
* `Step 17 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_17_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:40 GMT", 
      "keep-alive": "timeout=5, max=85", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 18 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003741
* `Step 18 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_18_request.xml>`_
* `Step 18 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_18_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:45 GMT", 
      "keep-alive": "timeout=5, max=84", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 19 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003600
* `Step 19 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_19_request.xml>`_
* `Step 19 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_19_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:50 GMT", 
      "keep-alive": "timeout=5, max=83", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 20 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004192
* `Step 20 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_20_request.xml>`_
* `Step 20 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_20_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:38:55 GMT", 
      "keep-alive": "timeout=5, max=82", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 21 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003346
* `Step 21 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_21_request.xml>`_
* `Step 21 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_21_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:39:00 GMT", 
      "keep-alive": "timeout=5, max=81", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 22 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003484
* `Step 22 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_22_request.xml>`_
* `Step 22 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_22_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:39:05 GMT", 
      "keep-alive": "timeout=5, max=80", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 23 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003365
* `Step 23 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_23_request.xml>`_
* `Step 23 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_23_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "718", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:39:10 GMT", 
      "keep-alive": "timeout=5, max=79", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 24 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003791
* `Step 24 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_24_request.xml>`_
* `Step 24 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_24_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "715", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:39:15 GMT", 
      "keep-alive": "timeout=5, max=78", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 25 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003856
* `Step 25 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_25_request.xml>`_
* `Step 25 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_25_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "715", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:39:20 GMT", 
      "keep-alive": "timeout=5, max=77", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 26 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004089
* `Step 26 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_26_request.xml>`_
* `Step 26 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_26_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "717", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:39:25 GMT", 
      "keep-alive": "timeout=5, max=76", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 27 - Issue a GetResultData to get answers for a question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004835
* `Step 27 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_27_request.xml>`_
* `Step 27 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_multiple_sensors_with_parameters_and_some_supplied_parameters_step_27_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "525", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1651-f06bac1f2233670ad8b9a0e5baf80705d75a746a0ea8129e9dccfcbe2c68d0cff1440afcfcadc0e84aeb3095fbde2df0e20a8e5d9f29231b1dbcf06eaae3262f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "11013", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:39:25 GMT", 
      "keep-alive": "timeout=5, max=75", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
