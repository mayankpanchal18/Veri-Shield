from __future__ import annotations

import cv2
import numpy as np


def _ela_mean(image: np.ndarray, quality: int = 90) -> float:
    ok, encoded = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not ok:
        return 0.0
    recompressed = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    diff = cv2.absdiff(image, recompressed)
    return float(np.mean(diff))


def analyze_forensics(images: list[np.ndarray]) -> dict:
    pages = []
    for idx, img in enumerate(images, start=1):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = float(laplacian.var())

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        noise = float(np.std(gray.astype(np.float32) - blurred.astype(np.float32)))
        edges = cv2.Canny(gray, 80, 180)
        edge_density = float(np.count_nonzero(edges) / edges.size)
        ela = _ela_mean(img)

        flags = []
        if sharpness < 55:
            flags.append("Low sharpness / blur may reduce reliability")
        if ela > 11:
            flags.append("Elevated JPEG recompression difference (ELA heuristic)")
        if noise > 16:
            flags.append("High local noise residual")
        if edge_density > 0.28:
            flags.append("Unusually dense edge pattern")

        pages.append({
            "page": idx,
            "width": int(img.shape[1]),
            "height": int(img.shape[0]),
            "ela_mean": round(ela, 3),
            "sharpness": round(sharpness, 3),
            "noise": round(noise, 3),
            "edge_density": round(edge_density, 4),
            "flags": flags,
        })

    if not pages:
        return {"pages": [], "aggregate": {}, "flags": ["No image pages could be analyzed"]}

    aggregate = {
        "ela_mean": round(float(np.mean([p["ela_mean"] for p in pages])), 3),
        "sharpness": round(float(np.mean([p["sharpness"] for p in pages])), 3),
        "noise": round(float(np.mean([p["noise"] for p in pages])), 3),
        "edge_density": round(float(np.mean([p["edge_density"] for p in pages])), 4),
    }
    flags = [flag for page in pages for flag in page["flags"]]
    return {"pages": pages, "aggregate": aggregate, "flags": sorted(set(flags))}
