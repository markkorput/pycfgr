from .Instance import Instance

class Type:
  def __init__(self, typeId, portDefs, createFunc):
    self.typeId = typeId
    self.createFunc = createFunc
    self.portDefs = portDefs

  def create_instance(self):
    obj = self.createFunc()

    ports = []
    for portdef in self.portDefs:
      port = portdef.createPortFor(obj)
      ports.append(port)

    inst = Instance(obj, ports)
    return inst
  
