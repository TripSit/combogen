from combogen.ChartGenerator import ChartGenerator, PROJECT_ROOT, TEMPLATE_ROOT, TRANSLATIONS_ROOT,  TOOLS_ROOT
from combogen.Config import Config

import os
import subprocess

RENDER_SCRIPT_PATH = os.path.join(TOOLS_ROOT, 'render.js')
OUTPUT_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, 'output'))
HTML_PATH = os.path.join(OUTPUT_PATH, 'html')
PNG_PATH = os.path.join(OUTPUT_PATH, 'png')
PDF_PATH = os.path.join(OUTPUT_PATH, 'pdf')
config = Config(os.path.join(PROJECT_ROOT, 'config.json'))

try:
    os.makedirs(HTML_PATH)
except FileExistsError:
    pass

try:
    os.makedirs(PNG_PATH)
except FileExistsError:
    pass

try:
    os.makedirs(PDF_PATH)
except FileExistsError:
    pass

try:
    print('> Starting chart generation...')
    chart_generator = ChartGenerator()
    chart_generator.debug()

    # for file in os.listdir(TRANSLATIONS_ROOT):
    #     if (file.endswith(".json")):
    #         lang = file.split(".")[0]
    lang = 'en'
    chart = chart_generator.generate(lang)

    htmlChartPath = os.path.join(HTML_PATH, 'drug-combinations-{}.html'.format(lang))

    with open(htmlChartPath, 'w+') as f:
        f.write(chart)

    print('Generating PNG for {}'.format(lang))
    subprocess.run(['node', RENDER_SCRIPT_PATH, htmlChartPath, str(config.width), str(config.height)])

except KeyboardInterrupt:
    print('> Script aborted prematurely !')