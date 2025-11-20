from modules.state import GraphState
from modules.workflow.chain.web_search_searx import structured_searx_search
from modules.workflow.chain.web_search_duckgo import structured_duckduckgo_search
from data.model import WebSearchOutput, normalize_documents, NormalizedDoc
from typing import Dict, List


def merge_web_outputs(*outputs: WebSearchOutput) -> WebSearchOutput:
    """
    聚合返回的多個 WebSearchOutput
    """
    all_results = []
    seen_urls = set()

    for out in outputs:
        for r in out.results:
            if str(r.url) not in seen_urls:
                seen_urls.add(str(r.url))
                all_results.append(r)

    return WebSearchOutput(
        query=outputs[0].query if outputs else "", results=all_results
    )


def web_search_node(state: GraphState) -> Dict[str, List[NormalizedDoc]]:
    """
    web檢索節點

    Args:
        query: str

    Returns:
        documents: List[Any] (檢索結果)
    """
    print("--正在進行網路搜尋")
    query = state["query"]
    # searx 檢索的內容大多偏離query，棄用。
    # searx_output = structured_searx_search(query, max_results=2)
    duck_output = structured_duckduckgo_search(query, max_results=5)
    # merged_output = merge_web_outputs(searx_output, duck_output)
    merged_output = merge_web_outputs(duck_output)
    doc = normalize_documents([merged_output])
    return {"documents": doc}
