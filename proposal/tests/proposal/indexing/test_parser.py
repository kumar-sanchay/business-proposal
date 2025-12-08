import os
import string
import random
from typing import List
from pathlib import Path
from reportlab.pdfgen import canvas
from langchain_community.docstore.document import Document

from proposal.indexing.parser import ProposalParser


def create_pdf_with_content(tmp_path: Path, content_sections: List[str]) -> str:
    pdf_name = ''.join(random.choices(string.ascii_lowercase, k=5)) + ".pdf"
    pdf_path = os.path.join(tmp_path, pdf_name)

    c = canvas.Canvas(str(pdf_path))
    c.setFont("Helvetica", 12)

    for section in content_sections:
        c.drawString(50, 800, section)
        c.showPage()

    c.save()
    return pdf_path


def test_proposal_parser_with_one_section(tmp_path):
    pdf_content: List[str] = ["First Section for testing"]
    pdf_path: str = create_pdf_with_content(tmp_path, pdf_content)

    documents: List[Document] = ProposalParser.parse(pdf_path)

    assert len(documents) == 1
    assert documents[0].page_content.strip() == "First Section for testing"



def test_proposal_parser_with_multiple_section(tmp_path):
    pdf_content: List[str] = ["First Section for testing", "Second Section for testing"]
    pdf_path: str = create_pdf_with_content(tmp_path, pdf_content)

    documents: List[Document] = ProposalParser.parse(pdf_path)

    assert len(documents) == 2
    assert documents[0].page_content.strip() == "First Section for testing"
    assert documents[1].page_content.strip() == "Second Section for testing"



def test_proposal_parser_with_empty_pdf(tmp_path):
    pdf_content: List[str] = []
    pdf_path: str = create_pdf_with_content(tmp_path, pdf_content)

    documents: List[Document] = ProposalParser.parse(pdf_path)

    assert len(documents) == 0


def test_proposal_parser_with_wrong_pdf_path():
    pdf_path: str = "fake.pdf"
    documents: List[Document] = ProposalParser.parse(pdf_path)
    
    assert len(documents) == 0