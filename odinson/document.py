from dataclasses import dataclass, field, asdict
import json


def dict_factory(data):
    result = dict()
    for k, v in data:
        if k == "type":
            # replace type with $type to match scala odinson documents
            k = "$type"
        result[k] = v
    return result


class Base:
    def to_dict(self):
        return asdict(self, dict_factory=dict_factory)

    def to_json(self):
        return json.dumps(self.to_dict())


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
