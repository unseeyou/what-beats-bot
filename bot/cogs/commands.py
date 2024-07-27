from discord import Interaction, app_commands
from discord.ext import commands

from bot.game.game_objects import GameEmbed, GameView


class BotCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="play", description="Play what beats rock game")
    async def play(self, interaction: Interaction) -> None:
        await interaction.response.defer(thinking=True)
        game_embed = GameEmbed("rock")
        await interaction.followup.send(embed=game_embed, view=GameView("ask"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BotCommands(bot))
