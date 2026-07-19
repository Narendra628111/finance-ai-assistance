"""
Custom exceptions for the Summarizer Agent.
"""


class SummarizationError(Exception):
    """Raised when the summarization process fails."""

    def __init__(self, message: str = "Failed to summarize the document."):
        super().__init__(message)


class InvalidSummaryError(Exception):
    """Raised when the LLM returns an invalid summary response."""

    def __init__(self, message: str = "Invalid summary response received from the LLM."):
        super().__init__(message)