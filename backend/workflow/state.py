from typing import Optional
from typing_extensions import TypedDict


class AssistantState(TypedDict):
    """
    Shared state passed between LangGraph nodes.
    """

    # User Input
    input_type: str               # text | image | pdf
    user_query: str
    file_path: Optional[str]

    # Agent Outputs
    extracted_text: str
    vision_result: str
    classification: str
    summary: str
    rag_context: str

    # Final Response
    final_answer: str