import discord
from discord.ext import commands
from Database import Database
import os
import asyncio
import sqlite3 
import random

class Memo(commands.Cog):
  def __init__(self,bot):
    self.bot = bot


  @commands.command()
  @commands.is_owner()
  async def embrace(self, ctx, url=None, *chara):
    async for command in ctx.history(limit=2):
      if command.author == ctx.author:
        await command.delete()
        break
 
    if url is None:
      await ctx.send("Please enter the url")
      return

    url = url.split("?")[0]
    if not chara:
      await ctx.send("Please enter the name of someone you want Violet to remember")
      return
    characters = " ".join(chara).title()

    if "yande.re" in url:
      table = 'yandere'
    elif 'danbooru' in url or 'donmai.us' in url:
      table = 'danbooru'
    else:
      await ctx.send("Violet can't remember that")
      return

    try:
      Database("Memories/Violet's Memories", table).add_data(url, characters)
    except:
      msg = await ctx.send("That post is already in my heart")
      await asyncio.sleep(30)
      await msg.delete()

      return

    res = await ctx.send(f"Violet will remember {characters} from now on for your sake")
    await asyncio.sleep(30)
    await res.delete()

  
  @commands.command()
  @commands.is_owner()
  async def get(self, ctx, terms = None):
    from Memories import Yandere
    async for command in ctx.history(limit=2):
      if command.author == ctx.author:
        await command.delete()
        break
      
    if terms is None:
      await ctx.send("Please enter the category")
      return

    if terms.lower() == 'db':
      table = "danbooru"
    elif terms.lower() == 'yd':
      table = "yandere"
    else:
      await ctx.send("No.")
      return

    data = Database("Memories/Violet's Memories", table).list_data()
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
    
    res = await ctx.send(embed=embed)
    await asyncio.sleep(120)
    await res.delete()



  @commands.command()
  @commands.is_owner()
  async def forget(self, ctx, link=None):
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
    await ctx.send("Violet will forget", embed=pic)


  

  @commands.command()
  @commands.is_owner()
  async def remember(self, ctx, terms=None, *tags):
    from MyAnimeList import ordinals
    from Memories import Yandere
    async for command in ctx.history(limit=2):
      if command.author == ctx.author:
        await command.delete()
        break
    if terms is None:
      await ctx.send("Please enter the category")
      return
    search = " ".join(tags).title()

    if terms.lower() == 'db':
      table = "danbooru"
    elif terms.lower() == 'yd':
      table = "yandere"
    else:
      await ctx.send("No.")
      return

    raw = Database("Memories/Violet's Memories", table).get_like(tags)
    results = {key:value for key,value in sorted(raw.items(), key=lambda x: x[1])}
    total_post = len([value for key,value in results.items()])
    random_number = random.randint(0,total_post-1)
    random_post = [key for key,value in results.items()][random_number]
    order = ordinals(random_number+1)

    with open(f"Memories/{table.capitalize()}.txt", "w", newline='') as f:
      f.write(table+"\n\n")
      for i, (key,value) in enumerate(results.items()):
        f.write(f"{i+1} •「{value.replace(',',' |')}」\n{key}\n\n")

    if total_post > 1:
      post = "posts"
    else:
      post = "post"

    embed = discord.Embed(title=search, description=f"Total {total_post} {post}", url=random_post)
    if "yande.re" in random_post:
      yd = Yandere(random_post).post()

      embed.add_field(name="Tags", value=yd['tags'].replace("_"," "))
      embed.add_field(name="",value= f"**[SOURCE]({yd['post_url']})**")
      embed.set_image(url=yd['sample'])
   
    else:
      embed.set_image(url=random_post)
    embed.set_footer(text=f"{order} post of「{search}」")
    with open(f"Memories/{table.capitalize()}.txt", "rb") as file:
      await ctx.send(embed=embed, file=discord.File(file))
    os.remove(f"Memories/{table.capitalize()}.txt")


  

  @commands.command()
  @commands.is_owner()
  async def recount(self, ctx, terms):
    from Memories import top 
    if terms is None:
      await ctx.send("Please enter the category")
      return

    if terms.lower() == 'db':
      table = "danbooru"
    elif terms.lower() == 'yd':
      table = "yandere"
    else:
      await ctx.send("No.")
      return

    all = Database("Memories/Violet's Memories", table).list_data()
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
    progress = await ctx.send("Violet is trying to remember stuff right now\nPlease wait a moment...")
    from Memories import data_chart
    data_chart(table,counts,(16,9))
    await progress.delete()
    await asyncio.sleep(1)

    embed = discord.Embed(title=table.capitalize(), description=f"Total {len(data)} Posts in Violet's Memories")
    embed.add_field(name="Top Characters", value=top_chara)
    with open("Memories/Chart.png", "rb") as f:
      await ctx.send(file=discord.File(f),embed=embed)
    os.remove("Memories/Chart.png")








  
  @commands.command()
  @commands.is_owner()
  async def cate(self,ctx, terms=None):
    from Memories import Yandere, top
    if terms is None:
      await ctx.send("Please enter the category")
      return
    if terms.lower() == 'db':
      table = "danbooru"
    elif terms.lower() == 'yd':
      table = "yandere"
    else:
      await ctx.send("No.")
      return

    progress = await ctx.send("Violet is trying to remember stuff right now\nPlease wait a moment...")

    raw = Database("Memories/Violet's Memories", table).list_data()

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
    data_chart(table,tags_count,(16,9))
    await progress.delete()
  
    embed = discord.Embed(
            title = "Top Yandere Tags",
            description = top_tags
            )
  
    with open("Memories/Chart.png", "rb") as f:
      await ctx.send(
          embed = embed,
          file  = discord.File(f))
    
    os.remove("Memories/Chart.png")







  
  @commands.command()
  @commands.is_owner()
  async def category(self, ctx):
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
      await ctx.send(f"{ctx.author.mention}, here you go",file=discord.File(file))
    os.remove("Memories/Tags.txt")

def setup(bot):
  bot.add_cog(Memo(bot))