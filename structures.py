import requests
import svgwrite
import json
import base64
from svgwrite import percent
from collections import OrderedDict

class DrugDatabase(object):
  CONFIG_FILE = "config.json"
  URL = "http://tripsit.me/combo_beta.json"
  RESPONSE_UNKNOWN_COMBO = "Unknown combination"
  RESPONSE_UNKNOWN_DRUG = "Unknown drug"

  def __init__(self):
    self._database = dict()
    self._config = dict()

  @property
  def database(self):
    return self._database

  @property
  def config(self):
    return self._config

  def populate(self):
    self._database = OrderedDict(requests.get(DrugDatabase.URL).json()) #type: OrderedDict
    config_file = open(DrugDatabase.CONFIG_FILE) 
    self._config = json.load(config_file)

  def interaction(self, drug_a, drug_b):
    drug_a = drug_a.lower()
    drug_b = drug_b.lower()
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

  def find_missing(self):
    missing_in_config = []
    missing_in_json = []

    for group in self.config['tableOrder']:
      for drug in group:
        missing_in_json.append(drug.lower())

    for drug in self.database.keys():
      try:
        missing_in_json.remove(drug.lower())
      except ValueError:
        missing_in_config.append(drug.lower())

    return (missing_in_config, missing_in_json)

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
    INTERACTION_SAFE_SYNERGY: '#31b149',
    INTERACTION_SAFE_NO_SYNERGY: '#84cf92',
    INTERACTION_SAFE_DECREASE: '#006cb3',
    INTERACTION_CAUTION: '#d5c625',
    INTERACTION_UNSAFE: '#d98427',
    INTERACTION_DANGEROUS: '#d5c625',
    INTERACTION_SEROTONIN_SYNDROME: '#684099',
    INTERACTION_UNKNOWN: 'white'
  }


  X_TABLE_MARGIN = 2
  Y_TABLE_MARGIN = 10
  CELL_MARGIN = 0.03

  def __init__(self, database, filename="drug-combinations.svg", size=('100%', '100%'), **extra):
    super(ComboChart, self).__init__(filename, size, **extra)
    self._database = database
    self.item_count = sum(sum(1 for drug in category) for category in self._database.config['tableOrder'])
    self.X_CELL_SIZE = (100 - 2 * ComboChart.X_TABLE_MARGIN) / (self.item_count + 2) - ComboChart.CELL_MARGIN
    self.Y_CELL_SIZE = (100 - 2 * ComboChart.Y_TABLE_MARGIN) / (self.item_count + 2) - ComboChart.CELL_MARGIN

  def interaction_color(self, interaction):
    try:
      return ComboChart.INTERACTION_COLOR_MAP[interaction.strip().lower()]
    except KeyError:
      return ComboChart.INTERACTION_COLOR_MAP[ComboChart.INTERACTION_UNKNOWN]

  def add_logo(self):
    with open('logo.svg') as f:
      logo = f.read().encode('utf-8')
      encoded = base64.b64encode(logo).decode('utf-8')
      dataURI = 'data:image/svg+xml;base64,{}'.format(encoded)

      position = (percent(ComboChart.X_TABLE_MARGIN), 0)
      size = (percent(ComboChart.Y_TABLE_MARGIN), ) * 2
      self.add(self.image(dataURI, position, size))

  def add_title(self, text="Guide to drug combinations", style="font-size:250%;fill:white"):
    position = ('50%', percent(ComboChart.Y_TABLE_MARGIN * 0.75))
    self.add(self.text(text, position, text_anchor='middle', style=style))

  def add_cell(self, y_index, x_index, color):
    x_pos = ComboChart.X_TABLE_MARGIN + x_index * (self.X_CELL_SIZE + ComboChart.CELL_MARGIN)
    y_pos = ComboChart.Y_TABLE_MARGIN + y_index * (self.Y_CELL_SIZE + ComboChart.CELL_MARGIN)
    pos = (percent(x_pos), percent(y_pos))
    size = (percent(self.X_CELL_SIZE), percent(self.Y_CELL_SIZE))

    self.add(self.rect(pos, size, fill=color))

  def add_label(self, text, y_index, x_index, color='white', text_style='font-size:0.6rem'):
    x_pos = ComboChart.X_TABLE_MARGIN + x_index * (self.X_CELL_SIZE + ComboChart.CELL_MARGIN) + self.X_CELL_SIZE / 2
    y_pos = ComboChart.Y_TABLE_MARGIN + y_index * (self.Y_CELL_SIZE + ComboChart.CELL_MARGIN) + self.Y_CELL_SIZE * 0.75
    pos = (percent(x_pos), percent(y_pos))

    self.add(self.text(text, pos, text_anchor='middle', fill=color, style=text_style))

  def add_legend(self):
    pass
