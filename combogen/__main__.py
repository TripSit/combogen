from combogen.ChartGenerator import ChartGenerator, PROJECT_ROOT, TEMPLATE_ROOT
import os

chart_generator = ChartGenerator()
chart_generator.debug()
chart = chart_generator.generate("3.0 [PRE-RELEASE|DO-NOT-USE - SOME DATA MAY BE INACCURATE]")

with open(os.path.join(PROJECT_ROOT, 'drug-combinations.html'), 'w+') as f:
  f.write(chart)
