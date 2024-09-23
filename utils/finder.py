# baselib
import json

from fuzzywuzzy import fuzz
from config.log_config import logger as log


def load_city_json(file_path: str) -> dict:
    log.info(f"Loading JSON file from path: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_city_id_wcc(city: str, country: str, city_data=None) -> int | None:
    if country is None or "":
        return find_city_id_wc(city, city_data)

    log.info(f"Finding city name with state that matches: {city} in {country}")
    city_list = []

    for city_obj in city_data:
        if fuzz.ratio(city_obj["name"].lower(), city.lower()) > 97 and \
                fuzz.ratio(city_obj["country"].lower(), country.lower()) > 97:
            log.info(f"Found city: {city_obj['name']} with id [{city_obj["id"]}] state: {city_obj["state"]}")
            log.info(city)
            city_list.append(city_obj)

    return city_list[0]["id"] if city_list else None


def find_city_id_wc(city: str, city_data) -> int | None:
    if city in ["", None] and city_data is None:
        return None

    log.info(f"Finding city name that matches query: {city}")
    city_list = []

    for city_obj in city_data:
        if fuzz.ratio(city_obj["name"].lower(), city.lower()) > 97:
            log.info(f"Found city: {city_obj["name"]} with id [{city_obj["id"]}] state {city_obj["state"]}")
            log.info(city)
            city_list.append(city_obj)

    return city_list[0]["id"] if city_list else None
