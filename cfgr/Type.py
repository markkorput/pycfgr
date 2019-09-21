from .TypeBuilder import TypeBuilder
from .Instance import Instance

class Type:
  def __init__(self, typeId, createFunc, cfgrFunc):
    self.typeId = typeId
    self.createFunc = createFunc

    builder = TypeBuilder()
    cfgrFunc(builder)
    self.portDefs = builder.getPortDefs()

  def create_instance(self):
    obj = self.createFunc()

    ports = []
    for portdef in self.portDefs:
      port = portdef.createPortFor(obj)
      ports.append(port)

    inst = Instance(obj, ports)
    return inst
  
