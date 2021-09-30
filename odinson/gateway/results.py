from __future__ import annotations
from dataclasses import dataclass
from py4j.java_gateway import get_field


@dataclass
class OdinsonResults:
    total_hits: int
    docs: list[ScoreDoc]

    @classmethod
    def from_scala(cls, res):
        total_hits = res.totalHits()
        docs = [ScoreDoc.from_scala(d) for d in res.scoreDocs()]
        return cls(total_hits, docs)


@dataclass
class ScoreDoc:
    doc: int
    score: float
    matches: list[OdinsonMatch]

    @classmethod
    def from_scala(cls, score_doc):
        doc = get_field(score_doc, "doc")
        score = get_field(score_doc, "score")
        matches = [OdinsonMatch.from_scala(m) for m in score_doc.matches()]
        return cls(doc, score, matches)


@dataclass
class OdinsonMatch:
    start: int
    end: int
    named_captures: list[NamedCapture]

    @classmethod
    def from_scala(cls, match):
        start = match.start()
        end = match.end()
        named_captures = [NamedCapture.from_scala(c) for c in match.namedCaptures()]
        return cls(start, end, named_captures)


@dataclass
class NamedCapture:
    name: str
    match: OdinsonMatch

    @classmethod
    def from_scala(cls, capture):
        name = capture.name()
        match = capture.capturedMatch()
        return cls(name, OdinsonMatch.from_scala(match))
