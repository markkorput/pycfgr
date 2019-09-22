from .PortBuilder import OutputBuilder, InputBuilder
from .Port import Port

class TypeBuilder:
  def __init__(self, context=None):
    self.portDefs = []
    self.context = context

  def addInput(self, id):
    portbuilder = InputBuilder(id)
    self.portDefs.append(portbuilder.portDef)
    return portbuilder

  def addOutput(self, id):
    portbuilder = OutputBuilder(id)
    self.portDefs.append(portbuilder.portDef)
    return portbuilder

  def getPortDefs(self):
    return self.portDefs
