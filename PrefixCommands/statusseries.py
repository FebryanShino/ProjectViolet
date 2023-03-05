import discord
from discord.ext import commands
import os
import asyncio
from Violet import bot_info
import csv

class StatusSeries(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def status(self, ctx):
    progress = await ctx.send("Creating a chart\nPlease wait a moment...")
  
    from Violet.StatusData import StatusData
    type = StatusData()
    data = discord.Embed(title='Status Database', color = 0xe5dbca)
    data.add_field(name='Status Counts',value= f"**Listening**: {type['music']}\n**Playing**: {type['game']}\n**Watching**: {type['movie']}")
    data.set_thumbnail(url=bot_info.image_url)
  
    with open("Violet/Chart.jpg", "rb") as f:
      await progress.delete()
      await asyncio.sleep(1)
      await ctx.send(embed=data,file=discord.File(f))
    os.remove("Violet/Chart.jpg")


  @commands.command()
  @commands.is_owner()
  async def addstatus(self, ctx, activity = None, *name):
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
        
        msg = await ctx.send(f"「{activity} {formatted_name}」is added into the status list")
        await asyncio.sleep(5)
        await msg.delete()
      
      else:
        msg3 = await ctx.send(f"{activity.capitalize()} is not a valid activity, yet")
        await asyncio.sleep(30)
        await msg3.delete()

  
  @commands.command()
  async def sortstatus(ctx):
    async for command in ctx.history(limit=2):
      if command.author == ctx.author:
        await command.delete()
        break
    from Violet.algorithm import SortStatus
    SortStatus()
    msg = await ctx.send("Violet has finished sorting and filtering the Status List.")
    await asyncio.sleep(30)
    await msg.delete()

  @commands.command(name='setstatus')
  @commands.is_owner()
  async def setstatus(ctx, action, *status):

    type = discord.ActivityType
    if action.lower() == 'listening':
      act = type.listening
    elif action.lower() == 'watching':
      act = type.watching
    elif action.lower() == 'playing':
      act = type.playing
    else:
      await ctx.send("Baaaka.")
      return

    status = " ".join(status)
    if action.lower() == 'listening':
      action = f"{action} to"
    await commands.change_presence(activity=discord.Activity(type=act, name=status))
    await ctx.send(f'Status set to: {action.capitalize()} {status}')



def setup(bot):
  bot.add_cog(StatusSeries(bot))
