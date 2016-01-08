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
    self._db = DrugDatabase(self._config)
    self._env = Environment(loader=PackageLoader('combogen', 'templates'), lstrip_blocks=True, trim_blocks=True)

  def generate(self):
    template = self._env.get_template('combo-chart-inline.html')
    logo_data_uri = file_to_dataURI(os.path.join(PROJECT_ROOT, 'logo.svg'))
    app_data_uri = file_to_dataURI(os.path.join(PROJECT_ROOT, 'app_qr.svg'))
    support_data_uri = file_to_dataURI(os.path.join(PROJECT_ROOT, 'support_qr.svg'))
    image_urls = {
      'logo': logo_data_uri,
      'app': app_data_uri,
      'support': support_data_uri
    }
    return template.render(title="Guide to drug combinations", image_urls=image_urls, db=self._db, cfg=self._config)

  def find_missing_drugs(self):
    config_drugs = self._config.all_drugs_in_order
    json_drugs = self._db.combos.keys()

    missing_from_config = [drug for drug in json_drugs if not self._config.is_drug_in_config(drug)]
    missing_from_json = [drug for drug in config_drugs if not self._db.is_drug_in_combos(drug)]
    return (missing_from_json, missing_from_config)

  def find_missing_combos(self):
    """
    This function allows you to find missing drug combos or asymmetric dug combos
    (If LSD->MDMA combo is defined, but MDMA->LSD isn't - This will be improved soon).

    It will also return interactions which don't have CSS class defined in config.json
    (In "interactionClass" section)
    """
    missing = []
    missing_classes = set()
    for drug_in_config in self._config.all_drugs_in_order:
      for drug_in_json in self._db.combos.keys():
        drug_in_config = drug_in_config.lower()
        drug_in_json = drug_in_json.lower()
        if drug_in_config == drug_in_json:
          continue

        cfg_json_interaction = self._db.interaction(drug_in_config, drug_in_json)
        json_cfg_interaction = self._db.interaction(drug_in_json, drug_in_config)

        if cfg_json_interaction is None:
          missing.append((drug_in_config, drug_in_json))
        elif self._config.interaction_to_class(cfg_json_interaction) == "unknown":
          missing_classes.add(repr(cfg_json_interaction.lower()))

        if json_cfg_interaction is None:
          missing.append((drug_in_json, drug_in_config))
        elif self._config.interaction_to_class(json_cfg_interaction) == "unknown":
          missing_classes.add(repr(json_cfg_interaction.lower()))

    return (missing, missing_classes)

  def debug(self):
    print("== DRUG GROUPS IN DATABASE (FROM CONFIG) ==\r\n")
    for group in self._db.drug_groups:
      drug_names = [drug.name for drug in group]
      drugs_with_commas = ', '.join(drug_names)
      message = "{} ({}): {}".format(group.name, len(group), drugs_with_commas)
      print(message)

    #print("\r\n== DRUG COMBOS (RAW JSON) ==")
    #pp.pprint(self._drug_database._combos)

    print("\r\n== MISSING DRUGS (ASYMMETRIC JSON <-> CONFIG) ==\r\n")
    from_json, from_config = self.find_missing_drugs()
    print("Missing from JSON ({}): {}".format(len(from_json), ', '.join(from_json)))
    print("Missing from Config ({}): {}".format(len(from_config), ', '.join(from_config)))

    print("\r\n== MISSING DRUG COMBOS AND CSS CLASSES ==\r\n")
    missing_combos, missing_classes = self.find_missing_combos()
    missing_combos = ["{}+{}".format(a, b) for a, b in missing_combos]
    print("Missing combos ({}): {}".format(len(missing_combos), ', '.join(missing_combos)))
    print("Missing CSS classes ({}): {}".format(len(missing_classes), ', '.join(missing_classes)))

if __name__ == "__main__":
  chart_generator = ChartGenerator()
  chart_generator.debug()
  chart = chart_generator.generate()
  with open(os.path.join(PROJECT_ROOT, 'drug-combinations.html'), 'w+') as f:
    f.write(chart)