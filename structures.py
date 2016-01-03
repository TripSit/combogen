import requests

class DrugDatabase(object):
  URL = "http://tripsit.me/combo.json"

  def __init__(self):
    self._database = dict()

  def populate(self):
    self._database = requests.get(DrugDatabase.URL).json() #type: dict

  def interaction(self, drug_a, drug_b):
    try:
      return self._database[drug_a][drug_b]
    except KeyError:
      return "Unknown combination"

  def interactions(self, drug):
    try:
      return self._database[drug]
    except KeyError:
      return "Unknown drug"