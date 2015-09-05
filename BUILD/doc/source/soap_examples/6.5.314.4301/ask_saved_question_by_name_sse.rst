
Ask Saved Question By Name Sse
==========================================================================================

Get the Saved Question object for Installed Applications then get the latest result data available using Server Side Export for that Saved Question


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.013948
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.016542
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8139-0f12025da6209f228db5eed2243d9665c128faf901598699e4016fad3abcdaea66d78861df8631f37a35f801afe4f2bc8ce014eb050bd2c97e84ee7777ee0b3d"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "114191", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find saved question objects
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.023872
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_3_response.xml>`_

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
      "session": "1-8139-0f12025da6209f228db5eed2243d9665c128faf901598699e4016fad3abcdaea66d78861df8631f37a35f801afe4f2bc8ce014eb050bd2c97e84ee7777ee0b3d"
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


Step 4 - Issue a GetObject to get the full object of the last question asked by a saved question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.006775
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "21616", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8139-0f12025da6209f228db5eed2243d9665c128faf901598699e4016fad3abcdaea66d78861df8631f37a35f801afe4f2bc8ce014eb050bd2c97e84ee7777ee0b3d"
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


Step 5 - Issue a GetResultData to start a Server Side Export and get an export_id
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004297
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_5_response.xml>`_

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
      "session": "1-8139-0f12025da6209f228db5eed2243d9665c128faf901598699e4016fad3abcdaea66d78861df8631f37a35f801afe4f2bc8ce014eb050bd2c97e84ee7777ee0b3d"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "877", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 6 - perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/494747304836.xml.status
* HTTP Method: GET
* Elapsed Time: 0:00:00.002953
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_6_request.txt>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_6_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8139-0f12025da6209f228db5eed2243d9665c128faf901598699e4016fad3abcdaea66d78861df8631f37a35f801afe4f2bc8ce014eb050bd2c97e84ee7777ee0b3d"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "11", 
      "content-type": "application/octet-stream"
    }


Step 7 - perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/494747304836.xml.status
* HTTP Method: GET
* Elapsed Time: 0:00:00.003819
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_7_request.txt>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_7_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8139-0f12025da6209f228db5eed2243d9665c128faf901598699e4016fad3abcdaea66d78861df8631f37a35f801afe4f2bc8ce014eb050bd2c97e84ee7777ee0b3d"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "29", 
      "content-type": "application/octet-stream"
    }


Step 8 - perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/494747304836.xml.gz
* HTTP Method: GET
* Elapsed Time: 0:00:00.002897
* `Step 8 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_8_request.txt>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_8_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8139-0f12025da6209f228db5eed2243d9665c128faf901598699e4016fad3abcdaea66d78861df8631f37a35f801afe4f2bc8ce014eb050bd2c97e84ee7777ee0b3d"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-encoding": "gzip", 
      "content-length": "10434", 
      "content-type": "application/octet-stream"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
