
Ask Manual Question Sensor With Parameters And No Supplied Parameters
==========================================================================================

Ask the question 'Get Folder Name Search with RegEx Match from all machines' using sane defaults for parameters, wait for result data to be complete, and get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.006460
* `Step 1 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.012795
* `Step 2 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "87813", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002139
* `Step 3 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_3_request.xml>`_
* `Step 3 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_3_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.013984
* `Step 4 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_4_request.xml>`_
* `Step 4 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "915", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.034328
* `Step 5 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_5_request.xml>`_
* `Step 5 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_5_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.001614
* `Step 6 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_6_request.xml>`_
* `Step 6 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_6_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.002247
* `Step 7 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_7_request.xml>`_
* `Step 7 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_7_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.002092
* `Step 8 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_8_request.xml>`_
* `Step 8 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_8_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.002088
* `Step 9 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_9_request.xml>`_
* `Step 9 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_9_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.002095
* `Step 10 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_10_request.xml>`_
* `Step 10 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_10_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.002077
* `Step 11 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_11_request.xml>`_
* `Step 11 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_11_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.001843
* `Step 12 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_12_request.xml>`_
* `Step 12 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_12_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.001758
* `Step 13 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_13_request.xml>`_
* `Step 13 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_13_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.002647
* `Step 14 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_14_request.xml>`_
* `Step 14 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_14_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.001766
* `Step 15 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_15_request.xml>`_
* `Step 15 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_15_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
* Elapsed Time: 0:00:00.001431
* `Step 16 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_16_request.xml>`_
* `Step 16 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_16_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 17 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001358
* `Step 17 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_17_request.xml>`_
* `Step 17 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_17_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 18 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001872
* `Step 18 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_18_request.xml>`_
* `Step 18 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_18_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 19 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002165
* `Step 19 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_19_request.xml>`_
* `Step 19 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_19_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 20 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002035
* `Step 20 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_20_request.xml>`_
* `Step 20 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_20_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 21 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002250
* `Step 21 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_21_request.xml>`_
* `Step 21 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_21_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 22 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002073
* `Step 22 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_22_request.xml>`_
* `Step 22 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_22_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 23 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001999
* `Step 23 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_23_request.xml>`_
* `Step 23 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_23_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 24 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002042
* `Step 24 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_24_request.xml>`_
* `Step 24 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_24_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 25 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002114
* `Step 25 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_25_request.xml>`_
* `Step 25 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_25_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 26 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002965
* `Step 26 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_26_request.xml>`_
* `Step 26 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_26_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 27 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003084
* `Step 27 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_27_request.xml>`_
* `Step 27 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_27_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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


Step 28 - Issue a GetResultData to get answers for a question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.005488
* `Step 28 Request Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_28_request.xml>`_
* `Step 28 Response Body <../_static/soap_outputs/ask_manual_question_sensor_with_parameters_and_no_supplied_parameters_step_28_response.xml>`_

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
      "session": "1-6991-050b6d41b647d68310f9deb32de806e13b27ac42be5cecefe7b740685b54e740d4af331c939f94bf7038d5cc6a51cf7bbd0a7c5a73e64b30295d94fc8fd6a0cb"
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
