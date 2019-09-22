class Converter:
  def __init__(self, tools, event):
    self.tools = tools
    self.event = event

  def onFired(self, callback):
    self.singleValueCallback(lambda *args, **kwargs: callback())

  def onFloat(self, callback):
    self.convertBeforeCallback(callback, lambda v: float(v))

  def onString(self, callback):
    self.convertBeforeCallback(callback, lambda v: str(v))

  def onInt(self, callback):
    self.convertBeforeCallback(callback, lambda v: int(v))

  def onBool(self, callback):
    self.convertBeforeCallback(callback, lambda v: bool(v))

  def convertBeforeCallback(self, callback, converter):
    self.singleValueCallback(lambda v: callback(converter(v)))

  def singleValueCallback(self, callback):
    def valueHandler(*args, **kwargs):
      
      # is it event data, like #DurationValue,#AllDurationsValue
      if len(args) == 1 and self.isEventData(args[0]):
        eventvalcallback = lambda *args, **kwargs: callback(*args, **kwargs)
        for e in self.tools.getEvents(args[0]):
          e += eventvalcallback
        return

      # assume it's a value that is, or can be converted to float value, like 100.3 or "86.2"
      callback(*args,**kwargs)

    self.portSplitValueCallback(valueHandler)

  def portSplitValueCallback(self, callback):
    def valueHandler(*args, **kwargs):
      if len(args) == 0:
        callback()
        return

      vals = args[0].split(',') if  isinstance(args[0], str) else [args[0]]
      for val in vals:
        callback(val)

    self.event += valueHandler

  def isEventData(self, data):
    return str(data).strip().startswith('#')

class PortTools:
  """
  PortTools is a collection of interfaces through which ports can Ports can fetch
  specific types of data
  """
  def __init__(self, objectFunc=None, eventsFunc=None):
    self.objectFunc = objectFunc
    self.eventsFunc = eventsFunc

  def getObject(self, data):
    return self.objectFunc(data) if self.objectFunc else None

  def getEvents(self, data):
    return self.eventsFunc(data) if self.eventsFunc else []

  def converter(self, event):
    return Converter(self, event)

  def signalFor(self, event):
    return lambda *args, **kwargs: event.fire()

