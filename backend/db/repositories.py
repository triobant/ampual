from sqlalchemy.orm import Session
from . import models, schemas
from typing import List
from datetime import datetime


class PlantRepo:

    async def create(db: Session, plant: schemas.PlantCreate):
        db_plant = models.Plant(
            id=plant.id,
            name=plant.name,
            raising_time=plant.raising_time,
            transplant_time=plant.transplant_time,
            harvest_time=plant.harvest_time,
        )
        db.add(db_plant)
        await db.commit()
        await db.refresh(db_plant)
        return db_plant

    def fetch_by_id(db: Session, _id):
        return db.query(models.Plant).limit(50).filter(models.Plant.id == _id).first()

    def fetch_by_name(db: Session, name):
        return db.query(models.Plant).filter(models.Plant.name == name).first()

    def fetch_by_partial_name(db: Session, name: str) -> List[models.Plant]:
        return db.query(Plant).filter(Plant.name.ilike(f"%{name}%")).all()

    def fetch_by_date(db: Session, date: str) -> List[models.Plant]:
        return db.query(models.Plant).filter(
                models.Plant.raising_time == date
                or models.Plant.transplant_time == date
                or models.Plant.harvest_time == date
        ).all()

    def fetch_by_month(db: Session, month: str) -> List[models.Plant]:
        try:
            month_num = int(month)
            if month_num < 1 or month_num > 12:
                raise ValueError
        except ValueError:
            month_num = datetime.strptime(month, "%B").month
        return db.query(models.Plant).filter(
                models.Plant.raising_time.like(f"%-{month_num:02d}-%")
                or models.Plant.transplant_time.like(f"%-{month_num:02d}-%")
                or models.Plant.harvest_time.like(f"%-{month_num:02d}-%")
        ).all()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Plant).offset(skip).limit(limit).all()

    async def delete(db: Session, plant_id):
        db_plant = db.query(models.Plant).filter_by(id=plant_id).first()
        db.delete(db_plant)
        await db.commit()

    async def update(db: Session, plant_data):
        updated_plant = db.merge(plant_data)
        await db.commit()
        return updated_plant
