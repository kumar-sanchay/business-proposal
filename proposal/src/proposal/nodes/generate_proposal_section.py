from typing import List, Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel

from proposal.core.graph_state import GraphState
from proposal.chains import generate_proposal_section


def format_docs(docs: List[str]):
    return "\n".join(docs)


def get_generate_proposal_section_node(llm: BaseChatModel, proposal_section: str):
    def generate_proposal_section_node(state: GraphState) -> Dict[str, Any]:

        generate_section: str = generate_proposal_section(llm).invoke(
            {
                'section': section,
                'problem_statement': state['user_requirement']['problem_statement'],
                'proposal_goal': state['user_requirement']['proposal_goal'],
                'approach': state['user_requirement']['approach'],
                'timeline': state['user_requirement']['timeline'],
                'scope_exclusions': state['user_requirement']['scope_exclusions'],
                'budget_range': state['user_requirement']['budget_range'],
                'technical_depth': state['user_requirement']['technical_depth'],
                'client_name': state['user_requirement']['client_info']['client_name'],
                'industry': state['user_requirement']['client_info']['industry'],
                'documents': format_docs(state['documents']),
                'client_websearch': format_docs(state['client_websearch'])
            }
        )

        return {
            'generated_section': generate_section
        }
    return generate_proposal_section_node