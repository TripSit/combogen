import json
import os

TRANSLATIONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'translations'))


class Config(object):
    def __init__(self, path):
        with open(path) as f:
            self._config = json.load(f)
        print(self._config)
        self._translations = dict()
        for file in os.listdir(TRANSLATIONS_DIR):
            if (file.endswith(".json")):
                lang = file.split(".")[0].lower()

                with open(os.path.join(TRANSLATIONS_DIR, file)) as f:
                    self._translations[lang] = json.load(f)

    @property
    def config(self):
        return self._config

    @property
    def url(self):
        return self._config['url']
    
    @property
    def local_file(self):
        return self._config['local_file']
    
    @property
    def version(self):
        return self._config['version']

    @property
    def width(self):
        return self._config['chart']['width']

    @property
    def height(self):
        return self._config['chart']['height']

    @property
    def rel_resources_path(self):
        return self._config['chart']['htmlRelativeResources']

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

    """
    Override an interaction (e.g. Serotonin Syndrome -> Dangerous)
    """

    def rewrite_interaction(self, interaction):
        try:
            return self._config['rewriteInteraction'][interaction.lower()]
        except KeyError:
            return interaction

    """
    Get CSS class for given interaction
    """

    def interaction_to_class(self, interaction):
        try:
            return self._config['interactionClass'][interaction.lower()][0]
        except KeyError:
            return self._config['interactionClass']['fallback'][0]

    """
    Get CSS class for interaction icon (FontAwesome)
    """

    def interaction_icon(self, interaction):
        try:
            return self._config['interactionClass'][interaction.lower()][1]
        except KeyError:
            return self._config['interactionClass']['fallback'][1]

    def is_drug_in_config(self, drug):
        all_drugs = list(map(str.lower, self.all_drugs_in_order))
        return drug.lower() in all_drugs

    def translate(self, lang, property):
        try:
            return self._translations[lang.lower()][property.lower()]
        except KeyError:
            print("{} translation for {} not found".format(lang, property))
            return property

    def translate_drug(self, lang, drug):
        try:
            return self._translations[lang.lower()]['drugs'][drug.lower()]
        except KeyError:
            print("{} translation for {} not found".format(lang, drug))
            return drug

    def translate_interaction(self, lang, interaction):
        try:
            return self._translations[lang.lower()]['interactions'][interaction.lower()]
        except KeyError:
            print("{} translation for {} not found".format(lang, interaction))
            return interaction
