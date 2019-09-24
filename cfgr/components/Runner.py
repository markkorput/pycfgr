# from evento import Event
import re
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
    builder.addInput('scope').string_to_method(lambda obj: obj.setScope)
    builder.addInput('create').signal_to_method(lambda obj: obj.create)
    builder.addInput('events').to_method(lambda obj: obj.setInputEvent)

  def __init__(self):
    self.isVerbose = False
    self.data = None
    self.componentId = None
    self.runtime = Runtime()
    self.scope = None
    self.filepath = None
    self.url = None

  def setVerbose(self, v): self.isVerbose = v

  def setRuntime(self, runtime):
    self.runtime = Runtime(copyTypesFrom=runtime)

  def setScope(self, scope):
    self.scope = scope

  def setComponent(self, compid):
    self.componentId = compid

  def setUrl(self, url):
    self.url = url
    if url.startswith('http://'):
      print('http data not yet supported')
      return

    self.filepath = re.compile('file\:\/\/').sub('', url)
    #if url.startswith('file://'): # DEFAULT 
    
    # if filepath:
    #   with open(filepath, "r") as f:
    #     self.verbose('[Runner] loading file: {}'.format(data))
    #     self.setData(f.read())

  # def setData(self, dat):
  #   self.data = dat

  def create(self):
    
    if not self.runtime:
      print('no runtime')
      return

    loader = Loader(runtime=self.runtime, file=self.filepath, verbose=True)
    self.verbose('[Runner] creating, root node: {} from schema: {}'.format(self.componentId, self.url))
    inst = loader.create(self.componentId, recursive=True)

  def setInputEvent(self, event_data):
    if type(event_data) == type({}):
      # for key in event_data:
        # for e in self.runtime.getEvents(key):
          # e.subscribe(lambda *args,**kwargs: 
          # pass)
      return

    print('Unsupported input events data')

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
