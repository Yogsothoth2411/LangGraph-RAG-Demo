# LangGraph-RAG-Demo

本專案結合 **Langgraph** 與 **Ollama**，打造一個針對技術文件與 PDF 的 RAG 系統。系統支援本地 PDF 檔案檢索與網路搜尋（DuckDuckGo），並提供結構化切割與檢索方式，精準提取文件知識，生成回答與摘要。



## 功能

* **RAG 文件檢索與生成**

  * 上傳本地 PDF（僅英文）
  * 自動解析、清洗、切分並建立向量資料庫
  * 依據檢索結果生成摘要與關鍵技術/章節內容

* **Web Search**

  * DuckDuckGo 搜尋，補充 RAG 資料


## 安裝與執行

### 1. 下載專案

```bash
git clone https://github.com/Yogsothoth2411/LangGraph-RAG-Demo.git
cd LangGraph-RAG-Demo
```

### 2. 環境準備

1. 建立 `.env` 檔案：

```bash
cp .env.example .env
```

並依需求修改參數。

2. 使用 uv 管理環境：

```bash
uv add -r requirements.txt
```

3. 安裝 Ollama 並下載模型：

```bash
ollama pull gemma3:12b-it-qat
ollama pull gemma3:4b
ollama pull embeddinggemma
```

### 3. 執行方式

1. 先使用 Docker + docker-compose：

```bash
docker-compose up -d
```

2. 再使用 uv 執行：

```bash
uv run main.py
```


## 更換模型

若要更換模型（例如切換成 gpt-ss:20b）：

1. 修改 `.env`：

   ```python
   # ollama model
    LLM_MODEL = "gemma3:12b-it-qat"
    LLM_MODEL_SMALL = "gemma3:4b"
    EMBED_MODEL = "embeddinggemma"
   ```

2. 下載新模型：

   ```bash
   ollama pull XXXX
   ```



## 注意事項

* 目前僅支援英文 PDF
* 文件過大或 PDF 中多個短元素可能影響 RAG 檢索效果
* 請確保 `.env` 設定正確，以便 API 與模型運行
