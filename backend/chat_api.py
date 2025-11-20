from modules.graph import app
from langchain_core.messages import HumanMessage
from modules.state import Mode
from data.model import merge_documents_for_grader_md
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    user_input: str
    mode:Mode


@router.post("/chat_response")
def chat_response(question:ChatRequest):
    try:
        config = {"configurable": {"thread_id": "abc123"}}
        result = app.invoke(
            {
                "question": question.user_input,
                "chat_history": HumanMessage(content=question.user_input),
                "mode": question.mode,
                "documents":[],
            },
            config,
        )
        # question = result["question"]
        # query = result["query"]
        # chat_history = result["chat_history"]
        documents = merge_documents_for_grader_md(result["documents"])
        generation = result["generation"]
        states = list(app.get_state_history(config))
        selected_state = states[-2]
        
        return {"status": "success", "message": "chat response success", "generation":generation,"documents":documents,"selected_state":selected_state}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {e}")