import os
import logging
import chromadb
from typing import List
from dotenv import load_dotenv
from langchain_community.docstore.document import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores.chroma import Chroma

from proposal.indexing.parser import ProposalParser
from proposal.core.logging_setup import setup_logging

load_dotenv()
setup_logging()

from proposal.indexing.sections.executive_summary import ExecutiveSummary
from proposal.indexing.sections.problem_statement import ProblemStatement
from proposal.indexing.sections.approach import Approach
from proposal.indexing.sections.deliverable import Deliverable
from proposal.indexing.sections.pricing_and_timeline import PricingAndTimeline
from proposal.core.embeddings import bge_embedding


logger = logging.getLogger(__name__)


def main():

    logger.info("Starting indexing of raw proposal pdfs")

    pdf_data_dir: str = "data/raw/proposals"
    pdf_files_path: List[str] = [os.path.join(pdf_data_dir, pdf_file_name) for pdf_file_name in os.listdir(pdf_data_dir)]

    logger.info(f"Total pfd files which will be processed: {len(pdf_files_path)}")

    documents: List[Document] = [
        doc
        for pdf_path in pdf_files_path
        for doc in ProposalParser.parse(pdf_path)
    ]

    logger.info(f"Total documents fetched from raw proposal pdfs: {len(documents)}")
    logger.debug(f"Document Data: {documents[:2]}")

    chain = (
            {"proposal_document": RunnablePassthrough()}
            | ExecutiveSummary()
            | ProblemStatement()
            | Approach()
            | Deliverable()
            | PricingAndTimeline()
        )

    documents = chain.invoke(documents)

    if 'proposal_document' in documents:
        documents = documents['proposal_document']
    

    for doc_idx, doc in enumerate(documents):
        if not doc.metadata.get('section_type', ''):
            documents[doc_idx].metadata['section_type'] = '<no_section>'


    chromadb_client = chromadb.Client()
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=bge_embedding,
        client=chromadb_client,
        collection_name=os.getenv('business_proposal_data'),
        persist_directory=os.getenv('chorma_vectorstore/')
    )
    vectorstore.persist()


if __name__ == '__main__':
    main()