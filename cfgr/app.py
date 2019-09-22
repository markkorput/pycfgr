import sys
from cfgr import Runtime, Json

from .components.app import App
from .components.string import String
from .components.print import Print

class Runner:
  def __init__(self, data_path, componentId, startEvent=None, stopEvent=None, verbose=False):
    self.runtime = Runtime()
    self.runtime.add_type(typeClass=App)
    self.runtime.add_type(typeClass=String)
    self.runtime.add_type(typeClass=Print)

    self.verbose = verbose
    self.loader = Json.Loader(runtime=self.runtime, file=data_path, verbose=self.verbose)
    self.componentId = componentId
    self.startEventId = startEvent
    
    self.isDone = False

    if stopEvent:
      e = self.runtime.get_event(stopEvent)
      e += self.onStopEvent

  def run(self):
    self.instance = self.loader.create(self.componentId, recursive=True)

    if self.startEventId:
      if self.verbose:
        print('firing start event: {}'.format(self.startEventId))
      self.runtime.get_event(self.startEventId).fire()

    while not self.isDone:
      pass

  def onStopEvent(self, *args, **kargs):
    if self.verbose:
      print('received stop event')
    self.stop()

  def stop(self):
    self.isDone = True

if __name__ == '__main__':
  runner = Runner(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None, sys.argv[5] == 'true' if len(sys.argv) > 5 else False)
  runner.run()