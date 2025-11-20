from langchain_classic.schema import BaseRetriever
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from typing import List
from data.model import ScoredDocument


class ScoredRetriever(BaseRetriever):
    """自訂Retriever類，用於提供回傳分數"""

    vectorstore: VectorStore  # 定義欄位給 Pydantic
    k: int = 8  # 可選，默認 8

    # 僅保留文件，不傳分數，langchain規定的做法，必須實作
    def _get_relevant_documents(self, query: str) -> List[Document]:
        docs_with_scores = self.vectorstore.similarity_search_with_score(
            query, k=self.k
        )
        return [doc for doc, score in docs_with_scores]

    # 自己的做法 另外調用支援回傳分數
    def get_relevant_documents_with_score(self, query: str) -> List[ScoredDocument]:
        results = self.vectorstore.similarity_search_with_score(query, k=self.k)
        return [
            ScoredDocument(query=query, document=doc, score=score)
            for doc, score in results
        ]
