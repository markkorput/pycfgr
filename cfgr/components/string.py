from cfgr.event import Event

class String:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('value').string_to_method(lambda obj: obj.setValue)
    builder.addInput('emit').signal_to_method(lambda obj: obj.emit)

    # outputs
    builder.addOutput('emit').from_event(lambda obj: obj.emitEvent)
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