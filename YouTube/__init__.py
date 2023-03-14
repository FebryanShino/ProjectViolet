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
      video_id = url.split('/')[-1]
      params = {
        'part': 'snippet',
        'id': video_id,
        'key': YOUTUBE_API
      }

      response = requests.get("https://www.googleapis.com/youtube/v3/videos?", params=params).json()
      self.data = response['items'][0]['snippet']

    def thumbnail(self):
      thumb = self.data['thumbnails']
      try:
        thumbnail = thumb['maxres']['url']
      except KeyError:
        thumbnail = thumb['high']['url']
      return thumbnail

    def titles(self):
      title = self.data['title']
      return title

  class Channel:

    def __init__(self, ch_id):
      self.ch_id = ch_id
      url = "https://www.googleapis.com/youtube/v3/channels?"
      params = {
        'part': 'snippet',
        'id': self.ch_id,
        'key': YOUTUBE_API
      }
      yt = requests.get(
        url,
        params=params
      ).json()
      self.data = yt['items'][0]['snippet']

    def info(self):
      picture = self.data['thumbnails']['high']['url']
      return picture
