from cfgr.event import Event

class Port:
  INPUT = 1
  OUTPUT = 2

  def __init__(self, id, flags, tools):
    self._id = id
    self.flags = flags
    self.tools = tools

    self.event = Event()

  def isInput(self): return self.flags == Port.INPUT

  def isOutput(self): return self.flags == Port.OUTPUT
