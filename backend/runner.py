from fastapi import FastAPI
from backend.pdf_api import router as pdf_router
from backend.chat_api import router as chat_router

app = FastAPI()
app.include_router(pdf_router, prefix="/pdf", tags=["PDF"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
