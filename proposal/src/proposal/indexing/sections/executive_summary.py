import logging
from typing import List
from langchain_community.docstore.document import Document

from proposal.indexing.sections.base_runnable import BaseRunnable
from proposal.prompts.data_preprocessing_prompts import executive_summary_ext_prompt
from proposal.core.llm import llm


logger = logging.getLogger(__name__)


class ExecutiveSummary(BaseRunnable):

    def invoke(self, inputs, config=None):
        logger.info("Executive summary detection started")

        documents: List[Document] = inputs["proposal_document"]
        
        executive_summary_keywords = ("About", "ABOUT", "Overview", "OVERVIEW", "Introduction", "INTRODUCTION",
                              "Summary", "SUMMARY", "Company", "COMPANY", "Executive","EXECUTIVE")
        
        chain = self._get_relevance_chain(executive_summary_ext_prompt)
        count = 0

        for doc_idx, document in enumerate(documents):

            if document.metadata["page_num"] < 4 and any(key in document.page_content for key in executive_summary_keywords):
                
                if chain.invoke(document.page_content) == "YES":
                    documents[doc_idx].metadata["section_type"] = "Executive Summary"
                    count += 1
        
        logger.info(f"Total document count identified as executive summary={count}")
        
        return {"proposal_document": documents}