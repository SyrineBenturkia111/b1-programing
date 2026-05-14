from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    age: int


class User(BaseModel):
    id: int
    name: str
    age: int