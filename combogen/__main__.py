from combogen.ChartGenerator import ChartGenerator, PROJECT_ROOT, TEMPLATE_ROOT, TRANSLATIONS_ROOT
import os

chart_generator = ChartGenerator()
chart_generator.debug()

for file in os.listdir(TRANSLATIONS_ROOT):
  if (file.endswith(".json")):
    lang = file.split(".")[0]
    chart = chart_generator.generate(lang)

    with open(os.path.join(PROJECT_ROOT, 'drug-combinations-{}.html'.format(lang)), 'w+') as f:
      f.write(chart)
