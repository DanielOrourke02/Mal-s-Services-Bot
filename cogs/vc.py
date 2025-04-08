

from util.utilities import *


class JoinToCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.create_channel_id = 1359081430466166878  # Replace with your Join to Create channel ID
        self.temp_channels = {}  # To keep track of created channels

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Check if the user joined the "Join to Create" channel
        if after.channel and after.channel.id == self.create_channel_id:
            # Create a new temporary voice channel
            guild = member.guild
            category = after.channel.category  # Use the same category as the Join to Create channel
            
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False),
                member: discord.PermissionOverwrite(connect=True, manage_channels=True),
            }

            temp_channel = await guild.create_voice_channel(
                name=f"{member.display_name}'s Room",
                category=category,
                overwrites=overwrites
            )

            # Move the user to the new channel
            await member.move_to(temp_channel)

            # Save the temporary channel to track it
            self.temp_channels[temp_channel.id] = member.id

        # Check if the user left a temporary channel and it became empty
        if before.channel and before.channel.id in self.temp_channels:
            temp_channel = before.channel
            if len(temp_channel.members) == 0:  # No one left in the channel
                del self.temp_channels[temp_channel.id]  # Remove from tracking
                await temp_channel.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | VC Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(JoinToCreate(bot))