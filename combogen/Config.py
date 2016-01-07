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
  def grouped_table_order(self):
    groups_with_names = list()

    for index, group in enumerate(self._config['tableOrder']):
      group_name = self._config['groupNames'][index]
      groups_with_names.append((group_name, group))

    return groups_with_names

  def interaction_to_class(self, interaction):
    try:
      return self._config['interactionClass'][interaction][0]
    except KeyError:
      return self._config['interactionClass']['fallback'][0]

  def interaction_fa(self, interaction):
    try:
      return self._config['interactionClass'][interaction][1]
    except KeyError:
      return self._config['interactionClass']['fallback'][1]