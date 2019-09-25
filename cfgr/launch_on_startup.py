from optparse import OptionParser
from .components.LaunchOnStartup import LaunchOnStartup

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-d', '--data', dest='data', default=None)
  parser.add_option('-c', '--create', dest='create', default=None)
  parser.add_option('-s', '--start-event', dest='startevent', default=None)
  parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False)
  parser.add_option('-u', '--uninstall', dest='uninstall', action="store_true", default=False)
  opts, args = parser.parse_args()

  comp = LaunchOnStartup()
  comp.setDataPath(opts.data)
  comp.setComponentId(opts.create)
  comp.setStartEvent(opts.startevent)
  if opts.uninstall:
    comp.uninstall()
  else:
    comp.install()