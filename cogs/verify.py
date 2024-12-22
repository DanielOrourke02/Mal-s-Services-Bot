

from util.utilities import *


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = 1320355645211545610

    @discord.slash_command(name="setup_verify", description="Sets up the verification system")
    @commands.has_permissions(administrator=True)
    async def setup_verify(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="🔒 Verification 🔒",
            description="React with ✅ to verify yourself and gain access to the server.",
            color=discord.Color.green()
        )

        message = await ctx.send(embed=embed)
        self.message_id = message.id  # Save the message ID
        await message.add_reaction("✅")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.message_id:  # Ensure it matches the setup message
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        if str(payload.emoji) == "✅":
            role = guild.get_role(1195702107215511603)  # Replace with your verification role ID
            if role:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    print(f"Failed to assign role to {member.display_name} due to permission issues.")
                except discord.HTTPException:
                    print(f"Failed to assign role to {member.display_name} due to a server error.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != self.message_id:  # Ensure it matches the setup message
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        if str(payload.emoji) == "✅":
            role = guild.get_role(1195702107215511603)  # Replace with your verification role ID
            if role:
                try:
                    await member.remove_roles(role)
                    await member.send("Your verification role has been removed.")
                except discord.Forbidden:
                    print(f"Failed to remove role from {member.display_name} due to permission issues.")
                except discord.HTTPException:
                    print(f"Failed to remove role from {member.display_name} due to a server error.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Verify Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(Verify(bot))
