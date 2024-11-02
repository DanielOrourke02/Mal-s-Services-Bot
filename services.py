import discord
from discord.ext import commands

bot = discord.Bot(intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"\nWe have logged in as: {bot.user.display_name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/ping"))

@bot.event
async def on_application_command_error(ctx, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            description=f"<a:denied:1300812792085090435> {error}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
    else:
        raise error

cogs = [
    'cogs.tickets',
    'cogs.other',
    'cogs.self_roles',
    'cogs.fun',
    'cogs.verify',
]

for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)
        
bot.run("token")