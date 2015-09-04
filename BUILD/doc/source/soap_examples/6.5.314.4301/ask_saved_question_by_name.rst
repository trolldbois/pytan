
Ask Saved Question By Name
==========================================================================================

Get the Saved Question object for Installed Applications then get the latest result data available for that Saved Question


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.006143
* `Step 1 Request Body <../_static/soap_outputs/ask_saved_question_by_name_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/ask_saved_question_by_name_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.013685
* `Step 2 Request Body <../_static/soap_outputs/ask_saved_question_by_name_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/ask_saved_question_by_name_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-7001-95ad8b27d21e8c51a44e4bb4f8e125350dd62c00fb17dbb01569a4b251a5702950f46c77201f7432ea6ef4ab59fce6082aae850f2b3d8c646a4ed416214592a8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "88324", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find saved question objects
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.012031
* `Step 3 Request Body <../_static/soap_outputs/ask_saved_question_by_name_step_3_request.xml>`_
* `Step 3 Response Body <../_static/soap_outputs/ask_saved_question_by_name_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "527", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-7001-95ad8b27d21e8c51a44e4bb4f8e125350dd62c00fb17dbb01569a4b251a5702950f46c77201f7432ea6ef4ab59fce6082aae850f2b3d8c646a4ed416214592a8"
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
* Elapsed Time: 0:00:00.003569
* `Step 4 Request Body <../_static/soap_outputs/ask_saved_question_by_name_step_4_request.xml>`_
* `Step 4 Response Body <../_static/soap_outputs/ask_saved_question_by_name_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "21616", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-7001-95ad8b27d21e8c51a44e4bb4f8e125350dd62c00fb17dbb01569a4b251a5702950f46c77201f7432ea6ef4ab59fce6082aae850f2b3d8c646a4ed416214592a8"
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


Step 5 - Issue a GetResultData to get the answers for the last asked question of this saved question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004121
* `Step 5 Request Body <../_static/soap_outputs/ask_saved_question_by_name_step_5_request.xml>`_
* `Step 5 Response Body <../_static/soap_outputs/ask_saved_question_by_name_step_5_response.xml>`_

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
      "session": "1-7001-95ad8b27d21e8c51a44e4bb4f8e125350dd62c00fb17dbb01569a4b251a5702950f46c77201f7432ea6ef4ab59fce6082aae850f2b3d8c646a4ed416214592a8"
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
