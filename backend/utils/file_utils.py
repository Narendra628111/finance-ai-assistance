"""
Utility functions for file handling.
"""

from __future__ import annotations

import mimetypes
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class FileUtils:
    """
    Helper methods for uploaded files.
    """

    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

    ALLOWED_IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    ALLOWED_DOCUMENT_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
        ".csv",
        ".xlsx",
    }

    @staticmethod
    async def validate_upload(
        upload_file: UploadFile,
        allowed_extensions: set[str],
    ) -> None:
        """
        Validate uploaded file.
        """

        if not upload_file.filename:
            raise HTTPException(
                status_code=400,
                detail="Filename is missing.",
            )

        extension = Path(upload_file.filename).suffix.lower()

        if extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unsupported file type '{extension}'. "
                    f"Allowed types: {', '.join(sorted(allowed_extensions))}"
                ),
            )

        contents = await upload_file.read()

        if len(contents) > FileUtils.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=(
                    "File exceeds the maximum allowed size "
                    "of 20 MB."
                ),
            )

        # Reset pointer after validation
        upload_file.file.seek(0)

    @staticmethod
    def save_upload_file(
        upload_file: UploadFile,
        prefix: str = "",
    ) -> Path:
        """
        Save an uploaded file and return its path.
        """

        extension = Path(upload_file.filename).suffix.lower()

        unique_name = (
            f"{prefix}_{uuid4().hex}{extension}"
            if prefix
            else f"{uuid4().hex}{extension}"
        )

        file_path = UPLOAD_DIR / unique_name

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        return file_path

    @staticmethod
    def delete_file(
        file_path: Path,
    ) -> None:
        """
        Delete a file if it exists.
        """

        try:
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass

    @staticmethod
    def get_mime_type(
        file_path: Path,
    ) -> str:
        """
        Return MIME type based on file extension.
        """

        mime_type, _ = mimetypes.guess_type(file_path)

        return mime_type or "application/octet-stream"