import discord
import asyncio
from discord.ext import commands

ROLE_ID = 1195702107215511603

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='ban', description="Ban a member from the server.")
    @commands.has_permissions(administrator=True)
    async def ban(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Option(discord.Member, "Select a member to ban", required=True), 
        reason: discord.Option(str, "Reason for the ban", default="No reason provided")
    ):
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="User Banned",
            description=f"{member.mention} has been banned.",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.respond(embed=embed)

    @discord.slash_command(name='kick', description="Kick a member from the server.")
    @commands.has_permissions(administrator=True)
    async def kick(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Option(discord.Member, "Select a member to kick", required=True), 
        reason: discord.Option(str, "Reason for the kick", default="No reason provided")
    ):
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="User Kicked",
            description=f"{member.mention} has been kicked.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.respond(embed=embed)

    @discord.slash_command(name='mute', description="Mute a member for a specified number of minutes.")
    @commands.has_permissions(administrator=True)
    async def mute(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Option(discord.Member, "Select a member to mute", required=True), 
        duration: discord.Option(int, "Duration of mute in minutes", required=True)
    ):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(muted_role)
        embed = discord.Embed(
            title="User Muted",
            description=f"{member.mention} has been muted for {duration} minutes.",
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed)
        
        await asyncio.sleep(duration * 60)
        await member.remove_roles(muted_role)

    @discord.slash_command(name='unmute', description="Unmute a member.")
    @commands.has_permissions(administrator=True)
    async def unmute(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Option(discord.Member, "Select a member to unmute")
    ):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muted_role)
        embed = discord.Embed(
            title="User Unmuted",
            description=f"{member.mention} has been unmuted.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(name='lock', description="Lock a channel for a specific role.")
    @commands.has_permissions(administrator=True)
    async def lock(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(discord.TextChannel, "Select a channel to lock", required=False)
    ):
        channel = channel or ctx.channel
        role = ctx.guild.get_role(ROLE_ID)
        await channel.set_permissions(role, send_messages=False, send_messages_in_threads=False, add_reactions=False)
        embed = discord.Embed(
            title="Channel Locked",
            description=f"{channel.mention} has been locked for {role.mention}. Typing and messaging are disabled.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(name='unlock', description="Unlock a channel for a specific role.")
    @commands.has_permissions(administrator=True)
    async def unlock(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(discord.TextChannel, "Select a channel to unlock", required=False)
    ):
        channel = channel or ctx.channel
        role = ctx.guild.get_role(ROLE_ID)
        await channel.set_permissions(role, send_messages=True, send_messages_in_threads=True, add_reactions=True)
        embed = discord.Embed(
            title="Channel Unlocked",
            description=f"{channel.mention} has been unlocked for {role.mention}. Typing and messaging are enabled.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(name='serverlock', description="Lock all channels in the server for a specific role.")
    @commands.has_permissions(administrator=True)
    async def serverlock(self, ctx: discord.ApplicationContext):
        role = ctx.guild.get_role(ROLE_ID)
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(role, send_messages=False, send_messages_in_threads=False, add_reactions=False)
        embed = discord.Embed(
            title="Server Locked",
            description=f"All channels have been locked for {role.mention}. Typing and messaging are disabled.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(name='serverunlock', description="Unlock all channels in the server for a specific role.")
    @commands.has_permissions(administrator=True)
    async def serverunlock(self, ctx: discord.ApplicationContext):
        role = ctx.guild.get_role(ROLE_ID)
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(role, send_messages=True, send_messages_in_threads=True, add_reactions=True)
        embed = discord.Embed(
            title="Server Unlocked",
            description=f"All channels have been unlocked for {role.mention}. Typing and messaging are enabled.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="<a:denied:1302388701422288957> You do not have permission to use this command.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Moderator Cog Loaded!')

def setup(bot):
    bot.add_cog(Moderator(bot))
