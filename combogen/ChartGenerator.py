from combogen.DrugDatabase import DrugDatabase
from combogen.Config import Config
from combogen.Utils import file_to_dataURI
from jinja2 import Environment, PackageLoader
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

class ChartGenerator(object):
  
  def __init__(self):
    self._config = Config(os.path.join(PROJECT_ROOT, 'config.json'))
    self._drug_database = DrugDatabase(self._config)
    self._env = Environment(loader=PackageLoader('combogen', 'templates'), lstrip_blocks=True)

  def generate(self):
    template = self._env.get_template('combo-chart-inline.html')
    return template.render(title="Test", style=None, logo_url=None)

  def debug(self):
    for group in self._drug_database.drug_groups:
      msg = "{} ({}): ".format(group.colour, len(group))
      for drug in group:
        msg += "{}, ".format(drug.name)
      print(msg)

if __name__ == "__main__":
  chart_generator = ChartGenerator()
  #print(chart_generator.generate())
  #chart_generator.debug()
