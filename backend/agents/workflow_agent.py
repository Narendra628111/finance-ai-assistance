"""
Workflow Agent.

Executes the LangGraph workflow.
"""

from __future__ import annotations

from backend.workflow.graph import graph
from backend.workflow.state import AssistantState
from pprint import pprint

class WorkflowAgent:
    """
    Workflow Agent responsible for executing
    the LangGraph workflow.
    """

    async def run(
        self,
        state: AssistantState,
    ) -> AssistantState:
        """
        Execute the workflow.
        """

        return await graph.ainvoke(state)
        print("\n" + "=" * 80)
        print("FINAL WORKFLOW STATE")
        pprint(result)
        print("=" * 80 + "\n")

        return result