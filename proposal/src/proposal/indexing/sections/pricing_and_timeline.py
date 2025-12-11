import logging
from typing import List
from langchain_community.docstore.document import Document

from proposal.indexing.sections.base_runnable import BaseRunnable
from proposal.prompts.data_preprocessing_prompts import pricing_and_timeline

logger = logging.getLogger(__name__)


class PricingAndTimeline(BaseRunnable):
    def invoke(self, inputs, config=None):
        logger.info("Pricing and Timeline detection started")

        documents: List[Document] = inputs["proposal_document"]

        chain = self._get_relevance_chain(pricing_and_timeline)

        count = 0
        for doc_id, document in enumerate(documents):

            if not document.metadata.get("section_type", "") and chain.invoke(document.page_content) == 'YES':
                documents[doc_id].metadata["section_type"] = "Pricing and Timeline"
                count += 1
        
        logger.info(f"Total document count identified as pricing and timeline={count}")
        
        return {"proposal_documents": documents}