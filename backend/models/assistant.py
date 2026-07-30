"""
Assistant request model.
"""

from __future__ import annotations

from pydantic import BaseModel


class AssistantResponse(BaseModel):

    success: bool

    answer: str

    sources: list[dict] = []