from langchain_core.runnables import Runnable, RunnablePassthrough, retry
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from proposal.core.llm import llm


class BaseRunnable(Runnable):

    def _get_relevance_chain(self, prompt: PromptTemplate):
        chain = (
            {
                'context': RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        chain_with_retry = retry.RunnableRetry(
            bound=chain,
            max_retries=5,
            wait=lambda: 60
        )

        return chain_with_retry

    def invoke(self, inputs, config=None):
        pass