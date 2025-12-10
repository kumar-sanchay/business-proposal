import logging
from typing import List
from langchain_core.runnables import Runnable, RunnablePassthrough, retry
from langchain_core.output_parsers import StrOutputParser
from langchain_community.docstore.document import Document

from proposal.prompts.data_preprocessing_prompts import executive_summary_ext_prompt
from proposal.core.llm import llm


logger = logging.getLogger(__name__)


class ExecutiveSectionChain(Runnable):

    def __get_relevance_chain(self):

        chain = ({
            "context": RunnablePassthrough()
            }
            | executive_summary_ext_prompt
            | llm
            | StrOutputParser()
        )

        chain_with_retry = retry.RunnableRetry(
            bound=chain,
            max_retries=5,
            wait=lambda attempt: 0.3 * attempt
        )

        return chain_with_retry

    def invoke(self, inputs, config=None):
        logger.info("Executive summary detection started")

        proposal_document: List[Document] = inputs["proposal_document"]
        
        executive_summary_keywords = ("About", "ABOUT", "Overview", "OVERVIEW", "Introduction", "INTRODUCTION",
                              "Summary", "SUMMARY", "Company", "COMPANY", "Executive","EXECUTIVE")
        
        chain = self.__get_relevance_chain()
        count = 0

        for doc_idx, document in enumerate(proposal_document):

            if document.metadata["page_num"] < 4 and any(key in document.page_content for key in executive_summary_keywords):
                
                if chain.invoke(document.page_content) == "YES":
                    proposal_document[doc_idx].metadata["section_type"] = "Executive Summary"
                    count += 1
        
        logger.info(f"Total document count identified as executive summary={count}")
        
        return {"proposal_document": proposal_document}