
Get Sensor By Names
==========================================================================================

Get multiple sensor objects by name


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.016618
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/get_sensor_by_names_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/get_sensor_by_names_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.014010
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/get_sensor_by_names_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/get_sensor_by_names_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-664-f22836856f66cfff94c7efc27e5bc27638179700a7134f111723c160b5ca31cef5ae0b1f5c8a608b83ad8973adabf980c43d3c7e3b0cec2fe5d03f640f598da1"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "20905", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.007956
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/get_sensor_by_names_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/get_sensor_by_names_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "566", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-664-f22836856f66cfff94c7efc27e5bc27638179700a7134f111723c160b5ca31cef5ae0b1f5c8a608b83ad8973adabf980c43d3c7e3b0cec2fe5d03f640f598da1"
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
