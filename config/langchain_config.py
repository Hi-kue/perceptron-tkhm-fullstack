# baselib
import os
import re

from dotenv import load_dotenv

# langchain 🦜⛓️
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.schema import AgentAction, AgentFinish


load_dotenv(dotenv_path=".env")

