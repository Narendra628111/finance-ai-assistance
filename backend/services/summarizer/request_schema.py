from pydantic import BaseModel, Field


class SummaryRequest(BaseModel):
    """
    Request body for document summarization.
    """

    text: str = Field(
        ...,
        min_length=1,
        description="Extracted document text.",
    )