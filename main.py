# baselib
import sys

from config.ai_config import send_request
from filter.finder import load_city_json, find_city_id_wc, find_city_id_wcc

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

        if "weather" in user_input.lower():
            city = Prompt.ask("[bold yellow]City Name: ")
            country = Prompt.ask("[bold yellow]Country Code (i.e, US, CA, ...): ")

            city_data = load_city_json("data/city_list.json")
            wcs_id = find_city_id_wcc(city, country, city_data)

            send_request(
                user_content=user_input,
                wcs_id=wcs_id
            )

        console.print(f"[bold blue]Alfred AI[/bold blue]: {send_request(user_input, wcs_id=None)}")


if __name__ == '__main__':
    run_simulation()
