# Screening model / evidence pipeline

VeriShield's "model" is a layered screening system rather than one opaque classifier.

1. **OCR:** Tesseract attempts local text extraction and produces basic field candidates.
2. **Image forensics:** OpenCV measures ELA recompression difference, sharpness, noise residual and edge density. These are heuristic signals and are not treated as proof of tampering.
3. **Signal calibration:** scikit-learn `MinMaxScaler` normalizes known metric ranges into a transparent deterministic risk signal.
4. **Gemini multimodal reasoning:** Gemini receives the original document plus the OCR/forensic evidence and outputs structured checks, extracted visible fields, suspicious signals, confidence and reviewer guidance.
5. **Combined screening risk:** the local score and Gemini score are combined with Gemini weighting moderated by reported confidence.
6. **Human review:** final validity is never inferred from the risk score. A reviewer sees the evidence and makes the decision.
7. **Tamper-evident record:** SHA-256 document/event hashes form a revision chain, with optional EVM anchoring.

This structure directly supports the PPT's claim that Gemini receives OCR/forensic signals and produces reviewer-facing reasoning.
