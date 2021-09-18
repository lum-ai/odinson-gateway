from dataclasses import dataclass, field, asdict


class Base:
    def to_dict(self):
        return asdict(self)


@dataclass
class Field(Base):
    type: str = field(init=False)
    name: str


@dataclass
class TokensField(Field):
    tokens: list[str]

    def __post_init__(self):
        self.type = "ai.lum.odinson.TokensField"


@dataclass
class GraphField(Field):
    edges: list[list[int, int, str]]
    roots: list[int]

    def __post_init__(self):
        self.type = "ai.lum.odinson.GraphField"


@dataclass
class Sentence(Base):
    numTokens: int
    fields: list[Field]


@dataclass
class Document(Base):
    id: str
    metadata: list[Field]
    sentences: list[Sentence]
