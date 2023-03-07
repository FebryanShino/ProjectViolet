"""
Using matplotlib to visualize Status Data as pie chart
"""

import csv
import matplotlib.pyplot as plt

def StatusData():
  listen = set()
  play = set()
  watch = set()
  with open("Violet/status.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for i in reader:
      type = i[0]
      name = i[1]
      if type == 'listening':
        if name not in listen:
          listen.add(name)
      if type == 'playing':
        if name not in play:
          play.add(name)
      if type == 'watching':
        if name not in watch:
          watch.add(name)

  labels = ['Listening','Playing','Watching']
  sizes = [len(listen),len(play),len(watch)]
  colors = ['#A798B7', '#EEEEED', '#E6DCC9']

  fig,ax1 = plt.subplots(figsize=(5,5))

  plt.subplots_adjust(bottom=-0.1)


  def my_autopct(pct):
    return f'{pct:.1f}%\n'
  ax1.pie(sizes,
        labels=labels,
        colors=colors,
        autopct=my_autopct,
        startangle=90,
        textprops={'fontsize': 14}
        )
  ax1.axis('equal')
  for text in ax1.texts:
    text.set_color("white")
    
  plt.title('Status Chart', fontsize=25, color = 'white')
  fig.set_facecolor('#2f3136')

  plt.tight_layout()
  plt.savefig('Violet/Chart.jpg')
  return {'music': len(listen),
          'game' : len(play),
          'movie': len(watch)}
