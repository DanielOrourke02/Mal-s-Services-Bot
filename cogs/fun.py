

from util.utilities import *


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='setup_rules')
    @commands.has_permissions(administrator=True)
    async def setup_rules(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="📜 Server Rules",
            description="Please read and follow these rules to ensure a welcoming and enjoyable experience for everyone.",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="1. Be Respectful",
            value="Treat everyone with respect. Harassment, hate speech, and offensive behavior will not be tolerated.",
            inline=False
        )
        embed.add_field(
            name="2. No Spamming/advertising",
            value="Avoid spamming and self promotion.",
            inline=False
        )
        embed.add_field(
            name="3. Keep It Safe for Work",
            value="Do not post NSFW content or anything that violates Discord's community guidelines.",
            inline=False
        )
        embed.add_field(
            name="4. Follow Channel Topics",
            value="Ensure your messages are relevant to the channel’s topic. Use the correct channels for specific discussions.",
            inline=False
        )
        embed.add_field(
            name="5. No Advertising",
            value="Do not promote other servers, products, or services without permission from the staff.",
            inline=False
        )
        embed.add_field(
            name="6. Use Common Sense",
            value="If something seems inappropriate, don’t do it. Always strive to maintain a positive environment.",
            inline=False
        )
        embed.add_field(
            name="6. Do not spam ping admins",
            value="When in a ticket or dms, do not spam ping staff. It will result in a ban."
        )

        embed.set_footer(text=f"Mal's Services", icon_url=ctx.bot.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        
        await ctx.send(embed=embed)

    @discord.slash_command(name='setup_prices')
    @commands.has_permissions(administrator=True)
    async def setup_prices(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="__**🌟 Discord Bot Services 🌟**__",
            description="Choose from our variety of bot tiers tailored to your needs!",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="💩 ~~£10~~ **£5 - Minimal**",
            value="A very simple Discord bot designed to do one or two specific tasks.",
            inline=False
        )

        embed.add_field(
            name="💵 ~~£15~~ **£10 - Basic**",
            value="A basic Discord bot with a small/medium range of commands of your choosing.",
            inline=False
        )

        embed.add_field(
            name="💎 ~~£20~~ **£15 - Pro**",
            value="A complex and large bot, great for big/growing servers. Plus custom features tailored for your server.",
            inline=False
        )

        embed.add_field(
            name="🚀 ~~£35~~ **£25 - Advanced**",
            value="An advanced, complex bot with lots of custom features. Suited for the most specific systems.",
            inline=False
        )

        embed.add_field(
            name="**❓ Not sure about the tier?**",
            value="> Just make a ticket and describe your bot!",
            inline=False
        )

        embed.add_field(
            name="__**🔥 Hot Deals 🔥**__",
            value=(
                "> 🎉 **Get 1 month hosting FREE** with the purchase of any bot tier.\n"
                "> 🎉 **2 Months Free Hosting** by purchasing the Pro or Advanced tier.\n"
                "> 🎉 **£10 for 3 months of hosting**"
            ),
            inline=False
        )
        embed.set_footer(text=f"Mal's Services", icon_url=ctx.bot.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

    @discord.slash_command(name='setup_hosting')
    @commands.has_permissions(administrator=True)
    async def setup_hosting(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="__**⭐ Hosting Services ⭐**__",
            description="I offer hosting for your Discord bot, inclusive of maintenance. This service includes addressing any disruptions and accommodating changes to commands, ensuring a seamless experience.",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="💰 **£5 per month**",
            value="> Reliable 24/7 hosting, with 24/7 customer support.",
            inline=True
        )

        embed.add_field(
            name="__**🔥 Hot Deals**__",
            value=(
                "> 🎉 **Get 1 month hosting FREE** with the purchase of any bot tier.\n"
                "> 🎉 **2 Months Free Hosting** by purchasing the Pro or Advanced tier.\n"
                "> 🎉 **£10 for 3 months of hosting**"
            ),
            inline=False
        )
        embed.set_footer(text=f"Mal's Services", icon_url=ctx.bot.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

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