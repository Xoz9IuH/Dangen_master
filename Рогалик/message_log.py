from typing import Iterable, List, Reversible, Tuple
import textwrap

import tcod

import color


class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        """Полный текст этого сообщения, включая количество, если необходимо."""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True) -> None:
        """Добавляет сообщение в этот журнал.

`text` — текст сообщения, `fg` — цвет текста.

Если `stack` — True, то сообщение может быть добавлено к предыдущему сообщению
с тем же текстом.
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(self, console: tcod.Console, x: int, y: int, width: int, height: int) -> None:
        """Отобразить этот журнал в указанной области.

`x`, `y`, `width`, `height` — это прямоугольная область для отображения на
`console`.
        """
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        """Верните готовое текстовое сообщение."""
        for line in string.splitlines():  # Handle newlines in messages.
            yield from textwrap.wrap(
                line,
                width,
                expand_tabs=True,
            )

    @classmethod
    def render_messages(
        cls, console: tcod.Console, x: int, y: int, width: int, height: int, messages: Reversible[Message]
    ) -> None:
        """Отображает предоставленные сообщения.

`messages` отображаются, начиная с последнего сообщения и
в обратном порядке.
        """
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(list(cls.wrap(message.full_text, width))):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return  # Больше нет места для печати сообщений.
