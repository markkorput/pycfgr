from .PortBuilder import PortBuilder
from .Port import Port

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
