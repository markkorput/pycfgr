from cfgr.event import Event
# import os
import subprocess

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
    builder.addOutput('stdout').from_event(lambda obj: obj.stdoutEvent)
    builder.addOutput('stdoutString').from_event(lambda obj: obj.stdoutStringEvent)

  def __init__(self):
    self.cmd = None
    self.isVerbose = False

    self.executingEvent = Event()
    self.executedEvent = Event()
    self.stdoutEvent = Event()
    self.stdoutStringEvent = Event()

  def setCmd(self, v):
    self.cmd = v

  def execute(self):
    self.verbose('[Cmd {}] executing'.format(self.cmd))
    self.executingEvent()
    # os.system(self.cmd)

    p = subprocess.Popen([self.cmd], stdout=subprocess.PIPE)
    self.executedEvent()

    # do we have listeners that are interested in stdout?
    if len(self.stdoutEvent) > 0 or len(self.stdoutStringEvent) > 0: 
      out = p.stdout.read()
      self.verbose('[Cmd {}] stdout: {}'.format(self.cmd, out))
      self.stdoutEvent(out)
      stripped = out.decode('ascii').strip()
      # self.verbose('[Cmd {}] stdoutString: {}'.format(self.cmd, stripped))
      self.stdoutStringEvent(stripped)

  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
