import requests
import json
from collections import OrderedDict

class DrugDatabase(object):

  def __init__(self, config):
    self._combos = requests.get(config.url).json()
    self._config = config
    self._drug_groups = []
    self.load_groups()

  @property
  def drug_groups(self):
    return self._drug_groups

  @property
  def drugs(self):
    drug_list = [drug
                 for group in self._drug_groups
                 for drug in group]
    return drug_list

  @property
  def combos(self) -> dict:
    return self._combos

  def load_groups(self):
    for group_name, config_group in self._config.grouped_table_order:
      drug_group = DrugGroup(group_name)

      for drug_name in config_group:
        drug = Drug(drug_name, drug_group, self)
        drug_group.add_drug(drug)

      self.add_group(drug_group)

  def add_group(self, group):
    self._drug_groups.append(group)

  def interaction(self, drug_a, drug_b, strict=False):
    drug_a_name = drug_a.lower() if isinstance(drug_a, str) else drug_a.name.lower()
    drug_b_name = drug_b.lower() if isinstance(drug_b, str) else drug_b.name.lower()
    try:
      interaction = self._combos[drug_a_name][drug_b_name]['status']
      return self._config.rewriteInteraction(interaction)
    except KeyError:
      if not strict:
        try:
          interaction = self._combos[drug_b_name][drug_a_name]['status']
          return self._config.rewriteInteraction(interaction)
        except KeyError:
          return 'NXDRUG'
      else:
        return 'NXDRUG'

  def is_drug_in_combos(self, drug):
    all_drugs = list(map(str.lower, self._combos.keys()))
    return drug.lower() in all_drugs

  def __iter__(self):
    return iter(self.drugs)

  def __len__(self):
    return sum([len(group) for group in self.drug_groups])


class DrugGroup(object):
  def __init__(self, name: str):
    self._name = name
    self._drugs = list()

  @property
  def name(self):
    return self._name

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

  def __eq__(self, other):
    return isinstance(other, Drug) and self.id == other.id

  def __str__(self):
    return self._name
