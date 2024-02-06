from typing import List, Optional
from pydantic import BaseModel


class PlantSchema(BaseModel):
    name: str
    raising_time: str
    transplant_time: str
    harvest_time: str
