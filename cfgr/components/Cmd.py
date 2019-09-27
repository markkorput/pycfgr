from cfgr.event import Event
import os

class Cmd:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('execute').signal_to_method(lambda obj: obj.execute)
    builder.addInput('cmd').string_to_method(lambda obj: obj.setCmd)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)

    # outputs
    builder.addOutput('executing').from_event(lambda obj: obj.executingEvent)
    builder.addOutput('executed').from_event(lambda obj: obj.executedEvent)

  def __init__(self):
    self.cmd = None
    self.isVerbose = False

    self.executingEvent = Event()
    self.executedEvent = Event()

  def setCmd(self, v):
    self.cmd = v

  def execute(self):
    self.verbose('[Cmd {}] executing'.format(self.cmd))
    self.executingEvent()
    os.system(self.cmd)
    self.executedEvent()

  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
