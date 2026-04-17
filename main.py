# from pipeline.pipeline import run_research_pipeline

from graph.builder import build_graph
from rich import print

topic=input("Enter a research topic: ")
# for langchain
# run_research_pipeline(topic)

#langgraph
graph=build_graph()
result=graph.invoke({
    "topic":topic
})

print("Output:",result)