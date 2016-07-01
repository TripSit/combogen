from combogen.ChartGenerator import ChartGenerator, PROJECT_ROOT, TEMPLATE_ROOT, TRANSLATIONS_ROOT,  TOOLS_ROOT
import os
import subprocess

RENDER_SCRIPT_PATH = os.path.join(TOOLS_ROOT, 'render.js')
OUTPUT_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, 'output'))
PNG_PATH = os.path.join(OUTPUT_PATH, 'png')
PDF_PATH = os.path.join(OUTPUT_PATH, 'pdf')


try:
    os.makedirs(PNG_PATH)
except FileExistsError:
    pass

try:
    os.makedirs(PDF_PATH)
except FileExistsError:
    pass

try:
    chart_generator = ChartGenerator()
    chart_generator.debug()

    for file in os.listdir(TRANSLATIONS_ROOT):
        if (file.endswith(".json")):
            lang = file.split(".")[0]
            chart = chart_generator.generate(lang)

            with open(os.path.join(PROJECT_ROOT, 'drug-combinations-{}.html'.format(lang)), 'w+') as f:
                f.write(chart)

            print('Generating PNG for {}'.format(lang))
            subprocess.run(['node', RENDER_SCRIPT_PATH, 'drug-combinations-{}'.format(lang)])

except KeyboardInterrupt:
    print('> Script aborted prematurely !')