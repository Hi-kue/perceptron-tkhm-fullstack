# baselib
import sys
import time
import json
from typing import Any

import requests

import constants
from config.log_config import logger as log
from openai import OpenAI, OpenAIError, APIConnectionError
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam

# NOTE: Function Call for Weather API
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


def make_api_request(city_id: int) -> str | dict[Any, Any]:
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
            return json.dumps(weather_fmt, indent=4)

    except Exception as e:
        log.error(f"Error occurred while requesting weather: {e}")
        return {}


def send_request(user_content: str, wcs_id: int = None) -> str | None:
    tool = [
        ChatCompletionToolParam(
            type="function",
            function={
                "name": "make_api_request",
                "description": "Get the weather for a location using OpenWeatherMap API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_id": {
                            "type": "integer",
                            "description": "The city id to get the weather for."
                        }
                    },
                    "required": ["city_id"]
                }
            }
        )
    ]
    response_unpacked = []

    try:
        start_time = time.time()
        openai = openai_connect()

        messages = [
            {"role": "system", "content": constants.ALFRED_SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]

        response = openai.chat.completions.create(
            model=constants.OPENAI_API_MODEL,
            messages=messages,
            tools=tool,
            tool_choice="auto"
        )

        log.info(f"Response: {response}")

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)

            for tc in tool_calls:
                log.info(f"Function: {tc.function.name}")
                log.info(f"Params/Arguments: {tc.function.arguments}")

                function_name = tc.function.name
                function_to_call = globals().get(function_name)

                function_args = json.loads(tc.function.arguments)
                wcs_id = function_args.get("city_id")

                if wcs_id:
                    function_response = function_to_call(wcs_id)
                    log.info(f"Function Response: {function_response}")

                    messages.append({
                        "tool_call_id": tc.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response
                    })

                else:
                    log.info("city_id not found in function arguments.")

        final_response = openai.chat.completions.create(
            model=constants.OPENAI_API_MODEL,
            messages=messages,
            stream=True
        )

        log.info(f"Response: {final_response}")
        log.info(f"Response time: {time.time() - start_time} seconds.")

        for chunk in final_response:
            if chunk.choices[0].delta.content not in [None, ""]:
                response_unpacked.append(chunk.choices[0].delta.content)

        return "".join(response_unpacked)

    except Exception as e:
        log.info(f"Error found from response sent: {e}")
