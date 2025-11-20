from typing import List
from data.model import PDFElement


def clean_elements(elements: List[PDFElement]) -> List[PDFElement]:
    """清洗elements中的內容，去除無法辨識/重複 資料"""
    # 去除無法辨識的內容
    drop_categories = {"Title","Header", "Footer", "UncategorizedText"}

    cleaned_elements = [
        e for e in elements
        if e.metadata.category not in drop_categories
        and e.page_content.strip()
    ]

    # 去除重複內容
    seen_contents = set()
    unique_elements = []

    for e in cleaned_elements:
        content_key = e.page_content.strip()
        if content_key and content_key not in seen_contents:
            seen_contents.add(content_key)
            unique_elements.append(e)

    return unique_elements
