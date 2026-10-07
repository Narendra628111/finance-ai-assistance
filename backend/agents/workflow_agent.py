"""
Workflow Agent.

Executes the LangGraph workflow.
"""

from __future__ import annotations

from pprint import pprint

from backend.workflow.graph import graph
from backend.workflow.state import AssistantState


class WorkflowAgent:
    """
    Workflow Agent responsible for executing
    the LangGraph workflow.
    """

    async def run(
        self,
        state: AssistantState,
    ) -> AssistantState:

        result = await graph.ainvoke(state)

        print("\n" + "=" * 80)
        print("FINAL WORKFLOW STATE")
        pprint(result)
        print("=" * 80 + "\n")

        return result