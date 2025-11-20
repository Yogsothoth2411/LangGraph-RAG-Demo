from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from modules.models.model import llm_model_small


class RouteQuery(BaseModel):
    """判斷使用者的輸入是否需要查詢"""

    is_need_search: bool = Field(
        ...,
        description="根據使用者的提問，是否需要查詢才可回覆，True or False",
        example=True,
    )


llm = llm_model_small

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """你是一個路由助理。你的任務是判斷使用者的問題是否需要透過資料檢索才能正確回答。
規則：
1. 若問題屬於日常對話、簡單問答、閒聊或不需要外部資料的內容，則輸出 False。
2. 若問題涉及需要查詢知識、文件內容、事實性資訊（例如技術、歷史、專案資料等），則輸出 True。
3. 不要判斷資料來源，僅需判斷是否需要查詢。
輸出一個布林值。"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "{question}",
        ),
    ]
)

question_router = prompt | structured_llm_router
