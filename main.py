import firebase_admin
from firebase_admin import credentials, firestore, auth
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Depends
from pydantic import BaseModel


cred = credentials.Certificate("my-project-yvonne-9ff25-firebase-adminsdk-fbsvc-4f21b6fbeb.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/add_driver_page", response_class=HTMLResponse)
async def add_driver_page(request: Request):
    return templates.TemplateResponse("add_driver.html", {"request": request})

@app.get("/add_team_page", response_class=HTMLResponse)
async def add_team_page(request: Request):
    return templates.TemplateResponse("add_team.html", {"request": request})

@app.get("/driver/{driver_id}")
async def driver_detail_json(driver_id: str):
    driver_doc = db.collection("drivers").document(driver_id).get()
    if not driver_doc.exists:
        return JSONResponse(status_code=404, content={"error": "Driver not found"})
    
    driver_data = driver_doc.to_dict()
    return JSONResponse(status_code=200, content=driver_data)

@app.get("/team/{team_id}")
async def get_team_json(team_id: str):
    team_doc = db.collection("teams").document(team_id).get()
    if not team_doc.exists:
        return JSONResponse(status_code=404, content={"error": "Team not found"})

    return JSONResponse(status_code=200, content=team_doc.to_dict())

@app.get("/all_drivers")
async def get_all_drivers():
    try:
        drivers_ref = db.collection("drivers").stream()
        driver_list = [{"id": doc.id, **doc.to_dict()} for doc in drivers_ref]

        return JSONResponse(status_code=200, content={"drivers": driver_list})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/all_teams")
async def get_all_teams():
    try:
        teams_ref = db.collection("teams").stream()
        team_list = [{"id": doc.id, **doc.to_dict()} for doc in teams_ref]

        return JSONResponse(status_code=200, content={"teams": team_list})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})









# Pydantic Models
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

    try:
        token = authorization.replace("Bearer ", "").strip()
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication token: {str(e)}")


@app.post("/add_driver")
async def add_driver(driver: Driver, authorization: str = Header(None)):
    try:
        print("🔍 Received Driver Data:", driver.dict())  # Debugging line

        driver_ref = db.collection("drivers").document()
        driver_ref.set(driver.dict())
        return JSONResponse(status_code=200, content={"message": "Driver added successfully!"})
    except Exception as e:
        print("❌ Error inserting driver:", str(e))  # Debugging line
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/add_team")
async def add_team(team: Team, authorization: str = Header(None)):
    try:
       
        if not authorization or "Bearer " not in authorization:
            raise HTTPException(status_code=401, detail="Missing authentication token")
        
        token = authorization.replace("Bearer ", "").strip()
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token.get("uid", "Unknown User")
        
        print("🔍 Received Team Data:", team.dict())  # ✅ Debugging line
        print(f"👤 User ID: {user_id}")
        
        
        if not team.team_name or team.year_founded <= 0:
            raise HTTPException(status_code=400, detail="Team name and year founded are required.")
        
        
        team_ref = db.collection("teams").document()
        team_ref.set(team.dict())
        
        return JSONResponse(status_code=200, content={"message": "Team added successfully!"})
    
    except HTTPException as http_err:
        return JSONResponse(status_code=http_err.status_code, content={"error": http_err.detail})
    
    except Exception as e:
        print("❌ Error adding team:", str(e))  # ✅ Debugging line
        return JSONResponse(status_code=500, content={"error": str(e)})



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
    

@app.post("/update_driver/{driver_id}")
async def update_driver(driver_id: str, updated_driver: Driver):
    try:
        driver_ref = db.collection("drivers").document(driver_id)
        if not driver_ref.get().exists:
            raise HTTPException(status_code=404, detail="Driver not found")

        driver_ref.update(updated_driver.dict())
        return JSONResponse(status_code=200, content={"message": "Driver updated successfully!"})

    except Exception as e:
        print("❌ Error updating driver:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
