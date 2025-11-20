from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.messages import trim_messages
from typing import List, Any
from dotenv import load_dotenv
import os

load_dotenv()

llm_model = ChatOllama(model=os.getenv("LLM_MODEL"))
llm_model_small = ChatOllama(model=os.getenv("LLM_MODEL_SMALL"))
embed_model = OllamaEmbeddings(model=os.getenv("EMBED_MODEL"))

def trim_chat_history(chat_history: List[Any], max_tokens: int = 10) -> List[Any]:
    """
    對 chat_history 進行裁剪，返回裁剪後的訊息列表

    Args:
        chat_history: List[Any]，原始對話訊息
        max_tokens: int，保留的最大 token 數量（含系統訊息計數可調）

    Returns:
        List[Any]，裁剪後的對話歷史
    """
    trimer = trim_messages(
        max_tokens=max_tokens,
        token_counter=len,
        strategy="last",
        include_system=False,
        allow_partial=False,
    )

    return trimer.invoke(chat_history)
