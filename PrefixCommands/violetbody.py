import discord
from discord.ext import commands
import os
from Violet import bot_info
from Lyrics import parts


class VioletBody(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  
  @commands.command()
  async def soul(
    self,
    ctx,
    path=None
  ):
  
    if path is None:
      path = "."

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

    except:
      await ctx.send("Can't find the directory")
      return
    embed = discord.Embed(
      title=f"{bot_info.bot_name}の体",
      url = bot_info.repository,
      description = "私のすべて",
      color = bot_info.color
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
    await ctx.send(embed=embed)


    
def setup(bot):
  bot.add_cog(VioletBody(bot))