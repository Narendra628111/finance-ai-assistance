"""
Custom exception hierarchy for the AI Assistant.
"""

from __future__ import annotations


class AIAssistantError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str = "An unexpected error occurred.") -> None:
        self.message = message
        super().__init__(self.message)


# ==========================
# Configuration Exceptions
# ==========================

class ConfigurationError(AIAssistantError):
    """Raised when application configuration is invalid."""


# ==========================
# Document Exceptions
# ==========================

class DocumentError(AIAssistantError):
    """Base document exception."""


class UnsupportedFileTypeError(DocumentError):
    """Raised for unsupported document types."""


class FileTooLargeError(DocumentError):
    """Raised when uploaded file exceeds the allowed size."""


class EmptyDocumentError(DocumentError):
    """Raised when a document contains no readable content."""


class DocumentLoadError(DocumentError):
    """Raised when document loading fails."""


# ==========================
# LLM Exceptions
# ==========================

class LLMError(AIAssistantError):
    """Base LLM exception."""


class LLMConnectionError(LLMError):
    """Raised when connection to the LLM fails."""


class LLMResponseError(LLMError):
    """Raised when the LLM returns an invalid response."""


class PromptGenerationError(LLMError):
    """Raised when prompt generation fails."""


# ==========================
# Extraction Exceptions
# ==========================

class ExtractionError(AIAssistantError):
    """Raised when structured extraction fails."""


class ResponseParsingError(ExtractionError):
    """Raised when parsing the LLM response fails."""


# ==========================
# Validation Exceptions
# ==========================

class ValidationError(AIAssistantError):
    """Raised for invalid input data."""


# ==========================
# Authentication Exceptions
# ==========================

class AuthenticationError(AIAssistantError):
    """Raised when authentication fails."""


class AuthorizationError(AIAssistantError):
    """Raised when user lacks required permissions."""


# ==========================
# Database Exceptions
# ==========================

class DatabaseError(AIAssistantError):
    """Raised for database-related failures."""


class RecordNotFoundError(DatabaseError):
    """Raised when a database record is not found."""