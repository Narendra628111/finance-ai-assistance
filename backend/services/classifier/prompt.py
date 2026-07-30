"""
Prompt templates for the Classifier Service.
"""

SYSTEM_PROMPT = """
You are a banking document classifier.

Classify the given content.

Return ONLY valid JSON.

{
    "document_type": "...",
    "intent": "...",
    "confidence": 0.95
}
"""


def build_classifier_prompt(
    text: str,
) -> str:
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Content:\n\n{text}"
    )