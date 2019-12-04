from cfgr.event import Event
import os.path, re

class HttpParamHandler:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('request').to_method(lambda obj: obj.processRequest)
    builder.addInput('param').string_to_method(lambda obj: obj.setParamName)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)
    # outputs
    builder.addOutput('value').from_event(lambda obj: obj.valueEvent)

  def __init__(self):
    self.paramName = ""
    self.isVerbose = False

    self.valueEvent = Event()

  def setParamName(self, v):
    self.paramName = v
  
  def processRequest(self, req):
    # self.verbose('[HttpParamHandler] req: {}'.format(req))
    # self.verbose('[HttpParamHandler] handler: {}'.format(req.handler))
    # self.verbose('[HttpParamHandler] headers: {}'.format(req.handler.headers))
    # self.verbose('[HttpParamHandler] req.query: {}'.format(req.query))
    query = req.query

    for pair in query.split('&'):
     keyval = pair.split('=')
     if len(keyval) == 2 and keyval[0] == self.paramName:
       self.verbose('[HttpParamHandler `{}`] got value: {}'.format(self.paramName, keyval[1]))
       self.valueEvent(keyval[1])

  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
