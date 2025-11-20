import subprocess
import time
import socket


def wait_for_port(host, port, timeout=100):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.2)
    return False


if __name__ == "__main__":

    # 1. 啟動 FastAPI（後端）
    api_proc = subprocess.Popen(
        ["uvicorn", "backend.runner:app", "--host", "127.0.0.1", "--port", "8000"]
    )

    # 2. 等待 FastAPI 啟動完成
    print("Waiting for FastAPI...")
    if not wait_for_port("127.0.0.1", 8000, timeout=100):
        api_proc.terminate()
        raise RuntimeError("FastAPI did not start in time")
    print("FastAPI is ready!")

    # 3. 啟動 Gradio（前端）
    ui_proc = subprocess.Popen(["uv", "run", "-m", "frontend.app"])

    # 4. 等待兩者結束
    api_proc.wait()
    ui_proc.wait()
