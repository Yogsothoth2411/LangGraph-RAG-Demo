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

    # 這裡的儲存會捨去頁面座標資訊（除非有要做PDF view高亮引用段落，單純RAG沒用到座標資訊）
    # 從第一性原理出發思考功能，用不上。如果需要座標資訊，可以扁平成json或是單一欄位存metadata
    documents = [
        Document(
            page_content=c["text"],
            metadata={k: v for k, v in c["metadata"].items() if k != "coordinates"},
        )
        for c in chunks
        if len(c["text"].strip()) >= min_len
    ]

    return documents
