from cfgr.event import Event

list_operator = list

class list:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('value').to_method(lambda obj: obj.setValue)
    builder.addInput('append').to_method(lambda obj: obj.append)
    builder.addInput('remove').to_method(lambda obj: obj.remove)
    builder.addInput('emit').signal_to_method(lambda obj: obj.emit)
    builder.addInput('iterate').signal_to_method(lambda obj: obj.iterate)
    builder.addInput('contains').string_to_method(lambda obj: obj.contains)
    builder.addInput('present').string_to_method(lambda obj: obj.present)

    # outputs
    builder.addOutput('emit').from_event(lambda obj: obj.emitEvent)
    builder.addOutput('contains').from_event(lambda obj: obj.containsEvent)
    builder.addOutput('present').from_event(lambda obj: obj.presentEvent)
    builder.addOutput('iterate').from_event(lambda obj: obj.iterateEvent)

  def __init__(self):
    self.value = None
    self.emitEvent = Event()
    self.containsEvent = Event()
    self.presentEvent = Event()
    self.iterateEvent = Event()

  def setValue(self, v):
    self.value = v if type(v) == type([]) else [v]

  def emit(self):
    self.emitEvent(self.value)
  
  def contains(self, v):
    result = (v in self.value) if self.value else False
    self.containsEvent(result)

  def present(self, v):
    result = (self.value in v) if v else False
    self.presentEvent(result)

  def append(self, v):
    if not self.value:
      self.value = []
    self.value = self.value + [v]
  
  def remove(self, v):
    if not self.value:
      return

    self.value = list_operator(filter(lambda x: x != v, self.value if self.value else []))

  def iterate(self):
    if not self.value:
      return
    items = self.value
    for item in items:
      self.iterateEvent(item)
    