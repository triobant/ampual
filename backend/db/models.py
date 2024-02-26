from sqlalchemy import Column, Integer, String
from .configurations import Base


class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    raising_time = Column(String, index=True)
    transplant_time = Column(String, index=True)
    harvest_time = Column(String, index=True)


    def __repr__(self):
        return (
            "PlantModel(name=%s, raising_time=%s, transplant_time=%s, harvest_time=%s)"
            % (self.name, self.raising_time, self.transplant_time, self.harvest_time)
        )
