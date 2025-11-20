from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field
from modules.models.model import llm_model_small


class CoverageScore(BaseModel):
    """使用布林分數對檢索到的文件進行評分"""

    score: bool = Field(
        ...,
        description="True 表示這組文件已足以回答問題；False 則表示不足，需要追加檢索。",
        json_schema_extra={"example": True},
    )


llm = llm_model_small
structured_llm_grader = llm.with_structured_output(CoverageScore)

system = """你是一個覆蓋度評估助理（coverage grader）。
請根據使用者的提問，判斷「整體文件集合」是否足以讓系統回答問題。

如果文件集合包含「必要資訊」即可視為足夠，不需要完全精準。
如果資訊不足、缺少關鍵內容，請輸出 False。"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "使用者的提問：{question}\n\n文件集合（已合併）：{documents}\n\n這組文件是否足以回答問題？請只輸出 True 或 False。",
        ),
    ]
)

# 顯式定義RunnableSequence 提供靜態類型檢查
coverage_grader: RunnableSequence = prompt | structured_llm_grader
