from unittest import TestCase
from evento import Event
import json

from cfgr import Runtime, Type, Instance, Json

class Product:
  def __init__(self):
    self.name = ''
    self.nameChangedEvent = Event()
    self.afterResetEvent = Event()

  def setName(self, v):
    if v == self.name:
      return

    self.name = v
    self.nameChangedEvent(self.name)

  def reset(self):
    self.setName('')
    self.afterResetEvent.fire()

  def cfgr(builder):
    """
    by default, the Runtime.add_type(<Type>) method will look for a static cfgr method.
    """
    builder.addInput('name').string(lambda v,obj: obj.setName(v))
    #builder.addOutput('nameChanged').apply(lambda outp,obj: obj.nameChangedEvent.subscribe(outp.event))
    builder.addOutput('nameChanged').connect(lambda obj: obj.nameChangedEvent)
    #builder.addInput('reset').apply(lambda inp,obj: inp.event.subscribe(obj.reset))
    builder.addInput('reset').connect(lambda obj: obj.reset)
    builder.addOutput('afterReset').connect(lambda obj: obj.afterResetEvent)

class TestJson(TestCase):

  def test_apply(self):
    json_text = '{\
      "Product1": {"name":"Product #1", "reset":"#Reset1" },\
      "Product2": {"name": "Product no. 2", "afterReset": "#Reset1, #reset3" },\
      "Product3": {"name": "Product3", "reset": "#reset3" }\
    }'

    data = json.loads(json_text)
    
    # create runtime
    runtime = Runtime()
    # create Product type
    typ = runtime.add_type(typeClass=Product)
    
    # create Product 1 instance
    inst1 = runtime.create_instance('Product')

    # verify initial state
    self.assertEquals(inst1.object.name, '')

    # configure Product instance using json data
    Json.apply(inst1, data['Product1'], runtime=runtime)
    self.assertEquals(inst1.object.name, 'Product #1')

    # create and configure Product2 instance using different json data
    inst2 = runtime.create_instance('Product')
    Json.apply(inst2, data['Product2'], runtime=runtime)
    self.assertEquals(inst2.object.name, 'Product no. 2')

    # create and configure Product3
    inst3 = runtime.create_instance('Product')
    Json.apply(inst3, data['Product3'], runtime=runtime)
    self.assertEquals(inst3.object.name, 'Product3')

    # verify that inst2 afterReset property fires #ResetAll event, which resets Product1
    self.assertEquals(inst1.object.name, 'Product #1')
    inst2.object.reset()
    self.assertEquals(inst1.object.name, '')
    self.assertEquals(inst3.object.name, '')
