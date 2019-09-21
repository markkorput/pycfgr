from .Type import Type

class Runtime:
  def __init__(self):
    self.types = []
    self.instances = []

  def create_type(self, typeId, typeClass):
    typ = Type(typeId, typeClass)
    self.types.append(typ)
    return typ

  def add_type(self, typeClass):
    return self.create_type(typeClass.__name__, typeClass)

  def create_instance(self, typeId):
    for typ in self.types:
      if typ.typeId == typeId:
        inst = typ.create_instance()
        self.instances.append(inst)
        return inst

    return None
