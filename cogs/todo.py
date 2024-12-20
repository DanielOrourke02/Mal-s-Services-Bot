

from util.utilities import *


class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect('databases/todo.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS todos
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      task TEXT,
                      priority TEXT,
                      deadline TIMESTAMP,
                      completed BOOLEAN DEFAULT 0,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    todo = discord.SlashCommandGroup("todo", "Manage your todo list")

    @todo.command(name="add")
    async def add_task(
        self, 
        ctx, 
        task: discord.Option(str, "Task description", max_length=200), # type: ignore
        priority: discord.Option(str, "Task priority", choices=["Low", "Medium", "High"]), # type: ignore
        deadline: Optional[str] = None
    ):
        """Add a new task to your todo list"""

        await ctx.defer()

        try:
            deadline_date = None
            if deadline:
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                if deadline_date < datetime.now():
                    raise ValueError("Deadline cannot be in the past")

            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute('''INSERT INTO todos (user_id, task, priority, deadline)
                        VALUES (?, ?, ?, ?)''',
                     (ctx.author.id, task, priority, deadline_date.isoformat() if deadline_date else None))
            task_id = c.lastrowid
            conn.commit()
            conn.close()

            embed = discord.Embed(
                title="✅ Task Added",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )

            embed.add_field(
                name="📝 Task Details",
                value=f"""```yml
ID: #{task_id}
Task: {task}
Priority: {priority}
Deadline: {deadline if deadline else 'None set'}```""",
                inline=False
            )

            embed.set_footer(
                text=f"Added by {ctx.author.display_name}",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None
            )

            await ctx.respond(embed=embed)

        except ValueError as e:
            await ctx.respond(f"❌ Error: {str(e)}", ephemeral=True)
        except Exception as e:
            await ctx.respond("❌ Failed to add task. Please use YYYY-MM-DD format for deadline.", ephemeral=True)

    @todo.command(name="list")
    async def list_tasks(
        self,
        ctx,
        filter: discord.Option(str, "Filter tasks", choices=["All", "Pending", "Completed"]) = "Pending" # type: ignore
    ):
        """List your todo tasks"""

        await ctx.defer()

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        if filter == "All":
            c.execute('''SELECT * FROM todos WHERE user_id = ? ORDER BY 
                        CASE priority
                            WHEN 'High' THEN 1
                            WHEN 'Medium' THEN 2
                            WHEN 'Low' THEN 3
                        END, 
                        deadline IS NULL, 
                        deadline''', (ctx.author.id,))
        else:
            completed = 1 if filter == "Completed" else 0
            c.execute('''SELECT * FROM todos WHERE user_id = ? AND completed = ? ORDER BY 
                        CASE priority
                            WHEN 'High' THEN 1
                            WHEN 'Medium' THEN 2
                            WHEN 'Low' THEN 3
                        END,
                        deadline IS NULL,
                        deadline''', (ctx.author.id, completed))

        tasks = c.fetchall()
        conn.close()

        if not tasks:
            embed = discord.Embed(
                title="📋 Todo List",
                description="```yml\nNo tasks found```",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            await ctx.respond(embed=embed)
            return

        embeds = []
        tasks_per_page = 5
        for i in range(0, len(tasks), tasks_per_page):
            embed = discord.Embed(
                title="📋 Todo List",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )

            for task in tasks[i:i + tasks_per_page]:
                task_id, _, task_desc, priority, deadline, completed, created_at = task
                status = "✅" if completed else "⏳"
                deadline_str = datetime.fromisoformat(deadline).strftime("%Y-%m-%d") if deadline else "No deadline"

                embed.add_field(
                    name=f"{status} Task #{task_id}",
                    value=f"""```yml
Task: {task_desc}
Priority: {priority}
Deadline: {deadline_str}```""",
                    inline=False
                )

            embed.set_footer(
                text=f"Page {len(embeds)+1} | {ctx.author.display_name}",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None
            )
            embeds.append(embed)

        if len(embeds) == 1:
            await ctx.respond(embed=embeds[0])
        else:
            # Implement pagination here if needed
            await ctx.respond(embed=embeds[0])

    @todo.command(name="complete")
    async def complete_task(
        self,
        ctx,
        task_id: discord.Option(int, "Task ID to mark as complete") # type: ignore
    ):
        """Mark a task as completed"""

        await ctx.defer()

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        
        c.execute('SELECT task, completed FROM todos WHERE id = ? AND user_id = ?', 
                 (task_id, ctx.author.id))
        result = c.fetchone()

        if not result:
            await ctx.respond("❌ Task not found or you don't own this task.", ephemeral=True)
            conn.close()
            return

        task_desc, completed = result
        if completed:
            await ctx.respond("❌ This task is already completed!", ephemeral=True)
            conn.close()
            return

        c.execute('UPDATE todos SET completed = 1 WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="✅ Task Completed",
            description=f"""```yml
Task #{task_id}: {task_desc}```""",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )

        embed.set_footer(
            text=f"Completed by {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )

        await ctx.respond(embed=embed)

    @todo.command(name="delete")
    async def delete_task(
        self,
        ctx,
        task_id: discord.Option(int, "Task ID to delete") # type: ignore
    ):
        """Delete a task from your list"""

        await ctx.defer()

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        
        c.execute('SELECT task FROM todos WHERE id = ? AND user_id = ?', 
                 (task_id, ctx.author.id))
        result = c.fetchone()

        if not result:
            await ctx.respond("❌ Task not found or you don't own this task.", ephemeral=True)
            conn.close()
            return

        c.execute('DELETE FROM todos WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="🗑️ Task Deleted",
            description=f"""```yml
Task #{task_id}: {result[0]}```""",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )

        embed.set_footer(
            text=f"Deleted by {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )

        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Todo List Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(Todo(bot))