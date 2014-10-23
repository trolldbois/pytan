from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = threading.currentThread().getName()
        self.wfile.write(message)
        self.wfile.write('\n')
        return

    # turn off logging messages so we don't seem the get requests in console
    # during unittests
    def log_message(self, format, *args):
        pass


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def threaded_http(host='localhost', port=4443):
    '''establishes an HTTP server on host:port in a thread'''
    server = ThreadedHTTPServer((host, port), Handler)
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()
    print ('Threaded HTTP server started on {}:{}').format(host, port)
    return server
