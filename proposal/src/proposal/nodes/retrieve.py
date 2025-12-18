from typing import Dict, Any, List
from langchain_core.runnables import Runnable
from langchain_community.docstore.document import Document

from proposal.core.graph_state import GraphState


def get_retriever_node(retriever: Runnable):
    def retriever_node(state: GraphState) -> Dict[str, Any]:
        
        problem_statement: str = state['user_requirement']['problem_statement']
        documents: List[Document] = retriever.invoke(problem_statement)
        return {'documents': documents}
    
    return retriever_node