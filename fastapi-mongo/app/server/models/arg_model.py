from typing import List
from pydantic import BaseModel, Field


class MongoBase(BaseModel):
    database: str
    collection: str


class Args(BaseModel):
    Object_1: int
    X_1: List[int]
    Y_1: List[int]
    Z_1: List[int]
    Object_2: int
    X_2: List[int]
    Y_2: List[int]
    Z_2: List[int]


class Document(BaseModel):
    number: int
    args: Args


class Model(BaseModel):
    database: str
    collection: str
    Document: Document
