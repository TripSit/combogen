import svgwrite
from svgwrite import cm, mm, px, percent

from structures import DrugDatabase, ComboChart

drug_db = DrugDatabase()
drug_db.populate()

DOUBLE_A4 = ('594mm', '210mm')

chart = ComboChart(drug_db, size=DOUBLE_A4)
background = chart.add(chart.rect((0, 0), ('100%', '100%'), fill='#1C1C1C'))

y_index = 0
for group_id, group in enumerate(drug_db.config['tableOrder']):

  for drug_a in group:
    group_color = drug_db.config['groupHeadingColours'][group_id]

    chart.add_cell(y_index+1, 0, group_color) # left
    chart.add_cell(y_index+1, chart.item_count+1, group_color) #right
    chart.add_cell(0, y_index+1, group_color) # top
    chart.add_cell(chart.item_count+1, y_index+1, group_color) # bottom

    chart.add_label(drug_a, y_index+1, 0, 'white') # left
    chart.add_label(drug_a, y_index+1, chart.item_count+1, drug_db.config['groupHeadingColours'][group_id]) #right
    chart.add_label(drug_a, 0, y_index+1, 'white') # top
    chart.add_label(drug_a, chart.item_count+1, y_index+1, drug_db.config['groupHeadingColours'][group_id]) # bottom

    x_index = 0
    for x_group_id, x_group in enumerate(drug_db.config['tableOrder']):
      for drug_b in x_group:

        if drug_a == drug_b:
          interaction_color = 'black'

          chart.add_cell(y_index+1, x_index+1, interaction_color)
          chart.add_label(drug_a, y_index+1, x_index+1)
        else:
          interaction = drug_db.interaction(drug_a, drug_b)
          interaction_color = chart.interaction_color(interaction)

          chart.add_cell(y_index+1, x_index+1, interaction_color)
        x_index += 1

    y_index += 1


chart.add_title()

print(chart.tostring())
