import sys
from optparse import OptionParser
from cfgr import Runtime, Json

from .components.app import App
from .components.string import String
from .components.print import Print
from .components.OscOut import OscOut
from .components.OscIn import OscIn
from .components.OscMessage import OscMessage

class Runner:
  DEFAULT_DATA_PATH = 'cfgr.json'
  DEFAULT_COMPONENT = 'App'

  def __init__(self, data_path=None, component_id=None, start_event=None, verbose=False):
    self.runtime = Runtime()
    self.runtime.add_type(typeClass=App)
    self.runtime.add_type(typeClass=String)
    self.runtime.add_type(typeClass=Print)
    self.runtime.add_type(typeClass=OscOut)
    self.runtime.add_type(typeClass=OscIn)
    self.runtime.add_type(typeClass=OscMessage)

    self.componentId = component_id
    self.verbose = verbose
    self.isDone = False
    self.start_event = start_event
    self.loader = Json.Loader(runtime=self.runtime, file=data_path if data_path else Runner.DEFAULT_DATA_PATH, verbose=self.verbose)

  def run(self):
    isDefaultApp = self.componentId == None
    inst = self.loader.create(Runner.DEFAULT_COMPONENT if isDefaultApp else self.componentId, recursive=True)
    self.app = inst.object if isDefaultApp else None

    if isDefaultApp:
      self.app.stopEvent += self.onStop
      self.app.start()

    if self.start_event:
      for e in self.loader.context.get_events(self.start_event):
        e.fire()

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

  parser = OptionParser()
  parser.add_option('-d', '--data', dest='data', default=None)
  parser.add_option('-c', '--create', dest='create', default=None)
  parser.add_option('-s', '--start-event', dest='startevent', default=None)
  parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False)
  opts, args = parser.parse_args()

  runner = Runner(data_path=opts.data, component_id=opts.create, start_event=opts.startevent, verbose=opts.verbose)
  runner.run()