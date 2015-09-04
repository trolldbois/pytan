
Create Group
==========================================================================================

Create a group called All Windows Computers API Test


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.006101
* `Step 1 Request Body <../_static/soap_outputs/create_group_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/create_group_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.015088
* `Step 2 Request Body <../_static/soap_outputs/create_group_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/create_group_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6914-d31dcf0ab7d38ea2bd8256b9ae9e7d6bf5348b17cce76f3a15e01cf9f00047e409bc9697a8e93d02024dbb325d09afd38e369ac973b509a12828ebf4a7bd5f36"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "86180", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find the object to be deleted
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002629
* `Step 3 Request Body <../_static/soap_outputs/create_group_step_3_request.xml>`_
* `Step 3 Response Body <../_static/soap_outputs/create_group_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "534", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6914-d31dcf0ab7d38ea2bd8256b9ae9e7d6bf5348b17cce76f3a15e01cf9f00047e409bc9697a8e93d02024dbb325d09afd38e369ac973b509a12828ebf4a7bd5f36"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "665", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 4 - Issue a GetObject to get the full object of specified sensors for inclusion in a group
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002210
* `Step 4 Request Body <../_static/soap_outputs/create_group_step_4_request.xml>`_
* `Step 4 Response Body <../_static/soap_outputs/create_group_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "568", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6914-d31dcf0ab7d38ea2bd8256b9ae9e7d6bf5348b17cce76f3a15e01cf9f00047e409bc9697a8e93d02024dbb325d09afd38e369ac973b509a12828ebf4a7bd5f36"
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


Step 5 - Issue an AddObject to add a Group object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.007362
* `Step 5 Request Body <../_static/soap_outputs/create_group_step_5_request.xml>`_
* `Step 5 Response Body <../_static/soap_outputs/create_group_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "692", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6914-d31dcf0ab7d38ea2bd8256b9ae9e7d6bf5348b17cce76f3a15e01cf9f00047e409bc9697a8e93d02024dbb325d09afd38e369ac973b509a12828ebf4a7bd5f36"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "762", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 6 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.011061
* `Step 6 Request Body <../_static/soap_outputs/create_group_step_6_request.xml>`_
* `Step 6 Response Body <../_static/soap_outputs/create_group_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "487", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6914-d31dcf0ab7d38ea2bd8256b9ae9e7d6bf5348b17cce76f3a15e01cf9f00047e409bc9697a8e93d02024dbb325d09afd38e369ac973b509a12828ebf4a7bd5f36"
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


Step 7 - Issue a GetObject to find the object to be deleted
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001725
* `Step 7 Request Body <../_static/soap_outputs/create_group_step_7_request.xml>`_
* `Step 7 Response Body <../_static/soap_outputs/create_group_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "534", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6914-d31dcf0ab7d38ea2bd8256b9ae9e7d6bf5348b17cce76f3a15e01cf9f00047e409bc9697a8e93d02024dbb325d09afd38e369ac973b509a12828ebf4a7bd5f36"
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


Step 8 - Issue a DeleteObject to delete an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002416
* `Step 8 Request Body <../_static/soap_outputs/create_group_step_8_request.xml>`_
* `Step 8 Response Body <../_static/soap_outputs/create_group_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1128", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6914-d31dcf0ab7d38ea2bd8256b9ae9e7d6bf5348b17cce76f3a15e01cf9f00047e409bc9697a8e93d02024dbb325d09afd38e369ac973b509a12828ebf4a7bd5f36"
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
