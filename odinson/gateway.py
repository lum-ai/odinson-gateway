from typing import Optional
from py4j.java_gateway import JavaGateway, GatewayParameters
from .document import Document
from .engine import ExtractorEngine


class OdinsonGatewayClient:
    def __init__(self):
        self.gateway = JavaGateway(
            gateway_parameters=GatewayParameters(auto_convert=True)
        )

    def make_index(self, path: Optional[str] = None) -> ExtractorEngine:
        if path is None:
            ee = self.gateway.entry_point.mkIndex()
        else:
            ee = self.gateway.entry_point.mkIndex(path)
        return ExtractorEngine(ee)

    def make_memory_index(self, documents: list[Document]) -> ExtractorEngine:
        data = [d.to_dict() for d in documents]
        ee = self.gateway.entry_point.mkMemoryIndex(data)
        return ExtractorEngine(ee)
