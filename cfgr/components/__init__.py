from os.path import dirname, basename, isfile
import glob

def getCfgrClasses():
  # find component .py files
  modules = glob.glob(dirname(__file__)+"/*.py")
  mods = [ basename(f)[:-3] for f in modules if isfile(f) and not f == '__init__.py']

  classes = []
  for mod in mods:
    m = __import__('cfgr.components.'+mod, fromlist=['cfgr.components'])
    for klass in m.__dict__.values():
      if hasattr(klass, 'cfgr'):
        classes.append(klass)

  return classes