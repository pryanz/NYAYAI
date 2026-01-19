from typing import List, Dict


def reconstruct_text(ocr_blocks: List[Dict]) -> str:
    if not ocr_blocks:
        return ""

    lines = [b["text"] for b in ocr_blocks]
    return "\n".join(lines)
