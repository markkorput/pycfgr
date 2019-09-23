from evento import Event


class OscMessage:
  """
  Osc sender client
  """
  def __init__(self):
    self.isVerbose = False
    self.sendMessage = Event()
    self.addr = None
    self.data = []

    self.sendEvent = Event()

  def setVerbose(self, v): self.isVerbose = v
  def setAddress(self, addr): self.addr = addr
  def setData(self, data): self.data = data
  def send(self): self.sendEvent((self.addr, self.data))

  @staticmethod
  def cfgr(builder):
    ## outputs
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)
    builder.addInput('address').string_to_method(lambda obj: obj.setAddress)
    builder.addInput('data').list_to_method(lambda obj: obj.setData)
    builder.addInput('send').signal_to_method(lambda obj: obj.send)
    builder.addOutput('send').from_event(lambda obj: obj.sendEvent)

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
