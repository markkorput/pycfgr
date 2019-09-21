class Instance:
  def __init__(self, object, ports):
    self.object = object
    self.ports = ports

  def input(self, id):
    for p in self.ports:
      if p.isInput() and p._id == id:
        return p
    return None

  def output(self, id):
    for p in self.ports:
      if p.isOutput() and p._id == id:
        return p
    return None
