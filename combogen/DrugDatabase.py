import requests
import json
from collections import OrderedDict

class DrugDatabase(object):
  URL = "http://tripsit.me/combo_beta.json"

  def __init__(self, config):
    self._combos = requests.get(DrugDatabase.URL).json()
    self._config = config
    self._drug_groups = []
    self.load_groups()

  @property
  def drug_groups(self):
    return self._drug_groups #type: [DrugGroup]

  @property
  def drugs(self):
    drug_list = [drug
                 for group in self._drug_groups
                 for drug in group]
    return drug_list

  def add_group(self, group):
    self._drug_groups.append(group)

  def load_groups(self):
    for config_group, colour in self._config.table_order_with_colours:
      drug_group = DrugGroup(colour)

      for drug_name in config_group:
        drug = Drug(drug_name, drug_group, self)
        drug_group.add_drug(drug)

      self.add_group(drug_group)

  def interaction(self, drug_a, drug_b):
    try:
      return self._combos[drug_a.name.lower()][drug_b.name.lower()]['status']
    except KeyError:
      return "unknown"

  def __iter__(self):
    return iter(self.drugs)


class DrugGroup(object):
  def __init__(self, colour: str):
    self._colour = colour
    self._drugs = list()

  @property
  def colour(self):
    return self._colour

  @property
  def drugs(self):
    return self._drugs

  def add_drug(self, drug):
    self._drugs.append(drug)

  def __iter__(self):
    return iter(self._drugs)

  def __len__(self):
    return len(self._drugs)

  def __getitem__(self, item):
    return self._drugs[item]


class Drug(object):
  def __init__(self, name, group, database):
    self._id = name.lower()
    self._name = name
    self._group = group
    self._db = database

  @property
  def id(self):
    return self._id

  @property
  def name(self):
    return self._name

  @property
  def group(self):
    return self._group

  def interaction_with(self, other):
    return self._db.interaction(self, other)

  def __eq__(self, other):
    return isinstance(other, Drug) and self.id == other.id

  def __str__(self):
    return self._name
