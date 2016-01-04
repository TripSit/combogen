import requests
import svgwrite
from svgwrite import percent
from collections import OrderedDict

class DrugDatabase(object):
  URL = "http://tripsit.me/combo_beta.json"
  RESPONSE_UNKNOWN_COMBO = "Unknown combination"
  RESPONSE_UNKNOWN_DRUG = "Unknown drug"

  def __init__(self):
    self._database = dict()

  @property
  def database(self):
    return self._database

  def populate(self):
    self._database = OrderedDict(requests.get(DrugDatabase.URL).json()) #type: OrderedDict

  def interaction(self, drug_a, drug_b):
    try:
      return self._database[drug_a][drug_b]['status']
    except KeyError:
      print(DrugDatabase.RESPONSE_UNKNOWN_COMBO + " ({} + {})".format(drug_a, drug_b))
      return DrugDatabase.RESPONSE_UNKNOWN_COMBO

  def interactions(self, drug):
    try:
      return self._database[drug]
    except KeyError:
      return DrugDatabase.RESPONSE_UNKNOWN_DRUG


class ComboChart(svgwrite.Drawing):
  INTERACTION_SAFE_SYNERGY = 'Low Risk & Synergy'.lower()
  INTERACTION_SAFE_NO_SYNERGY = 'Low Risk & No Synergy'.lower()
  INTERACTION_SAFE_DECREASE = 'Low Risk & Decrease'.lower()
  INTERACTION_CAUTION = 'Caution'.lower()
  INTERACTION_UNSAFE = 'Unsafe'.lower()
  INTERACTION_DANGEROUS = 'Dangerous'.lower()
  INTERACTION_SEROTONIN_SYNDROME = 'Serotonin Syndrome'.lower()
  INTERACTION_UNKNOWN = 'Unknown'.lower()

  INTERACTION_COLOR_MAP = {
    INTERACTION_SAFE_SYNERGY: 'darkgreen',
    INTERACTION_SAFE_NO_SYNERGY: 'lightgreen',
    INTERACTION_SAFE_DECREASE: 'blue',
    INTERACTION_CAUTION: 'yellow',
    INTERACTION_UNSAFE: 'orange',
    INTERACTION_DANGEROUS: 'red',
    INTERACTION_SEROTONIN_SYNDROME: 'purple',
    INTERACTION_UNKNOWN: 'white'
  }


  X_TABLE_MARGIN = 2
  Y_TABLE_MARGIN = 10
  CELL_MARGIN = 0.03

  def __init__(self, database, filename="drug-combinations.svg", size=('100%', '100%'), **extra):
    super(ComboChart, self).__init__(filename, size, **extra)
    self._database = database
    self.item_count = len(self._database.database)
    self.X_CELL_SIZE = (100 - 2 * ComboChart.X_TABLE_MARGIN) / (self.item_count + 2) - ComboChart.CELL_MARGIN
    self.Y_CELL_SIZE = (100 - 2 * ComboChart.Y_TABLE_MARGIN) / (self.item_count + 2) - ComboChart.CELL_MARGIN

  def interaction_color(self, interaction):
    try:
      return ComboChart.INTERACTION_COLOR_MAP[interaction.strip().lower()]
    except KeyError:
      return ComboChart.INTERACTION_COLOR_MAP[ComboChart.INTERACTION_UNKNOWN]

  def add_logo(self, position, size):
    pass

  def add_title(self, text="Guide to drug combinations", style="font-size:10mm;fill:white"):
    self.add(self.text(text, ('50%', '15mm'), text_anchor='middle', style=style))

  def add_cell(self, y_index, x_index, color):
    x_pos = ComboChart.X_TABLE_MARGIN + x_index * (self.X_CELL_SIZE + ComboChart.CELL_MARGIN)
    y_pos = ComboChart.Y_TABLE_MARGIN + y_index * (self.Y_CELL_SIZE + ComboChart.CELL_MARGIN)
    pos = (percent(x_pos), percent(y_pos))
    size = (percent(self.X_CELL_SIZE), percent(self.Y_CELL_SIZE))

    self.add(self.rect(pos, size, fill=color))

  def add_label(self, text, y_index, x_index, text_style='fill:white'):
    x_pos = ComboChart.X_TABLE_MARGIN + x_index * (self.X_CELL_SIZE + ComboChart.CELL_MARGIN) + self.X_CELL_SIZE / 2
    y_pos = ComboChart.Y_TABLE_MARGIN + y_index * (self.Y_CELL_SIZE + ComboChart.CELL_MARGIN) + self.Y_CELL_SIZE * 0.75
    pos = (percent(x_pos), percent(y_pos))

    self.add(self.text(text, pos, text_anchor='middle', style=text_style))

  def add_legend(self):
    pass