import discord
import asyncio
import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True 
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"\nWe have logged in as: {bot.user.display_name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))

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

import discord
import asyncio

@bot.event
async def on_member_join(member: discord.Member):
    ping_channel_id = 1302396598591950919
    welcome_channel_id = 1196022863430418523

    ping_channel = member.guild.get_channel(ping_channel_id)
    welcome_channel = member.guild.get_channel(welcome_channel_id)

    # Ping the member in the ping channel briefly
    if ping_channel:
        ping_message = await ping_channel.send(f"{member.mention}")
        await asyncio.sleep(3)
        await ping_message.delete()

    # Create the welcome embed message
    if welcome_channel:
        member_count = len([m for m in member.guild.members if not m.bot])
        suffix = "th" if 4 <= member_count % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(member_count % 10, "th")

        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed = discord.Embed(
            title="Welcome to Paradise Casino! 🎰",
            description=(
                f"Hello, {member.mention}! We're excited to have you here. 🎉\n\n"
                f"📋 **Make sure to:**\n"
                f"> Read the <#1197073841252466709> for server guidelines.\n"
                f"> Ask questions in <#1195705939651743824> if needed.\n"
                f"> Use `/help` to view all bot commands!\n\n"
                f"🎊 You are our **{member_count}{suffix}** member!"
            ),
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=f"User ID: {member.id}")
        embed.timestamp = discord.utils.utcnow()

        await welcome_channel.send(embed=embed)

        
@bot.slash_command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx: discord.ApplicationContext):
    """Shut down the bot."""
    embed = discord.Embed(
        title="Shutdown",
        description="Shutting down the bot...",
        color=discord.Color.red()
    )
    await ctx.respond(embed=embed)
    await bot.close()

start_time = datetime.datetime.now()

@bot.slash_command(name='uptime')
async def uptime(ctx: discord.ApplicationContext):
    """Check how long the bot has been running."""
    now = datetime.datetime.now()

    delta = now - start_time
    days, remainder = divmod(delta.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    formatted_uptime = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
    embed = discord.Embed(
        title="⏱ Bot Uptime",
        description=f"The bot has been running for **{formatted_uptime}**.",
        color=discord.Color.blurple()
    )
    await ctx.respond(embed=embed)

cogs = [
    'cogs.tickets',
    'cogs.other',
    'cogs.self_roles',
    'cogs.fun',
    'cogs.verify',
    'cogs.mod',
    'cogs.utility',
    'cogs.counting',
    'cogs.stats',
]

for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)
        
bot.run("TOKEN")