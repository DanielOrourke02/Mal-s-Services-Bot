import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

class CasinoBotMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.monitored_bot_id = 1272208314163396650 
        self.status_channel_id = 1312459902593142814 
        self.last_checked = None
        self.last_status = "Unknown"
        self.last_downtime = None
        self.uptime_start = None
        self.manual_override = None
        self.monitor_task.start()

    def cog_unload(self):
        self.monitor_task.cancel()

    @tasks.loop(minutes=5)
    async def monitor_task(self):
        guild = self.bot.get_guild(self.bot.guilds[0].id) 
        monitored_bot = guild.get_member(self.monitored_bot_id) if guild else None

        if self.manual_override:
            status = self.manual_override
        elif monitored_bot is None:
            status = "Not in Guild"
        else:
            status = str(monitored_bot.status).capitalize()

        self.last_checked = datetime.utcnow()
        if status == "Online":
            if not self.uptime_start:
                self.uptime_start = datetime.utcnow() 
        else:
            if self.uptime_start:
                self.last_downtime = datetime.utcnow()  
                self.uptime_start = None 

        embed = discord.Embed(
            title="🎲 Casino Bot Status Monitor 🎲",
            color=discord.Color.green() if status == "Online" else discord.Color.red(),
            timestamp=self.last_checked
        )
        embed.add_field(name="Bot Name", value=monitored_bot.name if monitored_bot else "Unknown", inline=False)
        embed.add_field(name="Bot ID", value=self.monitored_bot_id, inline=False)
        embed.add_field(name="Current Status", value=status, inline=False)
        embed.add_field(
            name="Last Checked",
            value=f"<t:{int(self.last_checked.timestamp())}:R> ({self.last_checked.strftime('%Y-%m-%d %H:%M:%S')} UTC)",
            inline=False
        )
        embed.add_field(name="Manual Override", value=self.manual_override or "None", inline=False)

        if self.uptime_start:
            uptime = datetime.utcnow() - self.uptime_start
            embed.add_field(name="Uptime", value=str(timedelta(seconds=int(uptime.total_seconds()))), inline=True)
        elif self.last_downtime:
            embed.add_field(
                name="Last Downtime",
                value=f"<t:{int(self.last_downtime.timestamp())}:R> ({self.last_downtime.strftime('%Y-%m-%d %H:%M:%S')} UTC)",
                inline=True
            )
        else:
            embed.add_field(name="Uptime", value="N/A", inline=True)

        embed.set_footer(text="Monitoring Service | Auto-updates every 5 minutes")

        channel = self.bot.get_channel(self.status_channel_id)
        if channel:
            messages = await channel.history(limit=1).flatten()
            if messages and messages[0].author == self.bot.user:
                await messages[0].edit(embed=embed)
            else:
                await channel.send(embed=embed)

    @monitor_task.before_loop
    async def before_monitor_task(self):
        await self.bot.wait_until_ready()

    @discord.slash_command(name="setbotstatus")
    @commands.has_permissions(administrator=True)
    async def set_bot_status(self, ctx, *, status: str):
        valid_statuses = ["Online", "Offline", "Idle", "Dnd", "Maintenance", "Not in Guild"]
        if status.capitalize() not in valid_statuses:
            await ctx.send(f"Invalid status. Choose from: {', '.join(valid_statuses)}")
            return

        self.manual_override = status.capitalize()
        await ctx.send(f"Manual override set to: **{self.manual_override}**")
        await self.monitor_task() 

    @discord.slash_command(name="clearbotstatus")
    @commands.has_permissions(administrator=True)
    async def clear_bot_status(self, ctx):
        self.manual_override = None
        await ctx.respond("Manual override cleared. Auto-monitoring resumed.")
        await self.monitor_task()

    @discord.slash_command(name="setmaintenance")
    @commands.has_permissions(administrator=True)
    async def set_maintenance_mode(self, ctx):
        self.manual_override = "Maintenance"
        await ctx.respond("Casino bot status set to: **Maintenance**.")
        await self.monitor_task()

def setup(bot):
    bot.add_cog(CasinoBotMonitor(bot))
