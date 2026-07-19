"""
Prompt templates for the Classifier Service.
"""

import json


SYSTEM_PROMPT = """
You are an expert AI document classifier.

Your task is to classify the extracted entities into meaningful categories.

Rules:
- Use ONLY the provided entities.
- Do NOT invent new entities.
- Group similar entities together.
- Use clear category names.
- If an entity does not fit a category, place it under "Other".
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT explain your reasoning.

Return the response in the following format:

{
    "categories": [
        {
            "label": "Programming Language",
            "items": [
                "Python",
                "Java"
            ]
        }
    ]
}
"""


def build_classifier_prompt(
    summary: str,
    entities: list[str],
) -> str:
    """
    Build the prompt for the classifier model.

    Args:
        summary: Document summary.
        entities: Extracted entities.

    Returns:
        Prompt string.
    """

    payload = {
        "summary": summary,
        "entities": entities,
    }

    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Input:\n"
        f"{json.dumps(payload, indent=2)}"
    )