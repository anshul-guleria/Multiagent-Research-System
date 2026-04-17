from agents.reader_agent import build_reader_agent
from agents.search_agent import build_search_agent
from chains.chain import writer_chain, critic_chain
from rich import print

# from llm.groq_service import Groq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

#LANGCHAIN LCEL - Langchain expression language |-> |-> | 

def run_research_pipeline(topic: str) -> dict:
    state={}

    print("\n"+"="*50)
    print("Step 1 - Search agent working....")
    print("\n"+"="*50)


    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages":[('user',f"Find recent, reliable and detailed information about: {topic}")]
    })

    state["search_results"]=search_result['messages'][-1].content

    print("\nSearch result:", state['search_results'])

    print("\n"+"="*50)
    print("Step 2 - Reader agent working....")
    print("\n"+"="*50)

    reader_agent=build_reader_agent()
    reader_result=reader_agent.invoke({
        "messages": [
            ('user',f"Based on the following search results about '{topic}', pick the most relevant URL and scrape it for deeper content.\n\nSearch results:\n{state['search_results'][:800]}")
        ]
    })

    state['scraped_content']=reader_result['messages'][-1].content

    print("\nScraped result:", state['scraped_content'])

    print("\n"+"="*50)
    print("Step 3 - Writer agent working....")
    print("\n"+"="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])


    print("\n"+"="*50)
    print("Step 4 - Critic is reviewing the report...")
    print("\n"+"="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\nCritic report \n", state['feedback'])

    return state
