from unittest import TestCase
from evento import Event

class Product:
  def __init__(self):
    self.name = ''
    self.nameChangedEvent = Event()

  def cfgr():
    return lambda x: print(x)

  def setName(self, v):
    if v == self.name:
      return

    self.name = v
    self.nameChangedEvent(self.name)

  def build(builder):
    builder.addInput('name').string(lambda v,obj: obj.setName(v))
    builder.addOutput('nameChanged').apply(lambda outp,obj: obj.nameChangedEvent.subscribe(outp.event))

class Instance:
  def __init__(self, object, ports):
    self.object = object
    self.ports = ports

  def input(self, id):
    for p in self.ports:
      if p.isInput() and p._id == id:
        return p
    return None

  def output(self, id):
    for p in self.ports:
      if p.isOutput() and p._id == id:
        return p
    return None

class Port:
  INPUT = 1
  OUTPUT = 2

  def __init__(self, id, flags):
    self._id = id
    self.flags = flags

    self.event = Event()

  def isInput(self): return self.flags == Port.INPUT

  def isOutput(self): return self.flags == Port.OUTPUT


class PortDef:

  def __init__(self, id, flags):
    self._id = id
    self.flags = flags
    self.applyFuncs = []

  def createPortFor(self, object):
    # create port
    p = Port(self._id, self.flags)

    # perform all logic of connecting the port to the given object
    for func in self.applyFuncs:
      func(p, object)

    # return port
    return p

class PortBuilder:
  def __init__(self, id, flags):
    self.portDef = PortDef(id, flags)

  def apply(self, func):
    self.portDef.applyFuncs.append(func)

  def string(self, stringFunc):
    # class StringApply:
      # def apply(self, )
    applyFunc = lambda port, obj: port.event.subscribe(lambda v: stringFunc(v, obj))
    self.apply(applyFunc)

class TypeBuilder:
  def __init__(self):
    self.portDefs = []

  def addInput(self, id):
    portbuilder = PortBuilder(id, Port.INPUT)
    self.portDefs.append(portbuilder.portDef)
    return portbuilder

  def addOutput(self, id):
    portbuilder = PortBuilder(id, Port.OUTPUT)
    self.portDefs.append(portbuilder.portDef)
    return portbuilder

  def getPortDefs(self):
    return self.portDefs

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


class TestRuntime(TestCase):
  def test_simple_type(self):
    # create runtime
    runtime = Runtime()

    # create Product type
    self.assertEquals(runtime.types, [])
    typ = runtime.add_type(Product)
    self.assertEquals(runtime.types, [typ])

    # create instance of Product type
    self.assertEquals(runtime.instances, [])
    inst = runtime.create_instance('Product')
    self.assertEquals(runtime.instances, [inst])

    # verify we received an Instance with a Product object
    self.assertEquals(type(inst), Instance)
    self.assertEquals(type(inst.object), Product)

    # verify the 'name' input updates the Product's name    
    self.assertEquals(inst.object.name, '')
    inst.input('name').event('New Product')
    self.assertEquals(inst.object.name, 'New Product')

    # verify the 'nameChanged' output fires when the product's name is changed
    catches = []
    inst.output('nameChanged').event += lambda val: catches.append(val)

    self.assertEquals(catches, [])
    inst.input('name').event('2nd name')
    self.assertEquals(catches, ['2nd name'])