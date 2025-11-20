# LangGraph-RAG-Demo

RAG system combining LangGraph and Ollama for local PDF retrieval and QA on technical documents.

## 專案簡介

LangGraph-RAG-Demo 利用 [LangGraph](https://github.com/langchain-ai/langgraph) workflow 與本地 [Ollama](https://ollama.com/) 大型語言模型，打造針對技術文件及 PDF 檔案的 RAG（Retrieval-Augmented Generation）問答系統，支援本地檔案檢索、文件自動摘要及關鍵資訊萃取。

---

## 目錄結構

```
LangGraph-RAG-Demo/
├── .env.example          # 環境變數範本
├── LICENSE               # 授權條款
├── README.md             # 專案說明
├── docker-compose.yml    # Docker 組成設定
├── main.py               # 主程式入口
├── requirements.txt      # Python 相依套件
├── backend/              # 後端核心與 API（可擴充）
├── frontend/             # 前端界面（如 Web 或測試用介面）
├── modules/              # 文件處理、RAG、模型等功能模組
├── data/                 # 暫存/專案資料
```

---

## 主要功能

- **PDF 技術文件檢索（僅支援英文）**
  - 上傳與解析本地 PDF 文件
  - 文件自動清洗、分割、建立嵌入向量資料庫
  - 根據查詢語句產生摘要與技術章節內容
- **Web Search 整合**
  - 結合 DuckDuckGo 搜尋，強化 RAG 檢索資料
- **模型切換**
  - 彈性更換 Ollama 支援的本地語言模型
- **結構化設計**
  - 採用 modules/ 區分核心業務，方便擴充和維護

---

## 安裝與執行

### 環境需求

- Python >= 3.10
- Docker、docker-compose
- Ollama (本地語言模型管理工具)

### 步驟

1. **下載專案**

    ```bash
    git clone https://github.com/Yogsothoth2411/LangGraph-RAG-Demo.git
    cd LangGraph-RAG-Demo
    ```

2. **建立並編輯環境設定檔**

    ```bash
    cp .env.example .env
    # 依需求編輯 .env 檔案內容
    ```

    - 請確認填寫正確，如 API KEY, LLM_MODEL, EMBED_MODEL 等。

3. **安裝 Python 相依套件**

    ```bash
    uv add -r requirements.txt
    ```

4. **安裝 Ollama 並下載所需模型**

    ```bash
    ollama pull gemma3:12b-it-qat
    ollama pull gemma3:4b
    ollama pull embeddinggemma
    ```

5. **啟動服務**

    - 使用 Docker：

        ```bash
        docker-compose up -d
        ```

    - 啟動主流程：

        ```bash
        uv run main.py
        ```

---

## 更換模型

- 編輯 `.env` 檔案設定：

    ```env
    LLM_MODEL = "gemma3:12b-it-qat"
    LLM_MODEL_SMALL = "gemma3:4b"
    EMBED_MODEL = "embeddinggemma"
    ```

- 執行 Ollama 下載新模型：

    ```bash
    ollama pull <MODEL_NAME>
    ```

---

## 常見問題 FAQ

- **Q:** 為什麼只支援英文 PDF？
  - 目前模型與文件預處理僅針對英文優化。
- **Q:** 文件過大或內容過多會怎樣？
  - 請分割檔案或調整檢索參數，避免 RAG 效果受影響。
- **Q:** `.env` 檔有哪些重要參數？
  - 主要包含 API key、模型名稱、嵌入模型等，請詳細參閱 `.env.example`。

---

## License

本專案採用 MIT 授權。詳見 [LICENSE](LICENSE)。