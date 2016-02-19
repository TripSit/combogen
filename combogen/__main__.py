from combogen.ChartGenerator import ChartGenerator, PROJECT_ROOT, TEMPLATE_ROOT
import os

chart_generator = ChartGenerator()
chart_generator.debug()
chart = chart_generator.generate()

with open(os.path.join(PROJECT_ROOT, 'drug-combinations.html'), 'w+') as f:
  f.write(chart)
