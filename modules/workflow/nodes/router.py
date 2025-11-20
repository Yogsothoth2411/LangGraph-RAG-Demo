from modules.state import GraphState
from modules.consts import LOCAL_SEARCH, WEB_SEARCH
from modules.state import Mode
from langgraph.types import Command


def router_node(state: GraphState) -> Command:
    """
    根據使用者的輸入和檢索模式跳轉路由

    """
    mode = state["mode"]
    print("--正在判斷路由")
    match mode:
        case Mode.LOCAL_SEARCH:
            print("--正在導向本地搜尋")
            goto = LOCAL_SEARCH
        case Mode.WEB_SEARCH:
            print("--正在導向網路搜尋")
            goto = WEB_SEARCH
        case _:
            raise ValueError(f"Unknown mode: {mode}")

    return Command(goto=goto)
