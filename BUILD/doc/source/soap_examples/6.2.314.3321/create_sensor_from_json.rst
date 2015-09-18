
Create Sensor From JSON
==========================================================================================

Get a sensor object, add ' API TEST' to the name of the sensor object, delete any pre-existing sensor with the new name, then create a new sensor object with the new name


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.016068
* `Step 1 Request Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_1_response.txt>`_

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
      "content-length": "110", 
      "content-type": "text/plain; charset=us-ascii", 
      "date": "Sat, 05 Sep 2015 05:19:31 GMT", 
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
* Elapsed Time: 0:00:00.001358
* `Step 2 Request Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_2_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1580-345d6c9cdb2f1c246eb306037b8c67c3c196bdb877f00c79e811bed0c3d8bad7bbf55c64f6ae417b29b989aa53ead243029d1167d515c64c7aa5a6b41cad1fd8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-length": "207", 
      "content-type": "text/html; charset=iso-8859-1", 
      "date": "Sat, 05 Sep 2015 05:19:31 GMT", 
      "keep-alive": "timeout=5, max=99", 
      "server": "Apache", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 3 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:444/info.json
* HTTP Method: POST
* Elapsed Time: 0:00:00.037185
* `Step 3 Request Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_3_request.txt>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_3_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "Content-Length": "0", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1580-345d6c9cdb2f1c246eb306037b8c67c3c196bdb877f00c79e811bed0c3d8bad7bbf55c64f6ae417b29b989aa53ead243029d1167d515c64c7aa5a6b41cad1fd8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "10256", 
      "content-type": "application/json"
    }


Step 4 - Issue a GetObject to find an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004745
* `Step 4 Request Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "507", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1580-345d6c9cdb2f1c246eb306037b8c67c3c196bdb877f00c79e811bed0c3d8bad7bbf55c64f6ae417b29b989aa53ead243029d1167d515c64c7aa5a6b41cad1fd8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "5225", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:19:31 GMT", 
      "keep-alive": "timeout=5, max=98", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 5 - Issue a GetObject to find the object to be deleted
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004188
* `Step 5 Request Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "552", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1580-345d6c9cdb2f1c246eb306037b8c67c3c196bdb877f00c79e811bed0c3d8bad7bbf55c64f6ae417b29b989aa53ead243029d1167d515c64c7aa5a6b41cad1fd8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "5239", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:19:31 GMT", 
      "keep-alive": "timeout=5, max=97", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 6 - Issue a DeleteObject to delete an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.011161
* `Step 6 Request Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "16013", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1580-345d6c9cdb2f1c246eb306037b8c67c3c196bdb877f00c79e811bed0c3d8bad7bbf55c64f6ae417b29b989aa53ead243029d1167d515c64c7aa5a6b41cad1fd8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "5228", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:19:31 GMT", 
      "keep-alive": "timeout=5, max=96", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 7 - Issue an AddObject to add an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.097855
* `Step 7 Request Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "16026", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1580-345d6c9cdb2f1c246eb306037b8c67c3c196bdb877f00c79e811bed0c3d8bad7bbf55c64f6ae417b29b989aa53ead243029d1167d515c64c7aa5a6b41cad1fd8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "5221", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:19:31 GMT", 
      "keep-alive": "timeout=5, max=95", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 8 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.106906
* `Step 8 Request Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.2.314.3321/create_sensor_from_json_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "488", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1580-345d6c9cdb2f1c246eb306037b8c67c3c196bdb877f00c79e811bed0c3d8bad7bbf55c64f6ae417b29b989aa53ead243029d1167d515c64c7aa5a6b41cad1fd8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "5233", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:19:31 GMT", 
      "keep-alive": "timeout=5, max=94", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
