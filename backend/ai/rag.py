"""Minimal local RAG pipeline using simple embeddings and JSON storage."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any


class LocalRagPipeline:
    def __init__(self, storage_path: str | Path | None = None) -> None:
        self.storage_path = Path(storage_path or "./.rag_store.json")
        self.documents: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if self.storage_path.exists():
            try:
                self.documents = json.loads(self.storage_path.read_text(encoding="utf-8"))
            except Exception:
                self.documents = []

    def _save(self) -> None:
        self.storage_path.write_text(json.dumps(self.documents, indent=2), encoding="utf-8")

    def index_documents(self, texts: list[str]) -> None:
        for text in texts:
            self.documents.append({"text": text, "embedding": self._simple_embedding(text)})
        self._save()

    def retrieve(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        query_embedding = self._simple_embedding(query)
        scored = []
        for item in self.documents:
            score = self._cosine_similarity(query_embedding, item["embedding"])
            scored.append((score, item))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [{"text": item["text"], "score": round(score, 4)} for score, item in scored[:top_k] if score > 0]

    def _simple_embedding(self, text: str) -> list[float]:
        lowered = text.lower()
        tokens = [token for token in re.findall(r"[a-z0-9]+", lowered) if token]
        vector = {}
        for token in tokens:
            vector[token] = vector.get(token, 0) + 1.0
        return [vector.get(token, 0.0) for token in sorted(vector)]

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        if not left or not right:
            return 0.0
        if len(left) != len(right):
            right = right[: len(left)]
        numerator = sum(a * b for a, b in zip(left, right))
        left_norm = math.sqrt(sum(a * a for a in left))
        right_norm = math.sqrt(sum(b * b for b in right))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return numerator / (left_norm * right_norm)
