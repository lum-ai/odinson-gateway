from typing import Optional
from .results import OdinsonResults

JAVA_MAX_INT = 2 ** 31 - 1


class ExtractorEngine:
    def __init__(self, extractor_engine):
        self.extractor_engine = extractor_engine

    def num_docs(self) -> int:
        """
        Returns the number of lucene documents in the index.
        Note that not all lucene documents correspond to sentences,
        some contain only metadata.
        """
        return self.extractor_engine.numDocs()

    def search(
        self,
        pattern: str,
        filter: Optional[str] = None,
        max_hits: Optional[int] = None,
        disable_match_selector: bool = False,
    ) -> OdinsonResults:
        if max_hits is None:
            max_hits = JAVA_MAX_INT
        if filter is None:
            query = self.extractor_engine.mkQuery(pattern)
        else:
            query = self.extractor_engine.mkQuery(pattern, filter)
        res = self.extractor_engine.query(query, max_hits, disable_match_selector)
        return OdinsonResults.from_scala(res)
