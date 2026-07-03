"""Background schedulers for ScrumBot.

The daily standup posts the standup prompt to the configured channel
(``STANDUP_CHANNEL_ID``). With no channel configured it is a no-op, so the bot
runs fine out of the box.
"""
from __future__ import annotations

import datetime
import logging

from discord.ext import commands, tasks

from scrumbot.config import get_settings
from scrumbot.prompts import STANDUP_PROMPT

logger = logging.getLogger(__name__)


class ScrumScheduler(commands.Cog):
    """Cog managing scheduled jobs."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._channel_id = get_settings().standup_channel_id
        self.daily_standup.start()

    def cog_unload(self) -> None:
        self.daily_standup.cancel()

    # 09:00 UTC every day.
    _run_at = datetime.time(hour=9, minute=0, tzinfo=datetime.timezone.utc)

    @tasks.loop(time=_run_at)
    async def daily_standup(self) -> None:
        logger.info("Running daily standup...")
        if not self._channel_id:
            return
        channel = self.bot.get_channel(self._channel_id)
        if channel is None:
            logger.warning("Standup channel %s not found or not cached.", self._channel_id)
            return
        await channel.send(STANDUP_PROMPT)

    @daily_standup.before_loop
    async def before_standup(self) -> None:
        await self.bot.wait_until_ready()


async def setup_scheduler(bot: commands.Bot) -> None:
    """Add the scheduler cog to ``bot``."""
    await bot.add_cog(ScrumScheduler(bot))
