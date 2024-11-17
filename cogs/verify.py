import discord
from discord.ext import commands


class VerificationView(discord.ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=None)
        self.correct_menu_selection = False
        
    @discord.ui.select(
        placeholder="Select verify",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Verification"),
            discord.SelectOption(label="ME!!"),     
            discord.SelectOption(label="verify"), 
            discord.SelectOption(label="Plz Verify"),    
            discord.SelectOption(label="select me"),    
        ]
    )
    async def select_category_callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "verify":
            self.correct_menu_selection = True
        else:
            self.correct_menu_selection = False

    @discord.ui.button(label="verify", style=discord.ButtonStyle.primary)
    async def verify(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.correct_menu_selection:
            role = interaction.guild.get_role(1195702107215511603) 
            if role is None:
                await interaction.response.send_message("Role not found.", ephemeral=True)
                return
                
            try:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("You've been verified!", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to add that role.", ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message("Failed to add role due to a server error.", ephemeral=True)
        else:
            await interaction.response.send_message("Please select 'verify' in the selection menu!", ephemeral=True)

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(name="send_verify")
    @commands.has_permissions(administrator=True)
    async def send_verify(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="<:twittercheck:1302398993367699466> __**Verification**__ <:twittercheck:1302398993367699466>",
            description="> 1. In the selection menu select 'verify'\n> 2. Then click the verify button.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Mal's Services", icon_url=ctx.bot.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        
        await ctx.send(embed=embed, view=VerificationView(self.bot, ctx))
            
    @send_verify.error
    async def send_send_verify_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error_embed = discord.Embed(
                description="<a:denied:1302388701422288957> You do not have permission to use this command.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=error_embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Verify Cog Loaded!')


def setup(bot):
    bot.add_cog(Verify(bot))