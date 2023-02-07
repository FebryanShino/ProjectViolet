import discord
from discord.ext import commands
import os
import openai
from website import heart
from ratelimiter import RateLimiter
from sympy import *
import math
import random
import requests
import asyncio
import qrcode
import sqlite3
import csv
import urllib.request
from PIL import Image
from replit import db
from pytube import YouTube
import pandas
import openpyxl

import bot_info
from disappointment import disappointment_sentence_list
from MY_LOVE import MY_LOVE
from praise import praise_high,praise_mid,praise_low
from help_command import help_name, help_value
from Command import sayhi



owner = int(os.getenv('MY_ID'))
violet_user_id = int(os.getenv('BOT_ID'))

intents = discord.Intents.all()

violet = commands.Bot(command_prefix='!', intents=intents,owner_ID = owner)

openai.api_key = os.getenv('API')
YOUTUBE_API = os.getenv('YOUTUBE_API')

command_limiter = RateLimiter(max_calls=1, period=1)

bot_name = 'ヴァイオレット'
channel_id = os.getenv('CHANNEL_ID')


@violet.event
async def change_status(): 
  while True:
    status_l = []
    status_p = []
    with open("bot_info/status.csv","r") as status_data:
      reader = csv.reader(status_data)
      next(reader)
      for row in reader:
        activity = row[0]
        status = row[1]
        if activity == 'listening':
          status_l.append(status)
        elif activity == 'playing':
          status_p.append(status)
    status_listening = random.choice(status_l)
    status_playing = random.choice(status_p)
    try:
      await violet.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_listening))
      await asyncio.sleep(15)
      await violet.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status_playing))
      await asyncio.sleep(15)
    except discord.DiscordException as e:
      if e.status == 429:
        reset_time = e.response['Retry-After']
        await asyncio.sleep(reset_time)
      else:
        raise e


@violet.event
async def on_ready():
  try:
    user = violet.get_user(owner)
    message = await user.send("フェブリアンさん、こんにちは!")
    await asyncio.sleep(30)
    await message.delete()
    print(f'{bot_name} has connected to Discord!')
  except Exception as e:
        print("An error ocurred: ", e)
        pass
  await violet.loop.create_task(change_status())



@violet.command()
async def botinfo(ctx):
  author_avatar = violet.get_user(owner).avatar
  violet_avatar = violet.get_user(violet_user_id).avatar
  
  info = discord.Embed(title = f"{bot_info.bot_name}", url = bot_info.repository, description = f"Created by {bot_info.author_name}", color = discord.Color.from_str('#e5dbca'))

  info.add_field(name = f"{bot_info.bot_name} {bot_info.bot_desc}", value = f"[Main Website]({bot_info.bot_site})")
  info.add_field(name = f"{bot_info.author_name} SNS", value = bot_info.author_desc)
  info.set_footer(text = f"{bot_info.author_name} 2023", icon_url = author_avatar)
  info.set_thumbnail(url = violet_avatar)
  info.set_image(url = bot_info.image_url)
  await ctx.send(embed=info)



@violet.command()
async def helpme(ctx):
  embed = discord.Embed(title="Welcome to Violet Bot Command Center\nHere are the available commands:", color = discord.Color.blue())
  
  for i in range(0,18):
    embed.add_field(name = help_name[i], value = help_value[i], inline=False)
  await ctx.send(embed=embed)



@violet.command()
@commands.is_owner()
async def addstatus(ctx, activity = None, *name):
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break
  try:
    activity = activity.lower()
  except:
    msg = await ctx.send(f"Please enter the activity you want me to do, {ctx.author.mention}-san")
    await asyncio.sleep(30)
    await msg.delete()
    return

  with open("bot_info/status.csv","a",newline = '') as status:
    writer = csv.writer(status)
    if activity in ['listening','playing']:
      if not name:
        msg = await ctx.send(f"What do you want me to {activity[:-3]}, {ctx.author.mention}-san")
        await asyncio.sleep(30)
        await msg.delete()
        return
      formatted_name = " ".join(name)
      writer.writerow([activity, formatted_name])
      msg = await ctx.send(f"'{activity.capitalize()} {formatted_name}' is added into the status list")
      await asyncio.sleep(30)
      await msg.delete()
    else:
      msg = await ctx.send(f"{activity.capitalize()} is not a valid activity, yet")
      await asyncio.sleep(30)
  await msg.delete()



@violet.command(name='setstatus')
@commands.is_owner()
async def setstatus(ctx, *, status):
  await violet.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
  await ctx.send(f'Status set to: Listening to {status}')



@violet.command(name='call')
async def call(ctx,user: discord.Member = None):
  with open("finally-awake-skyrim.gif", "rb") as gif:
    if user is not None:
      await ctx.send(f"{user.mention}\n\nHey you!\nYou're finally awake", file = discord.File(gif))
    else:
      await ctx.send(f"{ctx.author.mention}\n\nHey you!\nYou're finally awake", file = discord.File(gif))



@violet.command(name='whoareyou')
async def whoareyou(ctx):
    await ctx.send("I'm you but better 😎")



@violet.command(name='nournot')
async def nournot(ctx):
    await ctx.send("YES I AM!")



@violet.command(name='ping')
async def ping(ctx, user: discord.Member = None):
  if user is not None:
    await ctx.send(f'{user.mention}\n\npong!')
    msg = await user.send(f"{user.mention}\nYou've got pinged\nDon't blame me\nBlame {ctx.author.mention}")
    await asyncio.sleep(60)
    await msg.delete()

  else:
    await ctx.send(f'{ctx.author.mention}\n\npong!')



@violet.command(name='say')
async def say(ctx, *, message: str):
  await ctx.send(message, tts=True)



@violet.command(name='pow')
async def pow(ctx, a: float, b: float):
    await ctx.send(a**b)



@violet.command(name='ai')
async def ai(ctx, *, prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=3000,
            temperature=0.7,
        )
        await ctx.send(response["choices"][0]["text"])
    except openai.exceptions.OpenAiError as e:
        await ctx.send(f"Error: {e}")



@violet.command(name='calc')
async def calc(ctx, expression: str):
    x = Symbol('x')
    expr = parse_expr(expression)
    result = float(expr.evalf())
    await ctx.send(result)



@violet.command(name='area')
async def area(ctx, formula: str, a: float, b: float = None, c: float = None):
  formula = formula.lower()
  if formula == 'square':
    await ctx.send(f"The area of a square with\nSide of **{a}**\nIs **{a**2}**")
  elif formula == 'retangle' and b is not None:
    await ctx.send(f"The area of a triangle with\nLength of **{a}**\nWide of **{b}**\n Is **{a*b}**")
  elif formula == 'triangle' and b is not None:
    await ctx.send(f"The area of a triangle with\nBottom of **{a}**\nHeight of **{b}**\nIs **{a*b/2}**")
  elif formula == ['trapezium', 'trapezoid'] and b is not None and c is not None:
    await ctx.send(f"The area of {formula}™with\nParallel sides of **{a}** and **{b}**\nHeight of **{c}**\nIs **{(a+b)*c/2}**")
  elif formula == 'kite' and b is not None:
    await ctx.send(f"The area of a kite with\nDiagonals of **{a}** and **{b}**\nIs **{a*b/2}**")
  elif formula == 'circle':
    await ctx.send(f"The area of a circle with\nRadius of **{a}**\nIs **{math.pi*(a**2)}**")



@violet.command(name='rate')
async def rate(ctx, *waifu: str):
  waifu_name = "".join(waifu).lower()
  waifu_format = " ".join(waifu).title()
  gacha_rate = int(random.randint(0,100))
  
  praise_h = random.choice(praise_high)
  praise_m = random.choice(praise_mid)
  praise_l = random.choice(praise_low)
  disappointment = random.choice(disappointment_sentence_list)
  

  if not waifu_name:
    await ctx.send(f'{disappointment}\n- {bot_name}')

  elif waifu_name in MY_LOVE:
    await ctx.send(f"She's 1000/100, no doubt about that.\n- {bot_name}")
  
  elif waifu_name.isalpha():
    if gacha_rate>=75:
      await ctx.send(f"{waifu_format}'s beauty rate is {gacha_rate}/100.\n{praise_h}\n- {bot_name}")
    elif gacha_rate>=50:
      await ctx.send(f"{waifu_format}'s beauty rate is {gacha_rate}/100.\n{praise_m}\n- {bot_name}")
    else:
      await ctx.send(f"{waifu_format}'s beauty rate is {gacha_rate}/100.\n{praise_l}\n- {bot_name}")

  else:
    await ctx.send(f'{disappointment}\n- {bot_name}')




@violet.command(name='moles')
async def moles(ctx, find: str, a: float):
  AV_N = 6.02e23
  if find == 'mol':
    await ctx.send(f'The moles amount of **{a} particles** is **{a/AV_N} moles**')

  if find == 'partikel':
    result = str(format(a*AV_N))
    try:
      base = result.split('e')[0]
      power = result.split('e')[1].replace("+","")
      
      await ctx.send(f'The particle amound of **{a} moles** is **{base} x 10^{power}**')
    except:
      await ctx.send(f'The particle amound of **{a} moles** is **{result}**')



@violet.command(name='urban')
async def urban(ctx, *, word: str):
    url = f"https://api.urbandictionary.com/v0/define?term={word}"
    response = requests.get(url)
    data = response.json()
    if data['list']:
        definition = data['list'][0]['definition']
        await ctx.send(definition)
    else:
        await ctx.send(f"No results found for {word}")



@violet.command()
async def lyrics(ctx, *name):
  from Lyrics import formatted
  if not name:
    await ctx.send("Please enter the song name")
    return
  try:
    names = "".join(name)
    names = int(names)
  except:
    names = " ".join(name)
  name_format = formatted(names)
  if name_format == "":
    await ctx.send("Please enter the valid index/name of the song")
    return
  content = []
  try:
    with open(f"Lyrics/Title/{name_format}.txt", "r") as file:
      con = file.readlines()
      for lines in con:
        content.append(lines)
  except FileNotFoundError:
    await ctx.send(f"{' '.join(name)} is not found in the Lyrics List")
    return

  title = content[0].replace("\n","")
  artist = content[1]
  the_rest = "".join(content[4:]).split("\n\n")

  
  song_artist = artist.split("Song by ")[1]
  
  song_search = " ".join([title,song_artist])
  itunes = requests.get(f'https://itunes.apple.com/search?term={song_search}&entity=song')
  songs = itunes.json()
  song_data = songs['results']
  if len(song_data) > 0:
    song = song_data[0]
    song_url = song['trackViewUrl']
    song_preview = f"[{title} Preview]({song['previewUrl']})"
    artist_url = song['artistViewUrl']
    track_album = song['collectionName']
    track_art = song['artworkUrl100'].replace("100x100","4096x4096")

  else:
    track_art = ""
    track_album = ""
    song_url = ""
    artist_url = ""
    song_preview = ""

  artist_v1 = content[1].replace("\n","")
  artist_name = "".join(artist_v1.split(" by ")[-1:])
  if content[4].lower().strip() == 'instrumental music':
    artist = "Music by **[{}]({})**".format(artist_name,artist_url)
  else:
    artist = "Song by **[{}]({})**".format(artist_name,artist_url)

    
  try:
    dominant_color = content[2].split(":")[1].strip()
    embed_color = discord.Color.from_str(dominant_color)
  except:
    embed_color = discord.Color.blue()
    
  lyrics = discord.Embed(title = title, url = song_url, description = artist, color = embed_color)
  for row in the_rest:
    lyrics.add_field(name = "", value = row)
  if song_preview != "":
    lyrics.add_field(name="", value = song_preview)
  lyrics.set_image(url=track_art)
  lyrics.set_footer(text=track_album)
  await ctx.send(embed = lyrics)


@violet.command()
async def lysave(ctx, *filename):
  if not filename:
    await ctx.send("Please enter the file name")
    return
  file = ctx.message.attachments
  file_check = str(file).split("filename='")[1].split("' ")[0]

  name = " ".join(filename).title()
  file_format = "_".join(filename).lower()
  if file:
    if file_check.endswith(".txt"):
      await file[0].save(fp=f"Lyrics/Title/{file_format}.txt")
      await ctx.send(f"**{name}** is saved")
    else:
      await ctx.send("The file you entered is not a text file")
  else:
    await ctx.send("Cannot find the file")



@violet.command()
async def lydel(ctx, *file):
  from Lyrics import formatted
  
  if not file:
    command = await ctx.send("Please enter the lyrics name")
    await asyncio.sleep(30)
    await command.delete()
    return

  try:
    names = "".join(file)
    names = int(names)
  except:
    names = " ".join(file)
    
  file_format = formatted(names)
  if file_format == "":
    await ctx.send("Please enter the valid index/name of the song")
    return
    
  filename = file_format.replace("_"," ").title()
  try:
    os.remove(f"Lyrics/Title/{file_format}.txt")
    await ctx.send(f'{filename} is deleted from the Lyrics List')

  except:
    await ctx.send(f'Cannot find {filename} in the Lyrics List')





@violet.command()
async def lycolor(ctx, color: str = None, *name):
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break

  all = []
  name_format = "_".join(name).lower()
  if color is not None and len(color) == 6:
    try:
      with open(f"Lyrics/Title/{name_format}.txt", "r") as base:
        total_data = base.readlines()
        for data in total_data:
          all.append(data)
    except FileNotFoundError:
      await ctx.send(f"{name_format} is not found in the Lyrics List")
      return

    if len(all) < 5:
      await ctx.send(f"The file {name_format}.txt doesn't contain enough information to change the color")
      return
    credit = all[0] + all[1]
    content = all[4:]
    with open(f"Lyrics/Title/{name_format}.txt","w") as updated_data:
      updated_data.write(credit)
      updated_data.write(f"Color: #{color.upper()}\n\n")
      for new in content:
        updated_data.write(new)
  else:
    await ctx.send("Please enter a valid color code in the hex format")
    return

  title = all[0].replace("\n","")
  await ctx.send(f"{title} color is changed to #{color.upper()}")



@violet.command()
async def lylist(ctx):
  from Lyrics import parts
  
  file_list = sorted(os.listdir('Lyrics/Title'))
  name_v1 = "".join(file_list).replace("_"," ")
  name_v2 = "°".join(name_v1.split(".txt")[:-1]).title()
  lyrics_list = name_v2.split("°")
  format_beta = []
  for i, lyrics in enumerate(lyrics_list):
    format_beta.append("{} • {}".format(i+1,lyrics))

  max_num_length = max(len(number.split("•")[0]) for number in format_beta)

  max_text_length = max(len(text.split("•")[1]) for text in format_beta)

  format = []
  for i in format_beta:
    number, text = i.split("•")
    format.append("{:<{}} {} {:<{}}".format(number.strip(), max_num_length, "•", text.strip(), max_text_length))

    

  
  embed = discord.Embed(title='Lyrics List', color = discord.Color.random())
  for part in parts(format, 10):
    embed.add_field(name="", value="\n".join(part))
  await ctx.send(embed=embed)
    


@violet.command()
async def decimal(ctx, base: str, number: str):
  base = base.lower()
  try:
    number = int(number)
  except ValueError:
    await ctx.send(f"**{number}** is not a valid **integer**.")
    return
  if base == 'bin':
    await ctx.send(f"**{number}** converted to binary is **{bin(number)[2:]}**")
  elif base == 'hex':
    await ctx.send(f"**{number}** converted to hexadecimal is **{str(hex(number)[2:]).upper()}**")
  elif base == 'oct':
    await ctx.send(f"**{number}** converted to octal is **{oct(number)[2:]}**")
  else:
    await ctx.send(f"**{base.capitalize()}** is not a valid base.")

@violet.command()
async def binary(ctx, base: str, number: str):
    base = base.lower()
    try:
        int(number, 2)
    except ValueError:
        await ctx.send(f"**{number}** is not a valid binary number.")
        return
    if base == 'dec':
        decimal = int(number, 2)
        await ctx.send(f"**{number}** converted to decimal is **{decimal}**")
    elif base == 'hex':
        await ctx.send(f"**{number}** converted to hexadecimal is **{str(hex(int(number, 2))[2:]).upper()}**")
    elif base == 'oct':
        await ctx.send(f"**{number}** converted to octal is **{oct(int(number, 2))[2:]}**")
    else:
        await ctx.send(f"**{base.capitalize()}** is not a valid base.")



@violet.command()
async def hexa(ctx, base: str, number: str):
    base = base.lower()
    try:
        int(number, 16)
    except ValueError:
        await ctx.send(f"**{number}** is not a valid **hexadecimal** number.")
        return
    if base == 'dec':
        decimal = int(number, 16)
        await ctx.send(f"**{number}** converted to decimal is **{decimal}**")
    elif base == 'bin':
        await ctx.send(f"**{number}** converted to binary is **{(bin(int(number, 16))[2:])}**")
    elif base == 'oct':
        await ctx.send(f"**{number}** converted to octal is **{oct(int(number, 16))[2:]}**")
    else:
        await ctx.send(f"**{base.capitalize()}** is not a valid base.")



@violet.command()
async def octal(ctx, base: str, number: str):
    base = base.lower()
    try:
        int(number, 8)
    except ValueError:
        await ctx.send(f"**{number}** is not a valid **octal** number.")
        return
    if base == 'dec':
        decimal = int(number, 8)
        await ctx.send(f"**{number}** converted to decimal is **{decimal}**")
    elif base == 'bin':
        await ctx.send(f"**{number}** converted to binary is **{bin(int(number, 8))[2:]}**")
    elif base == 'hex':
        await ctx.send(f"**{number}** converted to hexadecimal is **{(str(hex(int(number, 8))[2:])).upper()}**")
    else:
        await ctx.send(f"**{base.capitalize()}** is not a valid base.")



@violet.command(name='loop')
async def loop(ctx, word: str, amount: str, in_between: str = None):
    try:
        amount = int(amount)
    except ValueError:
        await ctx.send(f"You can't loop {amount} times\nPlease use **integer** only")
        return

    if amount > 0:
        if in_between == '#space':
            in_between = " "
        elif in_between is None:
            in_between = ""

        result = in_between.join([word for i in range(amount)])
        if len(result) > 2000:
            await ctx.send("it's too much")
        else:
            await ctx.send(result)
    else:
        await ctx.send("You're too greedy")


  

@violet.command()
async def qr(ctx, link: str, name: str = None):
  image = qrcode.make(link)
  if name is None:
    image.save("qr_code_dir/qrcode.png", "PNG")
    with open("qr_code_dir/qrcode.png", "rb") as f:
      await ctx.send("Here's your QR code", file=discord.File(f))

  else:
    image.save(f"qr_code_dir/{name}.png", "PNG")
    with open(f"qr_code_dir/{name}.png", "rb") as f:
      await ctx.send(f"Here's your QR code named '{name}.png'", file=discord.File(f))



@violet.command()
async def url(ctx, act = None, key = None, value = None):
  try:
    act = act.lower()
  except:
    await ctx.send("You need to enter something....")
    return

  if act == 'save' and key is not None and value is not None:
    db[key] = value
    await ctx.send(f"'{key}' is saved")
  elif act == 'get':
    value = db[key]
    await ctx.send(f"URL for '{key}' is\n{value}")
    
  elif act == 'del':
    del db[key]
    await ctx.send(f"'{key}' is deleted")
    
  elif act == 'list':
    keys = sorted(list(db.keys()))
    keys_list = "\n".join(["• " + i for i in keys])
    embed = discord.Embed(title="Key Database", color = discord.Color.red())
    embed.add_field(name="", value = keys_list)
    await ctx.send(embed=embed)
  else:
      await ctx.send(f"{act} is not a valid input")



@violet.command()
async def short(ctx, long_url= None):
  if long_url is not None:
    response = requests.get(f'http://tinyurl.com/api-create.php?url={long_url}')
    short_url = response.text
    await ctx.send(f"Here's your shortened URL\n{short_url}")
  else:
    await ctx.send(f"Please enter the URL you're trying to shorten, {ctx.author.mention}-san")



@violet.command()
async def thumb(ctx, source: str):
  video_id = source.split('/')[-1]
  response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API}")
  data = response.json()
  thumbnail_url = data['items'][0]['snippet']['thumbnails']['maxres']['url']
  title = data['items'][0]['snippet']['title']
  format_title = title.replace(" ", "_")
  format_title_x = format_title.replace("/", "_")


  with urllib.request.urlopen(thumbnail_url) as image_url:
    s = image_url.read()

  with open(f"YouTube/Thumbnail/{format_title_x}.png", "wb") as f:
    f.write(s)

  with open(f"YouTube/Thumbnail/{format_title_x}.png", "rb") as thumbnail:
    await ctx.send(f"Here's the thumbnail for\n{title}", file = discord.File(thumbnail))



@violet.command()
async def yt(ctx, option: str = None, link = None):
  try:
    option = option.lower()
  except:
    await ctx.send(f"Please enter the option, {ctx.author.mention}-san")
    return
    
  try:
    yt = YouTube(link)
    video_id = link.split("/")[-1]
  except:
    await ctx.send(f"Please enter the valid URL, {ctx.author.mention}-san")
    return

  title = yt.title
  author = yt.author
  author_id = yt.channel_id
  author_url = yt.channel_url
  video_length = yt.length
  date = yt.publish_date
  views = yt.views
  rating = yt.rating
  description = yt.description
  
  channel_url = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={author_id}&key={YOUTUBE_API}")
  channel_data = channel_url.json()
  channel_icon = channel_data['items'][0]['snippet']['thumbnails']['default']['url']

  video_url = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API}")
  video_data = video_url.json()
  thumbnail_url = video_data['items'][0]['snippet']['thumbnails']['maxres']['url']


  
  def video_hours(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining = seconds % 60
    return "{:}:{:}:{:}".format(str(hours).zfill(2), str(minutes).zfill(2), str(remaining).zfill(2))

  length_format = video_hours(video_length)

  format_views = "{:,}".format(views)

  if option == 'desc' and link is not None:
    format = title.replace(" ", "_").replace("/","|")
    with open(f"YouTube/Description/{format}.txt", "w") as f:
      f.write(description)

    with open(f"YouTube/Description/{format}.txt", "rb") as desc:
      await ctx.send(f"Here's the description for\n\n{title}", file=discord.File(desc))
  
  elif option == 'info':
    if link is not None:
      embed = discord.Embed(title=title, url = link, description=f"[{author}]({author_url})", color = discord.Color.red())
      embed.add_field(name="", value= f"Views: {format_views}\nRating: {rating}\n\nVideo Length: {length_format}\nPublish Date: {date}")
      embed.set_image(url = thumbnail_url)
      embed.set_thumbnail(url = channel_icon)
      embed.set_footer(text=author, icon_url = channel_icon)
      await ctx.send(embed=embed)
    else:
      await ctx.send(f"Please enter the video URL, {ctx.author.mention}-san")

  else:
    await ctx.send(f"What do you want me to do, {ctx.author.mention}-san")



@violet.command()
async def ytdl(ctx, version = None, link = None):
  try:
    version = version.lower()
  except:
    await ctx.send(f"Please enter the format, {ctx.author.mention}-san")
    return


  try:
    yt = YouTube(link)
    channel_id = yt.channel_id
    channel_home = yt.channel_url
    channel_url = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={YOUTUBE_API}")
    channel_data = channel_url.json()
    channel_icon = channel_data['items'][0]['snippet']['thumbnails']['default']['url']
    
    video_id = link.split('/')[-1]
    response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API}")
    data = response.json()
    thumbnail_url = data['items'][0]['snippet']['thumbnails']['maxres']['url']

    progress = await ctx.send("少々お待ちください")
    for i in range(1,5):
      dots = "．" * i
      await progress.edit(content=f"少々お待ちください{dots}")
      await asyncio.sleep(1)
    
    title = yt.title
    author = yt.author
    video = yt.streams.get_highest_resolution()
    audio = yt.streams.get_audio_only()
  except:
    await ctx.send("Please enter the URL")
    return


  if version is not None and version == 'video' and link is not None:
    url = video.url
    bitrate = video.abr
    resolution = f"{video.resolution} Resolution"
  elif version is not None and version == 'audio' and link is not None:
    url = audio.url
    bitrate = audio.abr
    resolution = ""
  else:
    await progress.delete()
    await asyncio.sleep(1)
    await ctx.send(f"Please enter the right format, {ctx.author.mention}-san")
    return
    
  
  response = requests.get(f"https://tinyurl.com/api-create.php?url={url}")
  short_url = str(response.text)
  
  with open("YouTube/Database.csv", "a", newline="") as dir:
    writer = csv.writer(dir)
    writer.writerow([version,title,link,short_url])

  rows_data = []
  with open("YouTube/Database.csv", "r") as data:
    reader = csv.reader(data)
    next(reader)
    for row in reader:
      rows_data.append(row)
  sorted_data = sorted(rows_data, key=lambda row: (row[1].lower(), row[1]))

  with open("YouTube/Database.csv", "w", newline='') as updated_data:
    writer = csv.writer(updated_data)
    writer.writerow(["FORMAT","TITLE","YOUTUBE","URL"])
    for row in sorted_data:
      writer.writerow(row)

  
  theme = discord.Embed(title=title, url=link, description=f"[{author}]({channel_home})", color = discord.Color.blue())
  
  theme.add_field(name=f"In {version.capitalize()} Format", value = f"{bitrate} Bitrate")
  theme.add_field(name = resolution, value = f"**[DOWNLOAD]({short_url})**")
  
  theme.set_thumbnail(url = channel_icon)
  theme.set_image(url = thumbnail_url)
  theme.set_footer(text = author, icon_url = channel_icon)
    
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break
  await asyncio.sleep(1)
  await progress.delete()
  await asyncio.sleep(1)
  contents = await ctx.send(f"{ctx.author.mention}, Here you go", embed=theme)
  await asyncio.sleep(300)
  await contents.delete()



@violet.command()
async def ytlist(ctx, action = None, attribute = None):

  if action is not None and action.lower() in ['dl', 'download']:
    if attribute is not None and attribute.lower() == 'excel':
      file_original = pandas.read_csv('YouTube/Database.csv')
      file_original.to_excel('YouTube/Database_Excel.xlsx', index = False)
      with open('YouTube/Database_Excel.xlsx', "rb") as file:
        await ctx.send("Here's the YouTube Database in EXCELS file", file=discord.File(file))
    elif not attribute:
      with open("YouTube/Database.csv", "rb") as file:
        await ctx.send("Here's the YouTube Database in CSV file", file = discord.File(file))
    else:
      await ctx.send(f"{attribute.upper()} file is not supported yet")

  elif action is not None and action.lower() == 'clean':
    if ctx.author != violet.get_user(owner):
      await ctx.send("You have no permission to clean up the database")
      return
      
    with open("YouTube/Database.csv", "w", newline='') as data:
      writer = csv.writer(data)
      writer.writerow(["FORMAT","TITLE","YOUTUBE","URL"])
    await ctx.send("Finished cleaning up YouTube Database")

    
  else:
    row_list = []
    with open("YouTube/Database.csv", "r") as data:
      reader = csv.reader(data)
      for row in reader:
        row_list.append(row)

    yt_url_list = []
    video_list = []
    audio_list = []
    title_video = set()
    title_audio = set()
    for row in row_list:
      format = row[0]
      title = row[1]
      url = row[3]
      yt_url = row[2]
      if format == 'audio':
        if title not in title_audio:
          formatted = "[{}]({})".format(title, url)
          audio_list.append(formatted)
          title_audio.add(title)
          yt_url_list.append(yt_url)
      elif format == 'video':
        if title not in title_video:
          formatted = "[{}]({})".format(title, url)
          video_list.append(formatted)
          title_video.add(title)
          yt_url_list.append(yt_url)
          
    try:
      random_url = random.choice(yt_url_list)
      yt = YouTube(random_url)
      yt_title = yt.title
      yt_author_id = yt.channel_id
      video_id = random_url.split("/")[-1]
      video_get = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API}")
      yt_data = video_get.json()
      thumbnail = yt_data['items'][0]['snippet']['thumbnails']['maxres']['url']
      
      channel_get = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={yt_author_id}&key={YOUTUBE_API}")
      channel_data = channel_get.json()
      channel_icon = channel_data['items'][0]['snippet']['thumbnails']['high']['url']
    except:
      random_url = ""
      yt_title = ""
      thumbnail = ""
      channel_icon = ""

      
    video_format = "\n".join(["• " + i for i in video_list])
    audio_format = "\n".join(["• " + i for i in audio_list])
      
    data_list = discord.Embed(title="YouTube Database", url= random_url, color=discord.Color.red())
    data_list.add_field(name="Video", value=video_format)
    data_list.add_field(name="Audio", value=audio_format)

    data_list.set_thumbnail(url=bot_info.image_url)
    data_list.set_image(url = thumbnail)
    data_list.set_footer(text=yt_title, icon_url=channel_icon)
    await ctx.send(embed=data_list)





@violet.command()
async def pp(ctx, link = None):
  try:
    yt = YouTube(link)
    author = yt.author
    title = yt.title
    channel_id = yt.channel_id
  except:
    await ctx.send("バカですね...")
    return
  
  channel_url = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={YOUTUBE_API}")
  channel_data = channel_url.json()
  channel_icon = channel_data['items'][0]['snippet']['thumbnails']['high']['url']

  profile = discord.Embed(title=author, url=channel_icon, color = discord.Color.random())
  profile.set_image(url=channel_icon)
  profile.set_footer(text=title)
  
  await ctx.send(embed=profile)


@violet.command()
async def notes(ctx, action: str = None, key = None, *value: str):
  try:
    action = action.lower()
  except:
    await ctx.send("Please enter the action")
    return

  server = sqlite3.connect('Notes_Database/database.db')
  with server:
    database = server.cursor()
    
    if action is not None and action == 'save' and key is not None:
      end_value = " ".join(value)
      try:
        database.execute("INSERT INTO database(name,value) VALUES (?,?)", (key, end_value))
        server.commit()
        await ctx.send(f"**'{end_value}'** is saved as **'{key}'**")
      except sqlite3.IntegrityError:
        await ctx.send(f"'{key}' is already in the database")

    elif action is not None and action == 'list' and not value:
      database.execute("SELECT name FROM database")
      rows = database.fetchall()
      rows_format = ["{}".format(row[0]) for row in rows]
      format_string = "\n".join(["• " + i for i in rows_format])

      list = discord.Embed(title="Notes Database", color = discord.Color.random())
      list.add_field(name=format_string, value="")
      
      await ctx.send(embed=list)

    elif action is not None and action == 'get' and key is not None and not value:
      database.execute("SELECT value FROM database WHERE name=?", (key,))
      result = database.fetchone()
      if result:
        result_temp = discord.Embed(title=key, description=result[0], color = discord.Color.random())
        await ctx.send(embed=result_temp)
      else:
        await ctx.send(f"**{key}** is not found in the database")
        
      
    elif action is not None and action in ['del', 'delete'] and key is not None and not value:
      database.execute("DELETE FROM database WHERE name=?", (key,))
      if database.rowcount == 0:
        await ctx.send(f"**{key}** is not found in the database")
      else:
        server.commit()
        await ctx.send(f"**{key}** is deleted from the database")

    else:
      await ctx.send(f"**{action}** is not a valid action, {ctx.author.mention}-san")



@violet.command()
async def excel(ctx, action = None, *content):
  try:
    action = action.lower()
  except:
    await ctx.send("Please enter the action")
    return


    
    

  if action == 'create':
    content_string = "•".join(content).replace("_", " ")
    content_final = content_string.split('•')
    data_string = " | ".join(content_final)

    with open("Excels/excel_data.csv", "w", newline="") as data:
      writer = csv.writer(data)
      writer.writerow(content_final)
    command = await ctx.send(f"Created\n| {data_string} |")
    await asyncio.sleep(300)
    await command.delete()

  elif action == 'add':
    content_string = "•".join(content).replace("_", " ")
    content_format = content_string.replace("#", " ")
    content_final = content_format.split('•')
    data_string = " | ".join(content_final)
    
    with open("Excels/excel_data.csv", "a", newline="") as data:
      
      writer = csv.writer(data)
      writer.writerow(content_final)
    command = await ctx.send(f"Added\n| {data_string} |")
    await asyncio.sleep(120)
    await command.delete()

  elif action == 'get':
    if not content:
      filename = "File"
    else:
      filename = "_".join(content).replace(" ","_")
      
    cursor = pandas.read_csv('Excels/excel_data.csv')
    cursor.to_excel(f'Excels/{filename}.xlsx', index=False)

    with open(f'Excels/{filename}.xlsx', "rb") as file:
      object = await ctx.send("Here's the Excels file", file = discord.File(file))
      if 'preview' in filename.lower():
        await asyncio.sleep(30)
        await object.delete()
      os.remove(f'Excels/{filename}.xlsx')

  elif action in ['rn', 'rename']:
    content_string = "•".join(content).replace("_", " ")
    content_final = content_string.split('•')
    data_string = " | ".join(content_final)
    data_list = []
    
    with open("Excels/excel_data.csv", "r") as database:
      reader = csv.reader(database)
      next(reader)
      for data in reader:
        data_list.append(data)

    with open("Excels/excel_data.csv", "w") as updated_data:
      writer = csv.writer(updated_data)
      writer.writerow(content_final)
      for row in data_list:
        writer.writerow(row)
    await ctx.send(f"Renamed to\n| {data_string} |")
  
  else:
    await ctx.send(f"{action.capitalize()} is not a valid action, {ctx.author.mention}-san")
      


@violet.command()
async def color(ctx):
  from Image import dominant_color
  file = ctx.message.attachments
  print(file)
  file_check = str(file).split("filename='")[1].split("' ")[0]
  format = file_check.split(".")[-1]
  if format not in ['png','jpg','jpeg']:
    await ctx.send(f"Remember, No {format.upper()}")
    return
  progress = await ctx.send("少々お待ちください")
  await file[0].save(fp=f"Image/base.{format}")

  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break
  
  rgb = dominant_color(f'Image/base.{format}')
  hex_value = '#{:02x}{:02x}{:02x}'.format(rgb[0],rgb[1],rgb[2])

  Color_image = Image.new("RGB",(1024,1024),(rgb[0],rgb[1],rgb[2]))
  Color_image.save(f"Image/Color/Color.jpg")
  
  with open("Image/Color/Color.jpg", "rb") as f:
    await progress.delete()
    await ctx.send(f"Here's the dominant color\nHex Value: {hex_value.upper()}", file = discord.File(f))
  os.remove(f"Image/base.{format}")



@violet.command()
async def mal(ctx, *title):
  if not title:
    await ctx.send(f"Please enter the title, {ctx.author.mention}-san")
    return

  titles = "%20".join(title)
  parameters = {'q': titles,
               }
  anime = requests.get("https://api.jikan.moe/v4/anime?", params=parameters)
  response = anime.json()['data'][0]

  try:
    title = response['title_english']
    title_jp = response['title_japanese']
    season = response['season']
    year = response['year']
    synopsis = response['synopsis'].split("\n\n")
    url = response['url']
    image = response['images']['jpg']['large_image_url']
  except AttributeError:
    await ctx.send("Can't find the series")
    return

  theme = discord.Embed(title=title,url=url, description=f"Season: {season.capitalize()}\nYear: {year}")
  for i in synopsis:
    theme.add_field(name="", value=i)
  theme.set_image(url=image)
  theme.set_footer(text=title_jp)
  await ctx.send(embed=theme)


#Experimental
@violet.command()
async def yo(ctx,arg):
  result = sayhi(arg)
  await ctx.send(f"{result} {ctx.author.mention}")


heart()
violet.run(os.getenv('YEET'))
