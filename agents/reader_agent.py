from langchain.agents import create_agent

# from tools.web_search_tool import web_search
from tools.scrape_tool import scrape_tool

from llm.groq_service import Groq

llm=Groq()

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_tool]
    )