import pytest

from httpx import AsyncClient
from api.modules.database.mock_database_handler import MockDBHandler
from api import app


# Override production database_handler dependency for mock test interactions
@pytest.fixture(scope="module")
def configure_mock_dependency():
    app.app.dependency_overrides[app.database_dependency] = MockDBHandler


@pytest.mark.asyncio
async def test_create_user(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/users", json={"id": "mock_id", "name": "my_name", "email": "my_email", "password": "12345"})
    assert response.status_code == 200
    assert response.json() == {"id": "mock_id", "name": "my_name", "email": "my_email"}


@pytest.mark.asyncio
async def test_read_all_users(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/users")
    assert response.status_code == 200
    assert response.json() == [{"id": "my_id_1", "name": "my_name_1", "email": "my_email_1"},
                               {"id": "my_id_2", "name": "my_name_2", "email": "my_email_2"}]


@pytest.mark.asyncio
async def test_read_user(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/users/mock_id")
    assert response.status_code == 200
    assert response.json() == {"id": "mock_id", "name": "my_name", "email": "my_email"}


@pytest.mark.asyncio
async def test_update_user(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.put("/users/mock_id", json={"name": "my_name", "email": "my_email", "password": "12345"})
    assert response.status_code == 200
    assert response.json() == {"id": "mock_id", "name": "my_name", "email": "my_email"}


@pytest.mark.asyncio
async def test_delete_user(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.delete("/users/mock_id")
    assert response.status_code == 200
    assert response.json() == {"id": "mock_id", "name": "my_name", "email": "my_email"}


@pytest.mark.asyncio
async def test_create_team(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/teams", json={"id": "mock_id", "name": "my_name", "description": "my_description"})
    assert response.status_code == 200
    assert response.json() == {"id": "mock_id", "name": "my_name", "description": "my_description"}


@pytest.mark.asyncio
async def test_read_all_teams(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/teams")
    assert response.status_code == 200
    assert response.json() == [{"id": "my_id_1", "name": "my_name_1", "description": "my_description_1"},
                               {"id": "my_id_2", "name": "my_name_2", "description": "my_description_2"}]


@pytest.mark.asyncio
async def test_read_team(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/teams/mock_id")
    assert response.status_code == 200
    assert response.json() == {"id": "mock_id", "name": "my_name", "description": "my_description"}


@pytest.mark.asyncio
async def test_update_team(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.put("/teams/mock_id", json={"name": "my_name", "description": "my_description"})
    assert response.status_code == 200
    assert response.json() == {"id": "mock_id", "name": "my_name", "description": "my_description"}


@pytest.mark.asyncio
async def test_delete_team(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.delete("/teams/mock_id")
    assert response.status_code == 200
    assert response.json() == {"id": "mock_id", "name": "my_name", "description": "my_description"}


@pytest.mark.asyncio
async def test_read_user_teams(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/users/mock_id/teams")
    assert response.status_code == 200
    assert response.json() == [{"id": "my_id_1", "name": "my_name_1", "description": "my_description_1"},
                               {"id": "my_id_2", "name": "my_name_2", "description": "my_description_2"}]


@pytest.mark.asyncio
async def test_read_team_members(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/teams/mock_id/members")
    assert response.status_code == 200
    assert response.json() == [{"id": "my_id_1", "name": "my_name_1", "email": "my_email_1"},
                               {"id": "my_id_2", "name": "my_name_2", "email": "my_email_2"}]


@pytest.mark.asyncio
async def test_add_team_member(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/teams/mock_team_id/members", json={"user_id": "mock_user_id"})
    assert response.status_code == 200
    assert response.json() == {"id_team": "mock_team_id", "id_user": "mock_user_id"}


@pytest.mark.asyncio
async def test_delete_team_member(configure_mock_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.delete("/teams/mock_team_id/members/mock_user_id")
    assert response.status_code == 200
    assert response.json() == {"id_team": "mock_team_id", "id_user": "mock_user_id"}


