import discord
from discord.ext import commands
from replit import db
from Violet import bot_info

class DatabaseSeries(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  
  @commands.command()
  async def url(
    self, ctx,
    act = None,
    key = None,
    value = None
  ):
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
      if ctx.author != self.bot.get_user(bot_info.owner):
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

def setup(bot):
  bot.add_cog(DatabaseSeries(bot))