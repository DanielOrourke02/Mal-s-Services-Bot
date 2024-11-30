import discord
from discord.ext import commands

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Counting Cog Loaded!')

def setup(bot):
    bot.add_cog(Counting(bot))
