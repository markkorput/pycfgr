from .components import getCfgrClasses

def addAllTypes(runtime, modules=[], customTypeClasses=[]):
  for klass in getCfgrClasses():
    runtime.add_type(typeClass=klass)

  for klass in customTypeClasses:
    runtime.add_type(typeClass=klass)