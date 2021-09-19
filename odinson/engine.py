from typing import Optional
from .results import OdinsonResults


class ExtractorEngine:
    def __init__(self, extractor_engine):
        self.extractor_engine = extractor_engine

    def num_docs(self) -> int:
        return self.extractor_engine.numDocs()

    def search(
        self,
        pattern: str,
        max_hits: Optional[int] = None,
        disable_match_selector: bool = False,
    ) -> OdinsonResults:
        if max_hits is None:
            max_hits = self.num_docs()
        query = self.extractor_engine.mkQuery(pattern)
        res = self.extractor_engine.query(query, max_hits, disable_match_selector)
        return OdinsonResults.from_scala(res)
