"""
Discord event handlers.
"""
import logging

import discord
from discord.ext import commands


def setup_events(bot: commands.Bot) -> None:
    """Registers event listeners to the bot."""

    @bot.event
    async def on_ready() -> None:
        """Called when the bot is fully ready and connected."""
        logging.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
        logging.info("------")

    @bot.event
    async def on_message(message: discord.Message) -> None:
        """Called for every message."""
        # Ignore messages from the bot itself
        if message.author == bot.user:
            return

        # Process prefix commands if there are any
        await bot.process_commands(message)
