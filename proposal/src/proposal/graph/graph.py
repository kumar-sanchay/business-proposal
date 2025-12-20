from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph, END
from langchain_tavily import TavilySearch

from proposal.core.graph_state import GraphState
from proposal.graph import constants
from proposal.nodes import (get_generate_proposal_section_node, get_retriever_node, get_grade_document_node,
                            get_websearch_client_node, get_websearch_document_node)

from proposal.core.llm import get_llm
from proposal.indexing.retriever import get_retriever


def build_graph():
    llm = get_llm()
    tavily_search = TavilySearch(max_results=2)
    retriever = get_retriever()

    proposal_section = "Executive Summary"

    graph = StateGraph(GraphState)
    graph.add_node(constants.RETRIEVE, get_retriever_node(retriever=retriever))
    graph.add_node(constants.GRADE_DOCUMENTS, get_grade_document_node(llm=llm, proposal_section=proposal_section))
    graph.add_node(constants.WEBSEARCH_DOCUMENT, get_websearch_document_node(llm=llm, proposal_section=proposal_section,
                                                                              tavily=tavily_search))
    graph.add_node(constants.WEBSEARCH_CLIENT, get_websearch_client_node(llm=llm, tavily=tavily_search))
    graph.add_node(constants.GENERATE, get_generate_proposal_section_node(llm=llm, proposal_section=proposal_section))

    graph.set_entry_point(constants.RETRIEVE)
    graph.add_edge(constants.RETRIEVE, constants.GRADE_DOCUMENTS)

    def web_search_document_condition(state: GraphState):

        if len(state['documents']) >= 3:
            return constants.WEBSEARCH_CLIENT
        return constants.WEBSEARCH_DOCUMENT
    
    graph.add_conditional_edges(constants.GRADE_DOCUMENTS,
                                web_search_document_condition,
                                {
                                    constants.WEBSEARCH_CLIENT: constants.WEBSEARCH_CLIENT,
                                    constants.WEBSEARCH_DOCUMENT: constants.WEBSEARCH_DOCUMENT
                                }
        )
    
    graph.add_edge(constants.WEBSEARCH_DOCUMENT, constants.GRADE_DOCUMENTS)
    graph.add_edge(constants.WEBSEARCH_CLIENT, constants.GENERATE)
    graph.add_edge(constants.GENERATE, END)

    app = graph.compile()
    app.get_graph().draw_mermaid_png(output_file_path="test_graph.png")


if __name__ == '__main__':
    build_graph()