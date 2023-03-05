from AnimeSeries import WaifuIm, Kyoko
import discord
from discord.ext import commands


class AnimeSeries(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.command()
  async def mal(self, ctx, terms=None, *title):
    from MyAnimeList import ordinals, MyAnimeList
    if terms is None:
      await ctx.send("Please enter the valid search category")
      return

    if not title:
      await ctx.send(f"Please enter the title, {ctx.author.mention}-san")
      return

    title = " ".join(title)
  # AnimeSearch
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

      theme = discord.Embed(
        title=title_og ,
        url=url,
        description=f"**{type}**\n**Season**: {season}\n**Year**: {year}\n**Rank**: {ordinals(rank)}\n**Status**: {status}",
        color = color
      )

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

  # CharaSearch
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

  

  @commands.command()
  async def waifu(self, ctx, *tags):
    async for command in ctx.history(limit=2):
      if command.author == ctx.author:
        await command.delete()
        break
    wf = WaifuIm("search").waifu(tags)
    color = int(wf['color'][1:], 16)
    embed = discord.Embed(
            title = "Your Waifu",
            url = wf['source'],
            color = color
    )
    embed.set_image(url = wf['url'])
    await ctx.send(embed=embed)


  
  @commands.command()
  async def quote(self, ctx, lang='en'):
    q = Kyoko('quotes').quotes()
    embed = discord.Embed(title="")
    embed.add_field(
        name=q[lang],
        value=f"By {q['chara']}\nFrom {q['series']}"
    )
    await ctx.send(embed = embed)

def setup(bot):
  bot.add_cog(AnimeSeries(bot))