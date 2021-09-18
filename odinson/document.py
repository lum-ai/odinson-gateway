from dataclasses import dataclass, asdict


class Base:
    def asdict(self):
        return asdict(self)


@dataclass
class Field(Base):
    name: str


@dataclass
class TokensField(Field):
    tokens: list[str]


@dataclass
class GraphField(Field):
    edges: list[tuple[int, int, str]]
    roots: list[int]


@dataclass
class Sentence(Base):
    n_tokens: int
    fields: list[Field]


@dataclass
class Document(Base):
    id: str
    metadata: list[Field]
    sentences: list[Sentence]
