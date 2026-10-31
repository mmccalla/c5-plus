"""Compile English to a closed Query IR via gazetteer and intent patterns."""

from __future__ import annotations

import json
import re
from typing import Any

from ask.json_to_rdf import DEFAULT_JSON

# Group 1 is the seed phrase so intent cue words (e.g. node id "impact") are not gazetted.
INTENT_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"\bwhat does(?:\s+the)?\s+(.+?)\s+depend on\b", re.IGNORECASE),
        "depends_on",
    ),
    (
        re.compile(r"\bwhat depends on(?:\s+the)?\s+(.+?)\s*[.?]?\s*$", re.IGNORECASE),
        "dependents",
    ),
    (
        re.compile(r"\bwho depends on(?:\s+the)?\s+(.+?)\s*[.?]?\s*$", re.IGNORECASE),
        "dependents",
    ),
    (
        re.compile(r"\bdependents of(?:\s+the)?\s+(.+?)\s*[.?]?\s*$", re.IGNORECASE),
        "dependents",
    ),
    (re.compile(r"\bwho owns(?:\s+the)?\s+(.+?)\s*[.?]?\s*$", re.IGNORECASE), "owns"),
    (
        re.compile(
            r"\bwhich policies apply to(?:\s+the)?\s+(.+?)\s*[.?]?\s*$", re.IGNORECASE
        ),
        "policies",
    ),
    (
        re.compile(
            r"\bwhat policies apply to(?:\s+the)?\s+(.+?)\s*[.?]?\s*$", re.IGNORECASE
        ),
        "policies",
    ),
    (
        re.compile(
            r"\bhow is(?:\s+the)?\s+(.+?)\s+reali(?:s|z)(?:ed|ation)\b", re.IGNORECASE
        ),
        "realisation",
    ),
    (
        re.compile(
            r"\bwhat happens after(?:\s+the)?\s+(.+?)\s*[.?]?\s*$", re.IGNORECASE
        ),
        "sequence",
    ),
    (
        re.compile(
            r"\bwhat happens next(?:\s+the)?\s+(.+?)\s*[.?]?\s*$", re.IGNORECASE
        ),
        "sequence",
    ),
    (
        re.compile(
            r"\bwhat (?:will be|is|gets) impacted if (?:I |we )?change(?:\s+the)?\s+(.+?)\s*[.?]?\s*$",
            re.IGNORECASE,
        ),
        "impact",
    ),
    (
        re.compile(
            r"\bwhat will changing(?:\s+the)?\s+(.+?)\s+impact\b", re.IGNORECASE
        ),
        "impact",
    ),
    (
        re.compile(
            r"\bimpact of changing(?:\s+the)?\s+(.+?)\s*[.?]?\s*$", re.IGNORECASE
        ),
        "impact",
    ),
)


def _node_ids() -> dict[str, str]:
    data = json.loads(DEFAULT_JSON.read_text(encoding="utf-8"))
    return {node["id"].casefold(): node["id"] for node in data["nodes"]}


_NODES = _node_ids()


def _bounded(text: str, start: int, end: int) -> bool:
    if start > 0 and text[start - 1].isalnum():
        return False
    return not (end < len(text) and text[end].isalnum())


def _gazetteer_hits(question: str) -> list[str]:
    text = question.casefold()
    matches: list[tuple[int, int, str]] = []
    for folded, canonical in _NODES.items():
        start = 0
        while True:
            idx = text.find(folded, start)
            if idx < 0:
                break
            end = idx + len(folded)
            if _bounded(text, idx, end):
                matches.append((idx, end, canonical))
            start = idx + 1
    matches.sort(key=lambda item: (-(item[1] - item[0]), item[0]))
    chosen: list[tuple[int, int, str]] = []
    for start, end, canonical in matches:
        if any(start < kept[1] and end > kept[0] for kept in chosen):
            continue
        chosen.append((start, end, canonical))
    chosen.sort(key=lambda item: item[0])
    return list(dict.fromkeys(canonical for _, _, canonical in chosen))


def _intent_matches(question: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    seen: set[str] = set()
    for pattern, intent in INTENT_PATTERNS:
        match = pattern.search(question)
        if match and intent not in seen:
            seen.add(intent)
            found.append((intent, match.group(1)))
    return found


def _miss(error: str, candidates: list[str]) -> dict[str, Any]:
    return {"error": error, "candidates": candidates}


def compile(q: str) -> dict[str, Any]:
    """Return {intent, seed} or a miss with candidates. Never hops; never execute."""
    matches = _intent_matches(q)
    if not matches:
        return _miss("Unknown intent", _gazetteer_hits(q))
    if len(matches) != 1:
        candidates = list(
            dict.fromkeys(
                hit for _, phrase in matches for hit in _gazetteer_hits(phrase)
            )
        )
        return _miss("Ambiguous intent", candidates)
    intent, phrase = matches[0]
    seeds = _gazetteer_hits(phrase)
    if len(seeds) != 1:
        error = "Ambiguous seed" if seeds else "No matching seed"
        return _miss(error, seeds)
    return {"intent": intent, "seed": seeds[0]}
