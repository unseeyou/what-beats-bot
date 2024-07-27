import asyncio
import sys

import discord

from bot.bot import Bot


async def main() -> None:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = Bot(
        command_prefix="p!",
        intents=intents,
        case_insensitive=True,
        allowed_contexts=discord.app_commands.AppCommandContext(guild=True, dm_channel=False),
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="whatbeatsrock.com",
            url="https://whatbeatsrock.com",
        ),
    )
    async with bot:
        await bot.connect_to_database()
        await bot.start(bot.settings.discord_bot_token)
        await bot.close_database_connection()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot Stopped")
        sys.exit()
