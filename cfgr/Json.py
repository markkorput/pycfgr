
def apply(instance, json_data):
  for v in json_data:
    input = instance.input(v)
    output = instance.output(v)

    if input and output:
      print('ambiguous attribute name: {}, references both an input and an output port'.format(v))
      continue

    if input:
      apply_input(input, json_data[v])
    elif output:
      apply_output(output, json_data[v])
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

def apply_input(port, data):
  port.event.fire(data)

def apply_output(port, data):
  pass