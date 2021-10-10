import pytest
import sys
import aiosqlite
from httpx import AsyncClient
from api.modules.database.config import CONFIG_SQLITE
from api.modules.database import sqlite_database_handler
from api.modules.database.sqlite_database_handler import SQLiteDBHandler
from api.modules.data_classes import *

# Set up connection config to test DB ------------------------------------------------------------------
sqlite_database_handler.connection_config = CONFIG_SQLITE["test"]["db_file"]


# Utility functions for tests --------------------------------------------------------------------------

async def insert_fake_user(fake_user: InUser):
    async with aiosqlite.connect(sqlite_database_handler.connection_config) as db:
        await db.execute("INSERT INTO users values (:id, :name, :email, :password)", fake_user.dict())
        await db.commit()


async def insert_fake_team(fake_team: BaseTeam):
    async with aiosqlite.connect(sqlite_database_handler.connection_config) as db:
        await db.execute("INSERT INTO teams values (:id, :name, :description)", fake_team.dict())
        await db.commit()


async def insert_fake_team_member(fake_team_id: str, fake_user_id: str):
    async with aiosqlite.connect(sqlite_database_handler.connection_config) as db:
        await db.execute("INSERT INTO team_members values (:id_user, :id_team)",
                         {"id_team": fake_team_id, "id_user": fake_user_id})
        await db.commit()


@pytest.fixture
async def clean_test_db():
    async with aiosqlite.connect(sqlite_database_handler.connection_config) as db:
        await db.execute("DELETE FROM team_members")
        await db.execute("DELETE FROM teams")
        await db.execute("DELETE FROM users")
        await db.commit()


# Actual tests -----------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_select_user(clean_test_db):
    fake_user_data = {"id": "fakeuser01", "name": "John", "email": "j@gmail.com", "password": "hashed123"}
    fake_user = InUser(**fake_user_data)

    await insert_fake_user(fake_user)

    db_handler = SQLiteDBHandler()
    result_row = await db_handler.select_user(user_id=fake_user_data["id"])
    empty_result = await db_handler.select_user(user_id="none_existing_id")

    assert result_row == (fake_user.id, fake_user.name, fake_user.email)
    assert empty_result is None


@pytest.mark.asyncio
async def test_select_users(clean_test_db):
    db_handler = SQLiteDBHandler()
    result_rows = await db_handler.select_users()

    assert result_rows == []

    fake_user_a_data = {"id": "fakeuser01", "name": "John", "email": "j@gmail.com", "password": "hashed123"}
    fake_user_b_data = {"id": "fakeuser02", "name": "Jane", "email": "ja@gmail.com", "password": "hashedabc"}
    fake_user_a = InUser(**fake_user_a_data)
    fake_user_b = InUser(**fake_user_b_data)

    await insert_fake_user(fake_user_a)
    await insert_fake_user(fake_user_b)

    result_rows = await db_handler.select_users()

    assert result_rows == [(fake_user_a.id, fake_user_a.name, fake_user_a.email), (fake_user_b.id, fake_user_b.name, fake_user_b.email)]


@pytest.mark.asyncio
async def test_insert_user(clean_test_db):
    fake_user_data = {"id": "fakeuser01", "name": "John", "email": "j@gmail.com", "password": "hashed123"}
    fake_user = InUser(**fake_user_data)

    db_handler = SQLiteDBHandler()
    result_row = await db_handler.insert_user(new_user=fake_user)

    assert result_row == (fake_user.id, fake_user.name, fake_user.email)


@pytest.mark.asyncio
async def test_update_user(clean_test_db):
    fake_user_data = {"id": "fakeuser01", "name": "John", "email": "j@gmail.com", "password": "hashed123"}
    fake_user = InUser(**fake_user_data)
    await insert_fake_user(fake_user)

    fake_user_data_modified = {"id": "fakeuser01", "name": "Johnathan", "email": "jjoh@gmail.com", "password": "hashedabc"}
    fake_user_modified = UpdateUser(**fake_user_data_modified)

    db_handler = SQLiteDBHandler()
    result_row = await db_handler.update_user(user_id=fake_user_data_modified["id"], new_data=fake_user_modified)

    assert result_row == (fake_user_data_modified["id"], fake_user_modified.name, fake_user_modified.email)


@pytest.mark.asyncio
async def test_delete_user(clean_test_db):
    fake_user_data = {"id": "fakeuser01", "name": "John", "email": "j@gmail.com", "password": "hashed123"}
    fake_user = InUser(**fake_user_data)

    await insert_fake_user(fake_user)

    db_handler = SQLiteDBHandler()
    deleted_row = await db_handler.delete_user(user_id=fake_user.id)
    result_row = await db_handler.select_user(user_id=fake_user.id)

    assert deleted_row == (fake_user.id, fake_user.name, fake_user.email)
    assert result_row is None


@pytest.mark.asyncio
async def test_select_team(clean_test_db):
    fake_team_data = {"id": "faketeam01", "name": "THE TEAM", "description": "this is a description"}
    fake_team = BaseTeam(**fake_team_data)

    await insert_fake_team(fake_team)

    db_handler = SQLiteDBHandler()
    result_row = await db_handler.select_team(team_id=fake_team_data["id"])
    empty_result = await db_handler.select_team(team_id="none_existing_id")

    assert result_row == (fake_team.id, fake_team.name, fake_team.description)
    assert empty_result is None


@pytest.mark.asyncio
async def test_select_teams(clean_test_db):
    db_handler = SQLiteDBHandler()
    result_rows = await db_handler.select_teams()

    assert result_rows == []

    fake_team_a_data = {"id": "faketeam01", "name": "THE TEAM", "description": "this is a description"}
    fake_team_b_data = {"id": "faketeam02", "name": "THE SECOND TEAM", "description": "this is another description"}
    fake_team_a = BaseTeam(**fake_team_a_data)
    fake_team_b = BaseTeam(**fake_team_b_data)

    await insert_fake_team(fake_team_a)
    await insert_fake_team(fake_team_b)

    result_rows = await db_handler.select_teams()

    assert result_rows == [(fake_team_a.id, fake_team_a.name, fake_team_a.description), (fake_team_b.id, fake_team_b.name, fake_team_b.description)]


@pytest.mark.asyncio
async def test_insert_team(clean_test_db):
    fake_team_data = {"id": "faketeam01", "name": "THE TEAM", "description": "this is a description"}
    fake_team = BaseTeam(**fake_team_data)

    db_handler = SQLiteDBHandler()
    result_row = await db_handler.insert_team(new_team=fake_team)

    assert result_row == (fake_team.id, fake_team.name, fake_team.description)


@pytest.mark.asyncio
async def test_update_team(clean_test_db):
    fake_team_data = {"id": "faketeam01", "name": "THE TEAM", "description": "this is a description"}
    fake_team = BaseTeam(**fake_team_data)
    await insert_fake_team(fake_team)

    fake_team_data_modified = {"id": "faketeam01", "name": "THE TEAMMMM", "description": "this is a modified description"}
    fake_team_modified = UpdateTeam(**fake_team_data_modified)

    db_handler = SQLiteDBHandler()
    result_row = await db_handler.update_team(team_id=fake_team_data_modified["id"], new_data=fake_team_modified)

    assert result_row == (fake_team_data_modified["id"], fake_team_modified.name, fake_team_modified.description)


@pytest.mark.asyncio
async def test_delete_team(clean_test_db):
    fake_team_data = {"id": "faketeam01", "name": "THE TEAM", "description": "this is a description"}
    fake_team = BaseTeam(**fake_team_data)

    await insert_fake_team(fake_team)

    db_handler = SQLiteDBHandler()
    deleted_row = await db_handler.delete_team(team_id=fake_team.id)
    result_row = await db_handler.select_team(team_id=fake_team.id)

    assert deleted_row == (fake_team.id, fake_team.name, fake_team.description)
    assert result_row is None


@pytest.mark.asyncio
async def test_select_user_teams(clean_test_db):
    fake_user_data = {"id": "fakeuser01", "name": "John", "email": "j@gmail.com", "password": "hashed123"}
    fake_user = InUser(**fake_user_data)
    await insert_fake_user(fake_user)

    fake_team_a_data = {"id": "faketeam01", "name": "THE TEAM", "description": "this is a description"}
    fake_team_b_data = {"id": "faketeam02", "name": "THE SECOND TEAM", "description": "this is another description"}
    fake_team_a = BaseTeam(**fake_team_a_data)
    fake_team_b = BaseTeam(**fake_team_b_data)
    await insert_fake_team(fake_team_a)
    await insert_fake_team(fake_team_b)

    await insert_fake_team_member(fake_team_id=fake_team_a.id, fake_user_id=fake_user.id)
    await insert_fake_team_member(fake_team_id=fake_team_b.id, fake_user_id=fake_user.id)

    db_handler = SQLiteDBHandler()
    result_rows = await db_handler.select_user_teams(user_id=fake_user.id)
    empty_result = await db_handler.select_user_teams(user_id="none_existing_id")

    assert result_rows == [(fake_team_a.id, fake_team_a.name, fake_team_a.description), (fake_team_b.id, fake_team_b.name, fake_team_b.description)]
    assert empty_result == []


@pytest.mark.asyncio
async def test_select_team_members(clean_test_db):
    fake_team_data = {"id": "faketeam01", "name": "THE TEAM", "description": "this is a description"}
    fake_team = BaseTeam(**fake_team_data)
    await insert_fake_team(fake_team)

    fake_user_a_data = {"id": "fakeuser01", "name": "John", "email": "j@gmail.com", "password": "hashed123"}
    fake_user_b_data = {"id": "fakeuser02", "name": "Jane", "email": "ja@gmail.com", "password": "hashedabc"}
    fake_user_a = InUser(**fake_user_a_data)
    fake_user_b = InUser(**fake_user_b_data)
    await insert_fake_user(fake_user_a)
    await insert_fake_user(fake_user_b)

    await insert_fake_team_member(fake_team_id=fake_team.id, fake_user_id=fake_user_a.id)
    await insert_fake_team_member(fake_team_id=fake_team.id, fake_user_id=fake_user_b.id)

    db_handler = SQLiteDBHandler()
    result_rows = await db_handler.select_team_members(team_id=fake_team.id)
    empty_result = await db_handler.select_team_members(team_id="none_existing_id")

    assert result_rows == [(fake_user_a.id, fake_user_a.name, fake_user_a.email), (fake_user_b.id, fake_user_b.name, fake_user_b.email)]
    assert empty_result == []


@pytest.mark.asyncio
async def test_insert_team_member(clean_test_db):
    fake_team_data = {"id": "faketeam01", "name": "THE TEAM", "description": "this is a description"}
    fake_team = BaseTeam(**fake_team_data)
    await insert_fake_team(fake_team)

    fake_user_data = {"id": "fakeuser01", "name": "John", "email": "j@gmail.com", "password": "hashed123"}
    fake_user = InUser(**fake_user_data)
    await insert_fake_user(fake_user)

    db_handler = SQLiteDBHandler()
    result_row = await db_handler.insert_team_member(team_id=fake_team.id, user_id=fake_user.id)

    assert result_row == (fake_team.id, fake_user.id)


@pytest.mark.asyncio
async def test_delete_team_member(clean_test_db):
    fake_team_data = {"id": "faketeam01", "name": "THE TEAM", "description": "this is a description"}
    fake_team = BaseTeam(**fake_team_data)
    await insert_fake_team(fake_team)

    fake_user_data = {"id": "fakeuser01", "name": "John", "email": "j@gmail.com", "password": "hashed123"}
    fake_user = InUser(**fake_user_data)
    await insert_fake_user(fake_user)

    await insert_fake_team_member(fake_team_id=fake_team.id, fake_user_id=fake_user.id)

    db_handler = SQLiteDBHandler()
    deleted_row = await db_handler.delete_team_member(team_id=fake_team.id, user_id=fake_user.id)
    result_row = await db_handler.select_team_members(team_id=fake_team.id)

    assert deleted_row == (fake_team.id, fake_user.id)
    assert result_row == []


