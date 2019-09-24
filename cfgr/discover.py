from .components import getCfgrClasses

def addAllTypes(runtime, modules=[]):
  for klass in getCfgrClasses():
    runtime.add_type(typeClass=klass)