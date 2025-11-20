from langchain_community.tools import DuckDuckGoSearchResults
from data.model import WebResult, WebSearchOutput


def structured_duckduckgo_search(query: str, max_results=4) -> WebSearchOutput:
    if not query.strip():
        # 空查詢直接返回空結果，避免呼叫外部 API
        return WebSearchOutput(query=query, results=[])
    # 使用 list 格式回傳
    tool = DuckDuckGoSearchResults(output_format="list", num_results=max_results)
    raw_results = tool.invoke(query)  # 回傳 list[dict]

    results = [
        WebResult(
            title=r["title"], url=r["link"], snippet=r["snippet"], engine="duckduckgo"
        )
        for r in raw_results
        if r.get("link")
    ]

    return WebSearchOutput(query=query, results=results)
