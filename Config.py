import json

class Config(object):
  CONFIG_FILE = "config.json"

  def __init__(self):
    with open(Config.CONFIG_FILE) as f:
      self._config = json.load(f)

  @property
  def config(self):
    return self._config
