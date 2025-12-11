import logging
from typing import List
from langchain_community.docstore.document import Document

from proposal.indexing.sections.base_runnable import BaseRunnable
from proposal.prompts.data_preprocessing_prompts import deliverable_ext_prompt


logger = logging.getLogger(__name__)


class Deliverable(BaseRunnable):
    
    def invoke(self, inputs, config=None):
        logger.info("Deliverable detection started")

        documents: List[Document] = inputs["proposal_document"]

        chain = self._get_relevance_chain(deliverable_ext_prompt)

        count = 0

        for doc_id, document in enumerate(documents):
            if not document.metadata.get('section_type', '') and chain.invoke(document.page_content) == 'YES':
                documents[doc_id].metadata['section_type'] = 'Deliverable'
                count += 1
        
        logger.info(f"Total document count identified as deliverable={count}")

        return {"proposal_document": documents}
