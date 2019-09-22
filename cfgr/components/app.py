from evento import Event
import time

class App:
  """
  The cfgr.app's default app component
  """
  def __init__(self):
    self.startedEvent = Event()
    self.stopEvent = Event()
    self.sleeptime = 1.0

  def start(self):
    self.startedEvent.fire()

  def update(self):
    time.sleep(self.sleeptime)

  def setSleep(self, val): self.sleeptime = val

  def onStop(self, *args, **kwargs):
    self.stopEvent()

  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('stop').connect_to_method(lambda obj: obj.onStop)
    builder.addInput('sleep').float_to_method(lambda obj: obj.setSleep)
    # outputs
    builder.addOutput('started').connect_to_event(lambda obj: obj.startedEvent)
