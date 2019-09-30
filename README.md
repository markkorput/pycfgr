# cfgr
[![Build Status](https://travis-ci.org/markkorput/pycfgr.svg)](https://travis-ci.org/markkorput/pycfgr)

## Install

```pip install cfgr```

## Usage

Create at cfgr.json file (see [examples](#examples) below) and run;

```python -m cfgr.app```

## Wait, _what_ is this?

pycfgr is part of a cross-language exploration in search of new ways to create software systems.

pycfgr builds on the work of earlier projects;
* [JavaLibUiBuilder (Java)](https://github.com/fusefactory/JavaLibUiBuilder)
* [py2030 (python)](https://github.com/markkorput/py2030)
* [ciCMS (C++/Cinder)](https://github.com/markkorput/cicms)
* [ciInfo (C++/Cinder)](https://github.com/markkorput/ciinfo)

The ```cfgr``` module provides a set of APIs that encourage separation of configuration from logic. It helps organising the application logic in small, modular components and lets you put those together through configuration (json) files to create complex systems. 

The approach borrows concepts from Visual Programming Languages (VPLs) which generally let you create instances of pre-built building blocks and connect them together to perform complex tasks. ```pycfgr``` translates these concepts back into a text-based development workflow.

[<img src="https://github.com/markkorput/pycfgr/raw/master/docs/vpl-02-maxmsp.png" alt="MaxMSP" height="150" />](https://github.com/markkorput/pycfgr/raw/master/docs/vpl-02-maxmsp.png)
[<img src="https://github.com/markkorput/pycfgr/raw/master/docs/vpl-01-blueprints.jpg" alt="Blueprints" height="150" />](https://github.com/markkorput/pycfgr/raw/master/docs/vpl-01-blueprints.jpg)
[<img src="https://github.com/markkorput/pycfgr/raw/master/docs/vpl-03-touchdesigner.png" alt="TouchDesigner" height="150" />](https://github.com/markkorput/pycfgr/raw/master/docs/vpl-03-touchdesigner.png)

_three well known examples of VPLs (from left to right); [Cyling '74's Max](https://cycling74.com/products/max/), [Unreal Engine's Blueprints](https://docs.unrealengine.com/en-US/Engine/Blueprints/index.html) and [Derivative's TouchDesigner](http://derivative.ca)_

Why?
* A text-based workflow using standard formats (like JSON) allows for the most flexible/customizable development pipelines and benefit of massive set of available tools (version control systems, text-editors, IDEs, command-line, ssh, etc.).
* Removing configuration (as much as possible) from your application code keeps the code clear and concise.
* Enforcing a modular component structure encourages best practices like the single responsibility principle and writing modular code that is truly reusable.
* Separating configuration from the logic provides possiblity to make and actuate changes at runtime (from minor properties to major application structures).

### Some history

Motivation for this exploration came from many years of experience in professional software development, specifically non web-based UI software development in C++ and Java using frameworks like OpenFrameworks, Cinder and Processing and noticing patterns of repetition, both in code and in general workflow. This experience lead to, initially, the [JavaLibUiBuilder](https://github.com/fusefactory/JavaLibUiBuilder) which builds on top of a UI framework ([JavaLibUi](https://github.com/fusefactory/JavaLibUi), inspired by the [ofxInterface](https://github.com/galsasson/ofxInterface) library for OpenFrameworks/C++), which started the concept of building and configuring application logic from json config files (which feels a bit like writing CSS from a web-page).

This concept was translated into C++ using in the [ciCMS](https://github.com/markkorput/cicms) package for the [Cinder](https://libcinder.org/) framework and extended to provide "native" events and states to further reduce the amount of custom application code that needs to be written to make the different components communicate.

## Examples

Below are some basic examples, see the [examples folder](https://github.com/markkorput/pycfgr/tree/master/examples) for more.

Each of these configurations can be invoked by saving them as a json file and then running:

```bash
python -m cfgr.app --data <path/to/configuration.json>
```

### Hello World

```json
{
  "App": {"started":"#sayhello", "stop":"#stopapp"},
  "App.string": {"value": "Hello World!", "in-emit":"#sayhello", "out-emit":"#print,#stopapp"},
  "App.Print": {"on": "#print"}
}
```

### Send OSC messages
The below configuration will send an OSC ```/play``` message to ```127.0.0.1:3002``` at an interval of 30 seconds (30000 milliseconds).

```json
{
  "App": {"started":"#start_play_interval", "update":"#update_play_interval"},
  "App/Interval": {"start": "#start_play_interval", "ms":30000, "update":"#update_play_interval", "action":"#send_play"},
  "App/OscOut": {"host": "127.0.0.1", "port": 3002, "in-send": "#msg"},
  "App/OscOut/OscMessage": {"address": "/play", "in-send": "#send_play", "out-send": "#msg"}
}
```

### Web-interface for remote control
The below configuration starts an HTTP server on port 8080 that serves all files in the ```./public``` folder via the ```127.0.0.1:8080/static``` url and provides two remote control operations via its "API endpoints": ```/api/start``` and ```/api/stop```.

```json
{
  "App": {"started": "#starthttp"},
  "App/HttpServer": {"port": 8080, "request-out":"#httprequest", "start":"#starthttp"},
  "App/HttpServer/static": {"type":"HttpScope", "scope":"/static", "request-in": "#httprequest", "servePath": "./public"},
  "App/HttpServer/api": {"type":"HttpScope", "scope":"/api", "request-in": "#httprequest", "unscoped":"#apirequest"},
  "App/HttpServer/api/start": {"type":"HttpScope","scope":"/start", "request-in": "#apirequest", "match": "#action_start", "response":200, "verbose": true},
  "App/HttpServer/api/stop": {"type":"HttpScope","scope":"/stop", "request-in": "#apirequest", "match": "#action_stop", "response":200, "verbose": true},

  "App/string": {"value": "STARTED, woohoo!", "in-emit":"#action_start", "out-emit":"#print"},
  "App/string": {"value": "STOPPED, boring :/", "in-emit":"#action_stop", "out-emit":"#print"},
  "App/Print": {"on": "#print"}
} 
```