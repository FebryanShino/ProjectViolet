import discord
from discord.ext import commands
from Discord import date_format, timestamp


class AppCommands(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    
  @discord.user_command(name='info')
  async def userinfo(
    self, ctx,
    member: discord.Member
  ):
    guild = ctx.guild.name
    roles = "\n".join([i.mention for i in member.roles[1:][::-1]])
    user_date = date_format(str(member.created_at))
    member_date = date_format(str(member.joined_at))


    profile = discord.Embed(
      description = member.mention,
      color = member.color
    )
    profile.add_field(
      name = "Registered",
      value= f"On {user_date['date']}\nAt {user_date['time']} UTC"
    )
    profile.add_field(
      name = f"Joined to {guild}",
      value= f"On {member_date['date']}\nAt {member_date['time']} UTC"
    )

    if member.nick != None:
      profile.add_field(
        name = "Member Info",
        value = f"Nickname: {member.nick}"
      )
    profile.add_field(
      name= f"Roles[{len(member.roles[1:])}]",
      value= roles
    )

    avatar = member.avatar
    if avatar is not None:
      profile.set_image(url = avatar)
      profile.set_thumbnail(url = avatar) 
      profile.set_author(
        name=self.bot.get_user(member.id),
        icon_url= avatar
      )
    else:
      profile.set_author(
        name=self.bot.get_user(member.id)
      )
    profile.set_footer(
      text=f"ID: {member.id} | Today at {timestamp()} UTC")
    await ctx.respond(embed = profile)


  @discord.user_command(name='avatar')
  async def user_avatar(
    self, ctx,
    member: discord.Member
  ):
    embed = discord.Embed()
    embed.set_author(
      name = self.bot.get_user(member.id),
      icon_url = member.avatar
    )
    embed.set_image(url=member.avatar)
    await ctx.respond(embed = embed)


def setup(bot):
  bot.add_cog(AppCommands(bot))