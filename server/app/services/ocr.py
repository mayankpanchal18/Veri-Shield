from __future__ import annotations

import io
import re
from typing import Any

import cv2
import fitz
import numpy as np
from PIL import Image
import pytesseract

from ..core.config import settings

if settings.tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

DATE_RE = re.compile(r"\b(?:0?[1-9]|[12]\d|3[01])[-/.](?:0?[1-9]|1[0-2])[-/.](?:19|20)\d{2}\b")
ID_RE = re.compile(r"\b[A-Z0-9][A-Z0-9 -]{5,20}[A-Z0-9]\b", re.I)


def file_to_images(data: bytes, mime_type: str, max_pages: int = 3) -> list[np.ndarray]:
    images: list[np.ndarray] = []
    if mime_type == "application/pdf":
        doc = fitz.open(stream=data, filetype="pdf")
        for page_no in range(min(len(doc), max_pages)):
            page = doc.load_page(page_no)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            if pix.n == 4:
                arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
            else:
                arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
            images.append(arr)
    else:
        pil = Image.open(io.BytesIO(data)).convert("RGB")
        arr = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
        images.append(arr)
    return images


def _preprocess(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 7, 50, 50)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11)


def _extract_basic_fields(text: str) -> dict[str, Any]:
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]
    dates = DATE_RE.findall(text)

    name = ""
    for i, line in enumerate(lines):
        if re.search(r"\b(name|holder|full name)\b", line, re.I):
            candidate = re.sub(r"(?i).*?\b(name|holder|full name)\b\s*[:\-]?\s*", "", line).strip()
            if candidate and len(candidate) > 2:
                name = candidate[:120]
                break
            if i + 1 < len(lines):
                name = lines[i + 1][:120]
                break

    document_number = ""
    for line in lines:
        if re.search(r"\b(id|document|licen[cs]e|passport|aadhaar|number|no\.)\b", line, re.I):
            candidates = [m.group(0).strip() for m in ID_RE.finditer(line)]
            candidates = [x for x in candidates if not re.fullmatch(r"[A-Z ]+", x)]
            if candidates:
                document_number = max(candidates, key=len)[:80]
                break

    return {
        "full_name": name,
        "dates_detected": dates[:12],
        "document_number_candidate": document_number,
        "line_count": len(lines),
    }


def run_ocr(images: list[np.ndarray]) -> dict[str, Any]:
    texts: list[str] = []
    warnings: list[str] = []
    engine = "tesseract"

    for img in images:
        try:
            text = pytesseract.image_to_string(_preprocess(img), config="--psm 6")
        except pytesseract.TesseractNotFoundError:
            engine = "unavailable"
            warnings.append("Tesseract executable was not found. Gemini can still inspect the document, but local OCR is unavailable.")
            break
        except Exception as exc:
            warnings.append(f"OCR page failed: {type(exc).__name__}")
            continue
        texts.append(text)

    combined = "\n".join(texts).strip()
    fields = _extract_basic_fields(combined) if combined else {
        "full_name": "", "dates_detected": [], "document_number_candidate": "", "line_count": 0
    }
    return {
        "engine": engine,
        "text": combined,
        "fields": fields,
        "warnings": warnings,
    }
