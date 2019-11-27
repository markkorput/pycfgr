from cfgr.event import Event
import os
import subprocess

UnknownCommandError = None
try: # python3
  UnknownCommandError = FileNotFoundError
except NameError:
  # python2
  UnknownCommandError = OSError


class Cmd:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('execute').signal_to_method(lambda obj: obj.execute)
    builder.addInput('cmd').list_to_method(lambda obj: obj.setCmd)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)
    builder.addInput('background').bool_to_method(lambda obj: obj.setBackground)

    # outputs
    builder.addOutput('executing').from_event(lambda obj: obj.executingEvent)
    builder.addOutput('executed').from_event(lambda obj: obj.executedEvent)
    builder.addOutput('stdout').from_event(lambda obj: obj.stdoutEvent)
    builder.addOutput('stdoutString').from_event(lambda obj: obj.stdoutStringEvent)

  def __init__(self):
    self.cmd = None
    self.isVerbose = False
    self.inBackground = False

    self.executingEvent = Event()
    self.executedEvent = Event()
    self.stdoutEvent = Event()
    self.stdoutStringEvent = Event()

  def setCmd(self, v):
    self.cmd = v

  def setBackground(self, v):
    # print('setBG: {}'.format(v))
    self.inBackground = v

  def execute(self):
    self.verbose('[Cmd {}] executing{}'.format(self.cmd, ' in background' if self.inBackground else ''))
    self.executingEvent()

    if self.inBackground:
      os.system(' '.join(self.cmd))
      self.executedEvent()
      return

    p = None
    try:
      
      p = subprocess.Popen(self.cmd if type(self.cmd) == type([]) else [self.cmd], stdout=subprocess.PIPE)
    except UnknownCommandError as err:
      print("[Cmd {}] err: {}".format(self.cmd, str(err)))
      p = None
    except Exception as err:
      print("[Cmd {}] err: {}".format(self.cmd, str(err)))
      p = None

    if p == None:
      # TODO fire failure event?
      return

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
