"""
TXT document loader.

Supports:
- UTF-8 encoded text files
- Automatic encoding fallback
"""

from __future__ import annotations

from pathlib import Path

from backend.services.document.base_loader import BaseDocumentLoader
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class TXTLoader(BaseDocumentLoader):
    """
    Loader for plain text (.txt) documents.
    """

    SUPPORTED_ENCODINGS = (
        "utf-8",
        "utf-8-sig",
        "utf-16",
        "latin-1",
        "cp1252",
    )

    def __init__(self, file_path: str | Path) -> None:
        super().__init__(file_path)

    async def load(self) -> str:
        """
        Extract text from a TXT document.

        Returns:
            Extracted text.

        Raises:
            UnicodeDecodeError:
                If none of the supported encodings work.
        """
        self.validate()

        logger.info("Reading TXT: %s", self.file_path)

        last_exception: Exception | None = None

        for encoding in self.SUPPORTED_ENCODINGS:
            try:
                with self.file_path.open(
                    mode="r",
                    encoding=encoding,
                ) as file:
                    text = file.read().strip()

                logger.info(
                    "Successfully extracted %d characters from '%s' using '%s' encoding.",
                    len(text),
                    self.filename,
                    encoding,
                )

                return text

            except UnicodeDecodeError as exc:
                last_exception = exc
                continue

            except Exception:
                logger.exception(
                    "Failed while reading '%s'.",
                    self.filename,
                )
                raise

        logger.error(
            "Unable to decode '%s' using supported encodings.",
            self.filename,
        )

        if last_exception:
            raise last_exception

        raise UnicodeDecodeError(
            "utf-8",
            b"",
            0,
            1,
            "Unable to decode text file.",
        )

    def document_metadata(self) -> dict:
        """
        Return TXT metadata.

        Returns:
            Metadata dictionary.
        """
        return super().metadata()