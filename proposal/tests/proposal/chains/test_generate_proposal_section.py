import pytest
from langchain_core.runnables import RunnableSequence

from tests.proposal.helpers.fake_llm import FakeChatLLM
from proposal.chains import generate_proposal_section


@pytest.fixture
def llm():
    return FakeChatLLM()


def test_generate_proposal_section_returns_runnable(llm):
    chain = generate_proposal_section(llm)
    assert isinstance(chain, RunnableSequence)


def test_structured_output_is_getting_attached(llm):
    assert llm.structured_schema is None
    chain = generate_proposal_section(llm)
    # Not using structured output here
    assert llm.structured_schema is None