"""
Main bot setup and command registration.
"""
import logging
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


# Mock queue for tasks
class MockQueue:
    """A mock request queue for central processing."""
    
    async def put(self, item: dict) -> None:
        logging.info(f"Enqueued: {item}")


request_queue = MockQueue()


class ScrumCommands(commands.Cog):
    """Slash commands for ScrumBot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Ask the Scrum Master a question.")
    async def ask(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        await request_queue.put({"type": "ask", "user": interaction.user.id, "question": question})
        await interaction.followup.send(f"Thinking about: '{question}'...")

    @app_commands.command(name="board", description="View the current agile board.")
    async def board(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await request_queue.put({"type": "board", "user": interaction.user.id})
        await interaction.followup.send("Fetching the board...")

    @app_commands.command(name="standup", description="Start or view the daily standup.")
    async def standup(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await request_queue.put({"type": "standup", "user": interaction.user.id})
        await interaction.followup.send("Checking standup status...")

    task_group = app_commands.Group(name="task", description="Task management commands.")

    @task_group.command(name="update", description="Update a task's status.")
    async def task_update(self, interaction: discord.Interaction, task_id: str, status: str):
        await interaction.response.defer()
        await request_queue.put({
            "type": "task_update",
            "user": interaction.user.id,
            "task_id": task_id,
            "status": status
        })
        await interaction.followup.send(f"Updating task {task_id} to {status}...")

    @task_group.command(name="create", description="Create a new task.")
    async def task_create(self, interaction: discord.Interaction, title: str, description: Optional[str] = None):
        await interaction.response.defer()
        await request_queue.put({
            "type": "task_create",
            "user": interaction.user.id,
            "title": title,
            "description": description
        })
        await interaction.followup.send(f"Creating task '{title}'...")

    @app_commands.command(name="sync", description="Sync board with external trackers.")
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await request_queue.put({"type": "sync", "user": interaction.user.id})
        await interaction.followup.send("Syncing board...")

    @app_commands.command(name="clear", description="Clear completed tasks from the board.")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await request_queue.put({"type": "clear", "user": interaction.user.id})
        await interaction.followup.send("Clearing completed tasks...")


class ScrumBot(commands.Bot):
    """The main Discord bot class for ScrumBot."""

    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.messages = True
        super().__init__(command_prefix="!", intents=intents, *args, **kwargs)

    async def setup_hook(self) -> None:
        """Setup tasks to run before the bot starts."""
        from .events import setup_events
        from .scheduler import setup_scheduler
        
        setup_events(self)
        await setup_scheduler(self)

        await self.add_cog(ScrumCommands(self))
        await self.tree.sync()
        logging.info("ScrumBot setup complete.")
