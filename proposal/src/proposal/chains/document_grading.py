from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence

from proposal.core.schemas import GradeDocuments


def get_document_grading_chain(llm: BaseChatModel) -> str:

    system_prompt = """
    You are a strict grader assessing relevance of a retrieved document to a user's requirement. \n
    Since we have to generate consulting proposal's section as give below you have to grade
    based on whether these documents are helpful for this particular section.
    If the document is a valid example of consulting proposal section, grade it as relevant. \n
    Strictly give only binary score 'yes' or 'no' score to indicate whether the document is relevant to the requirement.
    """

    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name='messages'),
            ("human", "Retrieved Document: {document}\n\nUser's requirement: {requirement}\n\nProposal section: {section}")
        ]
    )

    return grade_prompt | llm | StrOutputParser()