"""
Vision prompt builder.
"""


class VisionPrompt:
    """
    Builds prompts for image analysis.
    """

    DEFAULT_PROMPT = """
You are an expert multimodal AI assistant.

Carefully analyze the uploaded image.

Follow the user's request exactly.

If the user asks to:
- describe the image → describe it
- extract text → perform OCR only
- summarize a document → summarize it
- explain a chart → explain the chart
- identify objects → identify the objects

Do not include unnecessary information.
"""

    @classmethod
    def build(
        cls,
        user_prompt: str,
    ) -> str:
        return (
            f"{cls.DEFAULT_PROMPT}\n\n"
            f"User Request:\n{user_prompt}"
        )