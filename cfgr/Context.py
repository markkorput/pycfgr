from evento import Event



def is_event_data(data):
  return data.strip().startswith('#')



class Context:
  def __init__(self, runtime):
    self.runtime = runtime

  def get_events(self, eventsdata):
    """
    Returns a list of pyevento.Event instances for the string-based eventsdata.
    Example of valid eventsdata: "#event1, #event2,#event3" (returns three event instances)
    """
    return list(map(lambda id: self.runtime.get_event(id.strip()), eventsdata.strip().split(',')))

  def create_instance(self, id, data=None):
    typ = data['type'] if data and 'type' in data else self._defaultTypeFor(id)
    inst = self.runtime.create_instance(typ, id)

    if data:
      self.cfg(inst, data)
    return inst

  def _defaultTypeFor(self, id):
    split = id.split('_')
    return split[0] if len(split) == 2 else id

  def cfg(self, instance, data):
    for v in data:
      input = instance.input(v)
      output = instance.output(v)

      if input and output:
        print('ambiguous attribute name: {}, references both an input and an output port'.format(v))
        continue

      attr_data = data[v]

      if input:
        self.apply_input(input, attr_data, runtime=self.runtime)
      elif output:
        self.apply_output(output, attr_data, runtime=self.runtime)
      elif v == 'inputs':
        self.apply_inputs(instance, attr_data)
      elif v == 'outputs':
        self.apply_outputs(instance, attr_data)
      # elif v.startswith('in-')
      # elif v.startswith('out-')

  def apply_inputs(self, instance, input_data):
    pass

  def apply_outputs(self, instance, output_data):
    pass

  def apply_input(self, port, data, runtime):
    if (data.startswith('#')):
      if not runtime:
        print("Don't have runtime to apply event input")
        return

      e = self.runtime.get_event(data)
      e.subscribe(port.event.fire)
      return

    port.event.fire(data)

  def apply_output(self, port, data, runtime):

    if not is_event_data(data):
      print('Unsupported output data, events should be prefixed with a hash symbol (#) and can be comma-separarted')
      return

    if not runtime:
      print("Don't have runtime to apply event input")
      return

    events = self.get_events(data)

    for e in events:
      port.event.subscribe(e.fire)
