from py4j.java_gateway import JavaGateway
from .document import Document


class Odinson:
    def __init__(self) -> None:
        self.gateway = JavaGateway()

    def make_memory_index(self, documents: list[Document]):
        return self.gateway.entry_point.make_memory_index(documents)
