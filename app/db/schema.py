from pydantic import BaseModel


class Plant(BaseModel):
    name: str
    raising_time: str
    transplant_time: str
    harvest_time: str
