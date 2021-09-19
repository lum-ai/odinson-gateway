from py4j.java_gateway import JavaGateway, GatewayParameters
from .document import Document
from .engine import ExtractorEngine


class OdinsonGatewayClient:
    def __init__(self) -> None:
        self.gateway = JavaGateway(
            gateway_parameters=GatewayParameters(auto_convert=True)
        )

    def make_memory_index(self, documents: list[Document]):
        data = [d.to_dict() for d in documents]
        ee = self.gateway.entry_point.mkMemoryIndex(data)
        return ExtractorEngine(ee)
