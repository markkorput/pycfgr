from unittest import TestCase
from evento import Event

from cfgr import Runtime, Type, Instance

class Product:
  def __init__(self):
    self.name = ''
    self.nameChangedEvent = Event()

  def setName(self, v):
    if v == self.name:
      return

    self.name = v
    self.nameChangedEvent(self.name)

  def reset(self):
    self.setName('')

  @staticmethod
  def cfgr(builder):
    """
    by default, the Runtime.add_type(<Type>) method will look for a static cfgr method.
    """
    builder.addInput('name').string(lambda v,obj: obj.setName(v))
    #builder.addOutput('nameChanged').apply(lambda outp,obj: obj.nameChangedEvent.subscribe(outp.event))
    builder.addOutput('nameChanged').connect(lambda obj: obj.nameChangedEvent)
    #builder.addInput('reset').apply(lambda inp,obj: inp.event.subscribe(obj.reset))
    builder.addInput('reset').connect(lambda obj: obj.reset)
    


class TestRuntime(TestCase):
  def test_simple_product_type(self):
    # create runtime
    runtime = Runtime()

    # create Product type
    self.assertEquals(runtime.types, [])
    typ = runtime.add_type(typeClass=Product)
    self.assertEquals(runtime.types, [typ])

    # create instance of Product type
    self.assertEquals(runtime.instances, [])
    inst = runtime.create_instance('Product')
    self.assertEquals(runtime.instances, [inst])

    # verify we received an Instance with a Product object
    self.assertEquals(type(inst), type(Instance(None, None)))
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

    # verify the reset input resets the product's name
    inst.input('reset').event()
    self.assertEquals(inst.object.name, '')
    self.assertEquals(catches, ['2nd name', ''])

    # cleanup
    runtime.remove_instance(inst)
    self.assertEquals(runtime.instances, [])
