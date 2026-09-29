from __future__ import annotations

import numpy as np
from sklearn.preprocessing import MinMaxScaler

# This is deliberately a transparent screening heuristic, not a trained fraud classifier.
# Scikit-learn is used to normalize the OpenCV signal ranges before a weighted calibration.
_BOUNDS = np.array([
    [0.0, 0.0, 0.0, 0.0],
    [18.0, 350.0, 25.0, 0.35],
])
_SCALER = MinMaxScaler(clip=True).fit(_BOUNDS)


def deterministic_risk(forensics: dict, ocr: dict) -> int:
    agg = forensics.get("aggregate") or {}
    x = np.array([[
        float(agg.get("ela_mean", 0)),
        float(agg.get("sharpness", 0)),
        float(agg.get("noise", 0)),
        float(agg.get("edge_density", 0)),
    ]])
    ela, sharp, noise, edge = _SCALER.transform(x)[0]
    blur_risk = 1.0 - sharp
    ocr_risk = 0.18 if ocr.get("engine") == "unavailable" else (0.12 if len(ocr.get("text", "")) < 30 else 0.0)
    score = (0.32 * ela + 0.24 * blur_risk + 0.18 * noise + 0.14 * edge + ocr_risk) * 100
    return int(round(max(0, min(100, score))))


def combine_risk(deterministic: int, gemini_score: int, confidence: float) -> int:
    confidence = max(0.0, min(1.0, float(confidence)))
    gemini_weight = 0.35 + (0.20 * confidence)
    deterministic_weight = 1.0 - gemini_weight
    return int(round(max(0, min(100, deterministic * deterministic_weight + gemini_score * gemini_weight))))


def risk_level(score: int) -> str:
    if score >= 70:
        return "High"
    if score >= 35:
        return "Medium"
    return "Low"
