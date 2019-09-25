from cfgr.event import Event
from urllib.parse import urlparse

class HttpScope:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('scope').string_to_method(lambda obj: obj.setScope)
    builder.addInput('response').to_method(lambda obj: obj.setResponse)
    builder.addInput('request').to_method(lambda obj: obj.processRequest)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)

    # outputs
    builder.addOutput('unscoped').from_event(lambda obj: obj.unscopedEvent)

  def __init__(self):
    self.unscopedEvent = Event()
    self.scope = "/"
    self.isVerbose = False

  def setScope(self, v):
    self.scope = v
  
  def setResponse(self, val):
    self.response = val

  def processRequest(self, req):
    if not self.isMatch(req):
      return

    self.verbose('[HttpScope {}] match'.format(self.scope))

    if len(self.unscopedEvent) > 0:
      unscoped = self.unscope(req)
      self.unscopedEvent(unscoped)

  def isMatch(self, req):
    
    urlParseResult = urlparse(req.path)
    path = urlParseResult.path

    if path == self.scope:
      return True

    return False

  def unscope(self, req):
    # TODO!
    return req

  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
