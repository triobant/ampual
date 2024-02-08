import json
import uvicorn
from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.configurations import init_db, db_session
from app.db.schema import PlantBase
from app.db.models import Plant


app = FastAPI(
    title="Ampual - Grow your food - Documentation",
    description="Ampual - with FastAPI, Tailwind-CSS, React, SQLite3 and SQLAlchemy",
    version="0.0.1",
)


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    data = {"Ping": "Pong"}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.get("/app/api/plants")
async def get_plants():
    return 1


@app.get("/app/api/plants{id}")
async def get_plants_by_id(id):
    return 2


@app.post("/app/api/plants")
async def post_plants(id):
    return 2


@app.put("/app/api/plants{id}")
async def put_plants(id, data):
    return 2


@app.delete("/app/api/plants{id}")
async def delete_plants(id):
    return 2
