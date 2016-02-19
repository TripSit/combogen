import json
import os

class Config(object):
  def __init__(self, path):
    with open(path) as f:
      self._config = json.load(f)

  @property
  def config(self):
    return self._config

  @property
  def url(self):
    return self._config['url']

  @property
  def version(self):
    return self._config['version']

  @property
  def grouped_table_order(self):
    groups_with_names = list()

    for index, group in enumerate(self._config['tableOrder']):
      group_name = self._config['groupNames'][index]
      groups_with_names.append((group_name, group))

    return groups_with_names

  @property
  def all_drugs_in_order(self):
    return [drug
            for group in self._config['tableOrder']
            for drug in group]

  def rewriteInteraction(self, interaction):
    try:
      return self._config['rewriteInteraction'][interaction.lower()]
    except KeyError:
      return interaction

  def interaction_to_class(self, interaction):
    try:
      return self._config['interactionClass'][interaction.lower()][0]
    except KeyError:
      return self._config['interactionClass']['fallback'][0]

  def interaction_fa(self, interaction):
    try:
      return self._config['interactionClass'][interaction.lower()][1]
    except KeyError:
      return self._config['interactionClass']['fallback'][1]

  def is_drug_in_config(self, drug):
    all_drugs = list(map(str.lower, self.all_drugs_in_order))
    return drug.lower() in all_drugs
