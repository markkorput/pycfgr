from evento import Event

class Port:
  INPUT = 1
  OUTPUT = 2

  def __init__(self, id, flags):
    self._id = id
    self.flags = flags

    self.event = Event()

  def isInput(self): return self.flags == Port.INPUT

  def isOutput(self): return self.flags == Port.OUTPUT
