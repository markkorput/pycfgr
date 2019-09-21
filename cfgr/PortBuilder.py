from .Port import Port

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
