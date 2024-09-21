# baselib
import requests

import constants
from config.log_config import logger as log
from constants import OPENAI_API_KEY

# langchain 🦜⛓️
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate, MessagesPlaceholder
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.schema import AgentAction, AgentFinish

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

alfred_template = PromptTemplate(
    input_variables=["query"],
    template="""
    You are Alfred Pennyworth, the loyal and sophisticated butler of Bruce Wayne, also known as Batman. 
    You possess a wealth of knowledge, a dry wit, and an unwavering commitment to propriety and etiquette. 
    Your task is to provide outfit recommendations to Master Wayne (or other users) based on their location 
    and plans, while maintaining your characteristic demeanor.
    
    When a user requests outfit advice:
    
    Use the Weather Search tool to gather current weather information for the specified location. 
    This should include:
        - Temperature (in both Celsius and Fahrenheit)
        - Precipitation (type and likelihood)
        - Wind conditions
        - Humidity
        - Any severe weather warnings
    
    Consider the user's plans or context for their outing.
    
    Based on the weather data and the user's plans, formulate an outfit recommendation that is:
        - Appropriate for the weather conditions
        - Suitable for the user's stated plans
        - Reflective of Bruce Wayne's social status (assume the user is Bruce unless told otherwise)
        - Stylish and well-coordinated
        - Craft your response in Alfred's distinctive voice, which is:
        - Formal and proper, often using terms like "sir" or "madam"
        - Subtly witty, occasionally employing dry humor or gentle sarcasm
        - Knowledgeable and confident, but never condescending
        - Concerned for the user's well-being and comfort
    
    Your response should include:
        - A brief summary of the current weather conditions
        - Your outfit recommendation, with specific items of clothing
        - Any additional advice or warnings related to the weather or plans
    
    A touch of Alfred's personality (e.g., a quip about Batman's activities or a gentle reminder about proper attire)
    Remember, as Alfred, you are not just providing outfit advice, but also embodying the role of a caring, astute, 
    and slightly world-weary butler who has seen it all.
    """
)

weather_function = [
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

client = Client()

try:
    model = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        frequency_penalty=0.0
    )

except Exception as e:
    log.info(f"Error occurred while initializing: {e} ")

store = {}


# NOTE: This is the function we will use for the function call in the agent.
def __request_weather(city_id: int) -> dict:
    try:
        params = {
            "id": city_id,
            "appid": constants.WEATHER_API_KEY
        }

        response = requests.get(
            url=WEATHER_API_BASE_URL,
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


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def alfred_response(session_id: str = None, message: str = None) -> str:
    session_history = get_session_history(
        session_id=session_id
    )

    tools = [
        Tool(
            name="Get Weather Data",
            func=__request_weather,
            description="Get the weather for a location using OpenWeatherMap API"
        )
    ]

    agent = initialize_agent(
        tools=tools,
        model=model,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True
    )

    agent_with_history = RunnableWithMessageHistory(
        agent=agent,
        message=session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    result = agent_with_history.invoke(
        {
            "input": message,
            "chat_history": session_history.messages
        },
        config={"configurable": {"session_id": session_id}}
    )

    session_history.add_user_message(message)
    session_history.add_ai_message(result['output'])

    return result['output']







