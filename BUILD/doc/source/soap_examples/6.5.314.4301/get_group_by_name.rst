
Get Group By Name
==========================================================================================

Get a group object by name


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.008251
* `Step 1 Request Body <../_static/soap_outputs/get_group_by_name_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/get_group_by_name_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.013705
* `Step 2 Request Body <../_static/soap_outputs/get_group_by_name_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/get_group_by_name_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6965-3a521fa0c9310ccd02c32be07145308cf883214615912fe07587f45591f1a674c8e1474f8029d4a1166b407473e117df311ea7ab2e32b90e34498427328e3aa7"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "87507", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002950
* `Step 3 Request Body <../_static/soap_outputs/get_group_by_name_step_3_request.xml>`_
* `Step 3 Response Body <../_static/soap_outputs/get_group_by_name_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "517", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6965-3a521fa0c9310ccd02c32be07145308cf883214615912fe07587f45591f1a674c8e1474f8029d4a1166b407473e117df311ea7ab2e32b90e34498427328e3aa7"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "941", 
      "content-type": "text/xml;charset=UTF-8"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
