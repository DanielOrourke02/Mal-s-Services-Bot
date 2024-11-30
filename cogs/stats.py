import discord
from discord.ext import commands, tasks

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = 1195701894937583716  
        self.total_members_channel_id = 1312458448021225654  
        self.human_members_channel_id = 1312458448499114015  
        self.bot_members_channel_id = 1312458467457372211 

        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel() 

    @tasks.loop(minutes=10)
    async def update_stats(self):
        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            return

        total_members = guild.member_count
        human_members = len([member for member in guild.members if not member.bot])
        bot_members = len([member for member in guild.members if member.bot])

        total_channel = guild.get_channel(self.total_members_channel_id)
        human_channel = guild.get_channel(self.human_members_channel_id)
        bot_channel = guild.get_channel(self.bot_members_channel_id)

        if total_channel:
            await total_channel.edit(name=f"「👥」Total Members: {total_members}")
        if human_channel:
            await human_channel.edit(name=f"「🧍」Humans: {human_members}")
        if bot_channel:
            await bot_channel.edit(name=f"「🤖」Bots: {bot_members}")

    @update_stats.before_loop
    async def before_update_stats(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Stats Cog Loaded!")

def setup(bot):
    bot.add_cog(Stats(bot))
