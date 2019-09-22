from evento import Event

class String:
  """
  A simple string-value component
  """

  def __init__(self):
    self.value = None
    self.emitEvent = Event()

  def setValue(self, v):
    self.value = v

  def emit(self):
    self.emitEvent(self.value)

  @staticmethod
  def cfgr(builder):
    ## outputs
    builder.addInput('value').string(lambda val,obj: obj.setValue(val))
    builder.addInput('emit').connect_to_method(lambda obj: obj.emit)

    ## outputs
    # builder.addOutput('emit').connect(lambda port, obj: obj.emitEvent.subscribe(port.event.fire()))
    builder.addOutput('emit').connect_to_event(lambda obj: obj.emitEvent)