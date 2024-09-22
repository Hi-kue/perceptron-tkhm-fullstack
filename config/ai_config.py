# baselib
import os
import sys
import time
import requests

import constants
from config.log_config import logger as log
from openai import OpenAI, OpenAIError, APIConnectionError


# NOTE: Function Call for Weather API\
weather_funcdef = [
    {
        "name": "get_location_weather",
        "description": "Get the weather for a location using OpenWeatherMAp API through a function call.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The users location to get current weather for."
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    }
]


def openai_connect():
    try:
        start_time = time.time()
        openai = OpenAI(
            api_key=constants.OPENAI_API_KEY,
        )
        log.info(f"Connected to OpenAI in {time.time() - start_time} seconds.")
        return openai

    except APIConnectionError as e:
        log.error(f"An error occurred while connecting to OpenAI: {e}")
        sys.exit(1)

    except OpenAIError as e:
        log.error(f"An error occurred while connecting to OpenAI: {e}")
        sys.exit(1)


def make_api_request(city_id: int) -> dict:
    try:
        params = {
            "id": city_id,
            "appid": constants.WEATHER_API_KEY
        }

        response = requests.get(
            url=constants.WEATHER_API_BASE_URL,
            params=params
        )

        if response.status_code == 200:
            weather_fmt = {
                "weather": {
                    "main": response.json()["weather"][0]["main"],
                    "description": response.json()["weather"][0]["description"]
                },
                "temperature_details": {
                    "temp": response.json()["main"]["temp"],
                    "feels_like": response.json()["main"]["feels_like"],
                    "humidity": response.json()["main"]["humidity"],
                    "wind": {
                        "speed": response.json()["wind"]["speed"]
                    }
                },
            }
            return weather_fmt

    except Exception as e:
        log.error(f"Error occurred while requesting weather: {e}")
        return {}


def send_request(user_content: str, wcs_id: int = None) -> str | None:
    tools = [
        {
            "type": "function",
            "function":  {
                "name": "make_api_request",
                "description": "Get the weather for a location using OpenWeatherMap API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_id": {
                            "type": "integer",
                            "description": "The city id to get the weather for."
                        },
                        "required": ["city_id"],
                        "additionalProperties": False
                    }
                }
            }
        }
    ]

    try:
        start_time = time.time()
        openai = openai_connect()

        if wcs_id is not None and "weather" in user_content.lower():  # TODO: Fix This.
            response = openai.chat.completions.create(
                model=constants.OPENAI_API_MODEL,
                messages=[
                    {"role": "system", "content": constants.ALFRED_SYSTEM_PROMPT},
                    {"role": "function", "content": weather_funcdef},
                    {"role": "user", "content": user_content}
                ],
                tools=tools,
                functions=weather_funcdef,
                function_call="auto"
            )
        else:
            response = openai.chat.completions.create(
                model=constants.OPENAI_API_MODEL,
                messages=[
                    {"role": "system", "content": constants.ALFRED_SYSTEM_PROMPT},
                    {"role": "user", "content": user_content}
                ],
            )

        log.info(f"Response: {response}")
        log.info(f"Response time: {time.time() - start_time} seconds.")

        if response.choices:
            return response.choices[0].message.content

        else:
            return None

    except Exception as e:
        log.info(f"Error found from response sent: {e}")
