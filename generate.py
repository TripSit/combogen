import svgwrite
from svgwrite import cm, mm, px, percent

from structures import DrugDatabase, ComboChart

drug_db = DrugDatabase()
drug_db.populate()

# Find missing drugs from either config or JSON
database_diff = drug_db.find_missing()
#print("Drugs missing from config: " + str(database_diff[0]))
#print("Drugs missing from JSON: " + str(database_diff[1]))

DOUBLE_A4 = ('594mm', '210mm')
ORIGINAL = ('3800px', '1600px')

chart = ComboChart(drug_db, size=DOUBLE_A4)
background = chart.add(chart.rect((0, 0), ('100%', '100%'), fill='#000'))
chart.add_style("@import url(https://fonts.googleapis.com/css?family=Oswald);")
chart.add_style(".name{font-family:'Oswald';font-size:0.7em}")

y_index = 0
for group_a_id, group_a in enumerate(drug_db.config['tableOrder']):
  for drug_a in group_a:
    group_color = drug_db.config['groupHeadingColours'][group_a_id]

    chart.add_cell(y_index+1, 0, group_color) # left
    chart.add_cell(y_index+1, chart.item_count+1, group_color) #right
    chart.add_cell(0, y_index+1, group_color) # top
    chart.add_cell(chart.item_count+1, y_index+1, group_color) # bottom

    chart.add_label(drug_a, y_index+1, 0) # left
    chart.add_label(drug_a, y_index+1, chart.item_count+1) #right
    chart.add_label(drug_a, 0, y_index+1) # top
    chart.add_label(drug_a, chart.item_count+1, y_index+1) # bottom

    x_index = 0
    for group_b_id, group_b in enumerate(drug_db.config['tableOrder']):
      for drug_b in group_b:

        if drug_a == drug_b:
          interaction_color = group_color

          chart.add_cell(y_index+1, x_index+1, interaction_color)
          chart.add_label(drug_a, y_index+1, x_index+1)
        else:
          interaction = drug_db.interaction(drug_a, drug_b)
          interaction_color = chart.interaction_color(interaction)

          chart.add_cell(y_index+1, x_index+1, interaction_color)
        x_index += 1

    y_index += 1

chart.add_title()
chart.add_logo()
chart.add_legend()
print(chart.tostring())
chart.save()
