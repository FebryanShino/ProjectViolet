from datetime import datetime
from MyAnimeList import ordinals
import time

class FileNames:
  """
  FileNames class
  Solely purpose for checking the discord
  attachments file format
  """


  def __init__(self,file):
    self.check = str(file).split("filename='")[1].split("' ")[0]

  def format(self):
    format = self.check.split(".")[-1]
    return format

def date_format(date_input:str):
  date_str = date_input[:10]
  day = date_str.split("-")[-1]
  date_obj = datetime.strptime(date_str,"%Y-%m-%d")
  formatted_date = date_obj.strftime("%B %d, %Y").replace(day, ordinals(day)).replace(" 0"," ")

  time = date_input.split(" ")[1][:5]
  hour = int(time[:2])
  if hour >= 12:
    if hour == 12:
      hour = "12"
    elif hour == 24:
      hour = "0"
    else:
      hour = str(hour-12)
    type = "PM"
  else:
    type = "AM"
  formatted_time = f"{hour}{time[-3:]} {type}"
  return {'date': formatted_date,
          'time': formatted_time}

def timestamp():
  now = time.gmtime(time.time())
  format = time.strftime("%H:%M", now)
  return format
