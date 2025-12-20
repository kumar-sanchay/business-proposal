from typing import List, Dict, Any
from langchain_tavily import TavilySearch
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.docstore.document import Document

from proposal.core.graph_state import GraphState
from proposal.chains import get_client_search_queries
from proposal.core.schemas import DocumentSearchQuery


def get_websearch_client_node(llm: BaseChatModel, tavily: TavilySearch):
    def websearch_client_node(state: GraphState) -> Dict[str, Any]:

        client_name: str = state['user_requirement']['client_info']['client_name']
        client_industry: str = state['user_requirement']['client_info']['industry']

        if client_name or client_industry:
            search_query: DocumentSearchQuery = get_client_search_queries(llm).invoke(
                {
                    'client_name': client_name,
                    'client_industry': client_industry
                }
            )

            web_results: List[Any] = tavily.batch({'query': query} for query in search_query)
            doc_results: List[Document] = []

            for result in web_results:
                result = result['results']
                joined_results = '\n'.join(res['content'] for res in result)
                doc_results.append(Document(page_content=joined_results))

        return {
            'client_websearch': doc_results
        }
    return websearch_client_node