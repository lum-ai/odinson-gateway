from typing import Optional
from py4j.java_gateway import JavaGateway, GatewayParameters, launch_gateway
from .document import Document
from .engine import ExtractorEngine


class OdinsonGateway:
    def __init__(self, gateway):
        self.gateway = gateway
        self.entry_point = self.gateway.jvm.odinson.EntryPoint()

    @classmethod
    def launch_gateway(cls, classpath="", javaopts=[]):
        # classpath="scala-gateway/target/scala-2.12/scala-gateway-assembly-0.1.0-SNAPSHOT.jar"
        port, proc = launch_gateway(
            classpath=classpath, javaopts=javaopts, return_proc=True
        )
        gateway = JavaGateway(
            gateway_parameters=GatewayParameters(port=port, auto_convert=True),
            java_process=proc,
        )
        return cls(gateway)

    def make_index(self, path: Optional[str] = None) -> ExtractorEngine:
        if path is None:
            ee = self.entry_point.mkIndex()
        else:
            ee = self.entry_point.mkIndex(path)
        return ExtractorEngine(ee)

    def make_memory_index(self, documents: list[Document]) -> ExtractorEngine:
        data = [d.to_dict() for d in documents]
        ee = self.entry_point.mkMemoryIndex(data)
        return ExtractorEngine(ee)
