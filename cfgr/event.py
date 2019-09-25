try:
  from evento import Event
except ImportError:
  Event = None
except ModuleNotFoundError:
  Event = None

if not Event:
  from .embeddedEvento import Event
