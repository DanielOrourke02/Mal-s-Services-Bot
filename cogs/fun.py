import discord
import random
import aiohttp
from discord.ext import commands


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='say')
    async def say(self, ctx: discord.ApplicationContext, message: discord.Option(str, description="What you want the bot to say", required=True)):
        await ctx.respond()

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
    async def eight_ball(self, ctx: discord.ApplicationContext, question: discord.Option(str, description="What you want to ask the bot", required=True)):
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
    async def roast(self, ctx: discord.ApplicationContext, member: discord.Option(discord.Member, description="User you want to roast", required=True)):
        """Sends a roast to a user."""
        roasts = ["You're as bright as a black hole.", "If ignorance is bliss, you must be the happiest person alive.", "You bring everyone so much joy when you leave the room."]
        target = member.mention if member else "you"
        
        embed = discord.Embed(description=f"{target}, {random.choice(roasts)}", color=discord.Color.dark_red())
        
        await ctx.respond(embed=embed)

    @discord.slash_command(name='rate')
    async def rate(self, ctx: discord.ApplicationContext, thing: discord.Option(str, description="Item to rate", required=True)):
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

    @discord.slash_command(name='rps')
    async def rps(self, ctx: discord.ApplicationContext):
        """Play Rock-Paper-Scissors with the bot."""
        
        options = [
            discord.SelectOption(label="Rock", value="rock", emoji="✊"),
            discord.SelectOption(label="Paper", value="paper", emoji="✋"),
            discord.SelectOption(label="Scissors", value="scissors", emoji="✌️")
        ]
        
        select = discord.ui.Select(
            placeholder="Choose rock, paper, or scissors",
            options=options
        )

        async def select_callback(interaction: discord.Interaction):
            choice = select.values[0]
            choices = ["rock", "paper", "scissors"]
            bot_choice = random.choice(choices)
            
            # Determine the outcome
            if choice == bot_choice:
                outcome = "It's a tie!"
            elif (choice == "rock" and bot_choice == "scissors") or \
                 (choice == "paper" and bot_choice == "rock") or \
                 (choice == "scissors" and bot_choice == "paper"):
                outcome = "You win!"
            else:
                outcome = "I win!"
                
            embed = discord.Embed(description=f"I chose {bot_choice}. {outcome}", color=discord.Color.gold())
            await interaction.response.edit_message(embed=embed, view=None)

        select.callback = select_callback

        view = discord.ui.View()
        view.add_item(select)
        
        embed = discord.Embed(description="Play Rock-Paper-Scissors with me! Choose an option below:", color=discord.Color.blue())
        await ctx.respond(embed=embed, view=view)

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

    @discord.slash_command(name='guessnumber')
    async def guess_number(self, ctx: discord.ApplicationContext):
        """Starts a number guessing game."""
        number = random.randint(1, 10)
        
        await ctx.respond(embed=discord.Embed(description="Guess a number between 1 and 10!", color=discord.Color.magenta()))

        def check(msg):
            return msg.author == ctx.author and msg.content.isdigit()

        guess = await self.bot.wait_for("message", check=check)
        
        if int(guess.content) == number:
            embed = discord.Embed(description="Correct!", color=discord.Color.green())
        else:
            embed = discord.Embed(description=f"Wrong! The number was {number}.", color=discord.Color.red())
            
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
                    await ctx.respond(embed=discord.Embed(description="Couldn't fetch a quote right now.", color=discord.Color.red()))

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
        print(f'Fun Cog Loaded!')

def setup(bot):
    bot.add_cog(fun(bot))