import logging
from typing import List
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Title, ListItem, Table, Element

from proposal.preprocessing.constants import WEIGHTED_PROPOSAL_KEYWORDS, PROPOSAL_RELEVANCE_THRESHOLD


LOGGER = logging.getLogger(__name__)


class Stages:

    def run(self):
        raise NotImplementedError


class ProposalRelevanceCheck(Stages):

    """
    This stage evaluates the relevance of a proposal document based on the presence of key sections and overall structure.
    It assigns scores based on weighted keywords and structural elements like titles, lists, and tables.
    If the total score exceeds a predefined threshold, the document is considered relevant.
    """

    def __init__(self, elements: List[Element]) -> List[Element]:
        super().__init__()
        self.elements = elements
    
    def run(self):
        LOGGER.info("Starting Proposal Relevance Check")

        keyword_score, structure_score = 0

        full_text: str = " ".join(e.text.lower() for e in self.elements if e.text)

        LOGGER.info(f"Full text for relevance check length: {len(full_text)}")

        for keyword, weight in WEIGHTED_PROPOSAL_KEYWORDS:
            keyword_score += full_text.count(keyword) * weight
        
        LOGGER.info(f"Keyword score: {keyword_score}")

        title_count = sum(1 for e in self.elements if isinstance(e, Title))
        list_count = sum(1 for e in self.elements if isinstance(e, ListItem))
        table = sum(1 for e in self.elements if isinstance(e, Table))

        LOGGER.info(f"Title count: {title_count}, List count: {list_count}, Table count: {table}")

        if title_count > 5:
            structure_score += 3
        if list_count / max(len(self.elements), 1) > 0.2:  # Check if more than 20% are lists
            structure_score += 2
        if table > 0:
            structure_score += 2

        LOGGER.info(f"Structure score: {structure_score}")
        LOGGER.info(f"Total score: {keyword_score + structure_score}")
        LOGGER.info("Completed Proposal Relevance Check")
        return self.elements if (keyword_score + structure_score) > PROPOSAL_RELEVANCE_THRESHOLD else []