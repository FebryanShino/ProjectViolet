import requests
import os

YOUTUBE_API = os.getenv('YOUTUBE_API')

class ytAPI:
  """
  YouTube class
  Using YouTube Official API
  """

  class Video:
    def __init__(self, url):
      self.url = url
      video_id = self.url.split('/')[-1]
      params = {'part': 'snippet',
              'id': video_id,
              'key': YOUTUBE_API}
    
      response = requests.get("https://www.googleapis.com/youtube/v3/videos?", params=params)
      self.data = response.json()['items'][0]['snippet']

  
    def thumbnail(self):
      try:
        thumb = self.data['thumbnails']['maxres']['url']
      except KeyError:
        thumb = self.data['thumbnails']['high']['url']
      return thumb

    def titles(self):
      title = self.data['title']
      return title

  
  class Channel:
    def __init__(self, ch_id):
      self.ch_id = ch_id
      url = "https://www.googleapis.com/youtube/v3/channels?"
      params = {'part': 'snippet',
                'id': self.ch_id,
                'key': YOUTUBE_API}
      yt = requests.get(url,params=params)
      self.data = yt.json()['items'][0]['snippet']
      
    def info(self):
      picture = self.data['thumbnails']['high']['url']
      return picture
