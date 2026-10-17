"""Small lexical Markdown retriever with content-versioned exact-query caching."""

from __future__ import annotations

import hashlib
import re
from functools import lru_cache
from pathlib import Path
from typing import Iterable

_WORDS = re.compile(r"[a-z0-9]+")


def _snapshot(directory: str) -> tuple[tuple[str, str, str], ...]:
    root = Path(directory)
    records = []
    for path in sorted(root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        records.append((path.name, digest, text))
    return tuple(records)


@lru_cache(maxsize=256)
def _search_snapshot(
    snapshot: tuple[tuple[str, str, str], ...], query: str, limit: int
) -> tuple[dict[str, str | int], ...]:
    query_terms = set(_WORDS.findall(query.lower()))
    if not query_terms:
        return ()
    results: list[tuple[int, str, str]] = []
    for filename, _digest, text in snapshot:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for paragraph in paragraphs:
            terms = set(_WORDS.findall(paragraph.lower()))
            score = len(query_terms & terms)
            if score:
                results.append((score, filename, paragraph[:900]))
    results.sort(key=lambda row: (-row[0], row[1], row[2]))
    return tuple(
        {"source": filename, "score": score, "excerpt": excerpt}
        for score, filename, excerpt in results[:limit]
    )


def search_knowledge_base(query: str, directory: str, limit: int = 3) -> dict[str, object]:
    """Search local Markdown and cache exact-query results for this corpus version."""
    if not query.strip():
        return {"query": query, "results": []}
    limit = min(max(limit, 1), 5)
    snapshot = _snapshot(directory)
    results = _search_snapshot(snapshot, query.strip().lower(), limit)
    return {"query": query, "results": list(results)}


def clear_search_cache() -> None:
    """Clear process-local retrieval results (useful in tests and demos)."""
    _search_snapshot.cache_clear()


def search_cache_info() -> object:
    return _search_snapshot.cache_info()
