import json
from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.configurations import init_db, db_session
from app.db.schema import PlantBase
from app.db.models import Plant


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"Ping": "Pong"}

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
