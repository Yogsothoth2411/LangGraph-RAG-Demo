from dotenv import load_dotenv
from data.loader import load_pdf_elements
from data.cleaning import clean_elements
from data.merge_elements import merge_elements
from data.chunk import chunk_elements
from data.store import create_vector_store
from data.retriever import ScoredRetriever
from neo4j import GraphDatabase
import hashlib
from pathlib import Path
from typing import Union, List
import os

load_dotenv()
url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


def compute_file_hash(file_path: str | Path) -> str:
    """計算檔案內容 SHA256 Hash"""
    file_path = Path(file_path)
    hasher = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def create_vectorstore_pipeline(
    pdf_paths: Union[str, Path, List[Union[str, Path]]],
) -> None:
    """新增資料的完整流程"""

    if isinstance(pdf_paths, (str, Path)):
        pdf_paths = [pdf_paths]

    store = create_vector_store()

    driver = GraphDatabase.driver(url, auth=(username, password))
    for pdf_path in pdf_paths:
        file_hash = compute_file_hash(pdf_path)

        with driver.session() as session:
            # 使用 hash 檢查是否已載入
            result = session.run(
                """
                MATCH (c:Chunk)
                WHERE c.file_hash IS NOT NULL AND c.file_hash = $file_hash
                RETURN COUNT(c) AS existing
            """,
                file_hash=file_hash,
            )

            if result.single()["existing"] > 0:
                print(f"⚠️ 檔案已存在 (hash={file_hash[:8]}...)，略過。")
                continue
        try:
            elements = load_pdf_elements(pdf_path=pdf_path)
            elements = clean_elements(elements=elements)
            elements = merge_elements(elements=elements)
            chunks = chunk_elements(unique_elements=elements)
        except Exception as e:
            print(f"[Pipeline Error] PDF {pdf_path} skipped due to error: {e}")
            continue

        # 為每個 chunk metadata 增加 file_hash
        for doc in chunks:
            doc.metadata["file_hash"] = file_hash

        # 新增資料
        store.add_documents(chunks)


def create_retriever() -> ScoredRetriever:
    store = create_vector_store()
    retriever = ScoredRetriever(vectorstore=store, k=5)
    return retriever


retriever = create_retriever()
