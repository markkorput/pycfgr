class PortTools:
  """
  PortTools is a collection of interfaces through which ports can Ports can fetch
  specific types of data
  """
  def __init__(self, objectFunc=None):
    self.objectFunc = objectFunc

  def getObject(self, data):
    return self.objectFunc(data)
