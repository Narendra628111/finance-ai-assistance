from fastapi import APIRouter, Depends

from backend.agents.rag_agent import RAGAgent
from backend.core.dependencies import get_rag_agent
from backend.models.rag import (
    BuildIndexRequest,
    BuildIndexResponse,
    QueryRequest,
    QueryResponse,
)

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/index",
    response_model=BuildIndexResponse,
)
async def build_index(
    request: BuildIndexRequest,
    agent: RAGAgent = Depends(get_rag_agent),
):

    count = await agent.build_index(
        rebuild=request.rebuild,
    )

    return BuildIndexResponse(
        success=True,
        indexed_chunks=count,
        message="Knowledge base indexed successfully.",
    )


@router.post(
    "/query",
    response_model=QueryResponse,
)
async def query(
    request: QueryRequest,
    agent: RAGAgent = Depends(get_rag_agent),
):

    result = await agent.ask(
        request.question,
    )

    return QueryResponse(**result)