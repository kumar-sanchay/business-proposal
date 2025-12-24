import pytest
from langchain_core.runnables import RunnableSequence

from tests.proposal.helpers.fake_llm import FakeChatLLM
from proposal.core.schemas import DocumentSearchQuery
from proposal.chains import get_client_search_queries


@pytest.fixture
def llm():
    return FakeChatLLM(DocumentSearchQuery(search_queries=['test_query_1', 'test_query_2']))


def test_get_client_search_queries_returns_runnable(llm):
    chain = get_client_search_queries(llm)
    assert isinstance(chain, RunnableSequence)


def test_structured_output_is_getting_attached(llm):
    assert llm.structured_schema is None
    chain = get_client_search_queries(llm)
    assert llm.structured_schema is DocumentSearchQuery