from typing import TypedDict

class AgentState(TypedDict):
    topic: str
    search_results: str
    scraped_content: str
    report: str
    feedback: str
