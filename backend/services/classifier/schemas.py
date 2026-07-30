"""
Schemas for the Classifier Service.
"""

from pydantic import BaseModel, Field


class ClassificationResponse(BaseModel):
    """
    Structured response returned by the Classifier Agent.
    """

    document_type: str = Field(
        ...,
        description="Detected document type.",
    )

    intent: str = Field(
        ...,
        description="Predicted user/document intent.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )