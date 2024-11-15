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
            discord.SelectOption(label="General Commands", description="View general bot commands", emoji="<a:BreadSlice:1304913531887550594>"),
            discord.SelectOption(label="Fun Commands", description="View fun and interactive commands", emoji="🎮"),
            discord.SelectOption(label="Utility Commands", description="Miscellaneous commands for various utilities.", emoji="🔧"),
            discord.SelectOption(label="Moderation Commands", description="View moderation tools", emoji="🔨"),
            discord.SelectOption(label="Admin Commands", description="View admin-only commands", emoji="<:Moderator_Neon:1304913304912658542>"),
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

            elif select.values[0] == "Utility Commands":
                embed.clear_fields()
                embed.add_field(name="🔧 Utility Commands", value="━━━━━━━━━━━━━━━━━━", inline=False)
                embed.add_field(name="`/uptime`", value="Check how long the bot has been running.", inline=False)
                embed.add_field(name="`/userinfo`", value="Display information about a specific user.", inline=False)
                embed.add_field(name="`/serverinfo`", value="Show server information.", inline=False)
                embed.add_field(name="`/membercount`", value="Show the current server membercount.", inline=False)
                embed.add_field(name="`/avatar`", value="Show the avatar of a user.", inline=False)
                embed.add_field(name="`/reminder`", value="Set a reminder for yourself.", inline=False)
                embed.add_field(name="`/calculate`", value="Calculate something.", inline=False)
                embed.add_field(name="`/uuid`", value="Generate a random unique identifier.", inline=False)

            elif select.values[0] == "Moderation Commands":
                embed.clear_fields()
                embed.add_field(name="🎉 Moderation Commands", value="━━━━━━━━━━━━━━━━━━", inline=False)
                embed.add_field(name="`/ban`", value="Ban a user from the server.", inline=False)
                embed.add_field(name="`/unban`", value="Unban a user from the server.", inline=False)
                embed.add_field(name="`/kick`", value="Kick a user from the server.", inline=False)
                embed.add_field(name="`/mute`", value="Mute a user.", inline=False)
                embed.add_field(name="`/unmute`", value="Unmute a user.", inline=False)
                embed.add_field(name="`/lock`", value="Lock the current channel.", inline=False)
                embed.add_field(name="`/unlock`", value="Unlock the current channel.", inline=False)
                embed.add_field(name="`/serverlock`", value="Lock the server.", inline=False)
                embed.add_field(name="`/serverunlock`", value="Unlock the server.", inline=False)

            elif select.values[0] == "Admin Commands":
                embed.clear_fields()
                embed.add_field(name="🎉 Admin Commands", value="━━━━━━━━━━━━━━━━━━", inline=False)
                embed.add_field(name="`/shutdown`", value="Turn the bot off.", inline=False)
                embed.add_field(name="`/setup_roles`", value="Send the self roles menu.", inline=False)
                embed.add_field(name="`/setup_tickets`", value="Setup tickets.", inline=False)

            elif select.values[0] == "Fun Commands":
                embed.clear_fields()
                embed.add_field(name="🎲 Fun Commands", value="━━━━━━━━━━━━━━━━━━", inline=False)
                embed.add_field(name="`/meme`", value="Get a random meme.", inline=False)
                embed.add_field(name="`/8ball`", value="Ask the magic 8-ball a question.", inline=False)
                embed.add_field(name="`/dadjoke`", value="Receive a random dad joke.", inline=False)
                embed.add_field(name="`/roast`", value="Get roasted by the bot.", inline=False)
                embed.add_field(name="`/rate`", value="Rate something out of 10.", inline=False)
                embed.add_field(name="`/truth_or_dare`", value="Play a truth or dare game.", inline=False)
                embed.add_field(name="`/rps`", value="Play Rock-Paper-Scissors with the bot.", inline=False)
                embed.add_field(name="`/joke`", value="Hear a random joke.", inline=False)
                embed.add_field(name="`/randomcolor`", value="Get a random color.", inline=False)
                embed.add_field(name="`/guessnumber`", value="Play a number guessing game.", inline=False)
                embed.add_field(name="`/quotes`", value="Get a random quote.", inline=False)
                embed.add_field(name="`/waifu`", value="Get a random waifu image.", inline=False)

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