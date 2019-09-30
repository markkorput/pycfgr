from cfgr.event import Event

class bool:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('value').bool_to_method(lambda obj: obj.setValue)
    builder.addInput('emit').signal_to_method(lambda obj: obj.emit)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)

    # outputs
    builder.addOutput('emit').from_event(lambda obj: obj.emitEvent)
    builder.addOutput('change').from_event(lambda obj: obj.changeEvent)
    builder.addOutput('true').from_event(lambda obj: obj.trueEvent)
    builder.addOutput('false').from_event(lambda obj: obj.falseEvent)

  def __init__(self):
    self.value = None
    self.isVerbose = False
    self.emitEvent = Event()
    self.changeEvent = Event()
    self.trueEvent = Event()
    self.falseEvent = Event()

  def setValue(self, v):
    change = self.value != v
    self.value = v

    if change:
      self.verbose('[bool] change, new value: {}'.format(v))
      self.changeEvent(self.value)
      if self.value == True:
        self.trueEvent()
      if self.value == False:
        self.falseEvent()

  def emit(self):
    self.emitEvent(self.value)
  
  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)