import sys
from cfgr import Runtime, Json

from .components.string import String
from .components.print import Print

class App:
  def __init__(self, data_path, componentId, startEvent=None, stopEvent=None):
    self.runtime = Runtime()
    self.runtime.add_type(typeClass=String)
    self.runtime.add_type(typeClass=Print)

    self.loader = Json.Loader(runtime=self.runtime, file=data_path, verbose=True)
    self.componentId = componentId
    self.startEventId = startEvent
    
    if stopEvent:
      e = self.runtime.get_event(stopEvent)
      e += self.stop

  def run(self):
    self.instance = self.loader.create(self.componentId)

    if self.startEventId:
      self.runtime.get_event(self.startEventId).fire()

    while not self.runtime.isDone:
      self.runtime.update()

  def stop(self):
    self.runtime.isDone = True

if __name__ == '__main__':
  app = App(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
  app.run()