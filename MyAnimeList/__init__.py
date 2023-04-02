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
      params = {'q': self.name}
      anime = requests.get("https://api.jikan.moe/v4/anime?", params=params)
      self.res = anime.json()['data']

    def anime_list(self):
      return self.res

  
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
      

    def chara_list(self):
      params = {'q': self.name}
      chara = requests.get("https://api.jikan.moe/v4/characters", params=params)
      data = chara.json()['data']

      return data


    def info(self, character):
      name = character['name']
      kanji= character['name_kanji']
      nickname = character['nicknames']
      url = character['url']
      about = character['about']
      if about is not None:
        about = about.split("\n\n")
      image = character['images']['jpg']['image_url']

      return {'name': name,
              'kanji': kanji,
              'nickname': nickname,
              'url': url,
              'bio': about,
              'image': image
             }

      




def titles(anime, lang):
  if lang == 'og':
    title = anime['title']
  elif lang == 'jp':
    title = anime['title_japanese']
  elif lang == 'en':
    title = anime['title_english']
  return title
        
def information(anime):
  season = anime['season']
  type = anime['type']
  year = anime['year']
  rank = anime['rank']
  status = anime['status']
  trailer = anime['trailer']
  synopsis = anime['synopsis']
  if synopsis is not None:
    synopsis = synopsis.replace("\n \n", "\n\n").split("\n\n")[:-1]
  url = anime['url']
  image = anime['images']['jpg']['large_image_url']

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