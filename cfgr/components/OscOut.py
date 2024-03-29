from cfgr.event import Event
import socket, logging

DEPS = None # {'osc_message_builder': None, 'dispatcher': None}

def loadDeps():
  result = {}

  try:
    from pythonosc import udp_client
    result['udp_client'] = udp_client
  except ImportError:
    logging.getLogger(__name__).warning("failed to load pythonosc dependency; OscOout component will not work")

  return result

class OscOut:

  @staticmethod
  def cfgr(builder):
    ## outputs
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)
    builder.addInput('host').string_to_method(lambda obj: obj.setHost)
    builder.addInput('port').int_to_method(lambda obj: obj.setPort)
    builder.addInput('send').to_method(lambda obj: obj.sendMessage)

  """
  Osc sender client
  """
  def __init__(self):
    self.host = None
    self.port = 0
    self.isVerbose = False
    self.client = None

    self.connectEvent = Event()
    self.disconnectEvent = Event()
    self.messageEvent = Event()

  def __del__(self):
    self.disconnect()

  def setVerbose(self, v): self.isVerbose = v
  def setHost(self, host): self.host = host
  def setPort(self, port): self.port = port
  def isConnected(self): return self.client != None

  def connect(self):
    global DEPS
    host = self.host
    port = self.port

    if not host:
      print("[OscOut] no host, can't connect")
      return False
    
    if not DEPS:
      DEPS = loadDeps()

    # try:
    #     # self.client = OSC.OSCClient()
    #     # if target.endswith('.255'):
    #     #     self.logger.info('broadcast target detected')
    #     #     self.client.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # except OSC.OSCClientError as err:
    #     self.logger.error("OSC connection failure: {0}".format(err))
    #     return False

    if not DEPS['udp_client']:
      print("[OscOut] missing OSC dependency")
      return False

    self.client = DEPS['udp_client'].SimpleUDPClient(host, port)
    self.connected = True
    self.connectEvent(self)
    self.verbose("[OscOut] connected to {}:{}".format(host, self.port))
    return True

  def disconnect(self):
    if not self.isConnected():
      return

    # self.client.close()
    self.client = None
    self.disconnectEvent(self)
    self.verbose("[OscOut] disconnect from {0}:{1}".format(self.host, self.port))

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)

  def sendMessage(self, message):
    if not self.isConnected():
      if not self.connect():
        print("[OscOut] failed to connect")
        return

    addr, data = message
    try:
      self.client.send_message(addr, data)
      self.messageEvent(message, self)
      self.verbose('[OscOut] sent {0}:{1} - {2} [{3}]'.format(self.host, self.port, addr, ", ".join(map(lambda x: str(x), data))))
    #     # self.client.send(msg)s
    # except OSC.OSCClientError as err:
    #     pass
    except AttributeError as err:
      print('[OscOut {}:{}] send error: {}'.format(self.host, self.port, str(err)))
    except socket.gaierror as err:
      print('[OscOut {}:{}] failed send message: {}'.format(self.host, self.port, str(err)))