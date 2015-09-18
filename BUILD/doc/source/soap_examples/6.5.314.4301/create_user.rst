
Create User
==========================================================================================

Create a user called API Test User


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.012725
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.040827
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-608-bf782776cd0ff216acd619ea90ea7616a5faa8c11066cb99a239638d716e70d6fcd1f9fd271c903fbd3c5ad0f7175a6cdee1e0cd1828d798d35f6aa197bba0e2"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "19289", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find the object to be deleted
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003331
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "468", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-608-bf782776cd0ff216acd619ea90ea7616a5faa8c11066cb99a239638d716e70d6fcd1f9fd271c903fbd3c5ad0f7175a6cdee1e0cd1828d798d35f6aa197bba0e2"
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


Step 4 - Issue a GetObject to find a user role
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.030474
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "468", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-608-bf782776cd0ff216acd619ea90ea7616a5faa8c11066cb99a239638d716e70d6fcd1f9fd271c903fbd3c5ad0f7175a6cdee1e0cd1828d798d35f6aa197bba0e2"
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


Step 5 - Issue an AddObject to add a User object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.039295
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1792", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-608-bf782776cd0ff216acd619ea90ea7616a5faa8c11066cb99a239638d716e70d6fcd1f9fd271c903fbd3c5ad0f7175a6cdee1e0cd1828d798d35f6aa197bba0e2"
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


Step 6 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.254671
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "2896", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-608-bf782776cd0ff216acd619ea90ea7616a5faa8c11066cb99a239638d716e70d6fcd1f9fd271c903fbd3c5ad0f7175a6cdee1e0cd1828d798d35f6aa197bba0e2"
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
* Elapsed Time: 0:00:00.004353
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "468", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-608-bf782776cd0ff216acd619ea90ea7616a5faa8c11066cb99a239638d716e70d6fcd1f9fd271c903fbd3c5ad0f7175a6cdee1e0cd1828d798d35f6aa197bba0e2"
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
* Elapsed Time: 0:00:00.009112
* `Step 8 Request Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.5.314.4301/create_user_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "2845", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-608-bf782776cd0ff216acd619ea90ea7616a5faa8c11066cb99a239638d716e70d6fcd1f9fd271c903fbd3c5ad0f7175a6cdee1e0cd1828d798d35f6aa197bba0e2"
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
