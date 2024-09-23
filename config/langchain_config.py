# baselib
import requests

import constants
from config.log_config import logger as log
from constants import OPENAI_API_KEY

# langchain 🦜⛓️
from langsmith import Client
from langchain_openai import OpenAI, ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate, MessagesPlaceholder
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.schema import AgentAction, AgentFinish

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

alfred_template = PromptTemplate(
    input_variables=["query"],
    template=constants.ALFRED_SYSTEM_PROMPT
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
        tiktoken_model_name="gpt-4o",
        openai_api_key=OPENAI_API_KEY,
        frequency_penalty=0.5,  # range 0.0 to 1.0
    )
except Exception as e:
    log.info(f"Error occurred while initializing: {e} ")

store = {}


# NOTE: Implement this function in next commit.
def make_api_request(location: str) -> str:
    pass


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
            func=make_api_request,
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

# NOTE: future implementations will require langchain implementation but for now, its just normal OpenAI.
