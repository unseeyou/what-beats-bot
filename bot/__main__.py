import asyncio
import contextlib
import sys

import discord

from bot.bot import Bot


async def main() -> None:
    async with bot:
        await bot.load_extensions("bot/cogs")
        await bot.connect_to_database()
        await bot.start(bot.settings.discord_bot_token)
        await bot.close_database_connection()
        await bot.close()


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        with contextlib.suppress(RuntimeError):
            asyncio.get_running_loop().close()
        bot.logger.warning("Keyboard Interrupt")
        print("Bot Stopped")
        sys.exit()
