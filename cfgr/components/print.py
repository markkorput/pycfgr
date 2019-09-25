class Print:
  """
  A simple text-printing component
  """
  def doPrint(self, v):
    print(v)

  @staticmethod
  def cfgr(builder):
    ## outputs
    builder.addInput('on').string_to_method(lambda obj: obj.doPrint)