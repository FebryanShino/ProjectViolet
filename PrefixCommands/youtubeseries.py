import discord
from discord.ext import commands
from YouTube import ytAPI
from pytube import YouTube
import asyncio
import requests

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



def setup(bot):
  bot.add_cog(YouTubeSeries(bot))