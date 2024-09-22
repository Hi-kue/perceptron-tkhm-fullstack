# baselib
import sys

from config.ai_config import send_request
from filter.finder import load_city_json, find_city_id_wc, find_city_id_wcc
from filter.typing import typrint_color

from rich.console import Console
from rich.prompt import Prompt

console = Console()


def run_simulation() -> None:
    console.print("[bold blue]Alfred AI[/bold blue]: Hello sir, I am Alfred, "
                  "your personal virtual assistant,"
                  "how can I help you today?")

    while True:
        user_input = Prompt.ask("[bold yellow]You[/bold yellow] ")

        if user_input.lower() in ["e", "exit", "quit", "q"]:
            console.print("[bold blue]Alfred AI[/bold blue]: Goodbye sir, shall we meet again.")
            sys.exit(0)

        typrint_color(
            pre_text="[bold blue]Alfred AI[/bold blue]: ",
            text=send_request(user_content=user_input),
            color="bold blue",
            delay=0.035
        )


if __name__ == '__main__':
    run_simulation()
