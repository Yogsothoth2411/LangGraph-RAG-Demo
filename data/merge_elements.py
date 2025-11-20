from typing import List
from data.model import PDFElement, PDFElementMetadata


def merge_elements(elements: List[PDFElement]) -> List[PDFElement]:
    merged: List[PDFElement] = []
    buffer_list = []

    for e in elements:
        cat = e.metadata.category

        # 收集 ListItem
        if cat == "ListItem":
            buffer_list.append(e.page_content.strip())
            continue

        # NarrativeText：合併 ListItem + NarrativeText 本身
        if cat == "NarrativeText":
            text_parts = []
            meta = e.metadata  # NarrativeText metadata 為主

            if buffer_list:
                text_parts.extend(buffer_list)
                buffer_list = []

            text_parts.append(e.page_content.strip())
            new_text = "\n".join(text_parts)

            new_meta_dict = meta.model_dump()
            new_meta_dict["element_id"] = f"{meta.element_id}_merged"
            new_meta = PDFElementMetadata(**new_meta_dict)

            merged.append(PDFElement(
                page_content=new_text,
                metadata=new_meta
            ))
            continue

    # 最後若還有 list，獨立成段
    if buffer_list:
        text = "\n".join(buffer_list)
        last_meta = elements[-1].metadata.model_copy()
        last_meta.element_id = f"{last_meta.element_id}_listonly"
        merged.append(PDFElement(page_content=text, metadata=last_meta))

    return merged
