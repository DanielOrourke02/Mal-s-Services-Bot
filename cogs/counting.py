import discord
from discord.ext import commands

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counting_channel_id = 1080576773483405443
        self.required_role_id = 1312452960910970931  
        self.current_count = 0 

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Counting Cog Loaded!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.channel.id != self.counting_channel_id:
            return

        required_role = discord.utils.get(message.author.roles, id=self.required_role_id)
        if not required_role:
            embed = discord.Embed(
                title="🔒 Access Denied",
                description=f"You must have the <@&{self.required_role_id}> role to participate in counting.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Counting Game")
            await message.channel.send(embed=embed, delete_after=5)
            return

        try:
            user_count = int(message.content)
        except ValueError:
            await message.delete()
            return

        if user_count == self.current_count + 1:
            self.current_count += 1 
            await message.add_reaction("✅")
        else:
            await message.delete()

def setup(bot):
    bot.add_cog(Counting(bot))
