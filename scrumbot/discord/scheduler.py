"""
Background tasks and schedulers for ScrumBot.
"""
import datetime
import logging

from discord.ext import commands, tasks


class ScrumScheduler(commands.Cog):
    """Cog for managing scheduled tasks."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.daily_standup.start()

    def cog_unload(self) -> None:
        self.daily_standup.cancel()

    # Schedule the loop for 9 AM UTC every day
    time = datetime.time(hour=9, minute=0, tzinfo=datetime.timezone.utc)

    @tasks.loop(time=time)
    async def daily_standup(self) -> None:
        """Executes the daily standup routine."""
        logging.info("Running daily standup...")
        # Add logic to notify channels or users here

    @daily_standup.before_loop
    async def before_standup(self) -> None:
        """Waits until the bot is ready before starting the loop."""
        await self.bot.wait_until_ready()


async def setup_scheduler(bot: commands.Bot) -> None:
    """Adds the scheduler cog to the bot."""
    await bot.add_cog(ScrumScheduler(bot))
