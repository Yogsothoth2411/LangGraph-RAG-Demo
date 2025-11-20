import gradio as gr
import requests
from modules.state import Mode
# --------------------------
# 狀態管理工具函式
# --------------------------


def safe_append(history, user_msg, bot_msg, selected_state=None):
    """
    安全地新增聊天記錄，返回 dict list，支援 selected_state。
    """
    new_entry = {
        "role": "user",
        "content": user_msg
    }
    new_history = history + [new_entry]

    bot_entry = {
        "role": "assistant",
        "content": bot_msg,
        "selected_state": selected_state 
    }
    new_history.append(bot_entry)

    return new_history


def safe_pop_last(history):
    """
    安全地移除最後一條聊天記錄。
    返回新的列表與最後一條用戶訊息。
    """
    if history:
        last_user_msg = history[-1][0]
        return history[:-1], last_user_msg
    return history, ""


# --------------------------
# Chat 功能
# --------------------------


def respond(message, history, mode, file_list):
    """
    根據模式回覆訊息。
    - mode: "網路搜索" 或 "本地檔案問答"
    - history: 聊天歷史
    - file_list: 上傳的檔案清單
    """
    if not message.strip():
        # 防止空訊息
        return history, ""

    # 本地檔案問答模式，檢查檔案清單
    if mode == Mode.LOCAL_SEARCH and not file_list:
        answer = "⚠️ 請先上傳檔案，再進行本地問答"
        new_history = safe_append(history, message, answer, None)
        return new_history, "", new_history

    # 正常呼叫 API
    answer = "❌ 無法取得回覆"
    selected_state = None
    api_url = "http://localhost:8000/chat/chat_response"
    try:
        response = requests.post(api_url, json={"user_input": message, "mode": mode})
        if response.status_code in (200, 202):
            data = response.json()
            generation = data["generation"]
            sources = data["documents"]
            selected_state = data["selected_state"]
            answer = f"{generation}\n\n<details><summary>📚 展開引用來源</summary>\n\n{sources}\n\n</details>"
        else:
            print(f"[API Error] {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[API Exception] {e}")

    new_history = safe_append(history, message, answer, selected_state)
    return new_history, "", new_history



def edit_last(history):
    """
    編輯最後一條聊天訊息。
    返回新的聊天歷史與最後一條用戶訊息。
    """
    return safe_pop_last(history)


# --------------------------
# 檔案清單管理
# --------------------------


def add_file_to_list(file_path, current_list):
    """
    新增檔案到清單，如果已存在則忽略。
    """
    if file_path and file_path not in current_list:
        new_list = current_list + [file_path]  # 創建新列表，避免原地修改
        # 呼叫 API
        api_url = "http://localhost:8000/pdf/load_pdf"
        try:
            response = requests.post(api_url, json={"pdf_paths": [file_path]})
            if response.status_code == 200 or response.status_code == 202:
                print(f"[API] PDF {file_path} submitted successfully")
            else:
                print(f"[API Error] {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[API Exception] {e}")
    else:
        new_list = current_list.copy()
    
    # 更新選擇器 value 為最新檔案
    value = new_list[-1] if new_list else None
    return new_list, gr.update(choices=new_list, value=value), None


def remove_file_from_list(selected_file, current_list):
    """
    從清單移除選中的檔案。
    """
    if selected_file in current_list:
        api_url = "http://localhost:8000/pdf/remove_chunk"
        try:
            response = requests.delete(api_url, json={"pdf_paths": selected_file})
            if response.status_code == 200 or response.status_code == 202:
                print(f"[API] PDF {selected_file} delete successfully")
            else:
                print(f"[API Error] {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[API Exception] {e}")
    new_list = [f for f in current_list if f != selected_file]
    value = new_list[-1] if new_list else None
    return new_list, gr.update(choices=new_list, value=value), None


def clear_file_list():
    """
    清空檔案清單。
    """
    api_url = "http://localhost:8000/pdf/remove_index"
    try:
        response = requests.delete(api_url)
        if response.status_code == 200 or response.status_code == 202:
            print(f"[API] PDF delete successfully")
        else:
            print(f"[API Error] {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[API Exception] {e}")
    return [], gr.update(choices=[], value=None), None


# --------------------------
# Gradio UI
# --------------------------

with gr.Blocks(title="AI Assistant") as demo:
    gr.Markdown("# AI Assistant")

    # 狀態管理
    file_list_state = gr.State(value=[])
    chat_history_state = gr.State(value=[])

    with gr.Tabs():
        # 分頁 1: Chat
        with gr.Tab("Chat"):
            mode_dropdown = gr.Dropdown(
                choices=[Mode.WEB_SEARCH, Mode.LOCAL_SEARCH], value=Mode.WEB_SEARCH, label="選擇模式"
            )
            chatbot = gr.Chatbot(type="messages", height=600, min_height=400, max_height=800)
            msg_input = gr.Textbox(label="輸入你的問題")
            # edit_btn = gr.Button("修改上一次輸入")

            # 提交訊息
            msg_input.submit(
                respond,
                inputs=[msg_input, chat_history_state, mode_dropdown, file_list_state],
                outputs=[chatbot, msg_input, chat_history_state],
            )

            # 修改最後一條訊息
            # edit_btn.click(
            #     edit_last,
            #     inputs=[chat_history_state],
            #     outputs=[chatbot, msg_input],
            # )

        # 分頁 2: 上傳檔案
        with gr.Tab("上傳檔案"):
            file_upload = gr.File(
                label="上傳PDF檔案", file_types=[".pdf"], type="filepath"
            )
            file_dropdown = gr.Dropdown(label="已上傳檔案清單", choices=[], value=None)
            remove_btn = gr.Button("移除選中文件")
            clear_files_btn = gr.Button("清空檔案清單")

            # 新增檔案
            file_upload.upload(
                add_file_to_list,
                inputs=[file_upload, file_list_state],
                outputs=[file_list_state, file_dropdown, file_upload],
            )

            # 移除檔案
            remove_btn.click(
                remove_file_from_list,
                inputs=[file_dropdown, file_list_state],
                outputs=[file_list_state, file_dropdown, file_upload],
            )

            # 清空檔案清單
            clear_files_btn.click(
                clear_file_list, outputs=[file_list_state, file_dropdown, file_upload]
            )

demo.launch()
