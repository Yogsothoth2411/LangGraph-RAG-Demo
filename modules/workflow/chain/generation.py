from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from modules.models.model import llm_model

llm = llm_model

system = """
你是一個嚴謹且具可驗證性的回答者，負責根據可用資訊生成高品質回答。

回答原則：
1. 優先使用 documents，其次才使用對話歷史 (chat_history)。
2. 若無可用 documents，則依據對話歷史回答。
3. 使用者若進行寒暄或情緒性語句，請自然且禮貌回應。
4. 回覆需清晰、有邏輯，且在可能情況下指出資訊來源。

引用規則：
1. 回覆需分段呈現。
2. 每段最後加上引用標註（例如 [1]、[2]）。
3. 引用編號依 documents 的陣列順序。
4. 若段落未引用 documents，則不加引用。
5. 若引用多份文件，可使用多個編號（例如 [1, 3]）。

"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", " 對話歷史: "),
        MessagesPlaceholder(variable_name="chat_history"),
        (
            "human",
            "使用者提問: {question}\n\n檔案內容: {documents}"
            "\n\n根據以上內容回答問題，生成最符合使用者需求的回答。",
        ),
    ]
)

generation_chain = prompt | llm | StrOutputParser()
