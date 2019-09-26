import threading, time, socket, os, re
import urllib.parse
from cfgr.event import Event

import http.client
from http.server import HTTPServer, SimpleHTTPRequestHandler


class HttpRequest:
  def __init__(self, path, handler, respondFunc):
    self.path = path
    self.handler = handler
    # self.command = self.handler.command

    self.respondFunc = respondFunc

  def respondWithCode(self, code):
    self.respondFunc(code)
  
  def respond(self, code, content):
    self.respondFunc(code, content)

  def unscope(self, scope):
    parts = urllib.parse.urlsplit(self.path)
    newpath = re.sub('^{}'.format(scope), '', parts.path)
    unscopedreqpath = urllib.parse.urlunsplit((parts.scheme, parts.netloc, newpath, parts.query, parts.fragment))
    return HttpRequest(unscopedreqpath, self.handler, self.respondFunc)

def createRequestHandler(requestCallback, verbose=False):
  class CustomHandler(SimpleHTTPRequestHandler, object):
    def __init__(self, *args, **kwargs):
      self.responded = False
      super(CustomHandler, self).__init__(*args, **kwargs)

    def respond(self, code=None, body=None, headers=None):
      self.responded = True

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

    def process_request(self):
      req = HttpRequest(self.path, self, self.respond)
      # urlParseResult = urllib.parse.urlparse(self.path)
      # print('urlpar:', urlParseResult)
      requestCallback(req)
      if not self.responded:
        self.respond(404)
      return True

    def do_HEAD(self):
      return self.process_request()
      # if self.process_request():
      #   return
      # super(CustomHandler, self).do_HEAD()

    def do_GET(self):
      self.process_request()
      # if self.process_request():
      #   return
      # super(CustomHandler, self).do_GET()

    def do_POST(self):
      self.process_request()
      # if self.process_request():
      #   return
      # super(CustomHandler, self).do_POST()

    # def translate_path(self, path):
    #     if self.event_manager != None and 'output_events' in self.options:
    #         if path in self.options['output_events']:
    #             self.event_manager.fire(self.options['output_events'][path])
    #             # self.send_error(204)
    #             self.send_response(200)
    #             self.wfile.write('OK')
    #             self.wfile.close()
    #             return ''

    #     relative_path = path[1:] if path.startswith('/') else path
    #     return SimpleHTTPRequestHandler.translate_path(self, os.path.join(self.root_path, relative_path))

    # def _onResponseContent(self, json):
    #     # self.logger.warn('response CONTENT: '+str(json))
    #     self.response_type = "application/json"
    #     self.response_content = json

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
    self.stop()

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
        connection = http.client.HTTPSConnection("127.0.0.1", self.port)
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
