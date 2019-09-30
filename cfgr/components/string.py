from cfgr.event import Event

class bool:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('value').string_to_method(lambda obj: obj.setValue)
    builder.addInput('emit').signal_to_method(lambda obj: obj.emit)
    builder.addInput('contains').string_to_method(lambda obj: obj.contains)
    builder.addInput('present').string_to_method(lambda obj: obj.present)

    # outputs
    builder.addOutput('emit').from_event(lambda obj: obj.emitEvent)
    builder.addOutput('contains').from_event(lambda obj: obj.containsEvent)
    builder.addOutput('present').from_event(lambda obj: obj.presentEvent)

  def __init__(self):
    self.value = None
    self.emitEvent = Event()
    self.containsEvent = Event()
    self.presentEvent = Event()

  def setValue(self, v):
    self.value = v

  def emit(self):
    self.emitEvent(self.value)
  
  def contains(self, v):
    result = (v in self.value) if self.value else False
    self.containsEvent(result)

  def present(self, v):
    result = (self.value in v) if v else False
    self.presentEvent(result)