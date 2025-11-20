from modules.workflow.chain.router import question_router
from modules.workflow.chain.query_rewrite import question_rewriter
from modules.state import GraphState
from typing import Dict, Any
from modules.models.model import trim_chat_history
from modules.consts import GENERATE,ROUTER
from langgraph.types import Command

def query_rewriter_node(state: GraphState) -> Dict[str, Any]:
    """
    使用者輸入轉寫成查詢用query

    Args:
        question: str
        chat_history: Annotated[list[AnyMessage], add_messages]

    Returns:
        question: str
        sub_questions: List[str]
    """

    question = state["question"]
    chat_history = state["chat_history"]
    print("--正在判斷是否需要檢索")
    result = question_router.invoke(
        {
            "question": question,
        }
    )
    need_search = result.is_need_search
    if need_search:
        print("--需要檢索，正在轉寫query")
        query = question_rewriter.invoke(
            {
                "question": question,
                "chat_history": trim_chat_history(chat_history),
            }
        )

        return Command(
            update={"query": query.query},
            goto=ROUTER,
        )
    
    print("--無需檢索，直接產生回覆")
    return Command(goto=GENERATE)
