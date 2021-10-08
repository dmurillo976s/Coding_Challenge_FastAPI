from fastapi import FastAPI, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from modules.data_classes import *
from typing import List

# API config----------------------------------------------------------

app = FastAPI()

# Enable cross-origin requests from any domain for potential dev needs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic CRUD Endpoints definition------------------------------------------------


@app.post("/users", response_model=BaseUser)
async def create_user(new_user: InUser):
    return None


@app.get("/users", response_model=List[BaseUser])
async def read_all_users():
    return None


@app.get("/users/{user_id}", response_model=BaseUser)
async def read_user(user_id: str = Path(...)):
    return None


@app.put("/users/{user_id}", response_model=BaseUser)
async def update_user(new_data: UpdateUser, user_id: str = Path(...)):
    return None


@app.delete("/users/{user_id}", response_model=BaseUser)
async def delete_user(user_id: str = Path(...)):
    return None


@app.post("/teams", response_model=BaseTeam)
async def create_team(new_team: BaseTeam):
    return None


@app.get("/teams", response_model=List[BaseTeam])
async def read_all_teams():
    return None


@app.get("/teams/{team_id}", response_model=BaseTeam)
async def read_team(team_id: str = Path(...)):
    return None


@app.put("/teams/{team_id}", response_model=BaseTeam)
async def update_team(new_data: UpdateTeam, team_id: str = Path(...)):
    return None


@app.delete("/teams/{team_id}", response_model=BaseTeam)
async def delete_team(team_id: str = Path(...)):
    return None


# Team Maintenance Endpoints definition------------------------------------------------

@app.get("/users/{user_id}/teams", response_model=List[BaseTeam])
async def read_user_teams(user_id: str = Path(...)):
    return None


@app.get("/teams/{team_id}/members", response_model=List[BaseUser])
async def read_team_members(team_id: str = Path(...)):
    return None


@app.post("/teams/{team_id}/members", response_model=List[BaseUser])
async def add_user_to_team(user_id: str = Body(...)):
    return None


@app.delete("/teams/{team_id}/members/{user_id}", response_model=List[BaseUser])
async def delete_user_from_team(team_id: str = Path(...), user_id: str = Path(...)):
    return None


