import logging
import pathlib
import typing

import aiosqlite
import discord
from discord.ext import commands
from rich.logging import RichHandler

from bot.settings import Settings


def configure_logging() -> None:
    file_handler = logging.FileHandler("zz.log", encoding="utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s: %(message)s",
        "%Y-%m-%d:%H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
        datefmt="%X",
        handlers=[RichHandler(), file_handler],
    )


class Bot(commands.Bot):
    def __init__(self, command_prefix: typing.Iterable[str], intents: discord.Intents, **options: typing.Any) -> None:  # noqa: ANN401
        super().__init__(command_prefix=command_prefix, intents=intents, **options)

        self.settings = Settings()  # pyright: ignore[reportCallIssue]

        configure_logging()
        self.logger = logging.getLogger("botcmds")

        self.database_connection: aiosqlite.Connection | None = None

        self.load_extensions("bot/cogs")

    async def connect_to_database(self) -> None:
        self.database_connection = await aiosqlite.connect(self.settings.database_path)

    async def close_database_connection(self) -> None:
        if self.database_connection is not None:
            await self.database_connection.close()

    async def load_extensions(self, path: str) -> None:
        for file in pathlib.Path(path).glob("*.py"):
            await self.load_extension(file.stem)
