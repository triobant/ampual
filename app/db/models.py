from sqlalchemy import Column, Integer, String
from .configurations import Base


class Plant(Base):
    __tablename__ = 'vegetables'
    id = Column(Integer, primary_key=True, index=True)
    raising_time = Column(String, index=True)
    transplant_time = Column(String, index=True)
    harvest_time = Column(String, index=True)
