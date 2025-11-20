from typing import List, TypedDict, Annotated, Any
from langgraph.graph.message import AnyMessage, add_messages
from enum import Enum


class Mode(str, Enum):
    WEB_SEARCH = "web_search"
    LOCAL_SEARCH = "local_search"


class GraphState(TypedDict):
    """包含 查詢、生成、對話歷史 和 文檔 的狀態"""

    question: str
    query: str
    chat_history: Annotated[list[AnyMessage], add_messages]
    documents: List[Any]
    generation: str
    mode: Mode
