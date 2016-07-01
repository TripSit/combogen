from combogen.DrugDatabase import DrugDatabase
from combogen.Config import Config
from jinja2 import Environment, PackageLoader, FileSystemLoader
from datetime import datetime, timezone
import os

CURRENT_PATH = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_PATH, '..'))
TEMPLATE_ROOT = os.path.abspath(os.path.join(CURRENT_PATH, 'templates'))
TRANSLATIONS_ROOT = os.path.abspath(os.path.join(CURRENT_PATH, 'translations'))
TOOLS_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'tools'))

class ChartGenerator(object):
    def __init__(self):
        self._config = Config(os.path.join(PROJECT_ROOT, 'config.json'))
        self._db = DrugDatabase(self._config)
        self._env = Environment(loader=FileSystemLoader([TEMPLATE_ROOT, TRANSLATIONS_ROOT]), lstrip_blocks=True,
                                trim_blocks=True)

    def generate(self, lang):
        template = self._env.get_template('combo-chart-full.html')

        time_generated = datetime.now(timezone.utc)
        status_msg = "Version {}<br>".format(self._config.version)
        status_msg += "Generated on {} at {} UTC".format(time_generated.strftime("%d %b %Y"),
                                                         time_generated.strftime("%H:%M"))

        return template.render(status=status_msg, lang=lang, db=self._db, cfg=self._config)

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
        unknown_interactions = set()
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
                    unknown_interactions.add(repr(a_to_b))

                if b_to_a is None:
                    missing.add((drug_b, drug_a))
                elif self._config.interaction_to_class(b_to_a) == "unknown":
                    unknown_interactions.add(repr(b_to_a))

                if (a_to_b is not None and b_to_a is not None) and a_to_b != b_to_a:
                    if "{}+{}".format(drug_b, drug_a) not in asymmetric_combos.keys():
                        asymmetric_combos["{}+{}".format(drug_a, drug_b)] = "'{}', '{}'".format(a_to_b, b_to_a)

        return (missing, asymmetric_combos, unknown_interactions)

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

        print("\r\n== MISSING DRUG COMBO DEFINITIONS AND  UNKNOWN INTERACTIONS ==\r\n")
        missing_combos, asymmetric_combos, unknown_interactions = self._find_missing_combos()
        missing_combos = ["{}->{}".format(a, b) for a, b in missing_combos]
        print("Combos missing in JSON ({}): {}".format(len(missing_combos), ', '.join(missing_combos)))
        print("Unknown interactions ({}): {}".format(len(unknown_interactions), ', '.join(unknown_interactions)))

        print("\r\n== ASYMMETRIC DRUG COMBOS ==\r\n")
        asymmetric_combos = ["{} ({})".format(combo, diff) for combo, diff in asymmetric_combos.items()]
        print("Asymmetric combos ({}): {}".format(len(asymmetric_combos), ", ".join(asymmetric_combos)))
