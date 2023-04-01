"""
All Information Related to Violet
"""

from os import getenv

owner = int(getenv('MY_ID_SEC'))
bot_name = "ヴァイオレット"
author_name = "FebryanS"
bot_site = "https://Experimental-Bot-by-FebryanS.febryanshino.repl.co"
color = 0x7353aa
repository = "https://github.com/FebryanShino/ProjectViolet"
invite = getenv('invite')

twitter = getenv('twitter')
instagram = getenv('instagram')
pixiv = getenv('pixiv')
github = getenv('github')
author_desc = f"[GitHub]({github})\n[Pixiv]({pixiv})\n[Twitter]({twitter})\n[Instagram]({instagram}\n\n)"

image_url = getenv('violet_image')
image_url2 = getenv('violet_banner')

def bot_desc():
  with open("Violet/Description.txt", "r") as f:
    lines = "".join(f.readlines())
  return lines
    