from typing import List
from langchain_tavily import TavilySearch
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode

from proposal.core.schemas import DocumentSearchQuery


def run_quries(search_queries: List[str]):
    """Run the queries"""
    tavily = TavilySearch(max_results=5)
    return tavily.batch({"query": query for query in search_queries})


execute_tools = ToolNode(
    [
        StructuredTool.from_function(run_quries, name=DocumentSearchQuery.__name__)
    ]
)