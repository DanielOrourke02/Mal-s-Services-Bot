

from util.utilities import *


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="setup_rules", description="Sets up the server rules embed")
    @commands.has_permissions(administrator=True)
    async def setup_rules(self, ctx: discord.ApplicationContext):
        # Create the main embed
        main_embed = discord.Embed(
            title="📜 __Server Rules & Guidelines__",
            description="Welcome to Mal's Services! To ensure everyone has a positive experience, please follow these rules:",
            color=0x5865F2  # Discord Blurple
        )
        
        # Core Rules with emojis and better formatting
        rules = [
            "🤝 **Respect All Members**\n› Be kind and courteous to everyone\n› No harassment, discrimination, or hate speech\n› Respect others' opinions and backgrounds",
            
            "📢 **No Spamming or Advertising**\n› Don't flood channels with messages\n› No unsolicited advertising of any kind\n› No invite links to other servers without permission",
            
            "🔞 **No NSFW Content**\n› Keep all content PG-13\n› No explicit images, videos, or discussions\n› No references to adult content",
            
            "📝 **Channel Guidelines**\n› Post content in the appropriate channels\n› Read channel descriptions and topics\n› Don't derail conversations with off-topic content",
            
            "💰 **No Begging**\n› Don't ask for money, items, or free services\n› Don't repeatedly ask for giveaways\n› Contribute positively to the community",
            
            "⚠️ **Staff Respect**\n› Don't spam ping admins or moderators\n› Follow staff instructions when given\n› Direct concerns through appropriate channels",
            
            "🎫 **Ticket System**\n› Only open tickets when you have a legitimate issue\n› Provide clear information when opening a ticket\n› Be patient waiting for responses",
            
            "🧠 **Use Common Sense**\n› If something feels wrong, it probably is\n› When in doubt, ask a moderator\n› Rules cannot cover everything - use good judgment",
            
            "🛡️ **Security & Privacy**\n› Never share personal information\n› Don't attempt to scam or phish other members\n› Report suspicious activity to moderators",
            
            "🤖 **Bot Usage**\n› Don't abuse or spam bot commands\n› Use bot commands in the appropriate channels\n› Report any bot issues to staff"
        ]
        
        # Add rules in groups of 5 to avoid hitting the field limit
        main_embed.add_field(name="__Core Rules__", value="\n\n".join(rules[:5]), inline=False)
        main_embed.add_field(name="__Additional Guidelines__", value="\n\n".join(rules[5:]), inline=False)
        
        # Add enforcement information
        enforcement = (
            "**Minor violations**: Warning → Mute → Kick\n"
            "**Serious violations**: Immediate ban\n"
            "**Moderation decisions** are at the discretion of staff members\n"
            "**Appeals** can be made through the ticket system\n\n"
            "*By participating in this server, you agree to follow these rules.*"
        )
        main_embed.add_field(name="__Enforcement__", value=enforcement, inline=False)
        
        # Add server information
        main_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else ctx.bot.user.avatar.url)
        main_embed.set_footer(text="Mal's Services • Rules Last Updated", icon_url=ctx.bot.user.avatar.url)
        main_embed.timestamp = discord.utils.utcnow()
        
        await ctx.respond("Rules embed has been created successfully!", ephemeral=True)
        await ctx.send(embed=main_embed)
        
    @discord.slash_command(name='meme')
    async def meme(self, ctx: discord.ApplicationContext):
        """Fetches a random meme."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    embed = discord.Embed(title=data["title"], url=data["postLink"], color=discord.Color.blue())
                    embed.set_image(url=data["url"])
                    
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=discord.Embed(description="Could not fetch a meme at the moment.", color=discord.Color.red()))

    @discord.slash_command(name='8ball')
    async def eight_ball(self, ctx: discord.ApplicationContext, question: discord.Option(str, description="What you want to ask the bot", required=True)): # type: ignore
        """Magic 8-ball answers your questions."""
        responses = ["Yes.", "No.", "Maybe.", "Absolutely.", "I don't think so.", "Ask again later."]
        
        embed = discord.Embed(description=f'🎱 {random.choice(responses)}', color=discord.Color.purple())
        
        await ctx.respond(embed=embed)

    @discord.slash_command(name='dadjoke')
    async def dad_joke(self, ctx: discord.ApplicationContext):
        """Fetches a random dad joke."""
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com/", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    embed = discord.Embed(description=data["joke"], color=discord.Color.orange())
                    
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=discord.Embed(description="Couldn't fetch a joke right now.", color=discord.Color.red()))

    @discord.slash_command(name='roast')
    async def roast(self, ctx: discord.ApplicationContext, member: discord.Option(discord.Member, description="User you want to roast", required=True)): # type: ignore
        """Sends a roast to a user."""
        roasts = ["You're as bright as a black hole.", "If ignorance is bliss, you must be the happiest person alive.", "You bring everyone so much joy when you leave the room."]
        target = member.mention if member else "you"
        
        embed = discord.Embed(description=f"{target}, {random.choice(roasts)}", color=discord.Color.dark_red())
        
        await ctx.respond(embed=embed)

    @discord.slash_command(name='rate')
    async def rate(self, ctx: discord.ApplicationContext, thing: discord.Option(str, description="Item to rate", required=True)): # type: ignore
        """Rates something out of 10."""
        rating = random.randint(1, 10)
        
        embed = discord.Embed(description=f"I'd give {thing} a {rating}/10.", color=discord.Color.green())
        
        await ctx.respond(embed=embed)

    @discord.slash_command(name='truth_or_dare')
    async def truth_or_dare(self, ctx: discord.ApplicationContext):
        """Play a game of truth or dare."""
        choice = random.choice(["Truth", "Dare"])
        
        embed = discord.Embed(description=f"{choice}!", color=discord.Color.blue())
        
        await ctx.respond(embed=embed)

    @discord.slash_command(name='joke')
    async def joke(self, ctx: discord.ApplicationContext):
        """Tells a random joke."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://official-joke-api.appspot.com/random_joke") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    embed = discord.Embed(title="Here's a joke!", description=f"{data['setup']} - {data['punchline']}", color=discord.Color.teal())
                    
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=discord.Embed(description="Couldn't fetch a joke right now.", color=discord.Color.red()))
    
    @discord.slash_command(name='randomcolor')
    async def random_color(self, ctx: discord.ApplicationContext):
        """Generates a random color with hex code."""
        color = random.randint(0, 0xFFFFFF)
        hex_color = f'#{color:06x}'
        
        embed = discord.Embed(description=f"Here's a random color: {hex_color}", color=color)
        
        await ctx.respond(embed=embed)

    @discord.slash_command(name='quotes')
    async def quotes(self, ctx: discord.ApplicationContext):
        """Sends a random inspirational quote."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.quotable.io/random") as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    embed = discord.Embed(description=f'"{data["content"]}" - {data["author"]}', color=discord.Color.blue())
                    
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=discord.Embed(descripwion="Couldn't fetch a quote right now.", color=discord.Color.red()))

    @discord.slash_command(name='waifu')
    async def waifu(self, ctx: discord.ApplicationContext):
        """Sends a random anime waifu image."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/waifu") as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    embed = discord.Embed(title="Here's your waifu!", color=discord.Color.nitro_pink())
                    embed.set_image(url=data["url"])
                    
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=discord.Embed(description="Couldn't fetch a waifu image right now.", color=discord.Color.red()))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Fun Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(fun(bot))