import threading, time, socket, os, re
from cfgr.event import Event



# import urllib.parse
urlsplit = None
urlunsplit = None
try: # python3
  import urllib.parse # python3  
  urlsplit = urllib.parse.urlsplit
  urlunsplit = urllib.parse.urlunsplit
except ImportError:
  urlsplit = None
  urlunsplit = None

  try: #python2
    import urlparse # python2
    urlsplit = urlparse.urlsplit
    urlunsplit = urlparse.urlunsplit
  except ImportError:
    print('[HttpServer] could not load url parsing dependencies')


# import http.client
HTTPSConnection = None
try: # python 3
  import http.client
  HTTPSConnection = http.client.HTTPConnection
except ImportError:
  try: # python 2
    import httplib
    HTTPSConnection = httplib.HTTPSConnection
  except ImportError:
    print('[HttpServer] could not load http client dependencies')


# from http.server import HTTPServer, CGIHTTPRequestHandler #SimpleHTTPRequestHandler
HTTPServer = None
CGIHTTPRequestHandler = None
try:
  import http.server
  HTTPServer = http.server.HTTPServer
  CGIHTTPRequestHandler = http.server.CGIHTTPRequestHandler
except ImportError:
  try:
    import BaseHTTPServer
    import CGIHTTPServer
    HTTPServer = BaseHTTPServer.HTTPServer
    CGIHTTPRequestHandler = CGIHTTPServer.CGIHTTPRequestHandler
  except ImportError:
    print('[HttpServer] Could not load server dependencies')

class HttpRequest:
  def __init__(self, path, handler, method='GET'):
    self.path = path
    self.handler = handler
    self.method = method

    parts = urlsplit(self.path)
    # newpath = re.sub('^{}'.format(scope), '', parts.path)
    # unscopedreqpath = urlunsplit((parts.scheme, parts.netloc, newpath, parts.query, parts.fragment))
    self.query = parts.query

  def respondWithCode(self, code):
    self.handler.respond(code)
  
  def respond(self, code, content):
    self.handler.respond(code, content)

  def respondWithFile(self, filePath):
    self.handler.respondWithFile(filePath)

  def unscope(self, scope):
    if urlsplit == None or urlunsplit == None:
      print('[HttpScope] unscope not working')
      return HttpRequest(self.path, self.handler, method=self.method)

    parts = urlsplit(self.path)
    newpath = re.sub('^{}'.format(scope), '', parts.path)
    unscopedreqpath = urlunsplit((parts.scheme, parts.netloc, newpath, parts.query, parts.fragment))
    return HttpRequest(unscopedreqpath, self.handler, method=self.method)

def createRequestHandler(requestCallback, verbose=False):
  class CustomHandler(CGIHTTPRequestHandler, object):
    def __init__(self, *args, **kwargs):
      self.hasResponded = False
      self.respondedWithFile = None
      super(CustomHandler, self).__init__(*args, **kwargs)

    def respond(self, code=None, body=None, headers=None):
      self.hasResponded = True

      if code == None:
        self.send_response(404)
        self.end_headers()
        # self.wfile.close()
        return

      self.send_response(code)
      if headers:
        for key in headers:
          self.send_header(key, headers[key])

      self.end_headers()
      if body:
        self.wfile.write(body)
      # self.wfile.close()
      return

    def respondWithFile(self, filePath):
      self.respondedWithFile = filePath

    def process_request(self, method='GET'):
      req = HttpRequest(self.path, self, method=method)
      requestCallback(req)

      return self.hasResponded

    def do_HEAD(self):
      if not self.process_request(method='HEAD'):
        super(CustomHandler, self).do_HEAD()

    def do_GET(self):
      if not self.process_request(method='GET'):
        super(CustomHandler, self).do_GET()

    def do_POST(self):
      if not self.process_request(method='POST'):
        super(CustomHandler, self).do_POST()

    def do_PUT(self):
      if not self.process_request(method='PUT'):
        super(CustomHandler, self).do_PUT()

    def translate_path(self, path):
      if self.respondedWithFile:
        if os.path.isfile(self.respondedWithFile):
          return self.respondedWithFile
      return CGIHTTPRequestHandler.translate_path(self, path)

  return CustomHandler

class HttpServer(threading.Thread):

  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('port').int_to_method(lambda obj: obj.setPort)
    builder.addInput('start').signal_to_method(lambda obj: obj.startServer)
    builder.addInput('stop').signal_to_method(lambda obj: obj.stopServer)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)

    # outputs
    builder.addOutput('request').from_event(lambda obj: obj.requestEvent)

  def __init__(self):
    threading.Thread.__init__(self)
    self.http_server = None
    self.threading_event = None
    self.port = 8080
    self.isVerbose = False

    self.requestEvent = Event()

  def __del__(self):
    self.stopServer()

  def startServer(self):
    self.threading_event = threading.Event()
    self.threading_event.set()
    self.verbose("[HttpServer] starting server thread")
    self.start() # start thread


  def stopServer(self, joinThread=True):
    if not self.isAlive():
      return

    self.threading_event.clear()
    self.verbose('[HttpServer] sending GET request to stop HTTP server from blocking...')

    try:
        connection = HTTPSConnection("127.0.0.1", self.port)
        connection.request('HEAD', '/')
        connection.getresponse()
    except socket.error:
        pass

    if joinThread:
      self.join()

  def setPort(self, p):
    self.port = p

  # thread function
  def run(self):
    self.verbose('[HttpServer] starting server on port {0}'.format(self.port))
    HandlerClass = createRequestHandler(self.onRequest, verbose=self.isVerbose)
    self.http_server = HTTPServer(('', self.port), HandlerClass)

    # self.httpd.serve_forever()
    # self.httpd.server_activate()
    while self.threading_event.is_set(): #not self.kill:
      try:
        self.http_server.handle_request()
      except Exception as exc:
        print('[HttpServer] exception:')
        print(exc)

    self.verbose('[HttpServer] closing server at port {0}'.format(self.port))
    self.http_server.server_close()
    self.http_server = None

  def onRequest(self, req):
    self.verbose('[HttpServer {}] request from {}'.format(str(req.path), str(req.handler.client_address)))
    self.requestEvent(req)

  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)

# # for testing
# if __name__ == '__main__':
#     logging.basicConfig()
#     ws = WebServer({'verbose': True, 'serve': 'examples'})
#     try:
#         ws.setup()
#         while True:
#             time.sleep(.1)
#     except KeyboardInterrupt:
#         print('KeyboardInterrupt. Quitting.')

#     ws.destroy()
