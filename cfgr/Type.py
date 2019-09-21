from .TypeBuilder import TypeBuilder
from .Instance import Instance

class Type:
  def __init__(self, typeId, typeClass, buildFunc=None):
    self.typeId = typeId
    self.typeClass = typeClass

    builder = TypeBuilder()

    if not buildFunc:
      buildFunc = typeClass.build

    buildFunc(builder)

    self.portDefs = builder.getPortDefs()

  def create_instance(self):
    obj = self.typeClass()

    ports = []
    for portdef in self.portDefs:
      port = portdef.createPortFor(obj)
      ports.append(port)

    inst = Instance(obj, ports)
    return inst
  
