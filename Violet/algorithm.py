import csv

"""
An algorithm to sort Status List database
"""

def SortStatus():
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

  musics = sorted(listen, key=lambda music: music.lower())
  games = sorted(play, key=lambda game: game.lower())
  movies = sorted(watch, key=lambda movie: movie.lower())

  with open("Violet/status.csv", "w", newline='') as output:
    w = csv.writer(output)
  
    w.writerow(["ACTIVITY","NAME"])
    for music in musics:
      w.writerow(["listening",music])
    for game in games:
      w.writerow(["playing",game])
    for movie in movies:
      w.writerow(["watching",movie])