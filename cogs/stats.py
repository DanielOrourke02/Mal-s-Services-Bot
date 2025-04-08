

from util.utilities import *


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = 1195701894937583716  
        self.total_members_channel_id = 1359083337133588500  
        self.human_members_channel_id = 1359083353134989442  
        self.bot_members_channel_id = 1359083364803547216 

        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel() 

    @tasks.loop(minutes=10)
    async def update_stats(self):
        try:
            guild = self.bot.get_guild(self.guild_id)
            if not guild:
                print(f"Could not find guild with ID {self.guild_id}")
                return

            total_members = guild.member_count
            human_members = len([member for member in guild.members if not member.bot])
            bot_members = len([member for member in guild.members if member.bot])

            total_channel = guild.get_channel(self.total_members_channel_id)
            human_channel = guild.get_channel(self.human_members_channel_id)
            bot_channel = guild.get_channel(self.bot_members_channel_id)

            # Check if channels exist
            if not total_channel:
                print(f"Could not find total members channel with ID {self.total_members_channel_id}")
            if not human_channel:
                print(f"Could not find human members channel with ID {self.human_members_channel_id}")
            if not bot_channel:
                print(f"Could not find bot members channel with ID {self.bot_members_channel_id}")

            # Create permission overwrites
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False)  # Prevent members from joining
            }

            # Update each channel if it exists
            if total_channel:
                await total_channel.edit(
                    name=f"「👥」{total_members} Members",
                    overwrites=overwrites
                )
                print(f"Updated total members channel: {total_members} Members")
                
            if human_channel:
                await human_channel.edit(
                    name=f"「🧍」{human_members} Humans",
                    overwrites=overwrites
                )
                print(f"Updated human members channel: {human_members} Humans")
                
            if bot_channel:
                await bot_channel.edit(
                    name=f"「🤖」{bot_members} Bots",
                    overwrites=overwrites
                )
                print(f"Updated bot members channel: {bot_members} Bots")

        except discord.Forbidden:
            print(f"Error updating stats: Missing permissions to edit channels")
        except discord.HTTPException as e:
            print(f"Error updating stats: HTTP Exception: {e}")
        except Exception as e:
            print(f"Error updating stats: {e}")

    @update_stats.before_loop
    async def before_update_stats(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Update stats immediately when a member joins"""
        if member.guild.id == self.guild_id:
            print(f"Member joined: {member.name}. Updating stats...")
            await self.update_stats()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Update stats immediately when a member leaves"""
        if member.guild.id == self.guild_id:
            print(f"Member left: {member.name}. Updating stats...")
            await self.update_stats()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Stats Cog Loaded! {Fore.RESET}')
        await self.update_stats()

def setup(bot):
    bot.add_cog(Stats(bot))