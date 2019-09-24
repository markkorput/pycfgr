import json as jsonlib
import re
from .Context import Context

class Loader:
  def __init__(self, runtime, data=None, text=None, file=None, verbose=False):
    self.context = Context(runtime, verbose=verbose)
    self.data = data

    if not self.data:
      if file:
        if verbose: print('Loading json file: {}'.format(file))
        with open(file, "r") as f:
          text = f.read()

      if text:
        self.data = jsonlib.loads(text) 

      if not self.data:
        self.data = {}


  def create(self, id, recursive=True):
    instance_data = self.data[id] if id in self.data else {}
    instance = self.context.create_instance(self.idToType(id), data=instance_data)

    if recursive:
      childids = self.findChildIdsFor(id, recursive=True)

      for childid in childids:
        child_data = self.data[childid] if childid in self.data else None
        self.context.create_instance(self.idToType(childid), data=child_data)

    return instance

  def findChildIdsFor(self, parent, recursive=True):
    childIds = []
    for key in self.data:
      if self.isDirectChild(key, parent):
        childIds.append(key)

        if recursive:
          childIds += self.findChildIdsFor(key, recursive=True)

    return childIds

  def isDirectChild(self, key, parentKey):
    pattern = "^{}\.\w+".format(parentKey)
    return re.match(pattern, key) != None

  def idToType(self, id):
    return id.split('.')[-1]