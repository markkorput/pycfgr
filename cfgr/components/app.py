from cfgr.event import Event
import time, os

class App:
  """
  The cfgr.app's default app component
  """
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('stop').signal_to_method(lambda obj: obj.stop)
    builder.addInput('sleep').float_to_method(lambda obj: obj.setSleep)
    # outputs
    builder.addOutput('started').from_event(lambda obj: obj.startedEvent)
    builder.addOutput('update').from_event(lambda obj: obj.updateEvent)
    builder.addOutput('pid').from_event(lambda obj: obj.pidEvent)
    builder.addOutput('stopped').from_event(lambda obj: obj.stoppedEvent)

  def __init__(self):
    self.startedEvent = Event()
    self.pidEvent = Event()
    self.updateEvent = Event()
    
    self.sleeptime = 0.001
    self.isActive = False

    self.stoppedEvent = Event()

  def start(self):
    pid = os.getpid()
    self.pidEvent(os.getpid())
    self.isActive = True
    self.startedEvent.fire()

  def update(self):
    self.updateEvent()
    # print('update')
    time.sleep(self.sleeptime)

  def setSleep(self, val):
    # print('setsleep: {}'.format(val))
    self.sleeptime = val

  def stop(self, *args, **kwargs):
    self.isActive = False
    self.stoppedEvent()
