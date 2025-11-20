from langchain_community.document_loaders import UnstructuredPDFLoader
import os
from pathlib import Path
from typing import List
from data.model import PDFElementMetadata, PDFElement


def load_pdf_elements(pdf_path: str | os.PathLike) -> List[PDFElement]:
    """載入PDF並拆分成elements"""
    pdf_path = Path(pdf_path)
    # 載入PDF
    pdf_loader = UnstructuredPDFLoader(
        pdf_path,
        mode="elements",
        unstructured_kwargs={
            "ocr_languages": ["eng"],  # 需要 Tesseract
            "extract_images_in_pdf": True,
            "chunking_strategy": "by_page",
        },
    )
    # 使用pydantic model 格式放載入資料
    elements = [
        PDFElement(
            page_content=doc.page_content, metadata=PDFElementMetadata(**doc.metadata)
        )
        for doc in pdf_loader.load()
    ]

    return elements
