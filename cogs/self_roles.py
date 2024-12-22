

from util.utilities import *


ROLE_LIST = {
    "<:announce_purple:1320352903382433832>": ("Announcement", "Get notified for bot announcements."),
    "<:Update:1320353221562335254>": ("Updates", "Get notified for bot updates, changes, etc."),
    "<:Bot:1320352836105670676>": ("Bot", "Get notified for bot maintenance and outages."),
    "<:Giveaways:1320352823770087515>": ("Giveaways", "Get notified for giveaways."),
    "<a:darkred_fire:1320353449019314217>": ("Events", "Get notified for server and bot events.")
}

class SelfRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = 1320355682154844192

    @discord.slash_command(name="setup_roles", description="Sends the self roles message")
    @commands.has_permissions(administrator=True)
    async def setup_roles(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="Choose Your Role! <a:GoldenShimmer:1320351384796663879>",
            description="\n".join(
                [f"{emoji} **{role_name}** -  *{description}*" for emoji, (role_name, description) in ROLE_LIST.items()]
            ),
            color=discord.Color.blue()
        )

        message = await ctx.send(embed=embed)
        self.message_id = message.id
        for emoji in ROLE_LIST.keys():
            await message.add_reaction(emoji)

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
        emoji = str(payload.emoji)
        if emoji in ROLE_LIST:
            role_name = ROLE_LIST[emoji][0]
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.add_roles(role)

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
        emoji = str(payload.emoji)
        if emoji in ROLE_LIST:
            role_name = ROLE_LIST[emoji][0]
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Self Roles Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(SelfRoles(bot))
