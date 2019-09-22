import json as jsonlib
from .Context import Context

class Loader:
  def __init__(self, runtime, data=None, json=None, file=None, verbose=False):
    self.context = Context(runtime)
    self.data = data

    if not self.data:
      if file:
        if verbose: print('Loading json file: {}'.format(file))
        with open(file, "r") as f:
          json = f.read()

      if json:
        self.data = jsonlib.loads(json) 

  def create(self, id):
    instance_data = self.data[id] if id in self.data else None
    instance = self.context.create_instance(id, data=instance_data)
    return instance
