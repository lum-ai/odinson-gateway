from __future__ import annotations
import os
from typing import Optional
from py4j.java_gateway import JavaGateway, GatewayParameters, launch_gateway
from .document import Document
from .engine import ExtractorEngine


class OdinsonGateway:
    def __init__(self, gateway):
        self.gateway = gateway
        self.entry_point = self.gateway.jvm.odinson.EntryPoint()

    @classmethod
    def launch_gateway(
        cls, classpath: Optional[str] = None, javaopts: list[str] = []
    ) -> OdinsonGateway:
        if classpath is None:
            classpath = find_jar()
        port, proc = launch_gateway(
            classpath=classpath,
            javaopts=javaopts,
            return_proc=True,
            die_on_exit=True,
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


def find_jar():
    dev_jar = "scala-gateway/target/scala-2.12/odinson-entrypoint.jar"
    if os.path.exists(dev_jar):
        return dev_jar
