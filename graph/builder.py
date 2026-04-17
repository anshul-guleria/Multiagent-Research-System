from langgraph.graph import StateGraph, END
from schema.agent_state import AgentState
from agents.reader_agent import build_reader_agent
from agents.search_agent import build_search_agent
from chains.chain import writer_chain, critic_chain


def search_node(state: AgentState):
    search_agent=build_search_agent()
    result=search_agent.invoke({
        "messages":[('user',f"Find recent, reliable and detailed information about: {state['topic']}")]})
    state["search_results"] = result["messages"][-1].content
    # print("\n[Search Done]\n", state["search_results"])
    return state

def reader_node(state: AgentState):
    reader_agent = build_reader_agent()

    result = reader_agent.invoke({
        "messages": [
            ("user",
             f"Pick best URL and scrape content:\n\n{state['search_results'][:800]}")
        ]
    })

    state["scraped_content"] = result["messages"][-1].content
    # print("\n[Reader Done]\n", state["scraped_content"])
    return state

def writer_node(state: AgentState):
    research = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": state["topic"],
        "research": research
    })

    # print("\n[Writer Done]\n", state["report"])
    return state

def critic_node(state: AgentState):
    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    # print("\n[Critic Done]\n", state["feedback"])
    return state

def build_graph():
    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("search", search_node)
    builder.add_node("reader", reader_node)
    builder.add_node("writer", writer_node)
    builder.add_node("critic", critic_node)

    # Starting point
    builder.set_entry_point("search")

    builder.add_edge("search", "reader")
    builder.add_edge("reader", "writer")
    builder.add_edge("writer", "critic")
    builder.add_edge("critic", END)

    return builder.compile()