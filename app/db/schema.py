from pydantic import BaseModel


class Plant(BaseModel):
    task: str
