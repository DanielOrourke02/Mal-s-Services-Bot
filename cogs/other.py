import discord
from discord.ext import commands
from discord.ui import View, Select
from discord import SelectOption, utils


#SUGGESTION_CHANNEL_ID = 1268322542633091112
SUGGESTION_CHANNEL_ID = 1301168301166039160 # suggestions

class Other(discord.cog.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx: discord.ApplicationContext):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**Latency:** {latency} ms",
            color=discord.Color.green()
        )
        
        await ctx.respond(embed=embed)

    @discord.slash_command(name="help", description="List all available commands")
    @commands.cooldown(1, 3, commands.BucketType.user) 
    async def help_command(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="📜 Help Menu",
            description="Choose a category from the dropdown to view available commands.",
            color=discord.Color.gold(),
            timestamp=utils.utcnow()
        )

        options = [
            discord.SelectOption(label="General Commands", description="View general bot commands", emoji="🛠️"),
            discord.SelectOption(label="User Reports & Suggestions", description="View commands for reporting bugs and players", emoji="🐞"),
            discord.SelectOption(label="Admin Features", description="View admin-only commands", emoji="🎉")
        ]

        select = discord.ui.Select(
            placeholder="Choose a category...",
            options=options
        )

        async def select_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("You are not allowed to use this selection.", ephemeral=True)
                return

            if select.values[0] == "General Commands":
                embed.clear_fields()
                embed.add_field(name="🛠️ General Commands", value="━━━━━━━━━━━━━━━━━━", inline=False)
                embed.add_field(name="`/ping`", value="Check the bot's latency.", inline=False)
                embed.add_field(name="`/help`", value="List all available commands.", inline=False)

            elif select.values[0] == "User Reports & Suggestions":
                embed.clear_fields()
                embed.add_field(name="🐞 User Reports & Suggestions", value="━━━━━━━━━━━━━━━━━━", inline=False)
                embed.add_field(name="`/suggest`", value="Suggest a feature.", inline=False)
                embed.add_field(name="`/user_report`", value="Report a user.", inline=False)

            elif select.values[0] == "Admin Features":
                embed.clear_fields()
                embed.add_field(name="🎉 Admin Features", value="━━━━━━━━━━━━━━━━━━", inline=False)
                embed.add_field(name="`/apply`", value="Get sent the staff app.", inline=False)
                embed.add_field(name="`/setup_roles`", value="Send the self roles.", inline=False)

            await interaction.response.edit_message(embed=embed, view=view)

        select.callback = select_callback

        view = discord.ui.View()
        view.add_item(select)
        await ctx.respond(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Other Cog Loaded!')


def setup(bot):
    bot.add_cog(Other(bot))