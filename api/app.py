import pathlib
import sys
import os
from fastapi import FastAPI, Path, Body, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

# Adds root of repo to path to ensure correct module imports
root_path = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(1, str(root_path.absolute()))
os.chdir(str(root_path.absolute()))

from api.modules.data_classes import *
from api.modules.database import *


# API config----------------------------------------------------------

app = FastAPI()

# Enable cross-origin requests from any domain for potential dev needs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Enable decoupling of database implementation via FastAPI Dependency that returns objects of supertype DBHandler
async def database_dependency(db_choice: Optional[str] = Query("sqlite", description="Dependency for resolving the type of DB to use")):
    if db_choice == "sqlite":
        return SQLiteDBHandler()
    return None


# Basic CRUD Endpoints definition------------------------------------------------


@app.post("/users", response_model=BaseUser, responses={400: {"description": "Constraint conflict with the database"}})
async def create_user(new_user: InUser, db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for inserting a new user record into the DB. A successful call returns JSON object with the inserted record
    """
    try:
        inserted_record = await db_handler.insert_user(new_user=new_user)
        inserted_record = init_BaseUser(inserted_record)
    except DBHandlerException as e:
        return JSONResponse(status_code=400)

    return inserted_record


@app.get("/users", response_model=List[BaseUser])
async def read_all_users(db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for retrieving all user records from DB. A successful call returns a list of JSON objects with the existing records
    """
    all_user_records = await db_handler.select_users()
    all_user_records = [init_BaseUser(record) for record in all_user_records]

    return all_user_records


@app.get("/users/{user_id}", response_model=BaseUser)
async def read_user(user_id: str = Path(..., description="ID value of the desired user"), db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for retrieving a single user record from DB. A successful call returns JSON object with the desired record
    """
    user_record = await db_handler.select_user(user_id=user_id)
    user_record = init_BaseUser(user_record)

    return user_record


@app.put("/users/{user_id}", response_model=BaseUser, responses={400: {"description": "Constraint conflict with the database"}})
async def update_user(new_data: UpdateUser, user_id: str = Path(..., description="ID value of the desired user"),
                      db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for updating the information of an existing user inside the DB. A successful call returns JSON object with the updated record
    """
    try:
        updated_record = await db_handler.update_user(user_id=user_id, new_data=new_data)
        updated_record = init_BaseUser(updated_record)
    except DBHandlerException as e:
        return JSONResponse(status_code=400)

    return updated_record


@app.delete("/users/{user_id}", response_model=BaseUser)
async def delete_user(user_id: str = Path(..., description="ID value of the desired user"),
                      db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for deleting an existing user record inside the DB. Also cascade deletes all team member records associated with the user.
    A successful call returns JSON object with the deleted user record
    """
    deleted_record = await db_handler.delete_user(user_id=user_id)
    deleted_record = init_BaseUser(deleted_record)

    return deleted_record


@app.post("/teams", response_model=BaseTeam, responses={400: {"description": "Constraint conflict with the database"}})
async def create_team(new_team: BaseTeam, db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for inserting a new team record into the DB. A successful call returns JSON object with the inserted record
    """
    try:
        inserted_record = await db_handler.insert_team(new_team=new_team)
        inserted_record = init_BaseTeam(inserted_record)
    except DBHandlerException as e:
        return JSONResponse(status_code=400)

    return inserted_record


@app.get("/teams", response_model=List[BaseTeam])
async def read_all_teams(db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for retrieving all team records from DB. A successful call returns a list of JSON objects with the existing records
    """
    all_team_records = await db_handler.select_teams()
    all_team_records = [init_BaseTeam(record) for record in all_team_records]

    return all_team_records


@app.get("/teams/{team_id}", response_model=BaseTeam)
async def read_team(team_id: str = Path(..., description="ID value of the desired team"), db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for retrieving a single team record from DB. A successful call returns JSON object with the desired record
    """
    team_record = await db_handler.select_team(team_id=team_id)
    team_record = init_BaseTeam(team_record)

    return team_record


@app.put("/teams/{team_id}", response_model=BaseTeam, responses={400: {"description": "Constraint conflict with the database"}})
async def update_team(new_data: UpdateTeam, team_id: str = Path(..., description="ID value of the desired team"),
                      db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for updating the information of an existing team inside the DB. A successful call returns JSON object with the updated record
    """
    try:
        updated_record = await db_handler.update_team(team_id=team_id, new_data=new_data)
        updated_record = init_BaseTeam(updated_record)
    except DBHandlerException as e:
        return JSONResponse(status_code=400)

    return updated_record


@app.delete("/teams/{team_id}", response_model=BaseTeam)
async def delete_team(team_id: str = Path(..., description="ID value of the desired team"),
                      db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for deleting an existing team record inside the DB. Also cascade deletes all team member records associated with the team.
    A successful call returns JSON object with the deleted user record
    """
    deleted_record = await db_handler.delete_team(team_id=team_id)
    deleted_record = init_BaseTeam(deleted_record)

    return deleted_record


# Team Maintenance Endpoints definition------------------------------------------------

@app.get("/users/{user_id}/teams", response_model=List[BaseTeam])
async def read_user_teams(user_id: str = Path(..., description="ID value of the desired user"),
                          db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for retrieving all team records associated with a user. A successful call returns a list of JSON objects with the existing records
    """
    all_records = await db_handler.select_user_teams(user_id=user_id)
    all_records = [init_BaseTeam(record) for record in all_records]

    return all_records


@app.get("/teams/{team_id}/members", response_model=List[BaseUser])
async def read_team_members(team_id: str = Path(..., description="ID value of the desired team"),
                            db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for retrieving all user records associated with a team. A successful call returns a list of JSON objects with the existing records
    """
    all_records = await db_handler.select_team_members(team_id=team_id)
    all_records = [init_BaseUser(record) for record in all_records]

    return all_records


@app.post("/teams/{team_id}/members", response_model=Dict[str, str], responses={400: {"description": "Constraint conflict with the database"}})
async def add_team_member(team_id: str = Path(..., description="ID value of the desired team"),
                          user_id: str = Body(..., description="ID value of the desired user", embed=True),
                          db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for inserting a new team member record into the DB. A successful call returns JSON object with the inserted record
    """
    try:
        inserted_record = await db_handler.insert_team_member(team_id=team_id, user_id=user_id)
        inserted_record = {"id_team": inserted_record[0], "id_user": inserted_record[1]}
    except DBHandlerException as e:
        return JSONResponse(status_code=400)

    return inserted_record


@app.delete("/teams/{team_id}/members/{user_id}", response_model=Dict[str, str])
async def delete_team_member(team_id: str = Path(..., description="ID value of the desired team"),
                             user_id: str = Path(..., description="ID value of the desired user"),
                             db_handler: DBHandler = Depends(database_dependency)):
    """
    Endpoint for deleting an existing team member record from the DB. A successful call returns JSON object with the deleted record
    """
    deleted_record = await db_handler.delete_team_member(team_id=team_id, user_id=user_id)
    deleted_record = {"id_team": deleted_record[0], "id_user": deleted_record[1]}

    return deleted_record


