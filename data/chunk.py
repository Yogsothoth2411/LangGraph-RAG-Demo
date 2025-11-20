from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from data.model import PDFElement


def chunk_elements(unique_elements: List[PDFElement], min_len: int = 100) -> List[Document]:
    """切分經過清洗的elements，同時過濾過短文本"""
    # 過濾掉過短的文本
    filtered_elements = [e for e in unique_elements if len(e.page_content.strip()) >= min_len]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=200, separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = []
    for e in filtered_elements:
        split_texts = splitter.split_text(e.page_content)
        for i, t in enumerate(split_texts):
            chunk_meta = e.metadata.model_dump()  # metadata 保留
            chunk_meta["chunk_id"] = f"{e.metadata.element_id}_{i}"
            chunks.append({"text": t, "metadata": chunk_meta})

    # 儲存時移除頁面座標資訊 (coordinates)，因為單純 RAG 檢索不需要此資訊。
    # 若未來需要支持 PDF 高亮或精確定位，可將座標資訊保留，或扁平成 JSON / 單一欄位存入 metadata。
    documents = [
        Document(
            page_content=c["text"],
            metadata={k: v for k, v in c["metadata"].items() if k != "coordinates"},
        )
        for c in chunks
        if len(c["text"].strip()) >= min_len
    ]

    return documents
