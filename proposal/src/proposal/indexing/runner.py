import os
import logging
from typing import List
from dotenv import load_dotenv
from langchain_community.docstore.document import Document
from langchain_core.runnables import RunnablePassthrough

from proposal.indexing.parser import ProposalParser
from proposal.core.logging_setup import setup_logging

load_dotenv()
setup_logging()
from proposal.indexing.sections.executive_section import ExecutiveSectionChain


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
            | ExecutiveSectionChain()
    )

    documents = chain.invoke(documents)


if __name__ == '__main__':
    main()