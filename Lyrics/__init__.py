import os
import requests
from collections import defaultdict

class iTunes:
  
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


def formatted(keyword):
  yeet = sorted(os.listdir('Lyrics/Title'))
  length = len(yeet)
  key = [i+1 for i in range(length)]
  value = dict(zip(key, yeet))

  try:
    if type(keyword) == int:
      file = value[keyword].split(".")[0]
    else:
      file = keyword.replace(" ","_").lower()
  except (KeyError, TypeError):
    file = ""

  return file


def parts(input, count):
  collection = 0
  while collection < len(input):
    yield input[collection:collection + count]
    collection += count


def times(second):
  minutes = second /1000 //60
  seconds = second /1000 % 60
  format = "{:}:{:}".format(str(minutes).split(".")[0].zfill(2), str(seconds).split(".")[0].zfill(2))
  return format
