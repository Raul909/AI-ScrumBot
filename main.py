import argparse
import asyncio
import os
from dotenv import load_dotenv

async def run_discord_bot():
    """Placeholder for the Discord bot execution."""
    print("Starting Discord bot...")
    # Import bot and run here
    # from scrumbot.bot import bot
    # await bot.start(os.getenv("DISCORD_TOKEN"))
    print("Discord bot stopped.")

def run_mcp_server():
    """Runs the MCP server."""
    print("Starting MCP server...")
    from scrumbot.mcp_server.server import run
    run()

async def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="ScrumBot Main Entry Point")
    parser.add_argument("--mode", choices=["discord", "mcp", "both"], default="both", help="Mode to run the bot in")
    args = parser.parse_args()
    
    if args.mode == "discord":
        await run_discord_bot()
    elif args.mode == "mcp":
        run_mcp_server()
    elif args.mode == "both":
        # Run MCP server in a separate thread or process if it blocks,
        # but stdio MCP server usually takes over stdin/stdout. 
        # For simplicity in this skeleton, we'll try to run them concurrently if possible, 
        # though stdio MCP might conflict with discord logs.
        # Ideally MCP uses SSE if running alongside discord, or we run them separately.
        print("Warning: Running both stdio MCP and Discord bot might have stdin/stdout conflicts.")
        task = asyncio.create_task(run_discord_bot())
        run_mcp_server()
        await task

if __name__ == "__main__":
    asyncio.run(main())
