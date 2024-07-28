from typing import Literal

import g4f
from discord import Embed, Interaction, ui


class GameEmbed(Embed):
    def __init__(
        self,
        item: str,
        prev_item: str | None = None,
        state: Literal["ask", "lose", "explain"] = "ask",
    ) -> None:
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

    def _get_emoji_representation(self, item: str) -> str:
        return "".join(
            [
                i
                for i in g4f.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"what would {item} be as one emoji?"}],
                )
                if not i.isalnum() and i not in ".,/?;:[]{}!@#$%^&*()-=_+`~"
            ],
        )


class InputModal(ui.Modal):
    def __init__(self, item: str) -> None:
        super().__init__(title=f"What beats {item}?")

    answer = ui.TextInput(
        label="Answer",
        placeholder="...",
        style=ui.TextInputStyle.short,
        required=True,
        max_length=30,
    )

    async def on_submit(self, interaction: Interaction) -> None:
        origin = await interaction.original_response()
        await origin.edit(view=GameView("explain", self.answer.value))


class InputButton(ui.Button):
    def __init__(self) -> None:
        super().__init__(style=ui.ButtonStyle.primary, label="Click to answer")

    async def callback(self, interaction: Interaction) -> None:
        view: GameView = self.view
        item = view.item
        await interaction.response.send_modal(
            InputModal(item),
        )


class GameView(ui.View):
    def __init__(self, state: Literal["ask", "lose", "explain"], item: str) -> None:
        super().__init__()
        self._state = state
        self.prev_item = item
        self.item = item
        match self._state:
            case "ask":
                self.clear_items()
                self.add_item(InputButton())
            case "lose":
                self.clear_items()
            case "explain":
                self.clear_items()
                winner = self.determine_winner()
                print(winner)

    def update_item(self, item: str) -> None:
        self.prev_item = self.item
        self.item = item

    def determine_winner(self) -> str:
        prompt = """You are to determine if item A would beat item B. These items will be supplied by the user.
        Provide your answer in the following format: ```{item1} beats/loses to {item2}!\n[reason](emoji1, emoji2)```
        where emoji1 and emoji2 are emojis that represent the items respectively."""
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{self.item} or {self.prev_item}?"},
            ],
        )
        output: str = str(response)
        return output
