

from util.utilities import *


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="userinfo", description="Display information about a specific user.")
    async def userinfo(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Option(discord.Member, "Select a user", required=False) # type: ignore
    ):
        """Display information about a specific user."""
        member = member or ctx.author
        embed = discord.Embed(
            title=f"👤 User Information: {member.display_name}",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="📅 Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="🎭 Roles", value=", ".join([role.mention for role in member.roles[1:]]) or "None", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="serverinfo", description="Show server information.")
    async def serverinfo(self, ctx: discord.ApplicationContext):
        """Show server information."""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"📊 Server Information: {guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
        embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
        embed.add_field(name="👑 Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="👥 Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="📅 Created On", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(
            name="📂 Channels",
            value=f"Text: {len(guild.text_channels)} | Voice: {len(guild.voice_channels)}",
            inline=True
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="membercount", description="Show the current server member count.")
    async def membercount(self, ctx: discord.ApplicationContext):
        """Show the current server member count."""
        embed = discord.Embed(
            title="Member Count",
            description=f"This server has {ctx.guild.member_count} members.",
            color=discord.Color.purple()
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(name="avatar", description="Show the avatar of a user.")
    async def avatar(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Option(discord.Member, "Select a user", required=False) # type: ignore
    ):
        """Show the avatar of a user."""
        member = member or ctx.author
        embed = discord.Embed(
            title=f"{member}'s Avatar",
            color=discord.Color.gold()
        )
        embed.set_image(url=member.avatar.url)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="reminder", description="Set a reminder for yourself (time in minutes).")
    async def reminder(
        self, 
        ctx: discord.ApplicationContext, 
        time: discord.Option(int, "Time in minutes", required=True),  # type: ignore
        message: discord.Option(str, "Reminder message", required=True) # type: ignore
    ):
        """Set a reminder for yourself (time in minutes)."""
        embed = discord.Embed(
            title="Reminder Set",
            description=f"I'll remind you in {time} minutes.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)
        await asyncio.sleep(time * 60)
        reminder_embed = discord.Embed(
            title="Reminder",
            description=message,
            color=discord.Color.orange()
        )
        await ctx.author.send(embed=reminder_embed)

    @discord.slash_command(name="calculate", description="Evaluate a simple math expression.")
    async def calculate(
        self, 
        ctx: discord.ApplicationContext, 
        expression: discord.Option(str, "Math expression to evaluate", required=True) # type: ignore
    ):
        """Evaluate a simple math expression."""
        try:
            result = eval(expression, {"__builtins__": {}})
            embed = discord.Embed(
                title="Calculation Result",
                description=f"The result of `{expression}` is `{result}`.",
                color=discord.Color.blurple()
            )
            await ctx.respond(embed=embed)
        except Exception:
            await ctx.respond("Invalid expression.", ephemeral=True)

    @discord.slash_command(name="uuid", description="Generate a random unique identifier.")
    async def uuid(self, ctx: discord.ApplicationContext):
        """Generate a random unique identifier."""
        unique_id = uuid.uuid4()
        embed = discord.Embed(
            title="Generated UUID",
            description=str(unique_id),
            color=discord.Color.teal()
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(name="qrcode", description="Generate a QR code from a provided link.")
    async def qrcode(self, ctx: discord.ApplicationContext, link: discord.Option(str, "URL to generate QR code for", required=True)): # type: ignore
        """Generate a QR code from a provided link."""
        buffer = BytesIO()
        img = qrcode.make(link)
        img.save(buffer, format="PNG")
        buffer.seek(0)

        file = discord.File(buffer, filename="qrcode.png")
        embed = discord.Embed(
            title="QR Code",
            description=f"Here is the QR code for [this link]({link}).",
            color=discord.Color.green()
        )
        embed.set_image(url="attachment://qrcode.png")
        await ctx.respond(embed=embed, file=file)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Utility Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(Utility(bot))
