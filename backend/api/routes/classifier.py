"""
Classifier API routes.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.agents.classifier.agent import ClassifierAgent
from backend.services.classifier.schemas import ClassificationResponse
from backend.services.classifier.request_schema import ClassificationRequest

router = APIRouter(
    prefix="/classify",
    tags=["Classifier"],
)

classifier = ClassifierAgent()


@router.post(
    "/",
    response_model=ClassificationResponse,
)
async def classify_document(
    request: ClassificationRequest,
) -> ClassificationResponse:
    """
    Classify extracted entities into categories.
    """

    return await classifier.classify(
        summary=request.summary,
        entities=request.entities,
    )