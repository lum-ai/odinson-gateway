from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Union, Optional
from py4j.java_gateway import JavaGateway, GatewayParameters, launch_gateway
from .document import Document
from .engine import ExtractorEngine


PathLike = Union[str, Path]


class OdinsonGateway:
    def __init__(self, gateway):
        self.gateway = gateway
        self.entry_point = self.gateway.jvm.odinson.EntryPoint()

    @classmethod
    def launch(
        cls, classpath: Optional[str] = None, javaopts: list[str] = []
    ) -> OdinsonGateway:
        """Starts the JVM and establishes a connection to it."""
        if classpath is None:
            classpath = find_jar_path()
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

    def index_document(self, document: Document, path: Optional[PathLike] = None):
        self.index_documents([document], str(path))

    def index_documents(self, documents: list[Document], path: Optional[PathLike] = None):
        data = [d.to_dict() for d in documents]
        if path is None:
            self.entry_point.indexDocuments(data)
        else:
            self.entry_point.indexDocuments(str(path), data)

    def open_index(self, path: Optional[PathLike] = None) -> ExtractorEngine:
        """Opens an existing index."""
        if path is None:
            ee = self.entry_point.mkExtractorEngine()
        else:
            ee = self.entry_point.mkExtractorEngine(str(path))
        return ExtractorEngine(ee)

    def open_memory_index(self, documents: list[Document]) -> ExtractorEngine:
        """Creates a memory index with the provided documents."""
        data = [d.to_dict() for d in documents]
        ee = self.entry_point.mkMemoryIndex(data)
        return ExtractorEngine(ee)


def find_jar_path():
    """Returns the path to the jar, or an empty string if the jar
    is not found in the usual locations."""
    jar_file = "odinson-entrypoint.jar"
    paths = []
    # this path works for conda
    paths.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "..",
            "share",
            "odinson",
            jar_file,
        )
    )
    paths.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "..",
            "..",
            "..",
            "..",
            "share",
            "odinson",
            jar_file,
        )
    )
    paths.append(os.path.join(sys.prefix, "share", "odinson", jar_file))
    # this path is useful when working in the repo
    paths.append(os.path.join("odinson-entrypoint", "target", "scala-2.12", jar_file))
    # look for the jar in the list of candidate paths
    for path in paths:
        if os.path.exists(path):
            return os.path.normpath(path)
    # can't find the jar
    return ""
