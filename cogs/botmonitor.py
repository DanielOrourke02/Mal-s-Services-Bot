import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

class CasinoBotMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.monitored_bot_id = 1272208314163396650  # The bot ID being monitored
        self.status_channel_id = 1312459902593142814  # The channel to post status updates
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
        """Periodically checks the status of the monitored bot and updates the embed."""
        guild = self.bot.get_guild(self.bot.guilds[0].id)  # Adjusted for multi-server compatibility
        monitored_bot = guild.get_member(self.monitored_bot_id) if guild else None

        # Determine status based on manual override or bot's actual status
        if self.manual_override:
            status = self.manual_override
        elif monitored_bot is None:
            status = "Not in Guild"
        else:
            status = str(monitored_bot.status).capitalize()

        self.last_checked = datetime.utcnow()
        if status == "Online":
            if not self.uptime_start:
                self.uptime_start = datetime.utcnow()  # Start tracking uptime
        else:
            if self.uptime_start:
                self.last_downtime = datetime.utcnow()  # Log downtime
                self.uptime_start = None  # Reset uptime tracking

        # Create the embed
        embed = discord.Embed(
            title="🎲 Casino Bot Status Monitor 🎲",
            color=discord.Color.green() if status == "Online" else discord.Color.red(),
            timestamp=self.last_checked
        )
        embed.add_field(name="Current Status", value=status, inline=False)
        embed.add_field(
            name="Last Checked",
            value=f"<t:{int(self.last_checked.timestamp())}:R> ({self.last_checked.strftime('%Y-%m-%d %H:%M:%S')} UTC)",
            inline=False
        )
        embed.add_field(name="Manual Override", value=self.manual_override or "None", inline=False)

        # Add uptime or last downtime
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

        # Send or edit the message in the status channel
        channel = self.bot.get_channel(self.status_channel_id)
        if channel:
            messages = await channel.history(limit=1).flatten()
            if messages and messages[0].author == self.bot.user:
                await messages[0].edit(embed=embed)
            else:
                await channel.send(embed=embed)

    @monitor_task.before_loop
    async def before_monitor_task(self):
        """Waits until the bot is ready before starting the monitoring loop."""
        await self.bot.wait_until_ready()

    @discord.slash_command(name="setbotstatus")
    @commands.has_permissions(administrator=True)
    async def set_bot_status(self, ctx, *, status: str):
        """Manually override the bot's status."""
        valid_statuses = ["Online", "Offline", "Idle", "Dnd", "Maintenance", "Not in Guild"]
        if status.capitalize() not in valid_statuses:
            await ctx.respond(f"Invalid status. Choose from: {', '.join(valid_statuses)}", ephemeral=True)
            return

        self.manual_override = status.capitalize()
        await ctx.respond(f"Manual override set to: **{self.manual_override}**", ephemeral=True)
        await self.monitor_task()  # Immediately update status

    @discord.slash_command(name="clearbotstatus")
    @commands.has_permissions(administrator=True)
    async def clear_bot_status(self, ctx):
        """Clears any manual overrides and resumes auto-monitoring."""
        self.manual_override = None
        await ctx.respond("Manual override cleared. Auto-monitoring resumed.", ephemeral=True)
        await self.monitor_task()  # Immediately update status

    @discord.slash_command(name="setmaintenance")
    @commands.has_permissions(administrator=True)
    async def set_maintenance_mode(self, ctx):
        """Set the monitored bot's status to Maintenance."""
        self.manual_override = "Maintenance"
        await ctx.respond("Casino bot status set to: **Maintenance**.", ephemeral=True)
        await self.monitor_task()  # Immediately update status

def setup(bot):
    bot.add_cog(CasinoBotMonitor(bot))
