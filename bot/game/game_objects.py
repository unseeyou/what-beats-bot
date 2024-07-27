from typing import Literal

import g4f
from discord import Embed, ui


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

    def determine_winner(self, item1: str, item2: str) -> str:
        prompt = """You are to determine if item A would beat item B. These items will be supplied by the user.
        Provide your answer in the following format: ```{item1} beats/loses to {item2}!\n[reason](emoji1, emoji2)```
        where emoji1 and emoji2 are emojis that represent the items respectively."""
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"{item1} or {item2}?"}],
        )
        output: str = str(response)
        return output


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
