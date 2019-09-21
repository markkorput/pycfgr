from .Type import Type

class Runtime:
  def __init__(self):
    self.types = []
    self.instances = []

  def create_type(self, typeId, typeClass):
    if not hasattr(typeClass, 'cfgr'):
      print("no build func for type: {}".format(typeId))
      return None

    # default create-object-instance-func; simply call constructor
    createFunc = typeClass
    # default builder func: a static cfgr method
    cfgrFunc = typeClass.cfgr
    typ = Type(typeId, createFunc, cfgrFunc)
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
