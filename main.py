"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ヴァイオレット
Created by FebryanS

Multifunctional Discord Bot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

"""
Modules Collection
---------------------
"""
import discord
from discord.ext import commands
import os
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

"""
Custom Modules
-----------------
Some resources that are exclusively tailored for Violet
"""
from Violet import bot_info
from Violet.bot_info import owner
from Memories import top
from Website import Heart
from YouTube import ytAPI
from Discord import FileNames
from AnimeSeries import Kyoko,WaifuIm
from Lyrics import parts, lyrics_list
from Database import Database
from DeepLearning import StableDiffusion, PastelMix, Deepbooru
from OpenAI import OpenAI, OpenAIData, CropSquare


"""
Discord Client and Stuff
----------------------------
Moshi moshi, discord-san?
"""

intents = discord.Intents.all()

violet = commands.Bot(command_prefix='!', intents=intents,owner_ID = owner)

command_limiter = RateLimiter(max_calls=1, period=1)


"""
Violet's Events
------------------
Every activities that Violet does
"""

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




"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Violet Commands
Everything that Violet can do as a favor for you~
--------------------------------------------
"""

"""
Violet Series
----------------
Wanna learn about Violet?

- violet : Violet's ID card
- helpme  : Need help, goshuujin-sama?
"""

@violet.command(
  name='violet',
  description="Violet's Business Card"
)
async def botinfo(ctx):
  author_avatar = violet.get_user(owner).avatar
  
  info = discord.Embed(
    title = bot_info.bot_name,
    description = bot_info.bot_desc(),
    color = bot_info.color
  )

  info.add_field(
    name = "All About Violet",
    value = f"[Violet's Website]({bot_info.bot_site})\n[Violet's Repository]({bot_info.repository})"
  )
  
  info.add_field(
    name = f"{bot_info.author_name} SNS",
    value = bot_info.author_desc
  )
  info.set_footer(
    text = f"Created by {bot_info.author_name}",
    icon_url = author_avatar
  )
  info.set_author(
    name = "Violet",
    icon_url = bot_info.image_url,
    url = bot_info.invite
  )
  
  info.set_thumbnail(url = violet.user.avatar)
  info.set_image(url = violet.user.avatar)
  await ctx.send(embed=info)

botinfo.name = "violet"



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




"""
Violet's Status Series
--------------------------
Everything that Violet does in her spare time~

- status    : Get a pie chart of status data
- addstatus : Add status for Violet to do
- setstatus : Force Violet to do something
              she doesn't want to (EVIL!)  

Slash Command
"""

status = violet.create_group(name='status')

@status.command(
  name='statistics',
  description='The statistics of status that Violet has'
)
async def statistics(ctx):
  await ctx.respond("Creating a chart\nPlease wait a moment...")
  
  from Violet.StatusData import StatusData
  type = StatusData()
  data = discord.Embed(title='Status Database', color = 0xe5dbca)
  data.add_field(name='Status Counts',value= f"**Listening**: {type['music']}\n**Playing**: {type['game']}\n**Watching**: {type['movie']}")
  data.set_thumbnail(url=bot_info.image_url)
  
  with open("Violet/Chart.jpg", "rb") as f:
    await ctx.respond(embed=data,file=discord.File(f))
  os.remove("Violet/Chart.jpg")



@status.command(name='add')
@commands.is_owner()
async def addstatus(
  ctx,
  activity: discord.Option(
    choices=['Listening','Playing','Watching']
  ),
  name
):
  with open("Violet/status.csv","a",newline = '') as status:
    writer = csv.writer(status)
    writer.writerow([activity.lower(), name])
      
  if activity == 'Listening':
      activity = f"{activity} to"
        
  await ctx.respond(
    f"「{activity} {name}」is added into the status list",
    ephemeral=True
  )



@status.command(name='sort')
async def sortstatus(ctx):
  from Violet.algorithm import SortStatus
  SortStatus()
  await ctx.respond(
    "Violet has finished sorting and filtering the Status List.",
  ephemeral=True
  )



@status.command(name='set')
@commands.is_owner()
async def setstatus(
  ctx,
  action: discord.Option(
    choices=['Listening','Playing','Watching']
  ),
  status):

  type = discord.ActivityType
  if action == 'Listening':
    act = type.listening
  elif action == 'Watching':
    act = type.watching
  elif action == 'Playing':
    act = type.playing
  else:
    await ctx.respond("Baaaka.")
    return

  if action == 'Listening':
    action = f"{action} to"
  await violet.change_presence(activity=discord.Activity(type=act, name=status))
  await ctx.respond(f'Status set to: {action} {status}', ephemeral=True)




"""
Violet's Body
----------------
Learn more deeply about Violet

soul   : Explore Violet's Directory
souldl : Learn more deeply about a specific
         part from Violet's Directory
"""

body = violet.create_group(name='soul')

@body.command(name='find')
async def soul(
  ctx,
  main: discord.Option(
    choices=[
      i for i in sorted(os.listdir(), key= lambda p: p.lower()) if "." not in i
    ]
  )=".",
  advance=""
):
  path = f"{main}/{advance.strip() if not None else ''}"
  
  if path == './':
    location = "Home"
  else:
    location = f"Home/{main}/{advance.strip()}"
  
  try:
    python_programs = []
    main = []
    folders = []
    texts = []
    csv_files = []
    memories = []
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
      elif ".db" in i:
        memories.append("• " + i)
      else:
        others.append("• " + i)

  except FileNotFoundError:
    await ctx.respond("Can't find the directory")
    return
  embed = discord.Embed(
    title=f"{bot_info.bot_name}の世界",
    description = f"**[{location}]({(bot_info.repository + '/tree/main/' + path).replace('./','')})**",
    color = bot_info.color
  )
  embed.set_author(
    name = bot_info.bot_name,
    icon_url = bot_info.image_url,
    url = bot_info.repository
  )

  if main != []:
    embed.add_field(name="Violet's Heart", value=f'[{"".join(main)}]({os.getenv("source_code")})')

  if folders != []:
    embed.add_field(name="Violet's Folders", value="\n".join(folders))

  if python_programs != []:
    embed.add_field(name="Violet's Python Programs", value = "\n".join(python_programs))

  if texts != []:
    count = 2
    name = "Violet's Texts"
    for part in parts(texts, 25):
      embed.add_field(name=name, value = "\n".join(part))
      name = f"Violet's Texts Part {count}"
      count += 1

  if csv_files != []:
    embed.add_field(name="Violet's CSV Database", value = "\n".join(csv_files))

  if memories != []:
    embed.add_field(name="Violet's Memories", value = "\n".join(memories))

  if others != []:
    embed.add_field(name="Violet's Other Stuff", value= "\n".join(others))

  embed.set_image(url = bot_info.image_url2)
  await ctx.respond(embed=embed)



@violet.command()
@commands.is_owner()
async def souldl(ctx, *path):
  if not path:
    path = "."
  path = " ".join(path)

  try:
    with open(path, "rb") as f:
      await ctx.send("Here's a part of myself", file=discord.File(f))
  except:
    await ctx.send("That's not a part of myself")




"""
Violet Data Upload
----------------------
Upload sentences that Violet can use to greet, praise, or even mock you
But don't worry, Violet is such a good girl, she won't mock you EXCEPT if you're such a BAKA

greet  : Add greeting sentences
praise : Add praise sentences 
bruh   : Add disappointment sentence 
"""

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




"""
Violet's Playground Series
-----------------------------
Have fun with Violet :)

- whoareyou : Who?
- nournot   : I said 'who'?
- call      : Call someone
- ping      : How to make enemies
- say       : Imagine a working command LOL
- loop      : MIKAMIKAMIKAMIKAMIKAMIKAMIKA
- rate      : Let Violet rates your waifu
"""

@violet.command(name='whoareyou')
async def whoareyou(ctx):
    await ctx.send("I'm you but better 😎")



@violet.command(name='nournot')
async def nournot(ctx):
    await ctx.send("YES I AM!")



@violet.command(name='call')
async def call(ctx,user: discord.Member = None):
  with open("finally-awake-skyrim.gif", "rb") as gif:
    if user is not None:
      await ctx.send(f"{user.mention}\n\nHey you!\nYou're finally awake", file = discord.File(gif))
    else:
      await ctx.send(f"{ctx.author.mention}\n\nHey you!\nYou're finally awake", file = discord.File(gif))



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




"""
Calculation Series
----------------------
It's FebryanS so you should expect that

- pow   : Calculate power
- calc  : Calculator
- area  : Calculate the area of an 2D shapes
- moles : Calculate moles or particles
          amount of an atom/molecules
"""

@violet.command(name='pow')
async def pow(ctx, a: float, b: float):
    await ctx.send(a**b)



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



from Calculation import AtomTheory
atom = violet.create_group(name="atom")


@atom.command(name='particles')
async def aparticles(
  ctx,
  particles=None,
  moles: float=None
):
  try:
    particles = float(particles)
  except TypeError:
    pass

  base = AtomTheory(
    particles = particles,
    moles = moles
  )
  try:
    result = base.get_particles()
    await ctx.respond(result)
  except TypeError:
    await ctx.respond("バカですね．．．", ephemeral=True)


@atom.command(name='volume')
async def avolume(
  ctx,
  volume: float=None,
  moles: float=None,
  pressure: float=None,
  temperature: float=None,
):
  base = AtomTheory(
    volume = volume,
    moles = moles,
    pressure = pressure,
    temperature = temperature 
  )
  try:
    try:
      result = base.get_volume()
    except TypeError:
      result = base.get_volume("STP")
    await ctx.respond(result)
  except TypeError:
    await ctx.respond("バカですね．．．", ephemeral=True)


@atom.command(name='mass')
async def amass(
  ctx,
  mass: float=None,
  moles: float=None,
  molar_mass: float=None
):
  base = AtomTheory(
    mass = mass,
    moles = moles,
    molar = molar_mass
  )
  try:
    result = base.get_mass()
    await ctx.respond(result)
  except TypeError:
    await ctx.respond("バカですね．．．", ephemeral=True)




"""
Lyrics Series
-----------------
My Creator really loves music~

- ly      : Get a lyric from Lyrics Database
            You can search by index or title
- lylist  : All the available lyrics
- lysave  : Add lyrics to Lyrics Database
            Must be .txt file with:
            - 1st line : Song Title
            - 2nd line : Song by <artist>
            - 3rd line : Color: <hex> (Opt)
            - 5th - EOF: Lyrics Content
- lydel   : Delete a lyric from Lyrics
            Database
- lycolor : Change the embed color (hex)
"""

lyrics = violet.create_group(name="lyrics")

@lyrics.command(name='get')
async def ly(ctx, title):
  from Lyrics import formatted, iTunes, times

  try:
    title = int(title)
  except ValueError:
    pass
  name_format = formatted(title)
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
    await ctx.respond(f"{title} is not found in the Lyrics List")
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
    color = content[2].split(":")[1].strip()
    dominant_color = int(color[1:], 16)
    embed_color = dominant_color
  except:
    embed_color = discord.Color.blue()
    
  lyrics = discord.Embed(
    title = title, url = song['song'],
    description = artist,
    color = embed_color
  )
  if song['song'] != "":
    lyrics.add_field(
      name="Track Information",
      value=f"**Disc {song['disc']} Track** {song['track']}\n**Genre:** {song['genre']}\n\n{times(song['time'])}"
    )
  if content[4].lower().strip() != 'instrumental music':
    for row in the_rest:
      lyrics.add_field(
        name = "",
        value = row
      )
  else:
    lyrics.add_field(
      name="",
      value="**Instrumental Song**\nLet the music play"
    )
  if song['preview'] != "":
    lyrics.set_author(
      name="Preview",
      url = song['preview'],
      icon_url = song['art']
    )
  lyrics.set_image(url=song['art'])
  lyrics.set_footer(text=f"{song['album']}\nPrice: {song['price']}")
  await ctx.respond(embed = lyrics)



@lyrics.command(name='save')
async def lysave(ctx, file: discord.Attachment, title):
  
  format = str(file).split(".")[-1]

  name = title.title()
  file_format = title.lower()
  if format == "txt":
    await file.save(fp=f"Lyrics/Title/{file_format}.txt")
    await ctx.send(f"**{name}** is saved")
  else:
    await ctx.respond("The file you entered is not a text file", ephemeral=True)



@lyrics.command(name='delete')
@commands.is_owner()
async def lydel(ctx, file):
  from Lyrics import formatted
  
  if not file:
    command = await ctx.send("Please enter the lyrics name")
    await asyncio.sleep(30)
    await command.delete()
    return

  try:
    file = int(file)
  except ValueError:
    pass
    
  file_format = formatted(file)
    
  filename = file_format.replace("_"," ").title()
  try:
    os.remove(f"Lyrics/Title/{file_format}.txt")
    await ctx.respond(f'{filename} is deleted from the Lyrics List')

  except:
    await ctx.respond(f'Cannot find {filename} in the Lyrics List', ephemeral=True)



@lyrics.command(name='color')
@commands.is_owner()
async def lycolor(ctx, color: str, name):
  from Lyrics import formatted
  
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break

  all = []
  try:
    name = int(name)
  except ValueError:
    pass
  name_format = formatted(name)
    
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
    await ctx.respond("Please enter a valid color code in the hex format")
    return

  title = all[0].replace("\n","")
  await ctx.respond(f"{title}'s color is changed to #{color.upper()}")



@lyrics.command(
  name='list',
  description='List of the available lyrics'
)
async def lylist(
  ctx,
  type: discord.Option(
    choices=['Original','Romaji']
  )='Romaji',
  artist: bool=False,
  hidden: bool=True
):
  
  lyrics = lyrics_list(type)
  format_beta = []
  for i, (lyric,author) in enumerate(lyrics.items()):
    if artist is True:
      format_beta.append(
        f"{i+1} • **{lyric}** - {author}"
      )
    elif artist is False:
      format_beta.append(
        f"{i+1} • **{lyric}**"
      )
  
  embed = discord.Embed(title='Lyrics List', color = discord.Color.random())
  for part in parts(format_beta, 25):
    embed.add_field(name="", value="\n".join(part))
  await ctx.respond(embed=embed, ephemeral=hidden)


@lyrics.command(
  name='statistics',
  description='Artist statistics'
)
async def lystats(ctx):
  songs = sorted(
    os.listdir("Lyrics/Title"),
    key=lambda title: title.lower()
  )
  artist_list = []
  for song in songs:
    with open(f"Lyrics/Title/{song}", "r") as f:
      info = f.readlines()
      artists = info[1].split(" by ")[1].replace("\n","")
    artist_list.append(artists)

  counts = {}
  for i in artist_list:
    if i in counts:
      counts[i] += 1
    else:
      counts[i] = 1
  await ctx.respond("ちょっと待ってくださいね～", ephemeral=True)
  from Memories import data_chart
  data_chart(
    "Artist Statistics",
    counts,
    (16,9)
  )
  with open("Memories/Chart.png","rb") as f:
    await ctx.respond(file=discord.File(f))

  os.remove("Memories/Chart.png")





"""
Conversion Series
--------------------
It's FebryanS so you should expect that v2

- decimal : Convert from decimal (base 10)
- binary  : Convert from binary  (base  2)
- hexa    : Convert from hexadec (base 16)
- octal   : Convert from ocal    (base  8)
"""

convert = violet.create_group(name="convert")

@convert.command()
async def decimal(ctx,
  base: discord.Option(choices=['Binary','Octal','Hexadecimal']), number: str):
  base = base.lower()
  try:
    number = int(number)
  except ValueError:
    await ctx.respond(f"**{number}** is not a valid **integer**.")
    return
  if base == 'binary':
    await ctx.respond(f"**{number}** converted to binary is **{bin(number)[2:]}**")
  elif base == 'hexadecimal':
    await ctx.respond(f"**{number}** converted to hexadecimal is **{str(hex(number)[2:]).upper()}**")
  elif base == 'octal':
    await ctx.respond(f"**{number}** converted to octal is **{oct(number)[2:]}**")
  else:
    await ctx.respond(f"**{base.capitalize()}** is not a valid base.")


@convert.command()
async def binary(ctx, base: discord.Option(choices=['Octal','Decimal','Hexadecimal']), number: str):
    base = base.lower()
    try:
        int(number, 2)
    except ValueError:
        await ctx.respond(f"**{number}** is not a valid binary number.")
        return
    if base == 'decimal':
        decimal = int(number, 2)
        await ctx.respond(f"**{number}** converted to decimal is **{decimal}**")
    elif base == 'hexadecimal':
        await ctx.respond(f"**{number}** converted to hexadecimal is **{str(hex(int(number, 2))[2:]).upper()}**")
    elif base == 'octal':
        await ctx.respond(f"**{number}** converted to octal is **{oct(int(number, 2))[2:]}**")
    else:
        await ctx.respond(f"**{base.capitalize()}** is not a valid base.")


@convert.command()
async def hexa(ctx, base: discord.Option(choices=['Binary','Octal','Decimal']), number: str):
    base = base.lower()
    try:
        int(number, 16)
    except ValueError:
        await ctx.respond(f"**{number}** is not a valid **hexadecimal** number.")
        return
    if base == 'decimal':
        decimal = int(number, 16)
        await ctx.respond(f"**{number}** converted to decimal is **{decimal}**")
    elif base == 'binary':
        await ctx.respond(f"**{number}** converted to binary is **{(bin(int(number, 16))[2:])}**")
    elif base == 'octal':
        await ctx.respond(f"**{number}** converted to octal is **{oct(int(number, 16))[2:]}**")
    else:
        await ctx.respond(f"**{base.capitalize()}** is not a valid base.")


@convert.command()
async def octal(ctx, base: discord.Option(choices=['Binary','Decimal','Hexadecimal']), number: str):
    base = base.lower()
    try:
        int(number, 8)
    except ValueError:
        await ctx.respond(f"**{number}** is not a valid **octal** number.")
        return
    if base == 'decimal':
        decimal = int(number, 8)
        await ctx.respond(f"**{number}** converted to decimal is **{decimal}**")
    elif base == 'binary':
        await ctx.respond(f"**{number}** converted to binary is **{bin(int(number, 8))[2:]}**")
    elif base == 'hexadecimal':
        await ctx.respond(f"**{number}** converted to hexadecimal is **{(str(hex(int(number, 8))[2:])).upper()}**")
    else:
        await ctx.respond(f"**{base.capitalize()}** is not a valid base.")




"""
Utility Series
----------------
Some APIs that might be useful

- qr    : Get a QR code od an URL
- short : Get a short URL from UUUURRRRLLLL
- urban : This.
"""

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
async def short(ctx, long_url= None):
  if long_url is not None:
    response = requests.get(f'http://tinyurl.com/api-create.php?url={long_url}')
    short_url = response.text
    await ctx.send(f"Here's your shortened URL\n{short_url}")
  else:
    await ctx.send(f"Please enter the URL you're trying to shorten, {ctx.author.mention}-san")




"""
Database Series
------------------
Want Violet to remember something for you?

- url   : Using Replit Database save URLs
- notes : Take, edit, read, delete notes
           Your choices :)
- data  : Private database for you ;)
"""

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
async def data(ctx, action=None, key=None, *value):
  user = ctx.author.id
  name = violet.get_user(user)
  avatar = ctx.author.avatar
  
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break
  
  db = Database("Database/UserData", user)

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

  elif act == 'edit' and key is not None:
    values = " ".join(value)
    result = db.edit_data(key,values)
    msg = await ctx.send(f"「**{key}**」content is updated to「**{values}**」")
    
  else:
    msg = await ctx.send("Please enter the **RIGHT** action")
    await asyncio.sleep(60)
    await msg.delete()




"""
YouTube Series
-----------------
Violet will use YouTube API to do you a favor~

- yt     : Get information about a video
           or even their description
- ytdl   : Download a video or its audio
- ytlist : All the data of download video
- thumb  : Get a video thumbnail
- pp     : Get a channel icon from video URL
"""

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
    channel_icon = ytAPI.Channel(channel_id).info()

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
    msg = await ctx.send("Cannot find the URL content")
    await asyncio.sleep(30)
    await msg.delete()
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

      
    video_format = ["• " + i for i in video_list]
    audio_format = ["• " + i for i in audio_list]
    print(video_format)
      
    data_list = discord.Embed(title="YouTube Database", url= random_url, color=discord.Color.red())
    data_list.add_field(name="Video", value="")
    for i in parts(video_format, 10):
      data_list.add_field(name='',value="\n".join(i))
      
    data_list.add_field(name="Audio", value='')
    for i in parts(audio_format, 10):
      data_list.add_field(name='',value="\n".join(i))
    data_list.set_thumbnail(url=bot_info.image_url)
    data_list.set_image(url = thumbnail)
    data_list.set_footer(text=yt_title, icon_url=channel_icon)
    await ctx.send(embed=data_list)



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




"""
Documents Series
-------------------
Want Violet to write documents?
Sure, why not

- excel : Create a simple excel document
- txt   : Create a text document
"""

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




"""
Anime Series
----------------
Otaku saves the world they say

- mal   : Search anime, character
          even user on MyAnimeList 
- waifu : Get a random waifu picture
- quote : Get a random quote from anime
"""

anime = violet.create_group(name='anime')

@anime.command(name='myanimelist')
async def mal(
  ctx,
  terms: discord.Option(
    choices=['Anime','Character','User']),
    title
):
  from MyAnimeList import ordinals, MyAnimeList
  if terms is None:
    await ctx.respond("Please enter the valid search category")
    return

  if not title:
    await ctx.respond(f"Please enter the title, {ctx.author.mention}-san")
    return
    

# AnimeSearch
  if terms.lower() == 'anime':
    try:
      anime = MyAnimeList.AnimeSearch(title)
      info = anime.info()
    except IndexError:
      await ctx.respond("Can't find the series")
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

    theme = discord.Embed(title=title_og ,url=url, description=f"**{type}**\n**Season**: {season}\n**Year**: {year}\n**Rank**: {ordinals(rank)}\n**Status**: {status}", color = color)

    theme.add_field(name="", value = f"**[{title_og} Trailer]({trailer})**")
    for i in synopsis:
      theme.add_field(name="", value=i)
    theme.set_image(url=image)
    theme.set_footer(text=title_jp)
    await ctx.respond(embed=theme)

# UserSearch
  elif terms.lower() == 'user':
    try:
      user = MyAnimeList.UserSearch(title).info()
    except IndexError:
      await ctx.respond("User not found")
      return

    username = user['username']
    url = user['user_url']
    profile = user['profile']
    status = user['status']

    embed = discord.Embed(title=username, url=url, description=f"Last Online: {status}")
    embed.set_image(url=profile)
    await ctx.respond(embed=embed)

# CharaSearch
  elif terms.lower() == 'character':
    try:
      chara = MyAnimeList.CharaSearch(title).info()
    except IndexError:
      await ctx.respond("User not found")
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
    await ctx.respond(embed=embed)

    
  else:
    await ctx.respond(f"Please enter the right category, {ctx.author.mention}-san")



@anime.command(name='waifu')
async def waifu(ctx, tags, nsfw:bool=False):
  tags = list(tags.split(" "))
  wf = WaifuIm("search").waifu(tags,nsfw)

  color = int(wf['color'][1:], 16)
  embed = discord.Embed(
          title = "Your Waifu",
          url = wf['source'],
          color = color)
  embed.set_image(url = wf['url'])
  await ctx.respond(embed=embed)


  
@anime.command()
async def quote(
  ctx,
  language: discord.Option(
    choices=['English', 'Indonesian'])
):
  if language == 'English':
    lang = 'en'
  elif language == 'Indonesian':
    lang = 'id'

  q = Kyoko('quotes').quotes()
  embed = discord.Embed(title="")
  embed.add_field(name=q[lang],
      value=f"By {q['chara']}\nFrom {q['series']}")
  await ctx.respond(embed = embed)




"""
Image Series
---------------
Using PIL module to generate and edit images
A.K.A Too lazy to open Photoshop

- color  : Get a dominant color from an
           image
- square : crop an image into a square
"""

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
async def square(ctx):
  file = ctx.message.attachments
  await file[0].save(fp='Image/CropSquare/raw.png')
  CropSquare('Image/CropSquare/raw', 'Image/CropSquare/result')
  with open('Image/CropSquare/result.png', "rb") as f:
    await ctx.send(file=discord.File(f))




"""
OpenAI Series
----------------
All of OpenAI APIs that available

- chatgpt : Get an answer for your random               question that doesn't even
            makes any sense
- codegpt : ChatGPT Programmer Mode
- imagine : Let DALL-E generate an image
            from your wild imagination
- var     : Create a variation of an image
- openai  : My Creator knows all of your
            warcrimes
            You Can (Not) Escape
"""

@violet.command()
async def chatgpt(ctx, *prompt):
  user = violet.get_user(ctx.author.id)

  if not prompt:
    await ctx.send("Please enter the prompt")
    return
  prompt = " ".join(prompt)
  progress = await ctx.send("Generating Answer\n少々お待ちください....")
  
  try:
    response = OpenAI().ChatGPT(prompt)
  except:
    await ctx.send("An error occurred. Please try again")
    await progress.delete()
    return
  OpenAIData('ChatGPT').add_data(prompt,response)
  await progress.delete()
  if len(response) > 1024:
    with open("OpenAI/chatgpt.txt", "w") as f:
      f.write(f"{prompt}\n\n{response}")
    with open("OpenAI/chatgpt.txt", "rb") as f:
      await ctx.send(
        "Discord didn't allow Violet to sent something more than 1024 characters so, here you go",
        file=discord.File(f)
      )
    os.remove("OpenAI/chatgpt.txt")
    return

  theme = discord.Embed(
            title=prompt,
            description=f"By {user}",
            color = 0xFFFFFF
  )
  theme.add_field(
    name="Answer",
    value = response
  )
  await ctx.send(f"{ctx.author.mention}, Here you go!", embed=theme)
  


@violet.command()
async def codegpt(ctx, *prompt):
  if not prompt:
    await ctx.send("Please enter the prompt")
    return
  prompt = " ".join(prompt)

  progress = await ctx.send("Generating Codes\n少々お待ちください....")

  result = OpenAI().CodeGPT(prompt)

  OpenAIData('CodeGPT').add_data(prompt,result)
  await progress.delete()
  with open("OpenAI/Codes.txt", "w") as raw:
    raw.write(result)

  with open("OpenAI/Codes.txt", "rb") as f:
    await ctx.send(f"{ctx.author.mention}, Here you go!", file = discord.File(f))
  os.remove("OpenAI/Codes.txt")



@violet.command()
async def imagine(ctx, *prompt):
  my_creator = violet.get_user(bot_info.owner)
  
  if not prompt:
    await ctx.send("Please enter the prompt")
    return
  prompt = " ".join(prompt)
  
  progress = await ctx.send("Generating Image\n少々お待ちください....")

  try:
    result = OpenAI().DALLE(prompt)
  except openai.InvalidRequestError:
    msg1 = await ctx.send("Please don't make My Creator gets banned...")
    await asyncio.sleep(1)
    msg2 =await ctx.send(f"{my_creator.mention},\n{ctx.author.mention} committed a war crime!")
    await asyncio.sleep(30)
    await msg1.delete()
    await asyncio.sleep(1)
    await msg2.delete()
    return
  OpenAIData('DALL_E').add_data(prompt)
  await progress.delete()
  theme = discord.Embed(title=prompt.title(), description = "", color = 0xFFFFFF)
  theme.set_image(url=result)
  await ctx.send(f"{ctx.author.mention}, here you go!", embed=theme)



@violet.command()
async def var(ctx):
  file = ctx.message.attachments
  if not file:
    await ctx.send("Please attach the image")
    return

  format = FileNames(file).format()
  if format not in ['jpg','png','jpeg']:
    await ctx.send(f"{format.upper()} file is not supported")
    return

  progress = await ctx.send("Generating Variation\n少々お待ちください....")
  await file[0].save(fp="OpenAI/Image/raw.png")

  CropSquare('OpenAI/Image/raw', 'OpenAI/Image/edited')
  result = OpenAI().Variation()
  await progress.delete()
  theme = discord.Embed(title="Variation", color= 0xFFFFFF)
  theme.set_image(url=result)
  await ctx.send(f"{ctx.author.mention}, here you go", embed=theme)
  os.remove("OpenAI/Image/raw.png")
  os.remove("OpenAI/Image/edited.png")



@violet.command()
@commands.is_owner()
async def openai(ctx, terms):
  if terms.lower() == 'chatgpt':
    table = 'ChatGPT'
  elif terms.lower() == 'codegpt':
    table = 'CodeGPT'
  elif terms.lower() == 'dalle':
    table = 'DALL_E'
  else:
    await ctx.send("Bruh....")
    return

  data = OpenAIData(table).list_data()
  with open(f"OpenAI/{table}.txt", "w") as f:
    f.write(f"{table} Database\n\n")
    for key, value in data.items():
      f.write(f"\n•「{key}」")
      f.write(value+"\n\n\n")

  total = len([key for key,value in data.items()])
  with open(f"OpenAI/{table}.txt","rb") as file:
    await ctx.send(f"{ctx.author.mention}, Here you go!\nTotal {total} requests", file = discord.File(file))
  os.remove(f"OpenAI/{table}.txt")




"""
Violet's Memories
---------------------
A little secret between Violet
and her creator~

- embrace  : ヒ・ミ・ツ〜
- get      : ヒ・ミ・ツ〜
- remember : ヒ・ミ・ツ〜
- forget   : ヒ・ミ・ツ〜
- recount  : ヒ・ミ・ツ〜
- cate     : ヒ・ミ・ツ〜
- category : ヒ・ミ・ツ〜
"""
memories = violet.create_group(name="memories")

@memories.command(name='embrace')
@commands.is_owner()
async def embrace(ctx, url, name):
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break
 
  if url is None:
    await ctx.send("Please enter the url")
    return

  url = url.split("?")[0]
  if not name:
    await ctx.send("Please enter the name of someone you want Violet to remember")
    return
  characters = name.title()

  if "yande.re" in url:
    table = 'yandere'
  elif 'danbooru' in url or 'donmai.us' in url:
    table = 'danbooru'
  else:
    await ctx.respond("Violet can't remember that")
    return

  try:
    Database("Memories/Violet's Memories", table).add_data(url, characters)
  except:
    msg = await ctx.send("That post is already in my heart")
    await asyncio.sleep(30)
    await msg.delete()
    return

  res = await ctx.respond(f"Violet will remember {characters} from now on for your sake")
  await asyncio.sleep(30)
  await res.delete()



@memories.command(name='get')
@commands.is_owner()
async def get(
    ctx,
    choice: discord.Option(choices=['Yandere','Danbooru']),
    hidden: bool=True):
  from Memories import Yandere
  data = Database("Memories/Violet's Memories", choice.lower()).list_data()
  link = []
  chara = []
  for key, value in data.items():
    link.append(key)
    chara.append(value)

  gacha = random.randint(0,len(link)-1)
  embed = discord.Embed(title=chara[gacha],url=link[gacha])
  if "yande.re" in link[gacha]:
    yd = Yandere(link[gacha]).post()
    
    embed.add_field(name="Tags", value=yd['tags'].replace("_"," "))
    embed.add_field(name="",value= f"**[SOURCE]({yd['post_url']})**")
    embed.set_image(url=yd['sample'])
    
  else:
    embed.set_image(url=link[gacha])
    
  res = await ctx.respond(embed=embed, ephemeral=hidden)



@memories.command(name='remember')
@commands.is_owner()
async def remember(
  ctx,
  choice: discord.Option(choices=['Yandere','Danbooru']),
  search: str,
  hidden: bool=True):
  from MyAnimeList import ordinals
  from Memories import Yandere

  raw = Database("Memories/Violet's Memories", choice.lower()).get_like(search.split(" "))
  results = {key:value for key,value in sorted(raw.items(), key=lambda x: x[1])}
  total_post = len([value for key,value in results.items()])
  random_number = random.randint(0,total_post-1)
  random_post = [key for key,value in results.items()][random_number]
  order = ordinals(random_number+1)

  with open(f"Memories/{choice}.txt", "w", newline='') as f:
    f.write(choice+"\n\n")
    for i, (key,value) in enumerate(results.items()):
      f.write(f"{i+1} •「{value.replace(',',' |')}」\n{key}\n\n")

  if total_post > 1:
    post = "posts"
  else:
    post = "post"

  embed = discord.Embed(title=search.title(), description=f"Total {total_post} {post}", url=random_post)
  if "yande.re" in random_post:
    yd = Yandere(random_post).post()

    embed.add_field(name="Tags", value=yd['tags'].replace("_"," "))
    embed.add_field(name="",value= f"**[SOURCE]({yd['post_url']})**")
    embed.set_image(url=yd['sample'])
    
  else:
    embed.set_image(url=random_post)
  embed.set_footer(text=f"{order} post of「{search.title()}」")
  with open(f"Memories/{choice}.txt", "rb") as file:
    await ctx.respond(embed=embed, file=discord.File(file), ephemeral=hidden)
  os.remove(f"Memories/{choice}.txt")



@memories.command(name='forget')
@commands.is_owner()
async def forget(ctx, link):
  async for command in ctx.history(limit=2):
    if command.author == ctx.author:
      await command.delete()
      break

  if link is None:
    await ctx.send("Please enter the URL you want Violet to forget")
    return
  if "yande.re" in link:
    table = 'yandere'
  elif 'danbooru' in link or 'donmai.us' in link:
    table = 'danbooru'
  else:
    await ctx.send("Who?")
    return

  try:
    data = Database("Memories/Violet's Memories", table)
    get = data.get_data(link)
    data.del_data(link)
  except sqlite3.InterfaceError:
    await ctx.send("Violet don't think she remembered it")
    return

  pic = discord.Embed(title=get)
  pic.set_image(url=link)
  await ctx.respond("Violet will forget", embed=pic, ephemeral = True)



@memories.command(name='recount')
@commands.is_owner()
async def recount(ctx, choice: discord.Option(choices=['Yandere','Danbooru'])):

  all = Database("Memories/Violet's Memories", choice.lower()).list_data()
  data = []
  for url, chara in all.items():
    data.append(chara)

  data = ",".join(data).split(",")
  for i,value in enumerate(data):
    data[i] = value.strip()
  counts = {}
  for i in sorted(data):
    if i in counts:
      counts[i] += 1
    else:
      counts[i] = 1

  top_chara = "\n".join(top(counts, 10))
  await ctx.respond("Violet is trying to remember stuff right now\nPlease wait a moment...", ephemeral=True)
  from Memories import data_chart
  data_chart(choice,counts,(16,9))

  embed = discord.Embed(title=choice, description=f"Total {len(data)} Posts in Violet's Memories")
  embed.add_field(name="Top Characters", value=top_chara)
  with open("Memories/Chart.png", "rb") as f:
    await ctx.respond(file=discord.File(f),embed=embed, ephemeral = True)
  os.remove("Memories/Chart.png")



@memories.command(name='precious')
@commands.is_owner()
async def cate(ctx):
  from Memories import Yandere

  await ctx.respond("Violet is trying to remember stuff right now\nPlease wait a moment...", ephemeral=True)

  raw = Database("Memories/Violet's Memories", "yandere").list_data()

  tags = []
  for key, value in raw.items():
    filter = Yandere(key).filter[2:]
    tags += filter
  
  tags_count = {}
  for i in sorted(tags):
    if i in tags_count:
      tags_count[i] += 1
    else:
      tags_count[i] = 1

  top_tags = "\n".join(top(tags_count, 5))
  from Memories import data_chart
  data_chart("Yandere",tags_count,(16,9))
  
  embed = discord.Embed(
          title = "Top Yandere Tags",
          description = top_tags
          )
  
  with open("Memories/Chart.png", "rb") as f:
    await ctx.respond(
        embed = embed,
        file  = discord.File(f),
        ephemeral = True
        )
    
  os.remove("Memories/Chart.png")



@memories.command(name='contents')
@commands.is_owner()
async def category(ctx):
  from Memories import Yandere
  
  raw = Database("Memories/Violet's Memories", "yandere").list_data()
  
  tags = []
  for key, value in raw.items():
    filter = Yandere(key).filter[2:]
    tags += filter

  tags_list = set()
  for i in tags:
    tags_list.add(i)

  formatted = [f"- {i}" for i in sorted(tags_list)]

  with open("Memories/Tags.txt","w", newline='') as f:
    f.write("Available Tags\n\n")
    f.write("\n".join(formatted))

  with open("Memories/Tags.txt","rb") as file:
    await ctx.respond(f"{ctx.author.mention}, here you go",file=discord.File(file), ephemeral=True)
  os.remove("Memories/Tags.txt")




"""
Deep Learning Series
------------------------
No description yet
"""

dl = violet.create_group(name="deeplearning")

@dl.command(name = 'deepbooru')
async def deepbooru(
  ctx,
  image: discord.Attachment,
  hidden:bool=False
):
  if ctx.author != violet.get_user(owner):
    hidden = False

  await ctx.respond("Violet is trying to think about stuff right now\nPlease wait a moment...", ephemeral=True)
  
  tags = Deepbooru(image)
  top_tag = next(iter(tags))
  _,*rest = tags.items()

  display = discord.Embed(
    title=f"Top Tag 「{top_tag}」",
    description=f"Results\n{str(tags[top_tag])[:5]} Accuracy",
    url=f"https://danbooru.donmai.us/posts?tags={top_tag.replace(' ','_').lower()}"
  )

  for tag, accuracy in dict(rest).items():
    display.add_field(
      name=f"• 「{tag}」",
      value=f"{str(accuracy)[:5]} Accuracy"
      )
    
  display.set_image(url=image)
  display.set_footer(text="Using Deepbooru Model")
  display.set_thumbnail(url=bot_info.image_url)
  await ctx.respond(embed=display, ephemeral=hidden)



@dl.command(name='stablediffusion')
@commands.is_owner()
async def stablediffusion(
  ctx,
  prompt,
  negative_prompt=None):
  await ctx.respond(
    "少々お待ちください",
    ephemeral=True
  )
  
  results = StableDiffusion().input(prompt,negative_prompt)
  
  embed = discord.Embed(
    title = prompt.title(),
    color = 0xFFFFFF,
    description = f"Negative Prompts: {results['negative_prompt']}"
  )
  embed.set_author(
    name = "Stable Diffusion by Stability AI",
    url = "https://stability.ai/blog/stable-diffusion-public-release",
    icon_url = "https://pbs.twimg.com/profile_images/1605286457207410701/Tac59LxK_400x400.jpg"
  )
  embed.set_image(url=results['image_url'])

  embed.set_footer(
    text=f"Resolution: {results['dimensions']}\nSteps: {results['steps']}\nGuidance Scale: {results['scale']}\nScheduler: {results['scheduler']}"
  )
  await ctx.respond(embed=embed)


#WIP
@dl.command(name='pastel-mix')
async def pastelmix(
  ctx,
  prompt:str,
  negative_prompt: str=None,
  width: int=512,
  height: int=512,
  steps: int=20,
  hires: bool=True,
  guidance: int=7,
  seed: int=0
):
  await ctx.respond(
    f"Generating\n{prompt.title()}\nNegative prompts: {negative_prompt}\nDimensions: {width}x{height}\nSteps: {steps}\nGuidance: {guidance}\nHires: {hires}\nSeed: {seed}"
  )
  prediction = PastelMix().input(
    prompt,
    negative_prompt,
    width,
    height,
    steps,
    guidance,
    seed,
    hires
  )
  embed = discord.Embed(title=prompt.title())
  #embed.set_image(url=prediction[0])
  print(list(prediction[0]))
  await ctx.respond(embed=embed)



"""
Nostalgia
-------------
Prefix commands version
"""

prefixs = os.listdir("PrefixCommands")
prefix_list = [
  i.split(".")[0] for i in prefixs
]

for prefix in prefix_list:
  violet.load_extension(f'PrefixCommands.{prefix}')


violet.load_extension('Commands.app_command')



"""
Violet's Soul
-----------------
Everything that keeps Violet alive
"""

Heart()
violet.run(os.getenv("Violet's Precious Thing"))