import discord
from discord.ext import commands


class ConverterSeries(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  
  @commands.command()
  async def decimal(self, ctx, base: str, number: str):
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


  @commands.command()
  async def binary(self, ctx, base: str, number: str):
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
      
  @commands.command()
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

      
  @commands.command()
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


def setup(bot):
  bot.add_cog(ConverterSeries(bot))
