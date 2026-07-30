from backend.services.classifier.classifier import ClassifierService
from backend.workflow.state import AssistantState


async def classifier_node(
    state: AssistantState,
) -> AssistantState:

    service = ClassifierService()

    if state.get("summary"):
        text = state["summary"]
    elif state.get("vision_result"):
        text = state["vision_result"]
    else:
        text = state["user_query"]

    result = await service.classify(text=text)

    print("=" * 80)
    print("CLASSIFIER RESULT")
    print(result)
    print("=" * 80)

    state["classification"] = result.intent
    state["classification_confidence"] = result.confidence

    return state
def route_after_classifier(
    state: AssistantState,
) -> str:

    intent = state.get("classification", "")

    print("=" * 80)
    print("ROUTER INTENT:", intent)
    print("=" * 80)
