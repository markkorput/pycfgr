from cfgr.event import Event
from time import time

class Interval:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('start').signal_to_method(lambda obj: obj.start)
    builder.addInput('stop').signal_to_method(lambda obj: obj.stop)
    builder.addInput('update').signal_to_method(lambda obj: obj.update)
    builder.addInput('ms').float_to_method(lambda obj: obj.setIntervalMs)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)

    # outputs
    builder.addOutput('action').from_event(lambda obj: obj.actionEvent)

  def __init__(self):
    self.isVerbose = False
    self.intervalSeconds = 1.0
    self.nextTime = None
    self.actionAtStart = True
    self._isActive = False

    self.actionEvent = Event()

  def setIntervalMs(self, v):
    self.intervalSeconds = v / 1000.0
    self.verbose('[Interval] new interval in seconds: {}'.format(str(self.intervalSeconds)))

  def start(self):
    if self.actionAtStart:
      self.actionEvent()
    self._isActive = True
    self.nextTime = time() + self.intervalSeconds

  def stop(self):
    self._isActive = False

  def update(self):
    if not self._isActive:
      return

    t = time()

    if t >= self.nextTime:
      self.verbose('[Interval] action')
      self.actionEvent()
      self.nextTime += self.intervalSeconds    

  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
