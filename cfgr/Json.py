from .Context import Context

class Loader:
  def __init__(self, runtime, data={}):
    self.context = Context(runtime)
    self.data = data

  def create(self, id):
    instance_data = self.data[id] if id in self.data else None
    instance = self.context.create_instance(id, data=instance_data)
    return instance
