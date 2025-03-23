import os
import requests
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

FIREBASE_API_KEY = "AIzaSyCtrT-uXPnvYYeE88C6sOPL3diA4LNzg1c"
PROJECT_ID = "my-project-yvonne-9ff25"
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------------------- Models ---------------------------- #
class Driver(BaseModel):
    driver_name: str
    age: int
    points_scored: int
    world_titles: int
    pole_positions: int
    fastest_laps: int
    team: str

class Team(BaseModel):
    team_name: str
    year_founded: int
    constructor_titles: int
    pole_positions: int
    race_wins: int
    previous_season_position: int

class Query(BaseModel):
    attribute: str
    condition: str
    value: int


def verify_token(authorization: str = Header(None)):
    if not authorization or "Bearer " not in authorization:
        raise HTTPException(status_code=401, detail="Missing authentication token")
    token = authorization.replace("Bearer ", "").strip()
    verify_url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
    response = requests.post(verify_url, json={"idToken": token})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return response.json()


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/add_driver_page", response_class=HTMLResponse)
async def add_driver_page(request: Request):
    return templates.TemplateResponse("add_driver.html", {"request": request})

@app.get("/add_team_page", response_class=HTMLResponse)
async def add_team_page(request: Request):
    return templates.TemplateResponse("add_team.html", {"request": request})

@app.get("/edit_driver/{driver_id}", response_class=HTMLResponse)
async def edit_driver_page(request: Request, driver_id: str):
    return templates.TemplateResponse("edit_driver.html", {"request": request, "driver_id": driver_id})

@app.get("/edit_team/{team_id}", response_class=HTMLResponse)
async def edit_team_page(request: Request, team_id: str):
    return templates.TemplateResponse("edit_team.html", {"request": request, "team_id": team_id})


def doc_path(collection, doc_id=""):
    return f"{FIRESTORE_URL}/{collection}/{doc_id}" if doc_id else f"{FIRESTORE_URL}/{collection}"


@app.post("/add_driver")
async def add_driver(driver: Driver, authorization: str = Header(None)):
    verify_token(authorization)
    data = {"fields": {k: {"stringValue": str(v)} if isinstance(v, str) else {"integerValue": v} for k, v in driver.dict().items()}}
    r = requests.post(doc_path("drivers"), json=data)
    if r.status_code == 200:
        return {"message": "Driver added successfully!"}
    return JSONResponse(status_code=500, content={"error": "Failed to add driver"})

@app.post("/add_team")
async def add_team(team: Team, authorization: str = Header(None)):
    verify_token(authorization)
    data = {"fields": {k: {"stringValue": str(v)} if isinstance(v, str) else {"integerValue": v} for k, v in team.dict().items()}}
    r = requests.post(doc_path("teams"), json=data)
    if r.status_code == 200:
        return {"message": "Team added successfully!"}
    return JSONResponse(status_code=500, content={"error": "Failed to add team"})

@app.get("/driver/{driver_id}")
async def get_driver(driver_id: str):
    r = requests.get(doc_path("drivers", driver_id))
    if r.status_code != 200:
        return JSONResponse(status_code=404, content={"error": "Driver not found"})
    fields = r.json().get("fields", {})
    return {k: int(v.get("integerValue", 0)) if "integerValue" in v else v.get("stringValue", "") for k, v in fields.items()}

@app.get("/team/{team_id}")
async def get_team(team_id: str):
    r = requests.get(doc_path("teams", team_id))
    if r.status_code != 200:
        return JSONResponse(status_code=404, content={"error": "Team not found"})
    fields = r.json().get("fields", {})
    return {k: int(v.get("integerValue", 0)) if "integerValue" in v else v.get("stringValue", "") for k, v in fields.items()}

@app.get("/all_drivers")
async def get_all_drivers():
    r = requests.get(doc_path("drivers"))
    try:
        docs = r.json().get("documents", [])
        return {"drivers": [{"id": doc['name'].split('/')[-1], **{k: int(v.get("integerValue", 0)) if "integerValue" in v else v.get("stringValue", "") for k, v in doc['fields'].items()}} for doc in docs]}
    except:
        return JSONResponse(status_code=500, content={"error": "Failed to load drivers"})

@app.get("/all_teams")
async def get_all_teams():
    r = requests.get(doc_path("teams"))
    try:
        docs = r.json().get("documents", [])
        return {"teams": [{"id": doc['name'].split('/')[-1], **{k: int(v.get("integerValue", 0)) if "integerValue" in v else v.get("stringValue", "") for k, v in doc['fields'].items()}} for doc in docs]}
    except:
        return JSONResponse(status_code=500, content={"error": "Failed to load teams"})

@app.post("/update_driver/{driver_id}")
async def update_driver(driver_id: str, updated_driver: Driver, authorization: str = Header(None)):
    verify_token(authorization)
    data = {
        "fields": {
            k: {"stringValue": str(v)} if isinstance(v, str) else {"integerValue": v}
            for k, v in updated_driver.dict().items()
        }
    }
    r = requests.patch(doc_path("drivers", driver_id), json=data)
    if r.status_code == 200:
        return {"message": "Driver updated successfully!"}
    else:
        return JSONResponse(status_code=500, content={"error": "Failed to update driver"})


@app.post("/update_team/{team_id}")
async def update_team(team_id: str, updated_team: Team, authorization: str = Header(None)):
    verify_token(authorization)
    data = {"fields": {k: {"stringValue": str(v)} if isinstance(v, str) else {"integerValue": v} for k, v in updated_team.dict().items()}}
    r = requests.patch(doc_path("teams", team_id), json=data)
    if r.status_code == 200:
        return {"message": "Team updated successfully!"}
    return JSONResponse(status_code=500, content={"error": "Failed to update team"})

@app.post("/query_drivers")
async def query_drivers(query: Query):
    r = requests.get(f"{FIRESTORE_URL}/drivers")
    if r.status_code != 200:
        return JSONResponse(status_code=500, content={"error": "Failed to fetch drivers"})

    drivers = []
    docs = r.json().get("documents", [])
    for doc in docs:
        fields = doc.get("fields", {})
        driver = {
            "id": doc["name"].split("/")[-1],
            **{k: int(v.get("integerValue", 0)) if "integerValue" in v else v.get("stringValue", "")
               for k, v in fields.items()}
        }

        # Apply the filtering logic
        attr = query.attribute
        val = driver.get(attr)
        if isinstance(val, int):
            if (query.condition == "lt" and val < query.value) or \
               (query.condition == "gt" and val > query.value) or \
               (query.condition == "eq" and val == query.value):
                drivers.append(driver)

    return {"drivers": drivers}


@app.post("/query_teams")
async def query_teams(query: Query):
    r = requests.get(f"{FIRESTORE_URL}/teams")
    if r.status_code != 200:
        return JSONResponse(status_code=500, content={"error": "Failed to fetch teams"})

    teams = []
    docs = r.json().get("documents", [])
    for doc in docs:
        fields = doc.get("fields", {})
        team = {
            "id": doc["name"].split("/")[-1],
            **{k: int(v.get("integerValue", 0)) if "integerValue" in v else v.get("stringValue", "")
               for k, v in fields.items()}
        }

        val = team.get(query.attribute)
        if isinstance(val, int):
            if (query.condition == "lt" and val < query.value) or \
               (query.condition == "gt" and val > query.value) or \
               (query.condition == "eq" and val == query.value):
                teams.append(team)

    return {"teams": teams}

@app.delete("/delete_driver/{driver_id}")
async def delete_driver(driver_id: str, authorization: str = Header(None)):
    verify_token(authorization)
    r = requests.delete(doc_path("drivers", driver_id))
    return JSONResponse(status_code=r.status_code, content={"message": "Driver deleted" if r.status_code == 200 else "Failed to delete"})

@app.delete("/delete_team/{team_id}")
async def delete_team(team_id: str, authorization: str = Header(None)):
    verify_token(authorization)
    r = requests.delete(doc_path("teams", team_id))
    return JSONResponse(status_code=r.status_code, content={"message": "Team deleted" if r.status_code == 200 else "Failed to delete"})
