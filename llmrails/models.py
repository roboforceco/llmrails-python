from enum import Enum
from typing import List
from dataclasses import dataclass

class ModelChoices(str, Enum):
    embedding_english_v1 = 'embedding-english-v1'
    embedding_multi_v1 = 'embedding-multi-v1'

@dataclass
class Datastore():
    status: str


@dataclass
class Embedding():
    object: str
    index: int
    embedding: List[float]


@dataclass
class Embeddings():
    object: str
    data: List[Embedding]
    model: str
    usage: dict
