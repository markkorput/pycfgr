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

  def string(self, stringFunc):
    applyFunc = lambda port, obj: port.event.subscribe(lambda v: stringFunc(v, obj))
    self.apply(applyFunc)

  def connect(self, connectFunc):
    """
    uses the connectFunc to fetch a method from our object
    which will be fires when the port's event is fired
    """
    applyFunc = lambda port, obj: port.event.subscribe(connectFunc(obj))
    self.apply(applyFunc)
  
  def object(self, valueObjectFunc):
    def applyfunc(port, obj):
      valfunc = lambda val: valueObjectFunc(port.tools.getObject(val), obj)
      port.event.subscribe(valfunc)

    self.apply(applyfunc)

class OutputBuilder(PortBuilder):
  def __init__(self, id):
    PortBuilder.__init__(self, id, Port.OUTPUT)

  def connect(self, eventFromObjectFunc):
    """
    uses the func to fetch an event from our object
    which will be forwarded by this output's event
    """
    applyFunc = lambda port, obj: eventFromObjectFunc(obj).subscribe(port.event)
    self.apply(applyFunc)
