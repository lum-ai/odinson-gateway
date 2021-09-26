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

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError

    @classmethod
    def from_json(cls, string):
        return cls.from_dict(json.loads(string))


@dataclass
class Field(Base):
    type: str = field(init=False)
    name: str

    @classmethod
    def from_dict(cls, data):
        field_type = data.get("$type")
        if field_type == "ai.lum.odinson.TokensField":
            return TokensField.from_dict(data)
        elif field_type == "ai.lum.odinson.GraphField":
            return GraphField.from_dict(data)
        elif field_type == "ai.lum.odinson.StringField":
            return StringField.from_dict(data)
        elif field_type == "ai.lum.odinson.DateField":
            return DateField.from_dict(data)
        elif field_type == "ai.lum.odinson.NumberField":
            return NumberField.from_dict(data)
        elif field_type == "ai.lum.odinson.NestedField":
            return NestedField.from_dict(data)
        else:
            raise Exception(f"unsupported field type {field_type!r}")


@dataclass
class TokensField(Field):
    tokens: list[str]

    def __post_init__(self):
        self.type = "ai.lum.odinson.TokensField"

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["tokens"])


@dataclass
class GraphField(Field):
    edges: list[list[int, int, str]]
    roots: list[int]

    def __post_init__(self):
        self.type = "ai.lum.odinson.GraphField"

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["edges"], data["roots"])


@dataclass
class StringField(Field):
    string: str

    def __post_init__(self):
        self.type = "ai.lum.odinson.StringField"

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["string"])


@dataclass
class DateField(Field):
    date: str

    def __post_init__(self):
        self.type = "ai.lum.odinson.DateField"

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["date"])


@dataclass
class NumberField(Field):
    value: float

    def __post_init__(self):
        self.type = "ai.lum.odinson.NumberField"

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["value"])


@dataclass
class NestedField(Field):
    fields: list[Field]

    def __post_init__(self):
        self.type = "ai.lum.odinson.NestedField"

    @classmethod
    def from_dict(cls, data):
        name = data["name"]
        fields = [Field.from_dict(f) for f in data["fields"]]
        return cls(name, fields)


@dataclass
class Sentence(Base):
    numTokens: int
    fields: list[Field]

    @classmethod
    def from_dict(cls, data):
        numTokens = data["numTokens"]
        fields = [Field.from_dict(f) for f in data["fields"]]
        return cls(numTokens, fields)


@dataclass
class Document(Base):
    id: str
    metadata: list[Field]
    sentences: list[Sentence]

    @classmethod
    def from_dict(cls, data):
        id = data["id"]
        metadata = [Field.from_dict(f) for f in data["metadata"]]
        sentences = [Sentence.from_dict(s) for s in data["sentences"]]
        return cls(id, metadata, sentences)
