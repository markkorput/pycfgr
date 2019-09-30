import threading
from cfgr.event import Event

DEPS = None # {'osc_server': None, 'dispatcher': None}

def loadDeps():
  result = {}
  try:
    from pythonosc import dispatcher
    from pythonosc import osc_server
    result['osc_server'] = osc_server
    result['dispatcher'] = dispatcher
  except ImportError:
    # logging.getLogger(__name__).warning("failed to load pythonosc dependency; OscIn component will not work")
    pass

  return result

class OscIn:
  
  @staticmethod
  def cfgr(builder):
    ## outputs
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)
    builder.addInput('host').string_to_method(lambda obj: obj.setHost)
    builder.addInput('port').int_to_method(lambda obj: obj.setPort)
    builder.addInput('connect').signal_to_method(lambda obj: obj.connect)
    
    builder.addInput('disconnect').signal_to_method(lambda obj: obj.disconnect)
    builder.addOutput('message').from_event(lambda obj: obj.messageEvent)
    builder.addOutput('connected').from_event(lambda obj: obj.connectedEvent)
    builder.addOutput('disconnected').from_event(lambda obj: obj.disconnectedEvent)

  def __init__(self):
    self.server = None
    self.isConnected = False
    self.running = False
    # self.osc_map = None
    self.thread = None
    self.host = ''
    self.port = 0
    self.isVerbose = False

    self.connectedEvent = Event()
    self.disconnectedEvent = Event()
    self.messageEvent = Event()

  def __del__(self):
    # self.msgEventMapping = None
    # self.event_manager = None
    # self.stop()
    self.disconnect()

  def connect(self):
    global DEPS

    if self.isConnected:
      return False

    if DEPS == None:
      DEPS = loadDeps()

      if not 'osc_server' in DEPS or not 'dispatcher' in DEPS:
        print('[OscIn] could not load dependencies')

    if not 'osc_server' in DEPS or not 'dispatcher' in DEPS:
      return False

    disp = DEPS['dispatcher'].Dispatcher()
    disp.map("*", self._onOscMsg)
    # disp.map("/logvolume", print_compute_handler, "Log volume", math.log)

    result = False
    try:
      self.server = DEPS['osc_server'].ThreadingOSCUDPServer((self.host, self.port), disp)
      self.server.daemon_threads = True
      self.server.timeout = 1.0
      # self.server = DEPS['osc_server'].BlockingOSCUDPServer((self.host, self.port), disp)
      def threadFunc():
          try:
              self.server.serve_forever()
          except KeyboardInterrupt:
              pass
          self.server.server_close()

      self.thread = threading.Thread(target = threadFunc);
      self.thread.start()
      # set internal connected flag
      result = True
    except OSError as err:
      print("[OscIn] Could not start OSC server: "+str(err))

    if result:
      # notify
      self.verbose("[OscIn {0}:{1}] server running".format(self.host, str(self.port)))
      self.connectedEvent(self)

    self.isConnected = result
    return result

  def disconnect(self):
    if self.isConnected:
      if self.server:
        self.server._BaseServer__shutdown_request = True
        self.server.shutdown()
        self.server = None
      self.isConnected = False
      self.disconnectedEvent(self)
      self.verbose('[OscIn {0}:{1}] server stopped'.format(self.host, str(self.port)))

  def _onOscMsg(self, addr, *args):
    # skip touch osc touch-up events
    # if len(data) == 1 and data[0] == 0.0:
    #     return
    self.verbose('[OscIn {0}:{1}] received {2} [{3}]'.format(self.host, self.port, addr, ", ".join(map(lambda x: str(x), args))))
    self.messageEvent((addr, args))
    # # trigger events based on incoming messages if configured
    # if addr in self.msgEventMapping:
    #     self.logger.debug('triggering output event: {0}'.format(self.msgEventMapping[addr]))
    #     self.event_manager.fire(self.msgEventMapping[addr])
    # elif self.autoAddrToEvent:
    #     self.logger.debug('triggering auto-output event: {0}'.format(addr))
    #     self.event_manager.fire(addr)

    # # this doesnt work yet?!
    # if addr in self.argEvents.keys():
    #     print('triggering argEvent:', addr)
    #     self.event_manager.get(self.argEvents[addr]).fire(args)

  def setVerbose(self, v): self.isVerbose = v
  def setHost(self, host): self.host = host
  def setPort(self, port): self.port = port
  def verbose(self, msg):
    if self.isVerbose:
      print(msg)