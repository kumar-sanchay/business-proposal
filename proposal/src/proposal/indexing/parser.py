import re
import logging
from typing import List
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from langchain_community.docstore.document import Document


logger = logging.getLogger(__name__)


class ProposalParser:

    @staticmethod
    def parse(pdf_path: str) -> List[Document]:

        logger.info(f"Extracting data for pdf: {pdf_path}")

        page_number: int = 1
        documents: List[Document] = []

        try:
            pdf_reader: PdfReader = PdfReader(pdf_path)
            for page in pdf_reader.pages:
                text: str = page.extract_text()
                sections: List[str] = re.split(r'\n{2,}', text)

                for sec in sections:
                    if sec:
                        documents.append(Document(page_content=sec, metadata={'page_num': page_number}))
                
                page_number += 1
    
        except (PdfReadError, FileNotFoundError) as e:
            logger.exception(f"PDF extraction failed for pdf : {pdf_path} with exception: {e}")
            
        logger.info(f"Extraction completed with total pages: {page_number} and documents: {len(documents)}")
        
        return documents