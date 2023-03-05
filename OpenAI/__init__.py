from PIL import Image
import sqlite3
import openai
import os

class OpenAI:
  def __init__(self):
    openai.api_key = os.getenv('OPENAI_API')
    
  def ChatGPT(self, arg: str):
    res = openai.Completion.create(
            model = 'text-davinci-003',
            prompt = arg,
            max_tokens = 4000,
            temperature= 0.5
            )
    answer = res['choices'][0]['text']
    return answer

  def CodeGPT(self, arg: str):
    res = openai.Completion.create(
            model = 'code-cushman-001',
            prompt = arg,
            max_tokens = 2000
            )
    code =res['choices'][0]['text']
    return code



  def DALLE(self, arg: str):
    res = openai.Image.create(
            prompt = arg,
            n = 1
            )
    image = res['data'][0]['url']
    return image

  def Variation(self):
    with open("OpenAI/Image/edited.png","rb") as f:
      res = openai.Image.create_variation(
            image = f,
            n = 1
            )
      variation = res['data'][0]['url']
      return variation


class OpenAIData:
  def __init__(self, table: str):
    self.user = table
    self.conn = sqlite3.connect("OpenAI/Database.db")
    self.cursor = self.conn.cursor()
      
    main_table = f'''
    CREATE TABLE IF NOT EXISTS {self.user} (
    key TEXT NOT NULL,
    value TEXT
    );
    '''
    self.cursor.execute(main_table)

  def add_data(self, key, value = ""):
    input = f'''
    INSERT INTO {self.user} (
    key, value)
    VALUES (?,?);
    '''
    self.cursor.execute(input,(key,value))

  def list_data(self):
    input = f'''
    SELECT * FROM {self.user};
    '''
    self.cursor.execute(input)
    data = self.cursor.fetchall()
    dictionary = {key:value for key,value in data}
    return dictionary

  def __del__(self):
    self.conn.commit()
    self.conn.close()




def CropSquare(input: str, output: str):
  """
  Using PIL to crop image into 1:1 ratio
  """

  im = Image.open(f"{input}.png")
  width, height = im.size
  
  size = min(width, height)
  
  left = (width - size) / 2
  top = (height - size) / 2
  right = (width + size) / 2
  bottom = (height + size) / 2
  cropped_im = im.crop((left, top, right, bottom))
  cropped_im.save(f"{output}.png")

