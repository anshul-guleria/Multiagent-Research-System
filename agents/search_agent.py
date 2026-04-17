from langchain.agents import create_agent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools.web_search_tool import web_search
from tools.scrape_tool import scrape_tool

from llm.groq_service import Groq

llm=Groq()

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )