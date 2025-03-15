import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

# Initialize Firebase Admin SDK
cred = credentials.Certificate("my-project-yvonne-9ff25-firebase-adminsdk-fbsvc-4f21b6fbeb.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Routes for pages
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/add_driver_page", response_class=HTMLResponse)
async def add_driver_page(request: Request):
    return templates.TemplateResponse("add_driver.html", {"request": request})

@app.get("/add_team_page", response_class=HTMLResponse)
async def add_team_page(request: Request):
    return templates.TemplateResponse("add_team.html", {"request": request})

# Pydantic Models
class Driver(BaseModel):
    driver_name: str
    age: int
    points_scored: int
    world_titles: int
    pole_positions: int
    fastest_laps: int
    team: str

class Query(BaseModel):
    attribute: str
    condition: str
    value: int

# Add a driver
@app.post("/add_driver")
async def add_driver(driver: Driver):
    try:
        driver_ref = db.collection("drivers").document()
        driver_ref.set(driver.dict())
        return JSONResponse(status_code=200, content={"message": "Driver added successfully!"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Query drivers
@app.post("/query_drivers")
async def query_drivers(query: Query):
    try:
        query_ref = db.collection("drivers")
        
        if query.condition == "lt":
            query_ref = query_ref.where(query.attribute, "<", query.value)
        elif query.condition == "gt":
            query_ref = query_ref.where(query.attribute, ">", query.value)
        elif query.condition == "eq":
            query_ref = query_ref.where(query.attribute, "==", query.value)
        
        results = query_ref.stream()
        driver_list = [{"id": doc.id, **doc.to_dict()} for doc in results]

        return JSONResponse(status_code=200, content={"drivers": driver_list})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
class Team(BaseModel):
    team_name: str
    year_founded: int
    constructor_titles: int
    pole_positions: int
    race_wins: int
    previous_season_position: int

@app.post("/add_team")
async def add_team(team: Team):
    try:
        team_ref = db.collection("teams").document()
        team_ref.set(team.dict())
        return JSONResponse(status_code=200, content={"message": "Team added successfully!"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/query_teams")
async def query_teams(query: Query):
    try:
        query_ref = db.collection("teams")
        
        if query.condition == "lt":
            query_ref = query_ref.where(query.attribute, "<", query.value)
        elif query.condition == "gt":
            query_ref = query_ref.where(query.attribute, ">", query.value)
        elif query.condition == "eq":
            query_ref = query_ref.where(query.attribute, "==", query.value)

        results = query_ref.stream()
        team_list = [{"id": doc.id, **doc.to_dict()} for doc in results]

        return JSONResponse(status_code=200, content={"teams": team_list})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
