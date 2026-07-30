"""
Assistant API.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)

from backend.agents.workflow_agent import WorkflowAgent
from backend.core.dependencies import (
    get_workflow_agent,
)
from backend.models.assistant import (
    AssistantResponse,
)

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"],
)


@router.post(
    "/chat",
    response_model=AssistantResponse,
)
async def chat(
    question: str = Form(...),
    file: UploadFile | None = File(None),
    agent: WorkflowAgent = Depends(
        get_workflow_agent,
    ),
):
    """
    Main assistant endpoint.
    """

    input_type = "text"
    file_path = None

    if file:

        suffix = Path(
            file.filename,
        ).suffix.lower()

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        )

        temp.write(
            await file.read(),
        )

        temp.close()

        file_path = temp.name

        if suffix in {
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".webp",
        }:
            input_type = "image"

        else:
            input_type = suffix.replace(".", "")

    state = {
        "input_type": input_type,
        "user_query": question,
        "file_path": file_path,
    }

    result = await agent.run(
        state,
    )

    return AssistantResponse(
        success=True,
        answer=result.get(
            "final_answer",
            "",
        ),
        sources=result.get(
            "rag_sources",
            [],
        ),
    )