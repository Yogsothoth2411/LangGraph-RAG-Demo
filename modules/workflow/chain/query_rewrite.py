from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field
from modules.models.model import llm_model


class QueryRewrite(BaseModel):
    """將使用者的輸入重寫為適合查詢的語句"""

    query: str = Field(
        ...,
        description="將使用者的輸入重新改寫成適合檢索的問句，問題應簡短且具體，方便後續處理。",
        json_schema_extra={
            "examples": [
                "AI如何影響醫療產業？",
                "AI在醫療影像分析中的應用有哪些？",
                "AI技術如何改善診斷準確率？",
            ]
        },
    )


llm = llm_model

structured_llm_router = llm.with_structured_output(QueryRewrite)

system = """
你是一個查詢優化助理，負責將使用者的輸入問題改寫成適合資訊檢索（如網路搜尋或文件索引）的查詢語句。

請遵守以下原則：
1. 改寫後的查詢應該具體、簡潔，包含能提升搜尋效果的關鍵詞。
2. 若使用者的提問過於抽象或籠統，請先運用「Step Back Prompting」——
   從原問題的上層概念或背景意圖出發，重新表述成更廣泛或核心的檢索方向。
3. 若對話歷史（chat_history）中提供了主題線索或上下文，請適度整合；若沒有，僅根據當前提問生成。
4. 僅輸出一條改寫後的查詢語句，不需任何解釋或補充文字。
5. 改寫後的語句應自然且符合搜尋語氣，而非命令或推理句。
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "使用者提問： {question} \n\n對話歷史： {chat_history}",
        ),
    ]
)

question_rewriter: RunnableSequence = prompt | structured_llm_router
