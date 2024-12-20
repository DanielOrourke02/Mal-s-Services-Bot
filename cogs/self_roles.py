

from util.utilities import *

ROLE_LIST = {
    "📢": ("Announcement", "Announcement"),
    "📰": ("Updates", "Updates"),
    "🤖": ("Bot", "Bot"),
    "🎁": ("Giveaways","Giveaways"),
}

class SelfRolesViews(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)
        for emoji, (role_name, custom_label) in roles.items():
            self.add_item(SelfRoleButton(label=custom_label, emoji=emoji, role_name=role_name))

class SelfRoleButton(discord.ui.Button):
    def __init__(self, label, emoji, role_name):
        super().__init__(
            style=discord.ButtonStyle.blurple, 
            label=label, 
            emoji=emoji, 
            custom_id=f"self_role_{role_name.lower().replace(' ', '_')}"
        )
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name=self.role_name)
        if role:
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                embed = discord.Embed(
                    description=f"<a:denied:1302388701422288957> Removed role **{self.role_name}**.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                embed = discord.Embed(
                    description=f"<a:tick_checkmark:1302388713040515147> Added role **{self.role_name}**.",
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                description=f"<a:denied:1302388701422288957> The role **{self.role_name}** does not exist.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)



class SelfRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None 

    @discord.slash_command(name="setup_roles", description="Sends the self roles UI")
    @commands.has_permissions(administrator=True)
    async def setup_roles(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="Self Roles",
            description="Select a role below to add or remove it.",
            color=discord.Color.blue()
        )

        embed.set_footer(text=f"Mal's Services", icon_url=ctx.bot.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        
        await ctx.send(embed=embed, view=SelfRolesViews(ROLE_LIST))
    
    @setup_roles.error
    async def send_setup_roles_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error_embed = discord.Embed(
                description="<a:denied:1302388701422288957> You do not have permission to use this command.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=error_embed)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(SelfRolesViews(ROLE_LIST)) 
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Self Roles Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(SelfRoles(bot))