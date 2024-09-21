# baselib
import sys

from config.log_config import logger as log
from filter.finder import load_city_json, find_city_id_wc, find_city_id_wcc

from rich.console import Console
from rich.prompt import Prompt

console = Console()


def run_simulation() -> None:
    console.print("[bold blue]Alfred AI[/bold blue]: Hello sir, I am Alfred, "
                  "your personal virtual assistant,"
                  "how can I help you today?")

    while True:
        user_input = Prompt.ask("[bold yellow]You[/bold blue]: ")

        if user_input.lower() in ["e", "exit", "quit", "q"]:
            console.print("[bold blue]Alfred AI[/bold blue]: Goodbye sir, shall we meet again.")
            sys.exit(0)


if __name__ == '__main__':
    # city_data = load_city_json("data/city_list.json")
    # city = "New York"
    # country = "US"
    # wcs_id = find_city_id_wcc(city, country, city_data)
    # wc_id = find_city_id_wc(city, city_data)
    #
    # log.info(f"City ID with state: {wcs_id}")
    # log.info(f"City ID without state: {wc_id}")
    pass
