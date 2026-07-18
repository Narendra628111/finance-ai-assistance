"""
Extractor API routes.
"""

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, File, Form, UploadFile

from backend.agents.extractor_agent import ExtractorAgent
from backend.core.file_manager import FileManager

router = APIRouter(
    prefix="/extract",
    tags=["Extractor"],
)

extractor = ExtractorAgent()
file_manager = FileManager()


@router.post("/")
async def extract_document(
    file: UploadFile = File(...),
    schema: str = Form(...),
    instructions: str | None = Form(default=None),
) -> dict[str, Any]:
    """
    Extract structured information from an uploaded document.
    """

    schema_dict = json.loads(schema)

    file_path = await file_manager.save(file)

    try:
        result = await extractor.extract(
            file_path=file_path,
            schema=schema_dict,
            instructions=instructions,
        )

        return result.model_dump()

    finally:
        file_manager.delete(file_path)