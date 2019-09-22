class Print:
  """
  A simple text-printing component
  """
  def print(self, v):
    print(v)

  @staticmethod
  def cfgr(builder):
    ## outputs
    builder.addInput('on').string_to_method(lambda obj: obj.print)