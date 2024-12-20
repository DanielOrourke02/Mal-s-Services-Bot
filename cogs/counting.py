

from util.utilities import *


def setup_database():
    conn = sqlite3.connect('databases/counting.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS counting_stats
                    (user_id INTEGER PRIMARY KEY,
                    correct_counts INTEGER DEFAULT 0,
                    failed_counts INTEGER DEFAULT 0,
                    last_count TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS high_scores
                    (id INTEGER PRIMARY KEY,
                    score INTEGER DEFAULT 0,
                    achieved_by INTEGER,
                    achieved_at TIMESTAMP)''')
    conn.commit()
    conn.close() 
    
class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counting_channel_id = 1312454065703096340
        self.required_role_id = 1312452960910970931
        self.current_count = 0
        self.last_counter = None
        setup_database()  # Call setup_database before getting high score
        self.high_score = self.get_high_score()

    def get_high_score(self):
        conn = sqlite3.connect('databases/counting.db')  # Fixed path
        c = conn.cursor()
        c.execute('SELECT score FROM high_scores ORDER BY score DESC LIMIT 1')
        result = c.fetchone()
        conn.close()
        return result[0] if result else 0

    def update_high_score(self, score, user_id):
        if score > self.high_score:
            conn = sqlite3.connect('databases/counting.db')  # Fixed path
            c = conn.cursor()
            c.execute('''INSERT INTO high_scores (score, achieved_by, achieved_at)
                        VALUES (?, ?, CURRENT_TIMESTAMP)''', (score, user_id))
            conn.commit()
            conn.close()
            self.high_score = score
            return True
        return False
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Counting Cog Loaded! {Fore.RESET}')
        channel = self.bot.get_channel(self.counting_channel_id)
        if channel:
            async for message in channel.history(limit=100):
                try:
                    if message.content.isdigit():
                        self.current_count = int(message.content)
                        self.last_counter = message.author.id
                        break
                except ValueError:
                    continue

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.channel.id != self.counting_channel_id:
            return

        required_role = discord.utils.get(message.author.roles, id=self.required_role_id)
        if not required_role:
            embed = discord.Embed(
                title="🔒 Access Denied",
                description=f"You need the <@&{self.required_role_id}> role to participate.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.set_footer(
                text=f"Requested by {message.author.display_name}",
                icon_url=message.author.avatar.url if message.author.avatar else None
            )
            await message.delete()
            await message.channel.send(embed=embed, delete_after=5)
            return

        if not message.content.isdigit():
            await message.delete()
            return

        user_count = int(message.content)
        expected_count = self.current_count + 1

        if self.last_counter == message.author.id:
            embed = discord.Embed(
                title="❌ Double Counting",
                description="You can't count twice in a row!",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.set_footer(
                text=f"Wait for someone else to count",
                icon_url=message.author.avatar.url if message.author.avatar else None
            )
            await message.delete()
            await message.channel.send(embed=embed, delete_after=5)
            return

        if user_count == expected_count:
            self.current_count = user_count
            self.last_counter = message.author.id
            self.update_user_stats(message.author.id, correct=True)

            reactions = ["✅"]
            if user_count % 100 == 0:
                reactions.extend(["🎉", "💯"])
            if user_count % 1000 == 0:
                reactions.extend(["🌟", "🏆"])

            for reaction in reactions:
                await message.add_reaction(reaction)

            if self.update_high_score(user_count, message.author.id):
                embed = discord.Embed(
                    title="🏆 New High Score!",
                    description=f"**{message.author.mention}** has set a new record: **{user_count}**!",
                    color=discord.Color.gold(),
                    timestamp=datetime.now()
                )
                await message.channel.send(embed=embed)

        else:
            self.update_user_stats(message.author.id, correct=False)
            embed = discord.Embed(
                title="❌ Counting Failed",
                description=f"Wrong number! The count has been reset.\nThe next number should have been **{expected_count}**.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.add_field(
                name="📊 Stats",
                value=f"""```yml
Current Count: 0 (reset from {self.current_count})
High Score: {self.high_score}```""",
                inline=False
            )
            embed.set_footer(
                text=f"Failed by {message.author.display_name}",
                icon_url=message.author.avatar.url if message.author.avatar else None
            )
            await message.delete()
            await message.channel.send(embed=embed)
            self.current_count = 0
            self.last_counter = None

    @commands.slash_command(name="counting_stats")
    async def counting_stats(self, ctx):
        """View your counting statistics"""
        
        await ctx.defer()

        conn = sqlite3.connect('databases/counting.db')
        c = conn.cursor()
        c.execute('SELECT correct_counts, failed_counts FROM counting_stats WHERE user_id = ?', 
                 (ctx.author.id,))
        result = c.fetchone()
        conn.close()

        if not result:
            correct, failed = 0, 0
        else:
            correct, failed = result

        total = correct + failed
        accuracy = (correct / total * 100) if total > 0 else 0

        embed = discord.Embed(
            title="🔢 Counting Statistics",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )

        embed.add_field(
            name="📊 Your Stats",
            value=f"""```yml
Correct Numbers: {correct}
Failed Attempts: {failed}
Total Attempts: {total}
Accuracy: {accuracy:.2f}%```""",
            inline=False
        )

        embed.add_field(
            name="🏆 High Score",
            value=f"```yml\nServer Record: {self.high_score}```",
            inline=False
        )

        embed.set_footer(
            text=f"Stats for {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Counting(bot))