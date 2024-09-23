from time import sleep
from rich.console import Console

console = Console()


def typrint(text: str, delay: float = 0.05) -> None:
    for char in text:
        console.print(char, end="", new_line_start=False)
        sleep(delay)


def typrint_color(text: str, pre_text: str, color: str, delay: float = 0.05) -> None:
    if pre_text:
        console.print(pre_text, style=color, end="", new_line_start=False)

    for char in text:
        console.print(char, end="", new_line_start=False)
        sleep(delay)
    console.print()
