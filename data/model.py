from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Tuple, TypedDict
from langchain_core.documents import Document


class WebResult(BaseModel):
    title: str
    url: HttpUrl
    snippet: Optional[str] = None
    engine: Optional[str] = None


class WebSearchOutput(BaseModel):
    query: str
    results: List[WebResult]


# 文件座標結構
class Coordinates(BaseModel):
    points: Tuple[
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
    ]
    system: str
    layout_width: float
    layout_height: float


# 文檔metadata載入結構
class PDFElementMetadata(BaseModel):
    source: str
    coordinates: Optional[Coordinates]
    filetype: str
    languages: List[str]
    last_modified: str
    page_number: int
    file_directory: str
    filename: str
    category: str
    element_id: str


# 文檔整體load 結構
class PDFElement(BaseModel):
    page_content: str
    metadata: PDFElementMetadata


class ScoredDocument(BaseModel):
    query: str
    document: Document
    score: float


class NormalizedDoc(TypedDict):
    text: str  # 用於生成與評分
    meta: dict  # 保留原始資訊 (score, url, title...)


def normalize_documents(docs) -> List[NormalizedDoc]:
    """
    將不同來源的文件物件轉換為統一的標準化結構，便於後續處理。

    Args:
        docs: List[Any]
            可能包含 ScoredDocument、WebSearchOutput 等不同文件來源的物件。

    Returns:
        List[NormalizedDoc]:
            每筆資料皆包含:
            - "text": 主要內容文字
            - "meta": 與來源相關的輔助資訊（如 score、query、url、engine 等）
    """
    normalized: List[NormalizedDoc] = []

    for doc in docs:
        # retriever
        if isinstance(doc, ScoredDocument):
            normalized.append(
                {
                    "text": doc.document.page_content,
                    "meta": {"score": doc.score, "query": doc.query},
                }
            )

        # web search
        elif isinstance(doc, WebSearchOutput):
            for r in doc.results:
                normalized.append(
                    {
                        "text": r.snippet or r.title,
                        "meta": {
                            "query": doc.query,
                            "url": str(r.url) if isinstance(r.url, HttpUrl) else r.url,
                            "title": r.title,
                            "engine": r.engine,
                        },
                    }
                )

    return normalized


def merge_documents_for_grader(documents: List[NormalizedDoc]) -> str:
    """
    將標準化後的文件內容合併為可供評分器使用的單一字串表示。

    Args:
        documents: List[NormalizedDoc]
            已標準化的文件列表，每筆包含 text 與 meta。

    Returns:
        str:
            以分段形式呈現的文件總覽，每一段以 [Doc i] 作為標示，
            並包含對應的 text 與 meta 資訊。
    """
    chunks = []
    for i, doc in enumerate(documents, start=1):
        chunks.append(f"[Doc {i}]\n{doc['text']}\n(meta: {doc['meta']})")
    return "\n\n".join(chunks)

def merge_documents_for_grader_md(documents: list) -> str:
    """
    將標準化後的文件內容合併為 Markdown 格式，每篇文件標示 [Doc i]，
    並將 meta 自動列出為 key: value，方便顯示。

    Args:
        documents: List[NormalizedDoc]
            已標準化的文件列表，每筆包含 text 與 meta。

    Returns:
        str:
            Markdown 格式的文件總覽。
    """
    chunks = []
    for i, doc in enumerate(documents, start=1):
        doc_lines = [f"### [Doc {i}]\n\n", doc['text'], "", "**Meta:**"]
        # 將 meta key/value 自動列出
        for k, v in doc.get('meta', {}).items():
            if k == "url":  # 將 URL 用 Markdown 超連結
                title = doc['meta'].get('title', v)
                doc_lines.append(f"- {k.capitalize()}: [{title}]({v})")
            else:
                doc_lines.append(f"- {k.capitalize()}: {v}")
        chunks.append("\n".join(doc_lines))
    return "\n\n---\n\n".join(chunks)