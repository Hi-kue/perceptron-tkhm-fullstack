from time import sleep
from rich import print as rprint


def typrint(text: str, delay: float = 0.5) -> None:
    for char in text:
        rprint(char, end="", flush=True)
        sleep(delay)


def typrint_color(text: str, color: str, delay: float = 0.5) -> None:
    for char in text:
        rprint(char, end="", color=color, flush=True)
        sleep(delay)
