import logging
from typing import List
from langchain_community.docstore.document import Document

from proposal.indexing.sections.base_runnable import BaseRunnable
from proposal.prompts.data_preprocessing_prompts import problem_statement_ext_prompt


logger = logging.getLogger(__name__)


class ProblemStatement(BaseRunnable):

    def invoke(self, inputs, config=None):
        logger.info("Problem Statement detection started")

        documents: List[Document] = inputs["proposal_document"]

        chain = self._get_relevance_chain(problem_statement_ext_prompt)
        count = 0

        for doc_idx, doc in enumerate(documents):
            if not doc.metadata.get('section_type', '') and chain.invoke(doc.page_content) == 'YES':
                documents[doc_idx].metadata['section_type'] = 'Problem Statement'
                count += 1
        
        logger.info(f"Total document count identified as problem statement={count}")
        
        return {'proposal_document': documents}