from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    name: str
    class_level: str
    language: str
    age: int
