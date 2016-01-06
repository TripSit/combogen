from combogen.DrugDatabase import DrugDatabase
from combogen.Config import Config
from jinja2 import Template

class ChartGenerator(object):
  
  def __init__(self):
    self._drug_database = DrugDatabase()
    self._config = Config()

  def generate(self):
    template = Template("put some template or template file load here")
    return template.render(drugs=self._drug_database, config=self._config)

if __name__ == "__main__":
  chart_generator = ChartGenerator()
  print(chart_generator.generate())
