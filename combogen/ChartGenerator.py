from combogen.DrugDatabase import DrugDatabase
from combogen.Config import Config
from combogen.Utils import file_to_dataURI
from jinja2 import Environment, PackageLoader
from datetime import datetime, timezone
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

class ChartGenerator(object):
  
  def __init__(self):
    self._config = Config(os.path.join(PROJECT_ROOT, 'config.json'))
    self._db = DrugDatabase(self._config)
    self._env = Environment(loader=PackageLoader('combogen', 'templates'), lstrip_blocks=True, trim_blocks=True)

  def generate(self, version):
    template = self._env.get_template('combo-chart-inline.html')
    logo_data_uri = file_to_dataURI(os.path.join(PROJECT_ROOT, 'logo.svg'))
    app_data_uri = file_to_dataURI(os.path.join(PROJECT_ROOT, 'app_qr.svg'))
    support_data_uri = file_to_dataURI(os.path.join(PROJECT_ROOT, 'support_qr.svg'))
    image_urls = {
      'logo': logo_data_uri,
      'app': app_data_uri,
      'support': support_data_uri
    }
    generated = datetime.now(timezone.utc)
    status_msg = "Version {}<br>".format(version)
    status_msg += "Generated on {} at {} UTC".format(generated.strftime("%d %b %Y"), generated.strftime("%H:%M"))
    return template.render(title="Guide to Drug Combinations", status=status_msg, image_urls=image_urls, db=self._db, cfg=self._config)

  def _find_missing_drugs(self):
    config_drugs = self._config.all_drugs_in_order
    json_drugs = self._db.combos.keys()

    missing_from_config = [drug for drug in json_drugs if not self._config.is_drug_in_config(drug)]
    missing_from_json = [drug for drug in config_drugs if not self._db.is_drug_in_combos(drug)]
    return (missing_from_json, missing_from_config)

  def _find_missing_combos(self):
    """
    Find missing or asymmetric drug combos
    (If DrugA->DrugB combo is defined, but DrugB->DrugA isn't).

    It will also return interactions which don't have CSS class defined in config.json
    (In "interactionClass" section)

    Only checks combos for drugs defined in config
    """
    all_drugs = self._config.all_drugs_in_order

    missing = set()
    missing_classes = set()
    asymmetric_combos = dict()
    for drug_a in all_drugs:
      for drug_b in all_drugs:
        if drug_a == drug_b:
          continue

        a_to_b = self._db.interaction(drug_a, drug_b, strict=True)
        b_to_a = self._db.interaction(drug_b, drug_a, strict=True)

        if a_to_b is None:
          missing.add((drug_a, drug_b))
        elif self._config.interaction_to_class(a_to_b) == "unknown":
          missing_classes.add(repr(a_to_b))

        if b_to_a is None:
          missing.add((drug_b, drug_a))
        elif self._config.interaction_to_class(b_to_a) == "unknown":
          missing_classes.add(repr(b_to_a))

        if (a_to_b is not None and b_to_a is not None) and a_to_b != b_to_a:
          if "{}+{}".format(drug_b, drug_a) not in asymmetric_combos.keys():
            asymmetric_combos["{}+{}".format(drug_a, drug_b)] = "'{}', '{}'".format(a_to_b, b_to_a)

    return (missing, missing_classes, asymmetric_combos)

  def debug(self):
    print("== DRUG GROUPS IN DATABASE (FROM CONFIG) ==\r\n")
    for group in self._db.drug_groups:
      drug_names = [drug.name for drug in group]
      drugs_with_commas = ', '.join(drug_names)
      message = "{} ({}): {}".format(group.name, len(group), drugs_with_commas)
      print(message)

    print("\r\n== MISSING DRUGS (ASYMMETRIC JSON <-> CONFIG) ==\r\n")
    from_json, from_config = self._find_missing_drugs()
    print("Missing from JSON ({}): {}".format(len(from_json), ', '.join(from_json)))
    print("Missing from Config ({}): {}".format(len(from_config), ', '.join(from_config)))

    print("\r\n== MISSING DRUG COMBOS AND CSS CLASSES ==\r\n")
    missing_combos, missing_classes, asymmetric_combos = self._find_missing_combos()
    missing_combos = ["{}->{}".format(a, b) for a, b in missing_combos]
    print("Combos missing in JSON ({}): {}".format(len(missing_combos), ', '.join(missing_combos)))
    print("Missing CSS classes for interactions ({}): {}".format(len(missing_classes), ', '.join(missing_classes)))

    print("\r\n== ASYMMETRIC DRUG COMBOS ==\r\n")
    asymmetric_combos = ["{} ({})".format(combo, diff) for combo, diff in asymmetric_combos.items()]
    print("Asymmetric combos ({}): {}".format(len(asymmetric_combos), ", ".join(asymmetric_combos)))
if __name__ == "__main__":
  chart_generator = ChartGenerator()
  chart_generator.debug()
  chart = chart_generator.generate("3.0 [PRE-RELEASE|DO-NOT-USE - SOME DATA MAY BE INACCURATE]")
  with open(os.path.join(PROJECT_ROOT, 'drug-combinations.html'), 'w+') as f:
    f.write(chart)
