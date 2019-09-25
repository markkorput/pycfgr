from cfgr.event import Event
import platform, os.path

class StartupScriptInstaller:
  def __init__(self, startupScriptPath, script, beforeCommand=None):
    self.beforeCommand = beforeCommand
    self.script = script
    self.startupScriptPath = startupScriptPath

  def isHookInstalled(self):
    alreadyContainsScript = False

    if not os.path.isfile(self.startupScriptPath):
      return False

    with open(self.startupScriptPath, "r") as f:
      content = f.read()
      alreadyContainsScript = self.script in content
    return alreadyContainsScript

  def install(self):
    if self.isHookInstalled():
      print('[LaunchOnStartup] hook already installed')
      return

    # should be insert our script code before a potential existing command?
    if self.beforeCommand:
      originalcontent = ''
      if os.path.isfile(self.startupScriptPath):
        with open(self.startupScriptPath, "r") as f:
          originalcontent = f.read()
    
      # can we find that specified in command in the existing file content?
      if self.beforeCommand in originalcontent:
        idx = originalcontent.find(self.beforeCommand)
        before_part = originalcontent[:idx]
        after_part = originalcontent[idx:]
        newcontent = "{}\n\n{}\n\n{}".format(before_part, self.script, after_part)

        with open(self.startupScriptPath, "w") as f:
          f.write(newcontent)

        return

    # simply append to end of file
    with open(self.startupScriptPath, "a") as f:
      f.write("\n"+self.script)

    print('[LaunchOnStartup] startup hook written to: {}'.format(self.startupScriptPath))

  def uninstall(self):
    if not self.isHookInstalled():
      print('[LaunchOnStartup] no hook found to uninstall in startup file: {}'.format(self.startupScriptPath))
      return
    
    content = ''
    with open(self.startupScriptPath, "r") as f:
      content = f.read()

    with open(self.startupScriptPath, "w") as f:
      f.write(content.replace(self.script, ''))

    print('[LaunchOnStartup] startup script removed from file: {}'.format(self.startupScriptPath))

  def getScript(self, cwd, data, component, startevent):
    cmd = 'python -m cfgr.app'

    if cwd:
      cmd = 'cd {} && {}'.format(cwd, cmd)

    if data:
      cmd = '{} -d {}'.format(cmd, data)

    if component:
      cmd = '{} -c {}'.format(cmd, component)

    if startevent:
      cmd = '{} -s {}'.format(cmd, startevent)

    return "# cfgr.StartupOnLaunch START\n{}\n# cfgr.StartupOnLaunch END".format(cmd)


class LinuxInstaller(StartupScriptInstaller):
  def __init__(self, cwd, data, component, startevent):
    StartupScriptInstaller.__init__(self, "/etc/rc.local", self.getScript(cwd, data, component, startevent), beforeCommand="exit 0")

class DarwinInstaller(StartupScriptInstaller): # TODO
  def __init__(self, cwd, data, component, startevent):
    StartupScriptInstaller.__init__(self, "rc.local.test", self.getScript(cwd, data, component, startevent), beforeCommand="exit 0")

class LaunchOnStartup:
  """
  Installs and uninstalls launch-on-startup scripts
  """
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('cwd').string_to_method(lambda obj: obj.setCwd)
    builder.addInput('data').string_to_method(lambda obj: obj.setDataPath)
    builder.addInput('component').string_to_method(lambda obj: obj.setComponentId)
    builder.addInput('startevent').string_to_method(lambda obj: obj.setStartEvent)
    builder.addInput('install').signal_to_method(lambda obj: obj.install)
    builder.addInput('uninstall').signal_to_method(lambda obj: obj.uninstall)
    builder.addOutput('done').from_event(lambda obj: obj.doneEvent)

  def __init__(self):
    self.cwd = None
    self.dataPath = None
    self.componentId = None
    self.startEventId = None
    self.doneEvent = Event()

  def setCwd(self, cwd):
    self.cwd = os.path.abspath(cwd)

  def setDataPath(self, p):
    self.dataPath = p
  
  def setComponentId(self, id):
    self.componentId = id

  def setStartEvent(self, ev):
    self.startEventId = ev

  def install(self):
    installer = self.getInstaller()

    if not installer:
      print('[LaunchOnStartup] {} is not a supported platfrom (yet).'.format(platform.system()))
      return

    installer.install()
    self.doneEvent()

  def uninstall(self):
    installer = self.getInstaller()
    if not installer:
      print('[LaunchOnStartup] {} is not a supported platfrom (yet).'.format(platform.system()))

    installer.uninstall()
    self.doneEvent()

  def getInstaller(self):
    # determine platform
    if platform.system() == 'Linux':
      installer = LinuxInstaller(self.cwd, self.dataPath, self.componentId, self.startEventId)
      return installer

    if platform.system() == 'Darwin': # mac
      installer = DarwinInstaller(self.cwd, self.dataPath, self.componentId, self.startEventId)
      return installer

    # pass
    return None
    
    