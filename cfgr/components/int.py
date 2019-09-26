from cfgr.event import Event

class int:
  """
  A simple int-value component
  """

  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('value').int_to_method(lambda obj: obj.setValue)
    builder.addInput('emit').signal_to_method(lambda obj: obj.emit)
    builder.addInput('add').int_to_method(lambda obj: obj.add)
    builder.addInput('max').int_to_method(lambda obj: obj.setMax)

    # outputs
    builder.addOutput('emit').from_event(lambda obj: obj.emitEvent)
    builder.addOutput('maxExceeded').from_event(lambda obj: obj.maxExceededEvent)

  def __init__(self):
    self.value = None
    self.max = None
    self.emitEvent = Event()
    self.maxExceededEvent = Event()


  def setValue(self, v):
    if self.max != None:
      if v > self.max:
        self.maxExceededEvent()
        v = self.max

    self.value = v

  def setMax(self, val):
    self.max = val

  def add(self, val=None):
    v = self.value if self.value != None else 0
    v += val if val else 1
    self.setValue(v)

  def emit(self):
    self.emitEvent(self.value)