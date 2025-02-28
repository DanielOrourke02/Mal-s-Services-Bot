

from util.utilities import *


PURCHASE_CATEGORY_ID = 1307085222457901136
BAN_APPEAL_CATEGORY_ID = 1345070997216297053
FAQ_CATEGORY_ID = 1307090109589356544
GIVEAWAYS_CATEGORY_ID = 1345070998248099850 
OTHER_CATEGORY_ID = 1307090153155723377

class ConfirmCloseView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None) 
        self.ctx = ctx

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
    async def confirm_close(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Only the command initiator can confirm this action.", ephemeral=True)
            return

        log_channel = discord.utils.get(interaction.guild.text_channels, name="「🔎」ticket-logs")
        if log_channel:
            embed = discord.Embed(
                title="Ticket Closed",
                description=f"Ticket `{interaction.channel.name}` was closed by {interaction.user.mention}.",
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)

        await interaction.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=None)
        self.bot = bot
        self.ctx = ctx
        self.ticket_category_mapping = {
            "Purchase": PURCHASE_CATEGORY_ID,
            "Ban Appeal": BAN_APPEAL_CATEGORY_ID,
            "FAQ": FAQ_CATEGORY_ID,
            "Giveaways": GIVEAWAYS_CATEGORY_ID,
            "Other": OTHER_CATEGORY_ID,
        }
        self.selected_category = None

    @discord.ui.select(
        placeholder="Select a ticket category...",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Purchase", 
                description="Patreon inquiries and purchases", 
                emoji="<:Donator:1345071548230533262>"
            ),
            discord.SelectOption(
                label="Ban Appeal", 
                description="Appeal a server ban", 
                emoji="<:ban_hammer:1345071574994128896>"
            ),
            discord.SelectOption(
                label="FAQ", 
                description="General questions and help", 
                emoji="<:Question:1345071437823869061>"
            ),
            discord.SelectOption(
                label="Giveaways", 
                description="Giveaway related inquiries", 
                emoji="<:Giveaways:1320352823770087515>"
            ),
            discord.SelectOption(
                label="Other", 
                description="Other inquiries", 
                emoji="🌀"
            ),
        ]
    )
    async def select_category_callback(self, select, interaction: discord.Interaction):
        self.selected_category = select.values[0]
        await interaction.response.defer()

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary)
    async def create_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            if self.selected_category is None:
                await interaction.response.send_message("Please select a ticket category.", ephemeral=True)
                return

            existing_tickets = [channel for channel in interaction.guild.text_channels 
                                if channel.category_id == self.ticket_category_mapping.get(self.selected_category) and 
                                interaction.user.name in channel.name]
            
            if existing_tickets:
                await interaction.response.send_message(f"You already have an open ticket in the **{self.selected_category}** category.", ephemeral=True)
                return

            category_id = self.ticket_category_mapping.get(self.selected_category)
            guild = interaction.guild

            category = discord.utils.get(guild.categories, id=category_id)
            
            if category is None: # this if statement will NEVER run
                await interaction.response.send_message("The specified category could not be found.", ephemeral=True)
                return

            # Set channel permissions for the user
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Hide channel from everyone
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),  # Allow access for ticket creator
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)  # Allow bot to read/send messages
            }

            ticket_channel = await guild.create_text_channel(
                name=f"{self.selected_category} Ticket - {interaction.user.name}",
                category=category,
                topic=f"Support ticket for {self.selected_category}",
                overwrites=overwrites
            )

            await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

            embed = discord.Embed(
                title="<:vsl_ticket:1304908762439745616> Ticket Opened",
                description=f"Hello {interaction.user.mention},\nOur support team will be with you shortly. Please provide any details about your issue to help us assist you faster.",
                color=discord.Color.gold()
            )
            avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
            if avatar_url:
                embed.set_thumbnail(url=avatar_url)
            embed.set_footer(text=f"Mal's Services", icon_url=self.ctx.bot.user.avatar.url)
            embed.timestamp = discord.utils.utcnow()
            
            view = TicketActionsView(interaction.user, ticket_channel)
            await ticket_channel.send(embed=embed, view=view)

        except Exception as e:
            print(e)

class TicketActionsView(discord.ui.View):
    def __init__(self, user, ticket_channel):
        super().__init__(timeout=None)
        self.user = user
        self.ticket_channel = ticket_channel
        self.claimed = False

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.success, emoji="🔒")
    async def claim_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Only administrators can claim this ticket.", ephemeral=True)
            return
        
        if self.claimed:
            await interaction.response.send_message("This ticket has already been claimed.", ephemeral=True)
            return

        self.claimed = True
        button.disabled = True
        await interaction.response.edit_message(view=self)

        embed = discord.Embed(
            title="Ticket Claimed",
            description=f"{interaction.user.mention} has claimed this ticket and will assist you shortly.",
            color=discord.Color.green()
        )
        await interaction.channel.send(embed=embed)
    
    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="<:vsl_ticket:1304908762439745616>")
    async def close_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Are you sure you want to close this ticket?", 
            ephemeral=True, 
            view=CloseConfirmationView(self.ticket_channel, interaction.user)
        )


class CloseConfirmationView(discord.ui.View):
    def __init__(self, ticket_channel, requester):
        super().__init__(timeout=None)
        self.ticket_channel = ticket_channel
        self.requester = requester

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
    async def confirm_close(self, button: discord.ui.Button, interaction: discord.Interaction):
        log_channel = discord.utils.get(interaction.guild.text_channels, name="「🔎」ticket-logs")
        if log_channel:
            log_embed = discord.Embed(
                title="Ticket Closed",
                description=f"Ticket `{self.ticket_channel.name}` was closed by {interaction.user.mention}.",
                color=discord.Color.red()
            )
            await log_channel.send(embed=log_embed)

        closing_embed = discord.Embed(
            title="Ticket Closed",
            description="This ticket will now be closed. Thank you for contacting support!",
            color=discord.Color.red()
        )
        await self.ticket_channel.send(embed=closing_embed)

        await self.ticket_channel.delete(reason="Ticket closed by staff")

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.slash_command(name='setup_tickets')
    @commands.has_permissions(administrator=True)
    async def tickets_setup(self, ctx: discord.ApplicationContext):
        try:
            embed = discord.Embed(
                title="<:vsl_ticket:1304908762439745616> Ticket Support System",
                description="Need assistance? Select a category below and click **Create Ticket** to get started.",
                color=discord.Color.from_rgb(0, 123, 255)
            )
            
            embed.add_field(
                name="Available Categories:",
                value=(
                    "💰 **Purchase** - Patreon inquiries and purchases\n"
                    "🔨 **Ban Appeal** - Appeal a server ban\n"
                    "❓ **FAQ** - General questions and help\n"
                    "🎉 **Giveaways** - Giveaway related inquiries\n"
                    "🌀 **Other** - Other inquiries"
                ),
                inline=False
            )
            
            embed.add_field(
                name="How It Works:", 
                value=(
                    "1. Select your ticket category\n"
                    "2. Click the Create Ticket button\n"
                    "3. Provide details about your inquiry\n"
                    "4. Wait for staff response"
                ), 
                inline=False
            )

            embed.set_footer(text=f"Mal's Services", icon_url=ctx.bot.user.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            view = TicketView(self.bot, ctx)
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            print(e)
            
    @discord.slash_command(name="close", description="Closes the current ticket channel")
    async def close(self, ctx):
        try:
            ticket_category_ids = [PURCHASE_CATEGORY_ID, GIVEAWAYS_CATEGORY_ID, BAN_APPEAL_CATEGORY_ID, FAQ_CATEGORY_ID, OTHER_CATEGORY_ID]

            if ctx.channel.category_id not in ticket_category_ids:
                embed = discord.Embed(
                    description="<a:denied:1302388701422288957> This command can only be used in a ticket channel.",
                    color=discord.Color.red()
                )
                await ctx.respond(embed=embed)
                return

            embed = discord.Embed(
                title="Close Ticket",
                description="Are you sure you want to close this ticket? Press **Confirm** below to proceed.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed, view=ConfirmCloseView(ctx))

        except Exception as e:
            print(e)

    @discord.slash_command(name='add')
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.Member):
        if "Ticket" or "ticket" in ctx.channel.name:
            await ctx.channel.set_permissions(user, read_messages=True, send_messages=True)
            
            embed = discord.Embed(
                title="User Added to Ticket",
                description=f"{user.mention} has been added to this ticket channel.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title="Invalid Channel",
                description="This command can only be used in a ticket channel.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
    
    @discord.slash_command(name='remove')
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.Member):
        if "Ticket" or "ticket" in ctx.channel.name:
            await ctx.channel.set_permissions(user, overwrite=None)
            
            embed = discord.Embed(
                title="User Removed from Ticket",
                description=f"{user.mention} has been removed from this ticket channel.",
                color=discord.Color.orange()
            )
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title="Invalid Channel",
                description="This command can only be used in a ticket channel.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)

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
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Tickets Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(Tickets(bot))