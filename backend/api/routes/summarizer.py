"""
Summarizer API routes.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.agents.summarizer_agent import SummarizerAgent
from backend.services.summarizer.request_schema import SummaryRequest

router = APIRouter(
    prefix="/summarize",
    tags=["Summarizer"],
)

summarizer = SummarizerAgent()


@router.post("/")
async def summarize_document(
    request: SummaryRequest,
):
    """
    Generate a structured summary.
    """

    result = await summarizer.summarize(
        text=request.text,
    )

    return result.model_dump()