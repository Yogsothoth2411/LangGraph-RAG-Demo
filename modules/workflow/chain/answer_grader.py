from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field
from modules.models.model import llm_model

class GradeAnswer(BaseModel):
    """對最終生成的答案進行評分，確認是否能回答使用者提問"""

    score: bool = Field(
        ..., description="生成的答案是否能回答使用者提問，True or False", example=True
    )


llm = llm_model
structured_llm_grader = llm.with_structured_output(GradeAnswer)

system = """
你是一個生成品質評估助理，負責判斷模型的生成是否有助於使用者的當前需求或意圖。
請根據以下原則回答 True 或 False：

- 如果生成對使用者的當前意圖有幫助，請回答 True。
- 如果生成無關、模糊、錯誤或未能滿足使用者需求，請回答 False。
- 使用者意圖可以是問答、指令執行、建議、寒暄或其他合理需求。

注意：
1. 對話歷史（chat_history）能提供上下文，請據此理解使用者當前意圖。
2. 僅回答 True 或 False，不要附加說明。
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "對話歷史（可用於理解上下文）："),
        MessagesPlaceholder(variable_name="chat_history"),
        (
            "human",
            "使用者原始提問：\n{question}\n\n"
            "生成的答案：\n{generation}\n\n"
            "請根據上述內容回答 True 或 False。",
        ),
    ]
)

# 顯式定義RunnableSequence 提供靜態類型檢查
answer_grader: RunnableSequence = prompt | structured_llm_grader
