from .results import OdinsonResults


class ExtractorEngine:
    def __init__(self, extractor_engine):
        self.extractor_engine = extractor_engine

    def search(self, pattern: str) -> OdinsonResults:
        query = self.extractor_engine.mkQuery(pattern)
        res = self.extractor_engine.query(query)
        return OdinsonResults.from_scala(res)
