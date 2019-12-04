from cfgr.event import Event
import os.path, re
import cgi

# from urllib.parse import urlparse
urlparse = None
try: # python3
  import urllib.parse # python3  
  urlparse = urllib.parse.urlparse
except ImportError:
  try: #python2
    import urlparse # python2
    urlparse = urlparse.urlparse
  except ImportError:
    print('[HttpScope] failed to load url parse dependencies')
    urlparse = None


class HttpFileHandler:
  @staticmethod
  def cfgr(builder):
    # inputs
    builder.addInput('request').to_method(lambda obj: obj.processRequest)
    builder.addInput('response').to_method(lambda obj: obj.setResponse)
    builder.addInput('saveTo').string_to_method(lambda obj: obj.setSaveTo)
    builder.addInput('saveToFolder').string_to_method(lambda obj: obj.setSaveToFolder)
    builder.addInput('verbose').bool_to_method(lambda obj: obj.setVerbose)
    # builder.addInput('keepExtension').bool_to_method(lambda obj: obj.setKeepExtension)
    builder.addInput('fileFormName').string_to_method(lambda obj: obj.setFileFormName)

    # outputs
    #builder.addOutput('match').from_event(lambda obj: obj.matchEvent)
    builder.addOutput('saved').from_event(lambda obj: obj.savedEvent)

  def __init__(self):
    self.responseCode = None
    self.isVerbose = False
    self.saveTo = None
    self.saveToFolder = None
    # self.keepExtension = False
    self.fileFormName = 'file'

    self.savedEvent = Event()

  def setResponse(self, val):
    self.responseCode = val
  
  def setSaveTo(self, val):
    self.saveTo = os.path.abspath(os.path.expanduser(val)) #val

  def setSaveToFolder(self, val):
    self.saveToFolder = os.path.abspath(os.path.expanduser(val)) #val

  # def setKeepExtension(self, val):
  #   self.keepExtension = val

  def setFileFormName(self, val):
    self.fileFormName = val

  def processRequest(self, req):
    form = cgi.FieldStorage(
        fp=req.handler.rfile, #self.rfile,
        headers=req.handler.headers, #self.headers,
        environ={'REQUEST_METHOD':'PUT', # 'POST',
                  'CONTENT_TYPE':req.handler.headers['Content-Type'],
                  })

    formfile = form[self.fileFormName]
    filename = formfile.filename
    data = formfile.file.read()
    file_length = req.handler.headers['content-length']

    filepath = "./%s" % filename
    if self.saveTo:
      filepath = self.saveTo
    if self.saveToFolder:
      filepath = "%s/%s" % (self.saveToFolder, filename)
    else:
      print("WARNING, no saveTo or saveToFolder option specified, saving to default path: %s" % filepath)

    open(filepath, "wb").write(data)
    # print(req.handler.headers['content-length'])

    # req.handler.respond("uploaded %s, thanks")
    req.handler.send_response(201, 'Created')
    req.handler.end_headers()    
    reply_body = 'Saved "%s"\n' % filename
    req.handler.wfile.write(reply_body.encode('utf-8'))

    self.verbose('[HttpFileHandler] wrote {} bytes to: {}'.format(file_length, filepath))
    self.savedEvent(filepath)

  def setVerbose(self, v):
    self.isVerbose = v

  def verbose(self, msg):
    if self.isVerbose:
      print(msg)
