"""
Response parser for LLM extraction responses.

Responsibilities:
- Remove markdown/code fences
- Extract JSON from mixed responses
- Validate JSON
- Return structured dictionaries
"""

from __future__ import annotations

import json
import re
from json import JSONDecodeError
from typing import Any

from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ResponseParser:
    """
    Parses and validates LLM responses.
    """

    _JSON_BLOCK_PATTERN = re.compile(
        r"```(?:json)?\s*(.*?)\s*```",
        flags=re.DOTALL | re.IGNORECASE,
    )

    @classmethod
    def parse(cls, response: str) -> dict[str, Any]:
        """
        Parse an LLM response into a dictionary.

        Args:
            response: Raw response from the LLM.

        Returns:
            Parsed JSON dictionary.

        Raises:
            ValueError:
                If valid JSON cannot be extracted.
        """
        cleaned = cls.clean(response)

        try:
            return json.loads(cleaned)

        except JSONDecodeError:
            logger.debug(
                "Direct JSON parsing failed. Attempting recovery..."
            )

        extracted = cls.extract_json(cleaned)

        try:
            return json.loads(extracted)

        except JSONDecodeError as exc:
            logger.exception("Unable to parse JSON response.")
            raise ValueError("Invalid JSON response received.") from exc

    @classmethod
    def clean(cls, response: str) -> str:
        """
        Remove markdown formatting.

        Args:
            response: Raw LLM response.

        Returns:
            Cleaned string.
        """
        response = response.strip()

        match = cls._JSON_BLOCK_PATTERN.search(response)

        if match:
            response = match.group(1)

        return response.strip()

    @classmethod
    def extract_json(cls, text: str) -> str:
        """
        Extract the first JSON object from text.

        Args:
            text: Text containing JSON.

        Returns:
            JSON string.

        Raises:
            ValueError:
                If JSON cannot be located.
        """
        start = text.find("{")

        if start == -1:
            raise ValueError("JSON object not found.")

        depth = 0

        for index in range(start, len(text)):
            char = text[index]

            if char == "{":
                depth += 1

            elif char == "}":
                depth -= 1

                if depth == 0:
                    return text[start : index + 1]

        raise ValueError("Incomplete JSON object.")

    @staticmethod
    def is_valid_json(text: str) -> bool:
        """
        Check whether a string is valid JSON.

        Args:
            text: Input string.

        Returns:
            True if valid.
        """
        try:
            json.loads(text)
            return True

        except Exception:
            return False

    @staticmethod
    def to_json(
        data: dict[str, Any],
        *,
        indent: int = 4,
    ) -> str:
        """
        Convert dictionary to formatted JSON.

        Args:
            data: Dictionary.
            indent: JSON indentation.

        Returns:
            JSON string.
        """
        return json.dumps(
            data,
            indent=indent,
            ensure_ascii=False,
        )