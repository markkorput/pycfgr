```
class SetView {
  public:
    void cfg(builder) {
      builder
        .addInput<Cam>("cam", (&cam, obj) => obj.camera = cam)
        .addInput<CamSelect>("camSelect", (camsel, obj) => obj.setCameraFetcher([camsel](){ return camsel.getCamera(); }))
        .addInput<ci::vec3>("pos", &SetView::pos)
        .addInput<ci::vec3>("lookAt", &SetView::lookAt)
        .addInput("on", &SetView::set);

    }
}



class Json {
  public:
    void config(builder) {
      builder
        .addInput<std::string>("resourceFile", (v, obj) => obj.setFilePath(ci::app::getResourcePath(v))
        .addInput("load", &Json::load)
        .addInput("save", &Json::load)
        .addOutput<cms::ModelCollection>("saving", (signal, obj) => {
          obj.saveSignal.connect([signal] => signal->emit(json));
        })
        .addOutput<cms::ModelCollection>("saving", &Json::saveSignal);
        .addOutput<cms::ModelCollection>("saved", &Json::savedSignal);
    }
}

-- SALONE//ciCMS::cfg --
"Runner.Json": {"resourceFile": "preferences.json",
    "loadOn": "setup,manualLoad", "saveOn": "exit,manualSave",
    "loadEmit": "jsonLoaded", "saveEmit": "jsonSaving",
    "Cam": "Runner.Cam0,Runner.Cam1,Runner.Cam2,Runner.Cam3,Runner.Cam4",
    "verbose":false },


"Runner.Json": {
  "inputs": {"file": "{resources}/preferences.json", "load": "setup,manualLoad", "save": "exit,manualSave", "Cam": "Cam0,Cam1,Cam2,...", "verbose":false},
  "output": {"load":"jsonLoaded", "saving":"jsonSaving", "saved":"jsonSaved"}},
  "output-saved": "jsonSaved",
  "out-saved": "jsonSaved",
  "out-saving": "jsonSaving"
  }
 


UserView1
UserView1.Camera
UserView1.ScreenArea
```