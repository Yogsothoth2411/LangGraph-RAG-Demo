import requests
from langchain_community.utilities import SearxSearchWrapper
from data.model import WebResult, WebSearchOutput


def structured_searx_search(query: str, engines=None, max_results=4) -> WebSearchOutput:
    if not query.strip():
        # 空查詢直接返回空結果，避免呼叫外部 API
        return WebSearchOutput(query=query, results=[])

    host = "http://127.0.0.1:8888"
    SearxSearchWrapper(searx_host="http://127.0.0.1:8888")
    params = {"q": query, "format": "json", "engines": engines}
    json_data = requests.get(host, params=params).json()  # 直接 dict

    results = [
        WebResult(
            title=r.get("title"),
            url=r.get("url"),
            snippet=r.get("content"),
            engine=r.get("engine"),
        )
        for r in json_data.get("results", [])[:max_results]
        if r.get("content") and r.get("url")
    ]

    return WebSearchOutput(
        query=json_data.get("query", ""),
        results=results,
    )
