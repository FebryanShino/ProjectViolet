import os

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
