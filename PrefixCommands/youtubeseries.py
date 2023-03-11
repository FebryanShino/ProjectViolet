import discord
from discord.ext import commands
from YouTube import ytAPI
from pytube import YouTube, exceptions
import asyncio
import requests
import csv
import pandas as pd
import os
import random
from Lyrics import parts
from Violet import bot_info


class YouTubeSeries(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.command()
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

  
    theme = discord.Embed(
      title=title,
      url=link,
      description=f"[{author}]({channel_home})",
      color = discord.Color.blue()
    )
  
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



  @commands.command()
  async def ytlist(self, ctx, action = None, attribute = None):

    if action is not None and action.lower() in ['dl', 'download']:
      if attribute is not None and attribute.lower() == 'excel':
        file_original = pd.read_csv('YouTube/Database.csv')
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
      if ctx.author != self.bot.get_user(bot_info.owner):
        await ctx.send("You need My Master's permission to clean up the database")
        return
      
      with open("YouTube/Database.csv", "w", newline='') as data:
        writer = csv.writer(data)
        writer.writerow(["TITLE","YOUTUBE"])
      await ctx.send("Finished cleaning up YouTube Database")
  
    else:
      row_list = []
      with open("YouTube/Database.csv", "r") as data:
        reader = csv.reader(data)
        next(reader)
        for row in reader:
          row_list.append(row)

      yt_url_list = []
      title_list = set()
      for row in row_list:
        title = row[0]
        yt_url = row[1]
        formatted = "[{}]({})".format(title, yt_url)
        title_list.add(formatted)
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

      
      title_format = ["• " + i for i in title_list]
      
      data_list = discord.Embed(
        title = "YouTube Database",
        color = discord.Color.red()
      )
      for i in parts(title_format, 10):
        data_list.add_field(
          name='',
          value="\n".join(i)
        )
      data_list.set_author(
        name=self.bot.user.name,
        icon_url=bot_info.image_url,
        url=random_url
      )
      data_list.set_image(url = thumbnail)
      data_list.set_footer(
        text=yt_title,
        icon_url=channel_icon
      )
      await ctx.send(embed=data_list)




    
  @commands.command()
  async def thumb(self, ctx, source=None):
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

  @commands.command()
  async def pp(self, ctx, link = None):
    try:
      yt = YouTube(link)
      author = yt.author
      title = yt.title
      channel_id = yt.channel_id
    except exceptions.RegexMatchError:
      await ctx.send("バカですね...")
      return
  
    channel_icon = ytAPI.Channel(channel_id).info()

    profile = discord.Embed(
      title=author,
      url=channel_icon,
      color = discord.Color.random())
    profile.set_image(url=channel_icon)
    profile.set_footer(text=title)
  
    await ctx.send(embed=profile)



def setup(bot):
  bot.add_cog(YouTubeSeries(bot))