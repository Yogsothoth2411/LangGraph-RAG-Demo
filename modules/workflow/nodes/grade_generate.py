from modules.state import GraphState
from modules.workflow.chain.hallucination_grader import hallucination_grader
from modules.workflow.chain.answer_grader import answer_grader
from langgraph.types import Command
from modules.consts import CHAT_HISTORY, GENERATE
from data.model import merge_documents_for_grader
from modules.models.model import trim_chat_history


def grade_generate_node(state: GraphState) -> Command:
    """
    生成的回答由LLM評分(幻覺/可用性)

    Args:
        documents: List[Any]
        chat_history: Annotated[list[AnyMessage], add_messages]
        generation: str
        question: str

    Returns:
        Command: goto next node
    """
    print("--正在判斷答案品質")
    documents = state["documents"]
    chat_history = state["chat_history"]
    generation = state["generation"]
    question = state["question"]

    hallucination_score = hallucination_grader.invoke(
        {
            "documents": merge_documents_for_grader(documents),
            "chat_history": trim_chat_history(chat_history),
            "generation": generation,
        }
    )

    if hallucination_score.score:
        answer_score = answer_grader.invoke(
            {
                "question": question,
                "generation": generation,
                "chat_history": trim_chat_history(chat_history),
            }
        )
        if answer_score.score:
            # 通過，跳轉記入聊天歷史
            return Command(goto=CHAT_HISTORY)
    # 不通過，重新生成
    print("--重新生成答案")
    return Command(goto=GENERATE)
