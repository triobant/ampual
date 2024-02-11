import json
import uvicorn
import backend.db.models as models
import backend.db.schemas as schemas
from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List,Optional
from backend.db.configurations import init_db, db_session, engine
from backend.db.schemas import PlantBase
from backend.db.models import Plant
from backend.db.repositories import PlantRepo


router = FastAPI(
    title="Documentation - Ampual - Grow your food",
    description="Ampual - with FastAPI, Tailwind-CSS, React, SQLite3 and SQLAlchemy",
    version="0.0.1",
)


init_db


router.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@router.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return HTMLResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

# Test route
@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    data = {"Ping": "Pong"}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@router.post('/plants', tags=["Plant"],response_model=schemas.Plant,status_code=201)
async def create_plant(plant_request: schemas.PlantCreate, db_session: Session = Depends(init_db)):
    """
    Create a Plant and store it in the database
    """

    db_plant = PlantRepo.fetch_by_name(db_session, name=plant_request.name)
    if db_plant:
        raise HTTPException(status_code=400, detail="Plant already exists!")

    return await PlantRepo.create(db_session=db_session, plant=plant_request)


@router.get('/plants', tags=["Plant"],response_model=List[schemas.Plant])
def get_all_plants(name: Optional[str] = None,db_session: Session = Depends(init_db)):
    """
    Get all the Plants stored in database
    """
    if name:
        plants = []
        db_plant = PlantRepo.fetch_by_name(db_session,name)
        plants.routerend(db_plant)
        return plants
    else:
        return PlantRepo.fetch_all(db_session)


@router.get('/plants/{plant_id}', tags=["Plant"],response_model=schemas.Plant)
def get_plant(plant_id: int, db_session: Session = Depends(init_db)):
    ...
#TODO: add function to get plant by name or dates

@router.delete()
async def delete_plants(plant_id: int, db_session: Session = Depends(init_db)):
    ...
#TODO: remove plant from database?? Maybe don't use this method


@router.put('/plants/{plant_id}', tags=["Plant"], response_model=schemas.Plant)
async def put_plants(plant_id: int, plant_request: schemas.Plant, db_session: Session = Depends(init_db)):
    """
    Update a Plant stored in the database
    """
    db_plant = PlantRepo.fetch_by_id(db_session, plant_id)
    if db_plant:
        update_plant_encoded = jsonable_encoder(plant_request)
        db_plant.name = update_plant_encoded['name']
        db_plant.raising_time = update_plant_encoded['raising_time']
        db_plant.transplant_time = update_plant_encoded['transplant_time']
        db_plant.harvest_time = update_plant_encoded['harvest_time']
        return await PlantRepo.update(db=db_session, plant_data=db_plant)
    else:
        raise HTTPException(status_code=400, detail="Plant not found with the given ID")



if __name__ == "__main__":
    uvicorn.run("main:router", port=9000, reload=True)
