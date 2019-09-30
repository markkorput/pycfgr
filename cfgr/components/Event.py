from cfgr.event import Event as EventoEvent

class Event:
  """
  Listens for one or more events and fires one or more other events
  """
  @staticmethod
  def cfgr(builder):
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)
    ## outputs
    builder.addInput('on').to_method(lambda obj: obj.fire)
    builder.addOutput('do').from_event(lambda obj: obj.doEvent)

  def __init__(self):
    self.isVerbose = False
    self.doEvent = EventoEvent()

  def fire(self, *args, **kwargs):
    self.verbose('[Event] with {} args'.format(len(args)+len((kwargs))))
    self.doEvent.fire(*args, **kwargs)

  def setVerbose(self, v): self.isVerbose = v
  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
