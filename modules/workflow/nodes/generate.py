from modules.state import GraphState
from modules.workflow.chain.generation import generation_chain
from typing import Dict, Any
from data.model import merge_documents_for_grader
from modules.models.model import trim_chat_history

def generate_node(state: GraphState) -> Dict[str, Any]:
    """
    根據輸入內容生成答案

    Args:
        question: str
        documents: List[Any]
        chat_history: Annotated[list[AnyMessage], add_messages]

    Returns:
        generation: str
    """
    print("--正在生成回覆")
    question = state["question"]
    documents = state["documents"]
    chat_history = state["chat_history"]
    answer = generation_chain.invoke(
        {
            "question": question,
            "documents": merge_documents_for_grader(documents),
            "chat_history": trim_chat_history(chat_history),
        }
    )

    return {"generation": answer}
