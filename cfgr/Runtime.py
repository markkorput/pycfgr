from evento import Event
from .Type import Type
from .TypeBuilder import TypeBuilder
from .PortTools import PortTools

def _portDefsFromClass(typeClass):
  """
  A Type is basically a collection of PortDefs (port-definitions) which contains
  the caller-provided logic of connecting the defined ports with the runtime object.
  """
  if not hasattr(typeClass, 'cfgr'):
    return None

  builderFunc = lambda builder: typeClass.cfgr(builder)

  builder = TypeBuilder()
  # default builder func: a static cfgr method
  builderFunc(builder)
  return builder.getPortDefs()


class Runtime:
  def __init__(self):
    self.types = []
    self.instances = []

    self.idInstances = {}
    self.events = {}

    # PortTools is a collection of interfaces that ports can use to fetch specific types of data
    self.port_tools = PortTools(objectFunc=lambda val: self.getObject(val))

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

  def create_instance(self, typeId, instanceId=None):
    for typ in self.types:
      if typ.typeId == typeId:
        inst = typ.create_instance(self.port_tools)
        self.instances.append(inst)

        if instanceId:
          self.idInstances[instanceId] = inst

        return inst

    return None

  def remove_instance(self, instance):
    self.instances.remove(instance)

  def get_event(self, id):
    if id in self.events:
      return self.events[id]

    e = Event()
    self.events[id] = e
    return e

  def getObject(self, id):
    return self.idInstances[id].object if id in self.idInstances else None
