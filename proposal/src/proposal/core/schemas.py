from typing import List
from pydantic import BaseModel, Field


class GradeDocuments(BaseModel):
    """
        Binary score for relevance check on retrieved documents
    """
    binary_score: str = Field("Documents are relevant to the question, 'yes' or 'no'")


class DocumentSearchQuery(BaseModel):
    """
        Queries which will help to websearch for getting the documents
    """
    search_queries: List[str] = Field("1-3 search queries list for researching")