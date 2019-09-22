from .Port import Port

class PortDef:
  def __init__(self, id, flags):
    self._id = id
    self.flags = flags
    self.applyFuncs = []

  def createPortFor(self, object, tools):
    # create port
    p = Port(self._id, self.flags, tools)

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


class InputBuilder(PortBuilder):
  def __init__(self, id):
    PortBuilder.__init__(self, id, Port.INPUT)

  def string(self, valueObjectFunc):
    applyFunc = lambda port,obj: port.tools.converter(port.event).onString(lambda val: valueObjectFunc(val, obj))
    self.apply(applyFunc)

  def int(self, valueObjectFunc):
    applyFunc = lambda port,obj: port.tools.converter(port.event).onInt(lambda val: valueObjectFunc(val, obj))
    self.apply(applyFunc)

  def bool(self, valueObjectFunc):
    applyFunc = lambda port,obj: port.tools.converter(port.event).onBool(lambda val: valueObjectFunc(val, obj))
    self.apply(applyFunc)

  def float(self, valueObjectFunc):
    applyFunc = lambda port,obj: port.tools.converter(port.event).onFloat(lambda val: valueObjectFunc(val, obj))
    self.apply(applyFunc)


  def bool_to_method(self, objMethodFunc):
    applyFunc = lambda port, obj: port.tools.converter(port.event).onBool(objMethodFunc(obj))
    self.apply(applyFunc)

  def int_to_method(self, objMethodFunc):
    applyFunc = lambda port, obj: port.tools.converter(port.event).onInt(objMethodFunc(obj))
    self.apply(applyFunc)

  def string_to_method(self, objMethodFunc):
    applyFunc = lambda port, obj: port.tools.converter(port.event).onString(objMethodFunc(obj))
    self.apply(applyFunc)

  def float_to_method(self, objMethodFunc):
    applyFunc = lambda port, obj: port.tools.converter(port.event).onFloat(objMethodFunc(obj))
    self.apply(applyFunc)

  def connect(self, objMethodFunc):
    self.connect_to_method(objMethodFunc)

  def connect_to_method(self, objMethodFunc):
    """
    uses the objMethodFunc to fetch a method from our object
    which will be invoked when the port's event is fired
    """
    applyFunc = lambda port, obj: port.event.subscribe(objMethodFunc(obj))
    self.apply(applyFunc)
  
  def connect_to_event(self, objEventFunc):
    """
    uses the objEventFunc to fetch an event from our object
    which will be fired when the port's event is fired
    """
    applyFunc = lambda port, obj: port.event.subscribe(objEventFunc(obj).fire)
    self.apply(applyFunc)  

  def object(self, valueObjectFunc):
    def applyfunc(port, obj):
      valfunc = lambda val: valueObjectFunc(port.tools.getObject(val), obj)
      port.event.subscribe(valfunc)

    self.apply(applyfunc)

  def string_to_method(self, objMethodFunc):
    # TODO; perform string payload validation
    self.connect_to_method(objMethodFunc)

class OutputBuilder(PortBuilder):
  def __init__(self, id):
    PortBuilder.__init__(self, id, Port.OUTPUT)

  def connect(self, eventFromObjectFunc):
    self.connect_to_event(eventFromObjectFunc)

  def connect_to_event(self, eventFromObjectFunc):
    """
    uses the func to fetch an event from our object
    which will be fired by this output's event
    """
    applyFunc = lambda port, obj: eventFromObjectFunc(obj).subscribe(port.event)
    self.apply(applyFunc)
