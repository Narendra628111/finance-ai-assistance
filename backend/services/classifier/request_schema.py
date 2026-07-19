"""
Request schema for the Classifier Service.
"""

from pydantic import BaseModel, Field


class ClassificationRequest(BaseModel):
    """
    Request model for document classification.
    """

    summary: str = Field(
        ...,
        description="Summary of the document.",
    )

    entities: list[str] = Field(
        default_factory=list,
        description="Extracted entities.",
    )