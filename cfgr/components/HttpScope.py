from cfgr.event import Event
from urllib.parse import urlparse
import os.path, re

class HttpScope:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('scope').string_to_method(lambda obj: obj.setScope)
    builder.addInput('response').to_method(lambda obj: obj.setResponse)
    builder.addInput('request').to_method(lambda obj: obj.processRequest)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)
    builder.addInput('servePath').string_to_method(lambda obj: obj.setServePath)

    # outputs
    builder.addOutput('match').from_event(lambda obj: obj.matchEvent)
    builder.addOutput('unscoped').from_event(lambda obj: obj.unscopedEvent)

  def __init__(self):
    self.responseCode = None
    self.scope = "/"
    self.isVerbose = False
    self.servePath = None

    self.matchEvent = Event()
    self.unscopedEvent = Event()

  def setScope(self, v):
    self.scope = v
  
  def setResponse(self, val):
    self.responseCode = val

  def setServePath(self, p):
    # strip trailing slash
    self.servePath = re.sub('/$', '', os.path.abspath(os.path.expanduser(p)))

  def processRequest(self, req):
    if not self.isMatch(req):
      return

    self.verbose('[HttpScope {}] match'.format(self.scope))
    self.matchEvent(req)

    if self.responseCode:
      req.respondWithCode(self.responseCode)

    if self.servePath:
      unscoped = req.unscope(self.scope)
      urlParseResult = urlparse(unscoped.path)
      requestedFilePath = re.sub('^/', '', urlParseResult.path)
      
      servedFilePath = os.path.join(self.servePath, requestedFilePath)
      self.verbose('[HttpScope] serving static file: {}'.format(servedFilePath))
      req.respondWithFile(servedFilePath)

    if len(self.unscopedEvent) > 0:
      unscoped = req.unscope(self.scope)
      # self.verbose("[HttpScope] unscoped: {}".format(unscoped.path))
      self.unscopedEvent(unscoped)

  def isMatch(self, req):
    urlParseResult = urlparse(req.path)
    path = urlParseResult.path

    if path.startswith(self.scope):
      return True

    return False

  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
