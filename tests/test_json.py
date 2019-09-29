from unittest import TestCase
from cfgr.event import Event

from cfgr import Runtime, Type, Instance, Json

class Product:
  def __init__(self):
    self.name = ''
    self.afterResetEvent = Event()
    self.parent = None

  def setName(self, v):
    if v == self.name:
      return

    self.name = v

  def setParent(self, product):
    self.parent = product

  def reset(self):
    self.setName('')
    self.afterResetEvent.fire()

  @staticmethod
  def cfgr(builder):
    """
    by default, the Runtime.add_type(<Type>) method will look for a static cfgr method.
    """
    builder.addInput('name').string(lambda v,obj: obj.setName(v))
    #builder.addInput('reset').apply(lambda inp,obj: inp.event.subscribe(obj.reset))
    builder.addInput('reset').signal_to_method(lambda obj: obj.reset)
    builder.addOutput('afterReset').from_event(lambda obj: obj.afterResetEvent)

    builder.addInput('parent').object(lambda v,obj: obj.setParent(v))

class TestJson(TestCase):

  def test_apply(self):
    json_text = '{\
      "Product#1": {"name": "Product #1", "reset":"#Reset1" },\
      "Product#2": {"name": "Product no. 2", "afterReset": "#Reset1, #reset3" },\
      "Product#3": {"name": "Product3", "reset": "#reset3", "parent": "Product#1" },\
      "Product#3/Product#4": {"name": "Product4" }\
    }'

    # create runtime
    runtime = Runtime()
    # create Product type
    typ = runtime.add_type(typeClass=Product)
    
    loader = Json.Loader(runtime=runtime, text=json_text)

    inst1 = loader.create("Product#1")
    inst2 = loader.create("Product#2")
    inst3 = loader.create("Product#3")
    inst4 = runtime.instances[3]

    self.assertEquals(inst1.object.name, 'Product #1')
    self.assertEquals(inst2.object.name, 'Product no. 2')
    self.assertEquals(inst3.object.name, 'Product3')
    self.assertEquals(inst4.object.name, 'Product4')

    # verify that inst2 afterReset property fires #ResetAll event, which resets Product1
    self.assertEquals(inst1.object.name, 'Product #1')
    inst2.object.reset()
    self.assertEquals(inst1.object.name, '')
    self.assertEquals(inst3.object.name, '')
    self.assertEquals(inst4.object.name, 'Product4')

    # verify product3's parent is product1
    self.assertEquals(inst3.object.parent, inst1.object)
    self.assertEquals(inst4.object.parent, None)


