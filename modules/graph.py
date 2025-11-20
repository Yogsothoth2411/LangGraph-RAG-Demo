from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from modules.consts import (
    REWRITE_QUERY,
    ROUTER,
    GENERATE,
    WEB_SEARCH,
    LOCAL_SEARCH,
    REFLEX,
    CHAT_HISTORY,
    GRADE_DOCUMENT,
    GRADE_GENERATE,
)
from modules.state import Mode
from modules.workflow.nodes.rewrite_query import query_rewriter_node
from modules.workflow.nodes.router import router_node
from modules.workflow.nodes.generate import generate_node
from modules.workflow.nodes.web_search import web_search_node
from modules.workflow.nodes.local_search import local_search_node
from modules.workflow.nodes.reflex import reflex_node
from modules.workflow.nodes.chat_history import chat_history_node
from modules.workflow.nodes.grade_document import grade_document_node
from modules.workflow.nodes.grade_generate import grade_generate_node
from modules.state import GraphState
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

def mode_router(state:GraphState):
    mode =  state["mode"]
    match mode:
        case Mode.LOCAL_SEARCH:
            print("--正在導向本地搜尋")
            return LOCAL_SEARCH
        case Mode.WEB_SEARCH:
            print("--正在導向網路搜尋")
            return WEB_SEARCH
        case _:
            raise ValueError(f"Unknown mode: {mode}")


workflow = StateGraph(GraphState)
workflow.add_node(REWRITE_QUERY, query_rewriter_node)
workflow.add_node(ROUTER, router_node)
workflow.add_node(GENERATE, generate_node)
workflow.add_node(WEB_SEARCH, web_search_node)
workflow.add_node(LOCAL_SEARCH, local_search_node)
workflow.add_node(REFLEX, reflex_node)
workflow.add_node(CHAT_HISTORY, chat_history_node)
workflow.add_node(GRADE_DOCUMENT, grade_document_node)
workflow.add_node(GRADE_GENERATE, grade_generate_node)

workflow.set_entry_point(REWRITE_QUERY)
workflow.add_edge(LOCAL_SEARCH, GRADE_DOCUMENT)
workflow.add_edge(WEB_SEARCH, GRADE_DOCUMENT)
workflow.add_edge(REFLEX, ROUTER)
workflow.add_edge(GENERATE, GRADE_GENERATE)
workflow.add_edge(CHAT_HISTORY, END)

memory = InMemorySaver()
app = workflow.compile(checkpointer=memory)
app.get_graph().draw_mermaid_png(output_file_path="graph.png")
