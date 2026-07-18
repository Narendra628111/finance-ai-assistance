"""
Prompt templates for the Extractor Agent.
"""

from __future__ import annotations

import json
from typing import Any


class ExtractionPrompt:
    """
    Builds prompts for structured document extraction.
    """

    SYSTEM_PROMPT = """
You are an expert AI Document Extraction Assistant.

Your responsibilities:

- Analyze the given document.
- Extract information according to the provided schema.
- Return ONLY valid JSON.
- Never include explanations.
- Never use markdown.
- Never wrap JSON inside code blocks.
- If a field is unavailable, return null.
- Preserve lists where appropriate.
- Do not hallucinate information.
"""

    @classmethod
    def build(
        cls,
        document_text: str,
        schema: dict[str, Any],
        instructions: str | None = None,
    ) -> str:
        """
        Build an extraction prompt.

        Args:
            document_text: Extracted document text.
            schema: JSON schema describing expected output.
            instructions: Optional extraction instructions.

        Returns:
            Prompt string.
        """

        schema_json = json.dumps(schema, indent=4)

        custom_instructions = instructions or (
            "Extract every field defined in the schema."
        )

        return f"""
{cls.SYSTEM_PROMPT}

----------------------------
EXTRACTION INSTRUCTIONS
----------------------------

{custom_instructions}

----------------------------
OUTPUT JSON SCHEMA
----------------------------

{schema_json}

----------------------------
DOCUMENT
----------------------------

{document_text}

----------------------------
OUTPUT
----------------------------

Return ONLY valid JSON.
"""