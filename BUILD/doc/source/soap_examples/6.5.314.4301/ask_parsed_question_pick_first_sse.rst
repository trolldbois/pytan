
Ask Parsed Question Pick First Sse
==========================================================================================

Ask the server to parse the question text 'computer name and ip route details' and add the question object that is returned in the first ParseResultGroup,  wait for result data to be complete, then use server side export to get the result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.014100
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_1_response.txt>`_

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
      "content-length": "135", 
      "content-type": "text/plain; charset=us-ascii"
    }


Step 2 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/info.json
* HTTP Method: GET
* Elapsed Time: 0:00:00.015508
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8119-2ceeb7853d2f1caba47d5f04e880f7958926d9d19564925dab0ce0d0118712d719852a9c876c825c5b6976c375de3c5e8db79cfccbad202d7c165e40b37fc600"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "113371", 
      "content-type": "application/json"
    }


Step 3 - Issue an AddObject to add a ParseJob for question_text and get back ParseResultGroups
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.045209
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "527", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8119-2ceeb7853d2f1caba47d5f04e880f7958926d9d19564925dab0ce0d0118712d719852a9c876c825c5b6976c375de3c5e8db79cfccbad202d7c165e40b37fc600"
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


Step 4 - Issue an AddObject to add the Question object from the chosen ParseResultGroup
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.008966
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "713", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8119-2ceeb7853d2f1caba47d5f04e880f7958926d9d19564925dab0ce0d0118712d719852a9c876c825c5b6976c375de3c5e8db79cfccbad202d7c165e40b37fc600"
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
* Elapsed Time: 0:00:00.013189
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "494", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8119-2ceeb7853d2f1caba47d5f04e880f7958926d9d19564925dab0ce0d0118712d719852a9c876c825c5b6976c375de3c5e8db79cfccbad202d7c165e40b37fc600"
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
* Elapsed Time: 0:00:00.002799
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8119-2ceeb7853d2f1caba47d5f04e880f7958926d9d19564925dab0ce0d0118712d719852a9c876c825c5b6976c375de3c5e8db79cfccbad202d7c165e40b37fc600"
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
* Elapsed Time: 0:00:00.004074
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8119-2ceeb7853d2f1caba47d5f04e880f7958926d9d19564925dab0ce0d0118712d719852a9c876c825c5b6976c375de3c5e8db79cfccbad202d7c165e40b37fc600"
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


Step 8 - Issue a GetResultData to start a Server Side Export and get an export_id
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003285
* `Step 8 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "558", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8119-2ceeb7853d2f1caba47d5f04e880f7958926d9d19564925dab0ce0d0118712d719852a9c876c825c5b6976c375de3c5e8db79cfccbad202d7c165e40b37fc600"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "877", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 9 - perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/494746885072.xml.status
* HTTP Method: GET
* Elapsed Time: 0:00:00.002898
* `Step 9 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_9_request.txt>`_
* `Step 9 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_9_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8119-2ceeb7853d2f1caba47d5f04e880f7958926d9d19564925dab0ce0d0118712d719852a9c876c825c5b6976c375de3c5e8db79cfccbad202d7c165e40b37fc600"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "27", 
      "content-type": "application/octet-stream"
    }


Step 10 - perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/494746885072.xml.gz
* HTTP Method: GET
* Elapsed Time: 0:00:00.003132
* `Step 10 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_10_request.txt>`_
* `Step 10 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_10_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8119-2ceeb7853d2f1caba47d5f04e880f7958926d9d19564925dab0ce0d0118712d719852a9c876c825c5b6976c375de3c5e8db79cfccbad202d7c165e40b37fc600"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-encoding": "gzip", 
      "content-length": "458", 
      "content-type": "application/octet-stream"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
