from sqlalchemy.orm import Session
from . import models, schemas


class PlantRepo:

    async def create(db: Session, plant: schema.PlantCreate):
        db_plant = models.Plant(name=plant.name, raising_time=plant.raising_time, transplant_time=plant.transplant_time, harvest_time=plant.harvest_time)
        db.add(db_plant)
        db.commit()
        db.refresh(db_plant)
        return db_plant


    def fetch_by_id(db: Session, _id):
        ...


    def fetch_by_name(db: Session, name):
        return db.query(models.Plant).filter(models.Plant.name == name).first()


    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Plant).offset(skip).limit(limit).all()
