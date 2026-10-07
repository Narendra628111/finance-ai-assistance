"""
Document Loader Factory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Type

from backend.services.document.base_loader import BaseDocumentLoader
from backend.services.document.docling_loader import DoclingLoader
from backend.services.document.txt_loader import TXTLoader

class LoaderFactory:
    """
    Creates document loaders based on file extension.
    """

    _registry: dict[str, Type[BaseDocumentLoader]] = {
        ".pdf": DoclingLoader,
        ".docx": DoclingLoader,

        ".png": DoclingLoader,
        ".jpg": DoclingLoader,
        ".jpeg": DoclingLoader,
        ".webp": DoclingLoader,
        ".bmp": DoclingLoader,
        ".tif": DoclingLoader,
        ".tiff": DoclingLoader,

        ".txt": TXTLoader,
    }

    @classmethod
    def register_loader(
        cls,
        extensions: str | list[str] | tuple[str, ...],
        loader: Type[BaseDocumentLoader],
    ) -> None:

        if isinstance(extensions, str):
            extensions = [extensions]

        for extension in extensions:
            cls._registry[extension.lower()] = loader

    @classmethod
    def get_loader(
        cls,
        file_path: str | Path,
    ) -> BaseDocumentLoader:

        path = Path(file_path)
        extension = path.suffix.lower()

        loader_class = cls._registry.get(extension)

        if loader_class is None:
            supported = ", ".join(
                sorted(cls._registry.keys())
            )

            raise ValueError(
                f"Unsupported document type '{extension}'. "
                f"Supported types: {supported}"
            )

        return loader_class(path)

    @classmethod
    def supported_extensions(cls) -> list[str]:
        return sorted(cls._registry.keys())

    @classmethod
    def is_supported(
        cls,
        file_path: str | Path,
    ) -> bool:
        return (
            Path(file_path).suffix.lower()
            in cls._registry
        )