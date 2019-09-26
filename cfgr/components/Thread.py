from cfgr.event import Event
from time import sleep
import threading

class Thread:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('start').signal_to_method(lambda obj: obj.start)
    builder.addInput('stop').signal_to_method(lambda obj: obj.stop)
    builder.addInput('sleeptime').float_to_method(lambda obj: obj.setSleepTime)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)

    # outputs
    builder.addOutput('started').from_event(lambda obj: obj.startedEvent)
    builder.addOutput('action').from_event(lambda obj: obj.actionEvent)
    builder.addOutput('stopped').from_event(lambda obj: obj.stoppedEvent)

  def __init__(self):
    self.thread = None
    self.isVerbose = False
    self.stayAlive = True
    self.sleeptime = 0.001
    self.actionEvent = Event()
    self.startedEvent = Event()
    self.stoppedEvent = Event()

  def setSleepTime(self, v):
    self.sleeptime = v
   
  def isAlive(self):
    return self.thread and self.thread.isAlive()

  def start(self):
    if self.isAlive():
      return

    self.stayAlive = True
    self.thread = threading.Thread(target=self.mainFunc)
    self.thread.start()

  def stop(self):
    self.stayAlive = False

  def mainFunc(self):
    self.verbose("[Thread] started")
    self.startedEvent()

    while self.stayAlive:
      # self.verbose("[Thread] update")
      self.actionEvent()
      sleep(self.sleeptime)

    self.verbose("[Thread] stopping")
    self.stoppedEvent()
    
  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
