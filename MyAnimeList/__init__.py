import requests

class MyAnimeList:
  """
  MyAnimeList class
  Using Jikan API
  To search for anime, character, and user
  """
  
  class AnimeSearch:
    """
    Search for Anime
    """

    def __init__(self, name):
      self.name = name
      parameters = {'q': self.name}
      anime = requests.get("https://api.jikan.moe/v4/anime?", params=parameters)
      self.res = anime.json()['data'][0]
    def titles(self, lang):
      if lang == 'og':
        title = self.res['title']
      elif lang == 'jp':
        title = self.res['title_japanese']
      elif lang == 'en':
        title = self.res['title_english']
      return title
        
    def info(self):
      season = self.res['season']
      type = self.res['type']
      year = self.res['year']
      rank = self.res['rank']
      status = self.res['status']
      trailer = self.res['trailer']['url']
      synopsis = self.res['synopsis'].split("\n\n")[:-1]
      url = self.res['url']
      image = self.res['images']['jpg']['large_image_url']

      if season == 'summer':
        color = 0xf9d62e
      elif season == 'spring':
        color = 0xc6d7b9
      elif season == 'fall':
        color = 0xf05133
      elif season == 'winter':
        color = 0xe3e3ff
      else:
        color = 0x2e51a1
      
      return {'season': season,
              'type': type,
              'year': year,
              'rank': rank,
              'status': status,
              'color': color,
              'trailer': trailer,
              'synopsis': synopsis,
              'url': url,
              'art': image
             }

  
  class UserSearch:
    """
    Search for User
    """

    def __init__(self, name):
      self.name = name
      params = {'q': self.name}
      user = requests.get("https://api.jikan.moe/v4/users", params=params)
      self.res = user.json()['data'][0]

    def info(self):
      username = self.res['username']
      user_url = self.res['url']
      status = self.res['last_online']
      profile = self.res['image']['jpg']['image_url']

      return {'username': username,
              'url': user_url,
              'status': status,
              'profile': profile
             }

  
  class CharaSearch:
    """
    Search for Character
    """

    def __init__(self, name):
      self.name = name
      params = {'q': self.name}
      chara = requests.get("https://api.jikan.moe/v4/characters", params=params)
      self.res = chara.json()['data'][0]

    def info(self):
      name = self.res['name']
      kanji= self.res['name_kanji']
      nickname = self.res['nicknames']
      url = self.res['url']
      about = self.res['about']
      image = self.res['images']['jpg']['image_url']

      return {'name': name,
              'kanji': kanji,
              'nickname': nickname,
              'url': url,
              'bio': about,
              'image': image
             }

      








def ordinals(x):
  """
  For ordinal numbering
  """
  x = str(x)
  
  if x[-1] == "1" and x != "11":
    result = x + "st"
  
  elif x[-1] == "2" and x != "12":
    result = x + "nd"
    
  elif x[-1] == "3" and x != "13":
    result = x + "rd"
    
  else:
    result = x + "th"
  return result