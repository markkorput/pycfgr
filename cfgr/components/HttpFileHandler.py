from cfgr.event import Event
from urllib.parse import urlparse
import os.path, re

class HttpFileHandler:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('request').to_method(lambda obj: obj.processRequest)
    builder.addInput('response').to_method(lambda obj: obj.setResponse)
    builder.addInput('saveTo').string_to_method(lambda obj: obj.setSaveTo)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)

    # outputs
    #builder.addOutput('match').from_event(lambda obj: obj.matchEvent)
    builder.addOutput('saved').from_event(lambda obj: obj.savedEvent)

  def __init__(self):
    self.responseCode = None
    self.isVerbose = False
    self.saveTo = None

    self.savedEvent = Event()

  def setResponse(self, val):
    self.responseCode = val
  
  def setSaveTo(self, val):
    self.saveTo = os.path.abspath(os.path.expanduser(val)) #val

  def processRequest(self, req):
    """Saves a file following a HTTP PUT request"""
    # https://f-o.org.uk/2017/receiving-files-over-http-with-python.html

    # # Don't overwrite files
    # if os.path.exists(filename):
    #     self.send_response(409, 'Conflict')
    #     self.end_headers()
    #     reply_body = '"%s" already exists\n' % filename
    #     self.wfile.write(reply_body.encode('utf-8'))
    #     return

    filename = self.saveTo if self.saveTo else os.path.basename(req.path)
    file_length = int(req.handler.headers['Content-Length'])
    with open(filename, 'wb') as output_file:
      output_file.write(req.handler.rfile.read(file_length))
    self.verbose('[HttpFileHandler] wrote {} bytes to: {}'.format(file_length, filename))

    req.handler.send_response(201, 'Created')
    req.handler.end_headers()
    
    reply_body = 'Saved "%s"\n' % filename
    req.handler.wfile.write(reply_body.encode('utf-8'))

    self.savedEvent(filename)

  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
