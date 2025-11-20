from data.ingestion import create_vectorstore_pipeline
from data.store import delete_chunks_by_path, clear_all_chunks
from pathlib import Path
from typing import Union, List
from fastapi import HTTPException, APIRouter, BackgroundTasks
from pydantic import BaseModel

router = APIRouter()

class PdfRequest(BaseModel):
    pdf_paths: List[Union[str, Path]]

class PdfDelete(BaseModel):
    pdf_paths: Union[str, Path]

@router.post("/load_pdf")
def load_pdf(req: PdfRequest, background_tasks: BackgroundTasks):
    # 檢查檔案是否存在（同步檢查）
    for p in req.pdf_paths:
        if not Path(p).exists():
            raise HTTPException(status_code=404, detail=f"File not found: {p}")

    # 確認無誤後才丟背景
    background_tasks.add_task(create_vectorstore_pipeline, req.pdf_paths)

    return {"status": "accepted", "message": "PDF is being processed in background"}

@router.delete("/remove_chunk")
def remove_chunk(req: PdfDelete, background_tasks: BackgroundTasks):
    # 檢查檔案是否存在（同步檢查）
    if not Path(req.pdf_paths).exists():
        raise HTTPException(status_code=404, detail=f"File not found: {req.pdf_paths}")

    # 確認無誤後才丟背景
    background_tasks.add_task(delete_chunks_by_path, req.pdf_paths)

    return {"status": "accepted", "message": "PDF is being delete in background"}

@router.delete("/remove_index")
def clear_index(background_tasks: BackgroundTasks):

    background_tasks.add_task(clear_all_chunks)

    return {"status": "accepted", "message": "PDF List is being delete in background"}