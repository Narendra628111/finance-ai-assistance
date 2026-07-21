"""
Vision API routes.
"""

from __future__ import annotations

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from backend.agents.vision_agent import VisionAgent
from backend.models.vision_models import VisionResponse
from backend.utils.file_utils import FileUtils

router = APIRouter(
    prefix="/vision",
    tags=["Vision"],
)

vision_agent = VisionAgent()


@router.post(
    "/analyze",
    response_model=VisionResponse,
)
async def analyze_image(
    image: UploadFile = File(...),
    prompt: str = Form("Describe this image in detail."),
) -> VisionResponse:
    """
    Analyze an uploaded image.
    """

    file_path = None

    try:
        await FileUtils.validate_upload(
            image,
            FileUtils.ALLOWED_IMAGE_EXTENSIONS,
        )

        file_path = FileUtils.save_upload_file(
            image,
            prefix="vision",
        )

        return await vision_agent.analyze(
            image_path=file_path,
            prompt=prompt,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    finally:
        if file_path:
            FileUtils.delete_file(file_path)