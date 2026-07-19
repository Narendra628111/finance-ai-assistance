class ClassificationError(Exception):
    """Raised when document classification fails."""


class InvalidClassificationError(ClassificationError):
    """Raised when the LLM returns an invalid classification."""