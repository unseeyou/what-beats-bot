import asyncio

import discord

from bot.bot import Bot


async def main() -> None:
    intents = discord.Intents.default()
    bot = Bot(
        command_prefix="p!",
        intents=intents,
        case_insensitive=True,
        allowed_contexts=discord.app_commands.AppCommandContext(guild=True, dm_channel=False),
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="whatbeatsrock.com",
            url="https://whatbeatsrock.com",
            buttons=[
                discord.ui.Button(
                    label="Check out the website",
                    url="https://whatbeatsrock.com",
                    style=discord.ButtonStyle.url,
                ),
            ],
        ),
    )
    await bot.connect_to_database()
    await bot.start(bot.settings.discord_bot_token)
    await bot.close_database_connection()


if __name__ == "__main__":
    asyncio.run(main())
