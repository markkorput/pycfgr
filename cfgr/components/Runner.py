import re
from cfgr.event import Event
from cfgr.Runtime import Runtime
from cfgr.Json import Loader


class Runner:
  """
  Runs an isolated (sub-)schema
  """

  @staticmethod
  def cfgr(builder):
    ## outputs
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)
    builder.addInput('runtime').to_method(lambda obj: obj.setRuntime)
    builder.addInput('url').string_to_method(lambda obj: obj.setUrl)
    builder.addInput('component').string_to_method(lambda obj: obj.setComponent)
    builder.addInput('load').signal_to_method(lambda obj: obj.load)
    builder.addInput('input').to_method(lambda obj: obj.setInputEvents)
    builder.addInput('output').to_method(lambda obj: obj.setOutputEvents)
    builder.addOutput('loaded').from_event(lambda obj: obj.loadedEvent)

  def __init__(self):
    self.isVerbose = False
    self.data = None
    self.componentId = None
    self.runtime = Runtime()
    self.parentRuntime = None
    self.filepath = None
    self.url = None

    self.loadedEvent = Event()

  def setVerbose(self, v): self.isVerbose = v

  def setRuntime(self, runtime):
    self.parentRuntime = runtime
    self.runtime = Runtime(copyTypesFrom=runtime)

  def setComponent(self, compid):
    self.componentId = compid

  def setUrl(self, url):
    self.url = url
    if url.startswith('http://'):
      print('http data not yet supported')
      return

    self.filepath = re.compile('file\:\/\/').sub('', url)

  def load(self):
    if not self.runtime:
      print('no runtime')
      return

    loader = Loader(runtime=self.runtime, file=self.filepath, verbose=self.isVerbose)
    self.verbose('[Runner] creating, root node: {} from schema: {}'.format(self.componentId, self.url))
    inst = loader.create(self.componentId, recursive=True)
    self.loadedEvent()

  def setInputEvents(self, event_data):
    # turn list into dict
    if type(event_data) == type([]):
      tmp = {}
      for val in event_data:
        tmp[val] = val
      event_data = tmp

    if type(event_data) == type({}):
      for key in event_data:
        value = event_data[key]
        source_event = self.parentRuntime.get_event(key)
        dest_event = self.runtime.get_event(value)
        source_event += dest_event.fire

        if self.verbose:
          source_event += lambda *args, **kwargs: self.verbose("[Runner] input event: {} -> {}".format(key,value))
      return

    print('Unsupported input events data')

  def setOutputEvents(self, event_data):
    # turn list into dict
    if type(event_data) == type([]):
      tmp = {}
      for val in event_data:
        tmp[val] = val
      event_data = tmp

    if type(event_data) == type({}):
      for key in event_data:
        value = event_data[key]

        source_event = self.runtime.get_event(key)
        dest_event = self.parentRuntime.get_event(value)
        source_event += dest_event.fire
        if self.verbose:
          source_event += lambda *args, **kwargs: self.verbose("[Runner] ouput event: {} -> {}".format(key,value))
      return

    print('Unsupported input events data')

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
