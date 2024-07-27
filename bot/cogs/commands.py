from typing import Literal

from discord import Embed, Interaction, app_commands, ui
from discord.ext import commands
from emoji_translate.emoji_translate import Translator


class GameEmbed(Embed):
    def __init__(
        self,
        item: str,
        prev_item: str | None = None,
        state: Literal["ask", "lose", "explain"] = "ask",
    ) -> None:
        self._translator = Translator()
        self._state = state
        self.item = item
        self._prev_item = prev_item
        title = description = None
        match self._state:
            case "ask":
                title = f"What beats {self.item}?"
                description = f"# {self._get_emoji_representation(item)}"
            case "lose":
                title = "You lose!"
                description = f"**{item}** does not beat **{self._prev_item}**"
            case "explain":
                title = "Explain"
                description = f"**{item}** beats **{self._prev_item}**"
        super().__init__(title=title, description=description)

    def _get_emoji_representation(self, string: str) -> str:
        emojis: str = self._translator.emojify(string)
        print(emojis)
        no_text = [i for i in emojis if not i.isalnum()]
        return max(no_text, key=lambda x: no_text.count(x))  # most common emoji


class GameView(ui.View):
    def __init__(self, state: Literal["ask", "lose", "explain"]) -> None:
        super().__init__()
        self._state = state
        match self._state:
            case "ask":
                pass
            case "lose":
                pass
            case "explain":
                pass


class BotCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="play", description="Play what beats rock game")
    async def play(self, interaction: Interaction) -> None:
        game_embed = GameEmbed("rock")
        await interaction.response.send_message(embed=game_embed, view=GameView("ask"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BotCommands(bot))
