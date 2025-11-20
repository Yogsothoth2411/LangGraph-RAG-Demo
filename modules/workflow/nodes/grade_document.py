from modules.state import GraphState
from modules.workflow.chain.retriever_grader import retrieval_grader
from modules.workflow.chain.coverage_grader import coverage_grader
from modules.consts import GENERATE, REFLEX
from langgraph.types import Command
from data.model import merge_documents_for_grader


def grade_document_node(state: GraphState) -> Command:
    """
    檢索到的文檔相關性由LLM評分

    Args:
        question: str
        documents: List[Any]

    Returns:
        Command: goto next node
        documents: List[Any]
    """
    print("--正在判斷文檔相關性")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []

    for doc in documents:
        score = retrieval_grader.invoke(
            {
                "question": question,
                "documents": f"\n{doc['text']}\n(meta: {doc['meta']})",
            }
        )
        if score.score:
            filtered_docs.append(doc)
        else:
            continue

    if not filtered_docs:
        print("--全部文檔都不相關，強制反思")
        return Command(goto=REFLEX)

    reflex = coverage_grader.invoke(
        {
            "question": question,
            "documents": merge_documents_for_grader(filtered_docs),
        }
    )

    if not reflex.score:
        # 有文檔不相關，進行額外的檢索
        print("--進行額外的檢索查詢補充")
        return Command(
            update={
                "documents": filtered_docs,
            },
            goto=REFLEX,
        )

    return Command(
        update={
                "documents": filtered_docs,
            },
        goto=GENERATE,
    )
