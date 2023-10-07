from enum import Enum
from typing import List, Optional
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

@dataclass
class ItemMetadata():
    type: str
    url: str
    name: str
    score: float


@dataclass
class SearchResult():
    text: str
    metadata: ItemMetadata


@dataclass
class SearchResults():
    results: List[SearchResult]
    summarization: Optional[str] = None



@dataclass
class ChatResult():
    id: str
    text: str
    session_id: str
    docs: Optional[List[ItemMetadata]] = None