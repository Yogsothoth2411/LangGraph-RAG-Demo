from modules.state import GraphState
from langchain_core.messages import AIMessage, SystemMessage
from data.model import merge_documents_for_grader


def chat_history_node(state: GraphState):
    chat_history = state["chat_history"]
    generation = state["generation"]
    documents = state["documents"]
    print("--正在記錄聊天歷史")
    if documents:
        doc_text = merge_documents_for_grader(documents)
        chat_history.append(SystemMessage(content=f"[Retrieved Documents]\n{doc_text}"))
    chat_history.append(AIMessage(content=generation))

    return {
        "chat_history": chat_history,
    }
