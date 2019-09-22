class Converter:
  def __init__(self, tools, event):
    self.tools = tools
    self.event = event

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
    def valueHandler(value):
      # is it event data, like #DurationValue,#AllDurationsValue
      if self.isEventData(value):
        eventvalcallback = lambda eventvalue: callback(eventvalue)
        for e in self.tools.getEvents(value):
          e += eventvalcallback
        return

      # assume it's a value that is, or can be converted to float value, like 100.3 or "86.2"
      callback(value)

    self.portSplitValueCallback(valueHandler)

  def portSplitValueCallback(self, callback):
    def valueHandler(value):
      vals = value.split(',') if isinstance(value, str) else [value]
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

