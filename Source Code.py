import discord
from discord.ext import commands
import os
import openai
from ratelimiter import RateLimiter
from sympy import *
import math
import random
import requests
import asyncio
import qrcode
import sqlite3
import csv
from PIL import Image
from replit import db
from pytube import YouTube
import pandas
import openpyxl

#Custom Modules
from Violet import bot_info
from Violet.bot_info import owner
from Website import Heart
from YouTube import ytAPI
from Discord import FileNames


intents = discord.Intents.all()

violet = commands.Bot(command_prefix='!', intents=intents,owner_ID = owner)

YOUTUBE_API = os.getenv('YOUTUBE_API')

command_limiter = RateLimiter(max_calls=1, period=1)


@violet.event
async def change_status(): 
  while True:
    status_l = set()
    status_p = set()
    status_w = set()
    with open("Violet/status.csv","r") as status_data:
      reader = csv.reader(status_data)
      next(reader)
      for row in reader:
        activity = row[0]
        status = row[1]
        if activity == 'listening':
          if status not in status_l:
            status_l.add(status)
        if activity == 'playing':
          if status not in status_p:
            status_p.add(status)
        if activity == 'watching':
          if status not in status_w:
            status_w.add(status)
            
    status_listening = random.choice(list(status_l))
    status_playing = random.choice(list(status_p))
    status_watching = random.choice(list(status_w))

    try:
      await violet.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_listening))
      await asyncio.sleep(120)
      await violet.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status_playing))
      await asyncio.sleep(120)
      await violet.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_watching))
      await asyncio.sleep(120)
    except discord.DiscordException as e:
      if e.status == 429:
        reset_time = e.response['Retry-After']
        await asyncio.sleep(reset_time)
      else:
        raise e


@violet.event
async def on_ready():
  try:
    greetings = []
    with open("Interactions/greeting.csv", "r") as f:
      reader = csv.reader(f)
      next(reader)
      for i in reader:
        greetings.append(i[0])

    greeting_random = random.choice(greetings)

    user = violet.get_user(owner)
    message = await user.send(greeting_random)
    await asyncio.sleep(30)
    await message.delete()
    print(f'{bot_info.bot_name} has connected to Discord!')
  except Exception as e:
        print("An error ocurred: ", e)
        pass
  await violet.loop.create_task(change_status())



@violet.command()
async def botinfo(ctx):
  author_avatar = violet.get_user(owner).avatar
  
  info = discord.Embed(title = f"{bot_info.bot_name}", url = bot_info.repository, description = f"Created by {bot_info.author_name}", color = discord.Color.from_str('#e5dbca'))

  info.add_field(name = f"{bot_info.bot_name} {bot_info.bot_desc}", value = f"[Main Website]({bot_info.bot_site})")
  info.add_field(name = f"{bot_info.author_name} SNS", value = bot_info.author_desc)
  info.set_footer(text = f"{bot_info.author_name} 2023", icon_url = author_avatar)
  info.set_thumbnail(url = bot_info.image_url)
  info.set_image(url = bot_info.image_url)
  await ctx.send(embed=info)



@violet.command()
async def status(ctx):
  progress = await ctx.send("Creating a chart\nPlease wait a moment...")
  
  from bot_info.StatusData import StatusData
  type = StatusData()
  data = discord.Embed(title='Status Database', color = discord.Color.from_str('#e5dbca'))
  data.add_field(name='Status Counts',value= f"**Listening**: {type['music']}\n**Playing**: {type['game']}\n**Watching**: {type['movie']}")
  data.set_thumbnail(url=bot_info.image_url)
  
  with open("Violet/Chart.jpg", "rb") as f:
    await progress.delete()
    await asyncio.sleep(1)
    await ctx.send(embed=data,file=discord.File(f))
  os.remove("Violet/Chart.jpg")



@violet.command()
@commands.is_owner()
async def addstatus(ctx, activity = None, *name):
  available = ['listening','playing','watching']

  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break
  try:
    activity = activity.lower()
  except:
    msg1 = await ctx.send(f"Please enter the activity you want me to do, {ctx.author.mention}-san")
    await asyncio.sleep(30)
    await msg1.delete()
    return

  with open("Violet/status.csv","a",newline = '') as status:
    writer = csv.writer(status)
    if activity in available:
      if not name:
        msg2 = await ctx.send(f"What do you want me to {activity[:-3]}, {ctx.author.mention}-san")
        await asyncio.sleep(30)
        await msg2.delete()
        return
      formatted_name = " ".join(name)
      writer.writerow([activity, formatted_name])
      
      if activity == 'listening':
        activity = f"{activity.capitalize()} to"
      else:
        activity = activity.capitalize()
        
      msg3 = await ctx.send(f"「{activity} {formatted_name}」is added into the status list")
      await asyncio.sleep(30)
      await msg3.delete()
    else:
      msg4 = await ctx.send(f"{activity.capitalize()} is not a valid activity, yet")
      await asyncio.sleep(30)
      await msg4.delete()



@violet.command()
async def sortstatus(ctx):
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break
  from Violet.algorithm import SortStatus
  SortStatus()
  msg = await ctx.send("Status List is sorted")
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
  openai.api_key = os.getenv('API')
  
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



@violet.command()
async def greet(ctx, *greeting):
  if not greeting:
    await ctx.send(f"Please enter the sentence you want to add to Greeting List, {ctx.author.mention}-san")

  greetings = " ".join(greeting)

  with open("Interactions/greeting.csv", "a", newline='') as f:
    writer = csv.writer(f)
    writer.writerow([greetings])
  await ctx.send(f"**{greetings}** is added into the Greeting List")



@violet.command()
async def praise(ctx, level = None, *sentence):
  try:
    level = level.lower()
    sentences = " ".join(sentence)
  except:
    await ctx.send("Please enter the right format")
    return

  with open("Interactions/praise.csv","a", newline='') as f:
    writer = csv.writer(f)
    
    if level not in ['low','mid','high']:
      await ctx.send("You can't get higher or lower than that")
      return

    writer.writerow([level, sentences])
    await ctx.send(f"**{sentences}** is added to the **praise {level} list**")



@violet.command()
async def bruh(ctx, *args):
  if not args:
    await ctx.send(f"Please enter the the sentence you want to add into Disappointment List, {ctx.author.mention}-san")
    return
  sentence = " ".join(args)
  with open("Interactions/disappointment.csv","a", newline='') as f:
    writer = csv.writer(f)
    writer.writerow([sentence])

  await ctx.send(f"**{sentence}** is added into the Disappointment List")


@violet.command(name='rate')
async def rate(ctx, *waifu: str):
  my_love = os.getenv('MY_LOVE')
  
  waifu_name = "".join(waifu).lower()
  waifu_format = " ".join(waifu).title()
  gacha_rate = int(random.randint(0,100))
  
  low = []
  mid = []
  high = []
  with open("Interactions/praise.csv","r") as data:
    reader = csv.reader(data)
    next(reader)
    for row in reader:
      level = row[0]
      sentences = row[1]
      if level == 'low':
        low.append(sentences)
      elif level == 'mid':
        mid.append(sentences)
      else:
        high.append(sentences)

  praise_h = random.choice(high)
  praise_m = random.choice(mid)
  praise_l = random.choice(low)

  disappointment_sentence = []
  with open("Interactions/disappointment.csv", "r") as diss:
    reader_diss = csv.reader(diss)
    next(reader_diss)
    for i in reader_diss:
      disappointment_sentence.append(i)
    
  disappointment = "".join(random.choice(disappointment_sentence))

  if not waifu_name:
    await ctx.send(f'{disappointment}\n- {bot_info.bot_name}')

  elif waifu_name == my_love :
    await ctx.send(f"She's 1000/100, no doubt about that.\n- {bot_info.bot_name}")
  
  elif waifu_name.isalpha():
    if gacha_rate>=75:
      await ctx.send(f"{waifu_format}'s beauty rate is {gacha_rate}/100.\n{praise_h}\n- {bot_info.bot_name}")
    elif gacha_rate>=50:
      await ctx.send(f"{waifu_format}'s beauty rate is {gacha_rate}/100.\n{praise_m}\n- {bot_info.bot_name}")
    else:
      await ctx.send(f"{waifu_format}'s beauty rate is {gacha_rate}/100.\n{praise_l}\n- {bot_info.bot_name}")

  else:
    await ctx.send(f'{disappointment}\n- {bot_info.bot_name}')




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
async def ly(ctx, *name):
  from Lyrics import formatted, iTunes, times
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
    await ctx.send("Please enter the valid title of the song")
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

  try:
    title = content[0].replace("\n","")
    artist = content[1]
    the_rest = "".join(content[4:]).split("\n\n")
  except IndexError:
    with open(f"Lyrics/Title/{name_format}.txt", "rb") as trouble:
      await ctx.send(f'{name_format.replace("_"," ").title()} is not in the valid format\nPlease fix it', file= discord.File(trouble))
    return

  
  song_artist = artist.split("Song ")[1]
  song_search = " ".join([title,song_artist])

  song = iTunes(song_search).data

  artist_v1 = content[1].replace("\n","")
  artist_name = "".join(artist_v1.split(" by ")[-1:])
  if content[4].lower().strip() == 'instrumental music':
    artist = "Music by **[{}]({})**".format(artist_name,song['artist'])
  else:
    artist = "Song by **[{}]({})**".format(artist_name,song['artist'])

    
  try:
    dominant_color = content[2].split(":")[1].strip()
    embed_color = discord.Color.from_str(dominant_color)
  except:
    embed_color = discord.Color.blue()
    
  lyrics = discord.Embed(title = title, url = song['song'], description = artist, color = embed_color)
  if song['song'] != "":
    lyrics.add_field(name="Track Information", value=f"**Disc {song['disc']} Track** {song['track']}\n**Genre:** {song['genre']}\n\n{times(song['time'])}")
  if content[4].lower().strip() != 'instrumental music':
    for row in the_rest:
      lyrics.add_field(name = "", value = row)
  else:
    lyrics.add_field(name="", value="**Instrumental Song**\nLet the music play")
  if song['preview'] != "":
    lyrics.add_field(name="", value = f"[{title} Preview]({song['preview']})")
  lyrics.set_image(url=song['art'])
  lyrics.set_footer(text=f"{song['album']}\nPrice: {song['price']}")
  await ctx.send(embed = lyrics)


@violet.command()
async def lysave(ctx, *filename):
  if not filename:
    await ctx.send("Please enter the file name")
    return
  file = ctx.message.attachments
  format = FileNames(file).format()

  name = " ".join(filename).title()
  file_format = "_".join(filename).lower()
  if file:
    if format == "txt":
      await file[0].save(fp=f"Lyrics/Title/{file_format}.txt")
      await ctx.send(f"**{name}** is saved")
    else:
      await ctx.send("The file you entered is not a text file")
  else:
    await ctx.send("Cannot find the file")



@violet.command()
@commands.is_owner()
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
@commands.is_owner()
async def lycolor(ctx, color: str = None, *name):
  from Lyrics import formatted
  
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break

  all = []
  try:
    names = "".join(name)
    names = int(names)
  except:
    names = " ".join(name)
  name_format = formatted(names)
  if name_format == "":
    await ctx.send("Please enter the valid title of the song")
    return
    
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
  for part in parts(format, 25):
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
    image.save("QRcode/qrcode.png", "PNG")
    with open("QRcode/qrcode.png", "rb") as f:
      await ctx.send("Here's your QR code", file=discord.File(f))

  else:
    image.save(f"QRcode/{name}.png", "PNG")
    with open(f"QRcode/{name}.png", "rb") as f:
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
    if ctx.author != violet.get_user(owner):
      await ctx.send("You need My Master's permission to delete a key")
      return
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
async def thumb(ctx, source=None):
  if source is None:
    await ctx.send("Please enter the video URL")

  try:
    url = ytAPI.Video(source)
  except IndexError:
    await ctx.send("Can't find the source")
    return

  thumbnail_url = url.thumbnail()
  title = url.titles()
  format_title = title.replace(" ", "_")
  format_title_x = format_title.replace("/", "_")
  file = requests.get(thumbnail_url)

  with open(f"YouTube/Thumbnail/{format_title_x}.png", "wb") as f:
    f.write(file.content)

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
  

  def video_hours(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining = seconds % 60
    return "{:}:{:}:{:}".format(str(hours).zfill(2), str(minutes).zfill(2), str(remaining).zfill(2))

  length_format = video_hours(video_length)

  format_views = "{:,}".format(views)

  if option == 'desc' and link is not None:
    format = title.replace("/","_")
    with open(f"YouTube/Description/{format}.txt", "w") as f:
      f.write(description)

    with open(f"YouTube/Description/{format}.txt", "rb") as desc:
      await ctx.send(f"Here's the description for\n\n{title}", file=discord.File(desc))
  
  elif option == 'info':
    if link is not None:
      thumbnail_url = ytAPI.Video(link).thumbnail()
      channel_icon = ytAPI.Channel(author_id).info()
      
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
    
    thumbnail_url = ytAPI.Video(link).thumbnail()
    channel_icon = yAPI.Channel(channel_id).info()

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
    await ctx.send("Cannot find the URL content")
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
      os.remove('YouTube/Database_Excel.xlsx')
      
    elif not attribute:
      with open("YouTube/Database.csv", "rb") as file:
        await ctx.send("Here's the YouTube Database in CSV file", file = discord.File(file))
        
    else:
      await ctx.send(f"{attribute.upper()} file is not supported yet")

  elif action is not None and action.lower() == 'clean':
    if ctx.author != violet.get_user(owner):
      await ctx.send("You need My Master's permission to clean up the database")
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

      thumbnail = ytAPI.Video(random_url).thumbnail()
      channel_icon = ytAPI.Channel(yt_author_id).info()
      
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
  
  channel_icon = ytAPI.Channel(channel_id).info()

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

  server = sqlite3.connect('Notes/database.db')
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
  
  format = FileNames(file).format()
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
  Color_image.save("Image/Color/Color.jpg")
  
  with open("Image/Color/Color.jpg", "rb") as f:
    await progress.delete()
    result = await ctx.send(f"{ctx.author.mention}\n**Here's the dominant color!**\n**Hex Value**: {hex_value.upper()}", file = discord.File(f))
  os.remove(f"Image/base.{format}")
  await asyncio.sleep(300)
  await result.delete()



@violet.command()
async def mal(ctx, terms=None, *title):
  from MyAnimeList import ordinals, MyAnimeList
  if terms is None:
    await ctx.send("Please enter the valid search category")
    return

  if not title:
    await ctx.send(f"Please enter the title, {ctx.author.mention}-san")
    return
    

#AnimeSearch
  if terms.lower() == 'anime':
    try:
      anime = MyAnimeList.AnimeSearch(title)
      info = anime.info()
    except IndexError:
      await ctx.send("Can't find the series")
      return

    title_og = anime.titles('og')
    title_jp = anime.titles('jp')
    type = info['type']
    season = info['season']
    color = info['color']
    year = info['year']
    rank = info['rank']
    synopsis = info['synopsis']
    url = info['url']
    image = info['art']
    trailer = info['trailer']
    status = info['status']
    try:
      season = season.capitalize()
    except AttributeError:
      pass

    theme = discord.Embed(title=title_og ,url=url, description=f"**{type}**\n**Season**: {season}\n**Year**: {year}\n**Rank**: {ordinals(rank)}\n**Status**: {status}", color = discord.Color.from_str(color))

    theme.add_field(name="", value = f"**[{title_og} Trailer]({trailer})**")
    for i in synopsis:
      theme.add_field(name="", value=i)
    theme.set_image(url=image)
    theme.set_footer(text=title_jp)
    await ctx.send(embed=theme)

# UserSearch
  elif terms.lower() == 'user':
    try:
      user = MyAnimeList.UserSearch(title).info()
    except IndexError:
      await ctx.send("User not found")
      return

    username = user['username']
    url = user['user_url']
    profile = user['profile']
    status = user['status']

    embed = discord.Embed(title=username, url=url, description=f"Last Online: {status}")
    embed.set_image(url=profile)
    await ctx.send(embed=embed)

#CharaSearch
  elif terms.lower() == 'chara':
    try:
      chara = MyAnimeList.CharaSearch(title).info()
    except IndexError:
      await ctx.send("User not found")
      return

    chara_name = chara['name']
    kanji = chara['kanji']
    nick = "\n".join(chara['nickname'])
    url = chara['url']
    bio = chara['bio']
    image = chara['image']

    embed = discord.Embed(title=chara_name, url=url, description=f"{kanji}\n\n{nick}")
    embed.add_field(name="About", value=bio)
    embed.set_image(url=image)
    await ctx.send(embed=embed)

    
  else:
    await ctx.send(f"Please enter the right category, {ctx.author.mention}-san")



@violet.command()
async def txt(ctx, action = None, *args):
  
  arg = " ".join(args).replace('#','.').split(".")
  result = "\n".join([x.strip() for x in arg])

  if '#' in "".join(args):
    filename = "_".join(args).split('#')[0].lower()[:-1]
    result = "\n".join([x.strip() for x in arg[1:]])
  else:
    filename = "text_file"

  
  if action.lower() == 'ly':
    data_place = "Lyrics/Title"

  else:
    data_place = "Database"

  with open(f"{data_place}/{filename}.txt", "w") as f:
    f.write(result)

  
  with open(f"{data_place}/{filename}.txt","rb") as file:
    await ctx.send(f"{filename.replace('_',' ').title()} is saved in {data_place}", file=discord.File(file))



@violet.command()
async def soul(ctx, path = None, action = None):
  
  if path is None:
    path = "."

  try:
    python_programs = []
    main = []
    folders = []
    texts = []
    csv_files = []
    others = []

    for i in sorted(os.listdir(path), key = lambda file: file.lower()):
      if i == "main.py":
        main.append("• " + i)
      elif ".py" in i:
        python_programs.append("• " + i)
      elif "." not in i:
        folders.append("• " + i)
      elif ".txt" in i:
        texts.append("• " + i)
      elif ".csv" in i:
        csv_files.append("• " + i)
      else:
        others.append("• " + i)

  except:
    await ctx.send("Can't find the directory")
    return
  embed = discord.Embed(title=f"{bot_info.bot_name}の体",url = bot_info.repository, description = "私のすべて", color = discord.Color.from_str('#e5dbca'))

  if main != []:
    embed.add_field(name="Violet's Heart", value=f'[{"".join(main)}]({os.getenv("source_code")})')

  if folders != []:
    embed.add_field(name="Violet's Folders", value="\n".join(folders))

  if python_programs != []:
    embed.add_field(name="Violet's Python Programs", value = "\n".join(python_programs))

  if texts != []:
    embed.add_field(name="Violet's Texts", value = "\n".join(texts))

  if csv_files != []:
    embed.add_field(name="Violet's CSV Database", value = "\n".join(csv_files))

  if others != []:
    embed.add_field(name="Violet's Other Stuff", value= "\n".join(others))
    
  embed.set_image(url = bot_info.image_url2)
  await ctx.send(embed=embed)



@violet.command()
@commands.is_owner()
async def souldl(ctx, path = None):
  if path is None:
    path = "."

  try:
    with open(path, "rb") as f:
      await ctx.send("Here's a part of myself", file=discord.File(f))
  except:
    await ctx.send("That's not a part of myself")



@violet.command()
async def helpme(ctx):
  from Commands import CommandCenter
  
  cd = CommandCenter().datalist()
  fields = [(key, cd[key]) for key in cd]
  for chunk in [fields[i:i + 25] for i in range(0, len(fields), 25)]:
    embed = discord.Embed(title="Command Center")
    for name, value in chunk:
      embed.add_field(name=name, value=value, inline=False)
    await ctx.send(embed=embed)



@violet.command()
async def data(ctx, action=None, key=None, *value):
  user = ctx.author.id
  name = violet.get_user(user)
  avatar = ctx.author.avatar
  
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break
  
  from Database import Database
  db = Database(user)

  if action is None and not value:
    msg = await ctx.send(f"Please enter the valid action, {ctx.author.mention}-san")
    await asyncio.sleep(60)
    await msg.delete()
    return

  act = action.lower()
  if act == 'add' and key is not None:
    values = " ".join(value)
    db.add_data(key,values)
    msg = await ctx.send(f"**「{key}」**is added into {ctx.author.mention}'s Database")
    await asyncio.sleep(300)
    await msg.delete()

  elif act == 'get' and key is not None and not value:
    result = db.get_data(key)
    embed = discord.Embed(title=key)
    embed.add_field(name='Content', value = result)
    embed.set_thumbnail(url=avatar)
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(300)
    await msg.delete()

  elif act == 'del' and key is not None and not value:
    result = db.del_data(key)
    msg = await ctx.send(f"**「{key}」**and its content is deleted from {ctx.author.mention}'s Database")
    await asyncio.sleep(60)
    await msg.delete()

  elif act == 'list' and not value:
    result = db.list_data()
    embed = discord.Embed(title=f"{name}'s Database")
    for key,value in result.items():
      embed.add_field(name=key,value=value)
    embed.set_thumbnail(url=avatar)
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(300)
    await msg.delete()

  elif act == 'clean' and not value:
    result = db.clean_data()
    msg = await ctx.send(f"Finished cleaning up {ctx.author.mention}'s Database")
    await asyncio.sleep(30)
    await msg.delete()

  elif act == 'edit' and key is not None:
    values = " ".join(value)
    result = db.edit_data(key,values)
    msg = await ctx.send(f"「**{key}**」content is updated to「**{values}**」")
    await asyncio.sleep(60)
    await msg.delete()
    
  else:
    msg = await ctx.send("Please enter the **RIGHT** action")
    await asyncio.sleep(60)
    await msg.delete()


Heart()
violet.run(os.getenv('YEET'))
