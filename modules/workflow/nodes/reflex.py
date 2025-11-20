from modules.state import GraphState
from modules.workflow.chain.reflex import reflex_router
from typing import Dict, Any


def reflex_node(state: GraphState) -> Dict[str, Any]:
    """
    根據輸入內容改寫query

    Args:
        question: str
        documents: List[Any]
        query: str

    Returns:
        query: str
    """
    print("--正在重新產生query")
    documents = state["documents"]
    question = state["question"]
    query = state["query"]

    reflex_query = reflex_router.invoke(
        {
            "documents": documents,
            "question": question,
            "query": query,
        }
    )

    return {"query": reflex_query.new_query}
