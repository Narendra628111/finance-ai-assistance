"""
Pydantic models for the Extractor Agent.

These models are generic and can be reused for any document type.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ExtractionField(BaseModel):
    """
    Represents a single extracted field.
    """

    model_config = ConfigDict(extra="allow")

    name: str = Field(..., description="Field name")
    value: Any = Field(None, description="Extracted value")
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score",
    )
    source: str | None = Field(
        default=None,
        description="Source text used for extraction",
    )


class ExtractionResult(BaseModel):
    """
    Standard extraction response returned by the Extractor Agent.
    """

    model_config = ConfigDict(extra="allow")

    document_name: str

    document_type: str | None = None

    extracted_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    fields: dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted structured data",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Document metadata",
    )

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )


class ExtractionRequest(BaseModel):
    """
    Request model used by the Extractor Agent.
    """

    model_config = ConfigDict(extra="allow")

    document_text: str

    schema: dict[str, Any]

    instructions: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ExtractionResponse(BaseModel):
    """
    Response returned by the Extractor Agent.
    """

    success: bool

    message: str

    result: ExtractionResult | None = None

    errors: list[str] = Field(default_factory=list)