from sqlalchemy.orm import Session
from . import models, schemas


class PlantRepo:

    async def create(db: Session, plant: schemas.PlantCreate):
        db_plant = models.Plant(name=plant.name, raising_time=plant.raising_time, transplant_time=plant.transplant_time, harvest_time=plant.harvest_time)
        db.add(db_plant)
        db.commit()
        db.refresh(db_plant)
        return db_plant


    def fetch_by_id(db: Session, _id):
        return db.query(models.Plant).limit(50).filter(models.Plant.id == _id).first()


    def fetch_by_name(db: Session, name):
        return db.query(models.Plant).filter(models.Plant.name == name).first()


    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Plant).offset(skip).limit(limit).all()


    async def delete(db: Session, plant_id):
        db_plant = db.query(models.Plant).filter_by(id=plant_id).first()
        db.delete(db_plant)
        db.commit()


    async def update(db: Session, plant_data):
        updated_plant = db.merge(plant_data)
        db.commit()
        return updated_plant
