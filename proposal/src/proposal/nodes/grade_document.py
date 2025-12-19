from typing import Dict, Any, List
from langchain_core.runnables import Runnable
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.docstore.document import Document

from proposal.core.graph_state import GraphState
from proposal.core.schemas import GradeDocuments
from proposal.chains import get_document_grading_chain


def get_grade_document_node(llm: BaseChatModel, proposal_section: str):
    def grade_document(state: GraphState) -> Dict[str, Any]:

        documents: List[Document] = state['documents']
        relevant_docs: List[Document] = []

        for doc in documents:
            score: GradeDocuments = get_document_grading_chain(llm).invoke({
                'document': doc,
                'requirement': state['user_requirement'],
                'section': proposal_section
            })

            if score.binary_score == 'yes':
                relevant_docs.append(doc)

        return {'documents': relevant_docs}

    return grade_document