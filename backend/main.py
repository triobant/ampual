import json
import uvicorn
import db.models as models
import db.schemas as schemas
from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from db.configurations import init_db, db_session, engine
from db.repositories import PlantRepo


router = FastAPI(
    title="Documentation - Ampual - Grow your food",
    description="Ampual - with FastAPI, Tailwind-CSS, React, SQLite3 and SQLAlchemy",
    version="0.0.1",
)


origins = [
        "http://localhost:3000",
        "localhost:3000"
]


router.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)


init_db()


templates = Jinja2Templates(directory="templates")


@router.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return HTMLResponse(
        status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}
    )


@router.post("/plants", tags=["Plant"], response_model=schemas.Plant, status_code=201)
async def create_plant(
    plant_request: schemas.PlantCreate, db_session: Session = Depends(db_session)
):
    """
    Create a Plant and store it in the database
    """

    db_plant = PlantRepo.fetch_by_name(db_session, name=plant_request.name)
    if db_plant:
        raise HTTPException(status_code=400, detail="Plant already exists!")

    return await PlantRepo.create(db_session=db_session, plant=plant_request)


@router.get("/plants", tags=["Plant"], response_model=List[schemas.Plant])
def get_all_plants(name: Optional[str] = None, db_session: Session = Depends(db_session)):
    """
    Get all the Plants stored in database
    """
    if name:
        plants = []
        db_plant = PlantRepo.fetch_by_name(db_session, name)
        plants.routerend(db_plant)
        return plants
    else:
        return PlantRepo.fetch_all(db_session)


@router.get("/plants/{plant_id}", tags=["Plant"], response_model=schemas.Plant)
def get_plant(plant_name: str, db_session: Session = Depends(db_session)):
    """
    Get the Plant with the given name provided by User stored in database
    """
    db_plant = PlantRepo.fetch_by_name(db_session, plant_name)
    if plant_name is None:
        raise HTTPException(
            status_code=404, detail="Plant not found with the given name"
        )
    return db_plant


@router.delete("/plants/{plant_name}", tags=["Plant"])
async def delete_plants(plant_name: str, db_session: Session = Depends(db_session)):
    """
    Delete the Plant with the given name provided by User stored in database
    """
    db_plant = PlantRepo.fetch_by_name(db_session, plant_name)
    if plant_name is None:
        raise HTTPException(
            status_code=404, detail="Plant not found with the given name"
        )
    await PlantRepo.delete(db_session, plant_name)
    return "Plant deleted successfully!"


@router.put("/plants/{plant_id}", tags=["Plant"], response_model=schemas.Plant)
async def put_plants(
    plant_id: int, plant_request: schemas.Plant, db_session: Session = Depends(db_session)
):
    """
    Update a Plant stored in the database
    """
    db_plant = PlantRepo.fetch_by_id(db_session, plant_id)
    if db_plant:
        update_plant_encoded = jsonable_encoder(plant_request)
        db_plant.name = update_plant_encoded["name"]
        db_plant.raising_time = update_plant_encoded["raising_time"]
        db_plant.transplant_time = update_plant_encoded["transplant_time"]
        db_plant.harvest_time = update_plant_encoded["harvest_time"]
        return await PlantRepo.update(db=db_session, plant_data=db_plant)
    else:
        raise HTTPException(status_code=400, detail="Plant not found with the given ID")


if __name__ == "__main__":
    uvicorn.run("main:router", port=9000, reload=True)
