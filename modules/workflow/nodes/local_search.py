from typing import Dict, Any, List
from data.model import ScoredDocument
from modules.state import GraphState
from data.ingestion import retriever
from data.model import normalize_documents


def local_search_node(state: GraphState) -> Dict[str, Any]:
    """
    向量檢索節點

    Args:
        query: str

    Returns:
        documents: List[Any] (檢索結果)
    """
    print("--正在進行本地檢索")
    query = state["query"]

    results: List[ScoredDocument] = retriever.get_relevant_documents_with_score(
        query=query
    )

    doc = normalize_documents(results)

    return {"documents": doc}
