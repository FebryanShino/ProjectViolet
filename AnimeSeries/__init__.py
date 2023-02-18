"""
Anime Series Resources
"""

import requests

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

  def waifu(self, tags):
    tags = list(tags)
    par = {
           'included_tags': tags,
           'is_nsfw'      : 'null'
          }
    res = requests.get(self.url,params=par).json()['images'][0]
    
    return {
            'url'   : res['url'],
            'source': res['source'],
            'color' : res['dominant_color']
           }
    


