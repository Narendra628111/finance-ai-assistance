from pydantic import BaseModel, Field, ConfigDict


class SummaryResponse(BaseModel):
    """
    Structured response returned by the Summarizer Agent.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    summary: str = Field(
        ...,
        description="Concise summary of the document.",
        min_length=1,
    )

    key_points: list[str] = Field(
        default_factory=list,
        description="Important points extracted from the document.",
    )

    document_type: str = Field(
        ...,
        description="Predicted type of document.",
        min_length=1,
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )