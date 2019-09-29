import sys
from optparse import OptionParser
from cfgr import Runtime, Json
from .discover import addAllTypes

DEFAULT_DATA_PATH = 'cfgr.json'
DEFAULT_COMPONENT = 'App'

def main(dataPath=None, componentId=None, startEvent=None, verbose=False):
  # prepare runtime with all component types
  runtime = Runtime()
  addAllTypes(runtime)

  # create our json loader
  loader = Json.Loader(runtime=runtime, file=dataPath if dataPath else DEFAULT_DATA_PATH, verbose=verbose)

  # instantiate our root component (including the complete sub-hierarchy)
  isDefaultApp = componentId == None
  inst = loader.create(DEFAULT_COMPONENT if isDefaultApp else componentId, recursive=True)
  app = inst.object if isDefaultApp else None

  # if we've instantiated the default App component, give it its start signal
  if isDefaultApp:
    app.start()

  # if we've received a startEvent command line option; trigger the specified event(s)
  if startEvent:
    for e in loader.context.get_events(startEvent):
      e.fire()

  try:
    while not isDefaultApp or app.isActive:
      if isDefaultApp:
        app.update()
  except KeyboardInterrupt:
    print('KeyboardInterrupt, stopping.')

  # print('Done.')


if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-d', '--data', dest='data', default=None)
  parser.add_option('-c', '--create', dest='create', default=None)
  parser.add_option('-s', '--start-event', dest='startevent', default=None)
  parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False)
  opts, args = parser.parse_args()

  main(dataPath=opts.data, componentId=opts.create, startEvent=opts.startevent, verbose=opts.verbose)