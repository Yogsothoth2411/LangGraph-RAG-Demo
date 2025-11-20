from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from modules.models.model import llm_model


class QueryReflex(BaseModel):
    """根據檢索情境重寫查詢語句"""

    new_query: str = Field(
        ...,
        description="改寫後的查詢語句，以提升檢索相關性或補足缺失資訊",
        json_schema_extra={"example": "Python 記憶體管理機制 原理與 GC 運作"},
    )


llm = llm_model
structured_llm_reflect = llm.with_structured_output(QueryReflex)

system = """
你是一個檢索查詢優化助手，負責根據上一版查詢結果的不足或偏差，改進查詢語句。
你的目標是讓新的查詢語句更貼近使用者真實意圖，並提升檢索的相關性與資訊覆蓋度。

原則：
1. 以上一版查詢（query）為主要基礎，只在必要時參考原始問題（question）。
2. 若文件（documents）內容與查詢主題不符，請修正或替換關鍵詞。
3. 若文件資訊不足，請補充必要的上下文、限制條件或語意關鍵詞。
4. 僅輸出新的查詢語句，不要附加任何解釋。
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "檢索到的文件摘要：{documents}\n\n"
            "原始使用者問題：{question}\n\n"
            "上一版查詢語句：{query}\n\n"
            "請基於上述內容，重寫查詢語句以改善檢索效果。",
        ),
    ]
)


reflex_router = prompt | structured_llm_reflect
