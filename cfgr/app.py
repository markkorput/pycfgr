import sys
from optparse import OptionParser
from cfgr import Runtime, Json
from .discover import addAllTypes
from cfgr.components.app import App

DEFAULT_DATA_PATH = 'cfgr.json'
DEFAULT_COMPONENT = 'App'

def main(dataPath=None, componentId=None, startEvent=None, verbose=False, customTypeClasses=[]):
  # prepare runtime with all component types
  runtime = Runtime()
  addAllTypes(runtime, customTypeClasses=customTypeClasses)

  # create our json loader
  loader = Json.Loader(runtime=runtime, file=dataPath if dataPath else DEFAULT_DATA_PATH, verbose=verbose)

  # instantiate our root component (including the complete sub-hierarchy)
  rootInstance = loader.create(DEFAULT_COMPONENT if componentId == None else componentId, recursive=True)
  app = rootInstance.object if isinstance(rootInstance.object, App) else None

  # if we've instantiated the default App component, give it its start signal
  if app:
    app.start()

  # if we've received a startEvent command line option; trigger the specified event(s)
  if startEvent:
    for e in loader.context.get_events(startEvent):
      e.fire()

  try:
    while app == None or app.isActive:
      if app:
        app.update()
  except KeyboardInterrupt:
    print('KeyboardInterrupt, stopping.')
    if app:
      app.stop()

  # print('Done.')


def run(customTypeClasses=[]):
  parser = OptionParser()
  parser.add_option('-d', '--data', dest='data', default=None)
  parser.add_option('-c', '--create', dest='create', default=None)
  parser.add_option('-s', '--start-event', dest='startevent', default=None)
  parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False)
  opts, args = parser.parse_args()

  main(dataPath=opts.data, componentId=opts.create, startEvent=opts.startevent, verbose=opts.verbose, customTypeClasses=customTypeClasses)

if __name__ == '__main__':
  run()
