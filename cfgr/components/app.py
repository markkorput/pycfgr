from cfgr.event import Event
import time, os

class App:
  """
  The cfgr.app's default app component
  """
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('stop').signal_to_method(lambda obj: obj.onStop)
    builder.addInput('sleep').float_to_method(lambda obj: obj.setSleep)
    # outputs
    builder.addOutput('started').from_event(lambda obj: obj.startedEvent)
    builder.addOutput('pid').from_event(lambda obj: obj.pidEvent)

  def __init__(self):
    self.startedEvent = Event()
    self.pidEvent = Event()
    self.stopEvent = Event()
    self.sleeptime = 0.001

  def start(self):
    pid = os.getpid()
    # print('pid: ', pid)
    self.pidEvent(os.getpid())
    self.startedEvent.fire()

  def update(self):
    # print('update')
    time.sleep(self.sleeptime)

  def setSleep(self, val):
    # print('setsleep: {}'.format(val))
    self.sleeptime = val

  def onStop(self, *args, **kwargs):
    self.stopEvent()
