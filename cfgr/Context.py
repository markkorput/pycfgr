from cfgr.event import Event
import re

class Context:
  
  ID_SEPARATOR = '/'
  NAME_SEPARATOR = '#'

  def __init__(self, runtime, verbose=False):
    self.runtime = runtime
    self.runtime.port_tools.eventsFunc = self.get_events
    self.isVerbose = verbose

  def get_events(self, eventsdata):
    """
    Returns a list of pyevento.Event instances for the string-based eventsdata.
    Example of valid eventsdata: "#event1, #event2,#event3" (returns three event instances)
    """
    def iter(v):
      return self.runtime.get_event(v.strip())

    return list(map(iter, eventsdata.strip().split(',')))  
    # return list(map(lambda id: self.runtime.get_event(id.strip()), eventsdata.strip().split(',')))

  def create_instance(self, id, data=None):
    self.verbose('Context.create_instance: {}'.format(id))

    typ = data['type'] if data and 'type' in data else self._defaultTypeFor(id)
    inst = self.runtime.create_instance(typ, id)

    if not inst:
      print('[Context] could not instantiate type: {}'.format(typ))
      return None

    if data:
      self.cfg(inst, data)
    return inst

  def _defaultTypeFor(self, id):
    split = id.split(Context.ID_SEPARATOR)[-1].split(Context.NAME_SEPARATOR)
    typ = split[0] if len(split) == 2 else id
    # print('_defaultTypeFor: {} --> {}'.format(id, typ))
    return typ

  def cfg(self, instance, data):
    for v in data:
      input = instance.input(v)
      output = instance.output(v)

      if input and output:
        print('ambiguous attribute name: {}, references both an input and an output port'.format(v))
        continue

      attr_data = data[v]

      if v.startswith('in-') and not input:
        input = instance.input(re.compile('^in-').sub('', v))
      elif v.endswith('-in') and not input:
        input = instance.input(re.compile('-in$').sub('', v))
      elif v.startswith('out-') and not output:
        output = instance.output(re.compile('^out-').sub('', v))
      elif v.endswith('-out') and not output:
        output = instance.output(re.compile('-out$').sub('', v))

      if input:
        input.event.fire(attr_data)
        continue

      if output:
        events = []
        if (type(attr_data) == type([])):
          events = list(map(lambda eid: self.runtime.get_event(eid), attr_data))
        else:
          events = self.get_events(attr_data)

        for e in events:
          output.event.subscribe(e.fire)
        continue

      if v == 'inputs':
        continue # TODO

      elif v == 'outputs':
        continue # TODO

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
