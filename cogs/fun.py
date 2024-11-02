import discord
from discord.ext import commands

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Fun Cog Loaded!')


def setup(bot):
    bot.add_cog(fun(bot))