from unittest import TestCase
from evento import Event
import json

from cfgr import Runtime, Type, Instance, Json

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

  def cfgr(builder):
    """
    by default, the Runtime.add_type(<Type>) method will look for a static cfgr method.
    """
    builder.addInput('name').string(lambda v,obj: obj.setName(v))
    #builder.addOutput('nameChanged').apply(lambda outp,obj: obj.nameChangedEvent.subscribe(outp.event))
    builder.addOutput('nameChanged').connect(lambda obj: obj.nameChangedEvent)
    #builder.addInput('reset').apply(lambda inp,obj: inp.event.subscribe(obj.reset))
    builder.addInput('reset').connect(lambda obj: obj.reset)

class TestJson(TestCase):

  def test_apply(self):
    json_text = '{ "Product": {"name":"Product #1"}, "Product2": {"name": "Product no. 2"} }'
    data = json.loads(json_text)
    
    # create runtime
    runtime = Runtime()
    # create Product type
    typ = runtime.add_type(typeClass=Product)
    # create Product instance
    inst = runtime.create_instance('Product')

    self.assertEquals(inst.object.name, '')

    # configure Product instance using json data
    Json.apply(inst, data['Product'])
    
    self.assertEquals(inst.object.name, 'Product #1')