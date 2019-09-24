from evento import Event as EventoEvent

class Event:
  """
  Listens for one or more events and fires one or more other events
  """
  @staticmethod
  def cfgr(builder):
    ## outputs
    builder.addInput('on').to_method(lambda obj: obj.doEvent.fire)
    builder.addOutput('do').from_event(lambda obj: obj.doEvent)

  def __init__(self):
    self.doEvent = EventoEvent()

  # def fire(self, *args, **kwargs):
  #   self.doEvent(*args, **kwargs)
