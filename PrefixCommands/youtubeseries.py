import discord
from discord.ext import commands
from YouTube import ytAPI

class YouTubeSeries(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
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