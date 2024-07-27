from discord.ext.commands import CommandError


class DatabaseNotConnectedError(CommandError):
    """Raised when the bot is not connected to the database."""
