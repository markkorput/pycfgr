
def apply(instance, json_data, runtime=None):
  for v in json_data:
    input = instance.input(v)
    output = instance.output(v)

    if input and output:
      print('ambiguous attribute name: {}, references both an input and an output port'.format(v))
      continue

    if input:
      apply_input(input, json_data[v], runtime=runtime)
    elif output:
      apply_output(output, json_data[v], runtime=runtime)
    elif v == 'inputs':
      apply_inputs(instance, json_data[v])
    elif v == 'outputs':
      apply_outputs(instance, json_data[v])
    # elif v.startswith('in-')
    # elif v.startswith('out-')

def apply_inputs(instance, input_data):
  pass

def apply_outputs(instance, output_data):
  pass

def apply_input(port, data, runtime):
  if (data.startswith('#')):
    if not runtime:
      print("Don't have runtime to apply event input")
      return

    e = runtime.getEvent(data)
    e.subscribe(port.event.fire)
    return

  port.event.fire(data)

def apply_output(port, data, runtime):

  if not is_event_data(data):
    print('Unsupported output data, events should be prefixed with a hash symbol (#) and can be comma-separarted')
    return

  if not runtime:
    print("Don't have runtime to apply event input")
    return

  events = get_events(data, runtime)

  for e in events:
    port.event.subscribe(e.fire)


def is_event_data(data):
  return data.strip().startswith('#')

def get_events(data, runtime):
  """
  Returns a list of pyevento.Event instances for the string-based json data.
  Example of valid data: "#event1, #event2,#event3" (returns three event instances)
  """
  return list(map(lambda id: runtime.getEvent(id.strip()), data.strip().split(',')))
