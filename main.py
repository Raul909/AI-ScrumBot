"""Universal entry point for AI ScrumBot.

Runs the Discord bot, the MCP server, or both against a single shared
application container:

    python main.py --mode discord   # Discord bot only (default)
    python main.py --mode mcp       # MCP server only (transport from env)
    python main.py --mode both      # bot + MCP (MCP forced to HTTP)

In "both" mode a stdio MCP transport would fight the Discord bot for
stdin/stdout, so it is transparently upgraded to HTTP.
"""
from __future__ import annotations

import argparse
import asyncio
import logging

from scrumbot.app import ScrumBotApp
from scrumbot.config import get_settings, setup_logging
from scrumbot.discord.bot import ScrumBot
from scrumbot.discord.dispatcher import chunk_message
from scrumbot.mcp_server.server import serve as serve_mcp
from scrumbot.webhooks import serve_webhooks

logger = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI ScrumBot entry point")
    parser.add_argument(
        "--mode",
        choices=["discord", "mcp", "both"],
        default="discord",
        help="Which surface(s) to run (default: discord).",
    )
    return parser.parse_args()


async def _run(mode: str) -> None:
    settings = get_settings()
    bot: ScrumBot | None = None

    async with ScrumBotApp(settings) as app:
        tasks: list[asyncio.Task] = []
        try:
            if mode in ("discord", "both"):
                if not settings.discord_token:
                    raise SystemExit("DISCORD_TOKEN is required to run the Discord bot.")
                bot = ScrumBot(app)
                tasks.append(asyncio.create_task(bot.start(settings.discord_token), name="discord"))

            if mode in ("mcp", "both"):
                transport = settings.mcp_transport
                if mode == "both" and transport == "stdio":
                    logger.warning("stdio MCP cannot coexist with the Discord bot; using HTTP.")
                    transport = "http"
                tasks.append(
                    asyncio.create_task(
                        serve_mcp(app, transport, settings.mcp_host, settings.mcp_port),
                        name="mcp",
                    )
                )

            if mode == "both" and settings.webhook_secret:
                async def _notify(text: str) -> None:
                    if bot is None or settings.notify_channel_id is None:
                        return
                    channel = bot.get_channel(settings.notify_channel_id)
                    if channel is None:
                        logger.warning("Notify channel %s not found.", settings.notify_channel_id)
                        return
                    for chunk in chunk_message(text):
                        await channel.send(chunk)

                tasks.append(
                    asyncio.create_task(
                        serve_webhooks(
                            app, settings.webhook_host, settings.webhook_port, notify=_notify
                        ),
                        name="webhooks",
                    )
                )

            # Run until the first surface exits (or errors), then unwind cleanly.
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)
            for task in done:
                if (exc := task.exception()) is not None:
                    raise exc
        finally:
            if bot is not None and not bot.is_closed():
                await bot.close()


def main() -> None:
    setup_logging()
    args = _parse_args()
    try:
        asyncio.run(_run(args.mode))
    except KeyboardInterrupt:
        logger.info("Shutting down (interrupted).")


if __name__ == "__main__":
    main()
