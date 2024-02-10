import json
import uvicorn
import app.db.models as models
import app.db.schemas as schemas
from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.configurations import init_db, db_session, engine
from app.db.schemas import PlantBase
from app.db.models import Plant
from app.db.repositories import PlantRepo


app = FastAPI(
    title="Documentation - Ampual - Grow your food",
    description="Ampual - with FastAPI, Tailwind-CSS, React, SQLite3 and SQLAlchemy",
    version="0.0.1",
)


init_db


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return HTMLResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

# Test route
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    data = {"Ping": "Pong"}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.post('/plants', tags=["Plant"],response_model=schemas.Plant,status_code=201)
async def create_plant(plant_request: schemas.PlantCreate, db_session: Session = Depends(init_db)):
    """
    Create a Plant and store it in the database
    """

    db_plant = PlantRepo.fetch_by_name(db_session, name=plant_request.name)
    if db_plant:
        raise HTTPException(status_code=400, detail="Plant already exists!")

    return await PlantRepo.create(db_session=db_session, plant=plant_request)


@app.get('/plants', tags=["Plant"],response_model=List[schemas.Plant])
def get_all_plants(name: Optional[str] = None,db_session: Session = Depends(init_db)):
    """
    Get all the Plants stored in database
    """
    if name:
        plants = []
        db_plant = PlantRepo.fetch_by_name(db_session,name)
        plants.append(db_plant)
        return plants
    else:
        return PlantRepo.fetch_all(db_session)


@app.get("/app/api/plants{id}")
async def get_plants_by_id(id):
    return 2


@app.delete("/app/api/plants{id}")
async def delete_plants(id):
    return 2


@app.put('/app/api/plants{id}')
async def put_plants(id, data):
    return 2


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
