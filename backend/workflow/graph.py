"""
LangGraph Workflow.
"""

from __future__ import annotations

from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from backend.workflow.state import AssistantState
from backend.workflow.router import (
    route_after_classifier,
    route_input,
)

from backend.workflow.nodes.document_node import document_node
from backend.workflow.nodes.summarizer_node import summarizer_node
from backend.workflow.nodes.classifier_node import classifier_node
from backend.workflow.nodes.rag_node import rag_node


builder = StateGraph(AssistantState)


# ---------------------------------------------------------
# Nodes
# ---------------------------------------------------------

builder.add_node(
    "document",
    document_node,
)

builder.add_node(
    "summarizer",
    summarizer_node,
)

builder.add_node(
    "classifier",
    classifier_node,
)

builder.add_node(
    "rag",
    rag_node,
)


# ---------------------------------------------------------
# Entry
# ---------------------------------------------------------

builder.add_conditional_edges(
    START,
    route_input,
    {
        "text": "classifier",
        "document": "document",
    },
)


# ---------------------------------------------------------
# Document flow
# ---------------------------------------------------------

builder.add_edge(
    "document",
    "summarizer",
)

builder.add_edge(
    "summarizer",
    "classifier",
)


# ---------------------------------------------------------
# Classifier → RAG
# ---------------------------------------------------------

builder.add_conditional_edges(
    "classifier",
    route_after_classifier,
    {
        "rag": "rag",
    },
)


# ---------------------------------------------------------
# RAG → END
# ---------------------------------------------------------

builder.add_edge(
    "rag",
    END,
)


graph = builder.compile()