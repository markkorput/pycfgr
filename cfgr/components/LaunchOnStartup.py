from cfgr.event import Event
import platform, os.path, re, sys

def getScript(cwd, data, component, startevent=None, background=True, outfile=None):
  # to make sure we'll uses the currently active python
  # even if this environment isn't activated (which not unlikely if this is
  # a script that's ran at startup)
  cmd = '{} -m cfgr.app'.format(sys.executable)

  if cwd:
    cmd = 'cd {} && {}'.format(cwd, cmd)

  if data:
    cmd = '{} -d {}'.format(cmd, data)

  if component:
    cmd = '{} -c {}'.format(cmd, component)

  if startevent:
    cmd = '{} -s {}'.format(cmd, startevent)

  if outfile:
    cmd = '{} &>> {}'.format(cmd, outfile)

  if background:
    cmd = '{} &'.format(cmd)

  return '\n# The line below is generated by cfgr.StartupOnLaunch\n{}\n\n'.format(cmd)

class StartupScriptInstaller:
  def __init__(self, startupScriptPath, script, localScriptPath=None, beforeCommand=None):
    self.beforeCommand = beforeCommand
    self.startupScript = script
    self.startupScriptPath = startupScriptPath
    
    self.localScriptPath = None
    if localScriptPath:
      self.localScriptPath = os.path.abspath(localScriptPath)
      self.localScript = script
      # change startupScript to invoke local script
      self.startupScript = '\n# The line below is generated by cfgr.StartupOnLaunch\n{}\n\n'.format(self.localScriptPath)
 
  def isHookInstalled(self):
    alreadyContainsScript = False

    if not os.path.isfile(self.startupScriptPath):
      return False

    with open(self.startupScriptPath, "r") as f:
      content = f.read()
      alreadyContainsScript = self.startupScript in content

    return alreadyContainsScript

  def install(self):
    # write local startup script
    if self.localScriptPath:
      if os.path.exists(self.localScriptPath):
        print('[LaunchOnStartup] {} already exists'.format(self.localScriptPath))
        return False
      
      with open(self.localScriptPath, "w") as f:
        f.write(self.localScript)
        print('[LaunchOnStartup] local script file written to: {}'.format(self.localScriptPath))

    if self.isHookInstalled():
      print('[LaunchOnStartup] hook already installed')
      return False


    # should be insert our script code before a potential existing command?
    if self.beforeCommand:
      if os.path.isfile(self.startupScriptPath):
        originalcontent = ''
        with open(self.startupScriptPath, "r") as f:
          originalcontent = f.read()

        match = re.search('^\s*{}\s*\n'.format(self.beforeCommand), originalcontent)
        if not match:
          match = re.search('\n\s*{}\s*\n'.format(self.beforeCommand), originalcontent)
        if not match:
          match = re.search('\n\s*{}\s*$'.format(self.beforeCommand), originalcontent)
        if not match:
          match = re.search('^\s*{}\s*$'.format(self.beforeCommand), originalcontent)

        if match:
          idx = match.span()[0]+1
          before_part = originalcontent[:idx]
          after_part = originalcontent[idx:]
          newcontent = "{}\n{}\n{}".format(before_part, self.startupScript, after_part)

          with open(self.startupScriptPath, "w") as f:
            f.write(newcontent)

          print('[LaunchOnStartup] startup hook inserted into: {}'.format(self.startupScriptPath))
          return True

    # simply append to end of file
    with open(self.startupScriptPath, "a") as f:
      f.write("\n"+self.startupScript)

    print('[LaunchOnStartup] startup hook appended to: {}'.format(self.startupScriptPath))
    return True

  def uninstall(self):
    if not self.isHookInstalled():
      print('[LaunchOnStartup] no hook found to uninstall in startup file: {}'.format(self.startupScriptPath))
      return False
    
    content = ''
    with open(self.startupScriptPath, "r") as f:
      content = f.read()

    with open(self.startupScriptPath, "w") as f:
      f.write(content.replace(self.startupScript, ''))

    print('[LaunchOnStartup] startup script removed from file: {}'.format(self.startupScriptPath))

    if self.localScriptPath:
      if os.path.exists(self.localScriptPath):
        os.remove(self.localScriptPath)
        print('local script file ({}) removed'.format(self.startupScriptPath, self.localScriptPath))

    return True

class LinuxInstaller(StartupScriptInstaller):
  def __init__(self, cwd, data, component, startevent):
    StartupScriptInstaller.__init__(self, "/etc/rc.local", getScript(cwd, data, component, startevent), localScriptPath="./launch_on_startup.sh", beforeCommand="exit 0")

class DarwinInstaller(StartupScriptInstaller): # TODO
  def __init__(self, cwd, data, component, startevent):
    StartupScriptInstaller.__init__(self, "rc.local.test", getScript(cwd, data, component, startevent), localScriptPath="./launch_on_startup.sh", beforeCommand="exit 0")

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
    self.failedEvent = Event()

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

    if installer.install():
      self.doneEvent()
    else:
      self.failedEvent()

  def uninstall(self):
    installer = self.getInstaller()
    if not installer:
      print('[LaunchOnStartup] {} is not a supported platfrom (yet).'.format(platform.system()))

    if installer.uninstall():
      self.doneEvent()
    else:
      self.failedEvent()

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
    
    