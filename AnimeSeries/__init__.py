"""
Anime Series Resources
"""

import requests
import random

class Kyoko:
  """
  Kyoko class
  Using Kyoko API to get a random anime quote
  """
  def __init__(self,type):
    self.url = f"https://kyoko.rei.my.id/api/{type}.php"
  
  def quotes(self):
    res = requests.get(self.url).json()['apiResult'][0]
    return {
            'en': res['english'],
            'id': res['indo'],
            'chara': res['character'],
            'series': res['anime']
           }


class WaifuIm:
  """
  WaifuIm class
  Using Waifu.im API to get a random waifu pic
  """

  def __init__(self, type):
    self.url = f"https://api.waifu.im/{type}/"

  def waifu(self, tags, nsfw):
    par = {
           'included_tags': tags,
           'is_nsfw'      : nsfw
          }
    res = requests.get(self.url,params=par).json()['images'][0]
    
    return {
            'url'   : res['url'],
            'source': res['source'],
            'color' : res['dominant_color']
           }
    


class Yandere:
  def __init__(
    self,
    popular: bool,
    tags,
    limit=None
  ):
    self.tags = tags
    response = requests.post("https://febryans-wakaranai.hf.space/run/predict", json={
      "data": [
        popular,
        self.tags,
        limit
      ]
    }).json()
    self.data = response["data"][0]

  def get_post(self, limit):
    posts = []
    counter = 0
    while counter < limit:
      post = random.choice(self.data['posts'])
      if post not in posts:
        posts.append(post)
        counter += 1
      if len(posts) == len(self.data['posts'])+1:
        break
    return posts

  def get_raw(self):
    return self.data



class Danbooru:
  def get_post(tags, limit):
    response = requests.post("https://febryans-danbooru.hf.space/run/predict", json={
      "data": [
        tags,
        limit
      ]
    }).json()
    data = response['data'][0]['data']
    return data
    


