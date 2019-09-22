import sys
from cfgr import Runtime, Json

from .components.app import App
from .components.string import String
from .components.print import Print

class Runner:
  def __init__(self, data_path, componentId=None, verbose=False):
    self.runtime = Runtime()
    self.runtime.add_type(typeClass=App)
    self.runtime.add_type(typeClass=String)
    self.runtime.add_type(typeClass=Print)

    self.componentId = componentId
    self.verbose = verbose
    self.isDone = False
    self.loader = Json.Loader(runtime=self.runtime, file=data_path, verbose=self.verbose)

  def run(self):
    isDefaultApp = self.componentId == None
    inst = self.loader.create('App' if isDefaultApp else self.componentId, recursive=True)
    self.app = inst.object if isDefaultApp else None

    if isDefaultApp:
      self.app.stopEvent += self.onStop
      self.app.start()

    try:
      while not self.isDone:
        if isDefaultApp:
          self.app.update()
    except KeyboardInterrupt:
      print('KeyboardInterrupt, stopping.')
      self.onStop()
          
  def onStop(self):
    self.isDone = True


if __name__ == '__main__':
  runner = Runner(sys.argv[1]) #, sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None, sys.argv[5] == 'true' if len(sys.argv) > 5 else False)
  runner.run()