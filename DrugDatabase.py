import requests
import json
from collections import OrderedDict

class DrugDatabase(object):
  URL = "http://tripsit.me/combo_beta.json"

  def __init__(self):
    db = OrderedDict(requests.get(DrugDatabase.URL).json()) #type: OrderedDict
    self._drugs  = dict()
    for name in db:
      self._drugs[name] = Drug(name, db[name])

  @property
  def drugs(self):
    return self._drugs

class Drug(object):
  def __init__(self, name, combinations):
    self._name = name
    self._combinations = combinations

  @property
  def name(self):
    return self._name

  @property
  def combinations(self):
    return self._combinations
