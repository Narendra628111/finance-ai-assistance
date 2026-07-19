"""
Schemas for the Classifier Service.
"""

from pydantic import BaseModel, Field


class Category(BaseModel):
    """
    Represents a single classification category.
    """

    label: str = Field(
        ...,
        description="Category name.",
    )

    items: list[str] = Field(
        default_factory=list,
        description="Entities belonging to this category.",
    )


class ClassificationResponse(BaseModel):
    """
    Structured response returned by the classifier.
    """

    categories: list[Category] = Field(
        default_factory=list,
        description="List of classified categories.",
    )