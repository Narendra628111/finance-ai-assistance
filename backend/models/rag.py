"""
Pydantic models for RAG APIs.
"""

from pydantic import BaseModel, Field


class BuildIndexRequest(BaseModel):
    """
    Request model for building the vector index.
    """

    rebuild: bool = Field(
        default=False,
        description="Rebuild the vector index.",
    )


class BuildIndexResponse(BaseModel):
    """
    Response model after indexing.
    """

    success: bool
    indexed_chunks: int
    message: str


class QueryRequest(BaseModel):
    """
    User query.
    """

    question: str = Field(
        ...,
        min_length=1,
    )


class SourceDocument(BaseModel):
    """
    Source document returned by RAG.
    """

    document: str
    page: int
    score: float


class QueryResponse(BaseModel):
    """
    Response from RAG.
    """

    answer: str
    sources: list[SourceDocument]