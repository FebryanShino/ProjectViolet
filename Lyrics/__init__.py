import os
import requests
from collections import defaultdict

class iTunes:
  """
  iTunes class
  To get information from a track
  """
  
  def __init__(self, search):
    self.search = requests.get(f'https://itunes.apple.com/search?term={search}&entity=song')
    self.data = self._data()
  
  def _data(self):
    songs = self.search.json()
    song_data = songs['results']
    database = defaultdict(lambda: '')
    song_url = ""
    song_preview = ""
    length = ""
    disc = ""
    track = ""
    genre = ""
    artist_url = ""
    track_album = ""
    price = "-"
    track_art = ""
    
    if len(song_data) > 0:
      song = song_data[0]
      song_url = song['trackViewUrl']
      song_preview = song['previewUrl']
      length = song['trackTimeMillis']
      disc = song['discNumber']
      track = song['trackNumber']
      genre = song['primaryGenreName']
      artist_url = song['artistViewUrl']
      track_album = song['collectionName']

      try:
        price = f"${song['collectionPrice']}"
      except:
        price = "-"
      
      track_art = song['artworkUrl100'].replace("100x100","4096x4096") 
    database = {
          'song': song_url,
          'preview': song_preview,
          'artist': artist_url,
          'album': track_album,
          'art': track_art,
          'time': length,
          'track': track,
          'disc': disc,
          'genre': genre,
          'price': price}

    return database



def real_titles():
  songs = sorted(
    os.listdir("Lyrics/Title"),
    key=lambda title: title.lower()
  )
  titles = []
  artists = []
  for song in songs:
    with open(f"Lyrics/Title/{song}", "r") as f:
      info = f.readlines()
      titles.append(info[0].replace("\n",""))
      artists.append(info[1].split(" by ")[1].replace("\n",""))
  return {
    'title': titles,
    'artist': artists
  }



def formatted(keyword):
  """
  A function so you can search a lyric by
  both its index and name
  """
  dir = sorted(os.listdir('Lyrics/Title'))
  length = len(dir)
  key = [i+1 for i in range(length)]
  value = dict(zip(key, dir))
  original = real_titles()['title']

  try:
    if type(keyword) == int:
      file = value[keyword].split(".")[0]
    elif keyword in original:
      file = value[original.index(keyword)+1].split(".")[0]
    else:
      file = keyword.replace(" ","_").lower()
  except (KeyError, TypeError):
    file = ""

  return file



def lyrics_list(choice):
  artist = real_titles()['artist']
  if choice == 'Romaji':
    file_list = sorted(os.listdir('Lyrics/Title'))
    name_v1 = "".join(file_list).replace("_"," ")
    name_v2 = "°".join(name_v1.split(".txt")[:-1]).title()
    lyrics_list = name_v2.split("°")

  elif choice == 'Original':
    lyrics_list = real_titles()['title']

  pack = dict(zip(lyrics_list,artist))
  return pack



def parts(input, count):
  """
  To split the lyrics into n/field
  so discord embed won't bonk me for
  exceeding the limit
  """
  collection = 0
  while collection < len(input):
    yield input[collection:collection + count]
    collection += count



def times(second):
  """
  Convert seconds to mm:ss format
  """
  minutes = second /1000 //60
  seconds = second /1000 % 60
  format = "{:}:{:}".format(str(minutes).split(".")[0].zfill(2), str(seconds).split(".")[0].zfill(2))
  return format