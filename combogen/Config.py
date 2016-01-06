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
  def table_order_with_colours(self):
    order_with_colours = list()

    for index, group in enumerate(self._config['tableOrder']):
      group_colour = self._config['groupHeadingColours'][index]
      order_with_colours.append((group, group_colour))

    return order_with_colours

  @property
  def interaction_colour(self, interaction):
    pass