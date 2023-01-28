import discord
from discord.ext import commands
import os
import openai
from keep_alive import keep_alive
from ratelimiter import RateLimiter
from sympy import *
import math
import random
import requests
import asyncio
import qrcode
from PIL import Image
from replit import db
import xml.etree.ElementTree as ET
from disappointment import disappointment_sentence_list
from MY_LOVE import MY_LOVE
from praise import praise_high,praise_mid,praise_low
from Status import status_l, status_p
from lyrics import lyrics
from help_command import help_name, help_value



owner = int(os.getenv('MY_ID'))

intents = discord.Intents.all()

violet = commands.Bot(command_prefix='!', intents=intents,owner_ID = owner)

openai.api_key = os.getenv('API')

command_limiter = RateLimiter(max_calls=1, period=1)

bot_name = 'ヴァイオレット'
channel_id = os.getenv('CHANNEL_ID')



async def change_status():
  while True:
    status_listening = random.choice(status_l)
    status_playing = random.choice(status_p)
    try:
      await violet.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_listening))
      await asyncio.sleep(60)
      await violet.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status_playing))
      await asyncio.sleep(60)
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
async def helpme(ctx):
  embed = discord.Embed(title="Welcome to Violet Bot Command Center\nHere are the available commands:", color = discord.Color.blue())
  
  for i in range(0,18):
    embed.add_field(name = help_name[i], value = help_value[i], inline=False)
  await ctx.send(embed=embed)



  

@violet.command(name='setstatus')
@commands.is_owner()
async def setstatus(ctx, *, status):
  await violet.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
  await ctx.send(f'Status set to: Listening to {status}')



@violet.command(name='call')
async def call(ctx,user: discord.Member = None):
  if user is not None:
    await ctx.send(f"{user.mention}\n\nHey you!\nYou're finally awake")
  else:
    await ctx.send(f"{ctx.author.mention}\n\nHey you!\nYou're finally awake")



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
async def rate(ctx, waifu: str, l_name: str = None):
  waifu = waifu.lower()
  gacha_rate = int(random.randint(0,100))
  praise_h = random.choice(praise_high)
  praise_m = random.choice(praise_mid)
  praise_l = random.choice(praise_low)
  disappointment = random.choice(disappointment_sentence_list)
  l_name = "" if l_name is None else l_name
  
  if waifu in MY_LOVE:
    await ctx.send(f"She's 1000/100, no doubt about that.\n- {bot_name}")


  elif waifu.isalpha():
    if gacha_rate>=75:
      await ctx.send(f"{waifu.capitalize()} {l_name.capitalize()}'s beauty rate is {gacha_rate}/100.\n{praise_h}\n- {bot_name}")
    elif gacha_rate>=50:
      await ctx.send(f"{waifu.capitalize()} {l_name.capitalize()}'s beauty rate is {gacha_rate}/100.\n{praise_m}\n- {bot_name}")
    else:
      await ctx.send(f"{waifu.capitalize()} {l_name.capitalize()}'s beauty rate is {gacha_rate}/100.\n{praise_l}\n- {bot_name}")

  else:
    await ctx.send(f'{disappointment}\n- {bot_name}')



@violet.command(name='moles')
async def moles(ctx, find: str, a: float):
  AV_N = 6.02214076e23
  if find == 'mol':
    await ctx.send(f'The moles amount of **{a} particles** is **{a/AV_N} moles**')

  if find == 'partikel':
    await ctx.send(f'The particle amound of **{a} moles** is **{format(a*AV_N)}**')



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



@violet.command(name='lyric')
async def lyric(ctx, *, word: str):
  word = word.lower()

  if word == 'saltatio favillae':
    await ctx.send(lyrics[0])
  elif word == 'true':
    await ctx.send(lyrics[1])
  elif word == 'moon halo':
    await ctx.send(lyrics[2])
  elif word in ['花の塔', 'hana no tou', 'はなのとう']:
    await ctx.send(lyrics[3])
  elif word in ['きみの名前', 'kimi no namae', 'きみのなまえ']:
    await ctx.send(lyrics[4])
  else:
    await ctx.send("Can't find the lyrics")



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


#work in progress
#@violet.command()
async def danbooru(ctx, *tags: str):
    danbooru_user = os.getenv('DB_USERNAME')
    danbooru_api = os.getenv('Chicken')

    params = {'tags': ' '.join(tags), 'login': danbooru_user, 'api_key': danbooru_api}
    try:
        response = requests.get('https://danbooru.donmai.us/posts.xml', params=params)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        if len(root) > 0:
          post = random.choice(root)
          image_url = post.find('file-url').text
          image_source = post.find('source').text
          image_artist = post.find('tag-string-artist').text
          
          await ctx.send(f"Artist: {image_artist}\nSource: {image_source}\nImage URL: {image_url}")
        else:
          await ctx.send("No image found with the given tags")
    except requests.exceptions.RequestException as err:
      await ctx.send(f"An error occurred {str(err)}")
    
    except IndexError:
      await ctx.send(f"No images is found with {tags} tags")

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
  if act is not None:
    act = act.lower()
    if act == 'save' and key is not None and value is not None:
      db[key] = value
      await ctx.send(f"'{key}' is saved")
    elif act == 'get' and value is None:
      value = db[key]
      await ctx.send(f"URL for '{key}' is\n{value}")
    elif act == 'del' and value is None:
      del db[key]
      await ctx.send(f"'{key}' is deleted")
    elif act == 'list' and key is None and value is None:
      keys = sorted(list(db.keys()))
      keys_list = "\n".join(["• " + i for i in keys])
      embed = discord.Embed(title="Key Database", color = discord.Color.red())
      embed.add_field(name="", value = keys_list)
      await ctx.send(embed=embed)
    else:
      await ctx.send(f"{act} is not a valid input")
  else:
    await ctx.send("You need to enter something...")
      
keep_alive()
violet.run(os.getenv('YEET'))
