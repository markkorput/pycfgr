from .Type import Type
from .TypeBuilder import TypeBuilder


def _portDefsFromClass(typeClass):
  """
  A Type is basically a collection of PortDefs (port-definitions) which contains
  the caller-provided logic of connecting the defined ports with the runtime object.
  """
  if not hasattr(typeClass, 'cfgr'):
    return None
   # default builder func: a static cfgr method
  cfgrFunc = typeClass.cfgr

  builder = TypeBuilder()
  cfgrFunc(builder)
  return builder.getPortDefs()


class Runtime:
  def __init__(self):
    self.types = []
    self.instances = []

  def add_type(self, typeId=None, typeClass=None):
    if not typeId:
      typeId = typeClass.__name__

    portDefs = _portDefsFromClass(typeClass)

    if not portDefs:
      print("no build func for type: {}".format(typeId))
      portDefs = []

    createFunc = typeClass
    typ = Type(typeId, portDefs, createFunc)
    self.types.append(typ)
    return typ

  def create_instance(self, typeId):
    for typ in self.types:
      if typ.typeId == typeId:
        inst = typ.create_instance()
        self.instances.append(inst)
        return inst

    return None

  def remove_instance(self, instance):
    self.instances.remove(instance)
