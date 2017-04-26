# Octothorpe
---
**I learned a lot about python writing this, however I discovered [Home Assistant](https://github.com/home-assistant/home-assistant), which is very similar and is far ahead of whatever I could have done on my own. It has a great developer community, I suggest you check it out.**

Octothorpe is rules engine and services framework. Basically it is a partial IFTTT clone which can be used to create custom services which can optionally spawn events that other services can consume via rule mappings while also providing real-time synchronous responses to the injector.

---

### Requirements
* Base
  * Python 3.6
  * lxml
* Slack
  * requests
  * six
  * websockets
  * websocket-client
* Scheduler
  * croniter

### Usage
Setup:
```bash
./run.py --config config.xml --setup
```

Running the server:
```bash
./run.py --config config.xml
```
