
threaded_http module
********************

Simple HTTP server for testing purposes

**class threaded_http.Handler(request, client_address, server)**

   Bases: `BaseHTTPServer.BaseHTTPRequestHandler
   <http://docs.python.org/2.7/library/basehttpserver.html#BaseHTTPServer.BaseHTTPRequestHandler>`_

   ``__module__ = 'threaded_http'``

   **do_GET()**

   **log_message(format, *args)**

**class threaded_http.ThreadedHTTPServer(server_address,
RequestHandlerClass, bind_and_activate=True)**

   Bases: ``SocketServer.ThreadingMixIn``, `BaseHTTPServer.HTTPServer
   <http://docs.python.org/2.7/library/basehttpserver.html#BaseHTTPServer.HTTPServer>`_

   Handle requests in a separate thread.

   ``__module__ = 'threaded_http'``

**threaded_http.threaded_http(host='localhost', port=4443,
verbosity=2)**

   establishes an HTTP server on host:port in a thread
