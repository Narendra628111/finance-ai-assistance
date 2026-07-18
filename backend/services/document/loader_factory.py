"""
Document Loader Factory.

Creates the appropriate document loader based on the file extension.

Supports easy registration of new loaders without modifying existing code.
"""

from __future__ import annotations

from pathlib import Path
from typing import Type

from backend.services.document.base_loader import BaseDocumentLoader
from backend.services.document.docx_loader import DOCXLoader
from backend.services.document.image_loader import ImageLoader
from backend.services.document.pdf_loader import PDFLoader
from backend.services.document.txt_loader import TXTLoader


class LoaderFactory:
    """
    Factory class for creating document loaders.
    """

    _registry: dict[str, Type[BaseDocumentLoader]] = {
        ".pdf": PDFLoader,
        ".docx": DOCXLoader,
        ".txt": TXTLoader,
        ".png": ImageLoader,
        ".jpg": ImageLoader,
        ".jpeg": ImageLoader,
        ".webp": ImageLoader,
        ".bmp": ImageLoader,
        ".tif": ImageLoader,
        ".tiff": ImageLoader,
    }

    @classmethod
    def register_loader(
        cls,
        extensions: str | list[str] | tuple[str, ...],
        loader: Type[BaseDocumentLoader],
    ) -> None:
        """
        Register a loader for one or more file extensions.

        Args:
            extensions: File extension(s).
            loader: Loader implementation.
        """
        if isinstance(extensions, str):
            extensions = [extensions]

        for extension in extensions:
            cls._registry[extension.lower()] = loader

    @classmethod
    def unregister_loader(cls, extension: str) -> None:
        """
        Remove a registered loader.

        Args:
            extension: File extension.
        """
        cls._registry.pop(extension.lower(), None)

    @classmethod
    def get_loader(
        cls,
        file_path: str | Path,
    ) -> BaseDocumentLoader:
        """
        Create a loader instance for the given file.

        Args:
            file_path: Path to the document.

        Returns:
            Document loader instance.

        Raises:
            ValueError:
                If no loader exists for the file type.
        """
        path = Path(file_path)
        extension = path.suffix.lower()

        loader_class = cls._registry.get(extension)

        if loader_class is None:
            supported = ", ".join(sorted(cls.supported_extensions()))

            raise ValueError(
                f"Unsupported document type '{extension}'. "
                f"Supported types: {supported}"
            )

        return loader_class(path)

    @classmethod
    def supported_extensions(cls) -> list[str]:
        """
        Return all supported extensions.

        Returns:
            Sorted list of supported extensions.
        """
        return sorted(cls._registry.keys())

    @classmethod
    def is_supported(cls, file_path: str | Path) -> bool:
        """
        Check whether the file type is supported.

        Args:
            file_path: Path to the file.

        Returns:
            True if supported, else False.
        """
        return Path(file_path).suffix.lower() in cls._registry