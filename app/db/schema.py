from typing import List, Optional
from pydantic import BaseModel


class PlantBase(BaseModel):
    name: str
    raising_time: str
    transplant_time: str
    harvest_time: str


class PlantCreate(PlantBase):
    pass


class Plant(PlantBase):
    id: int


    class Config:
        orm_mode = True
