import discord
from discord.ext import commands
import random
import uuid
import datetime
import asyncio

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="uptime")
    async def uptime(self, ctx: discord.ApplicationContext):
        """Check how long the bot has been running."""
        delta = datetime.datetime.now() - self.bot.start_time
        embed = discord.Embed(
            title="Bot Uptime",
            description=f"The bot has been running for {delta}.",
            color=discord.Color.blurple()
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(name="userinfo")
    async def userinfo(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Option(discord.Member, "Select a user", required=False)
    ):
        """Display information about a specific user."""
        member = member or ctx.author
        embed = discord.Embed(
            title=f"User Information - {member}",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=False)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="serverinfo")
    async def serverinfo(self, ctx: discord.ApplicationContext):
        """Show server information."""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"Server Information - {guild.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.add_field(name="Member Count", value=guild.member_count, inline=False)
        embed.add_field(name="Created On", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="membercount")
    async def membercount(self, ctx: discord.ApplicationContext):
        """Show the current server member count."""
        embed = discord.Embed(
            title="Member Count",
            description=f"This server has {ctx.guild.member_count} members.",
            color=discord.Color.purple()
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(name="avatar")
    async def avatar(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Option(discord.Member, "Select a user", required=False)
    ):
        """Show the avatar of a user."""
        member = member or ctx.author
        embed = discord.Embed(
            title=f"{member}'s Avatar",
            color=discord.Color.gold()
        )
        embed.set_image(url=member.avatar.url)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="reminder")
    async def reminder(
        self, 
        ctx: discord.ApplicationContext, 
        time: discord.Option(int, "Time in minutes"), 
        message: discord.Option(str, "Reminder message")
    ):
        """Set a reminder for yourself (time in minutes)."""
        embed = discord.Embed(
            title="Reminder Set",
            description=f"I'll remind you in {time} minutes.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)
        await asyncio.sleep(time * 60)
        reminder_embed = discord.Embed(
            title="Reminder",
            description=message,
            color=discord.Color.orange()
        )
        await ctx.author.send(embed=reminder_embed)

    @discord.slash_command(name="calculate")
    async def calculate(
        self, 
        ctx: discord.ApplicationContext, 
        expression: discord.Option(str, "Math expression to evaluate")
    ):
        """Evaluate a simple math expression."""
        try:
            result = eval(expression, {"__builtins__": {}})
            embed = discord.Embed(
                title="Calculation Result",
                description=f"The result of `{expression}` is `{result}`.",
                color=discord.Color.blurple()
            )
            await ctx.respond(embed=embed)
        except Exception:
            await ctx.respond("Invalid expression.", ephemeral=True)

    @discord.slash_command(name="uuid")
    async def uuid(self, ctx: discord.ApplicationContext):
        """Generate a random unique identifier."""
        unique_id = uuid.uuid4()
        embed = discord.Embed(
            title="Generated UUID",
            description=str(unique_id),
            color=discord.Color.teal()
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
